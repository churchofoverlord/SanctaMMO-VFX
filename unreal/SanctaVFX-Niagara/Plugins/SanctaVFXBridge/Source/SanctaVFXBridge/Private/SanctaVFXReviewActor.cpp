#include "SanctaVFXReviewActor.h"
#include "NiagaraComponent.h"
#include "NiagaraSystem.h"
#include "NiagaraSystemInstanceController.h"
#include "NiagaraSystemInstance.h"
#include "NiagaraEmitter.h"
#include "NiagaraRendererProperties.h"
#include "Materials/MaterialInterface.h"
#include "MaterialShared.h"
#include "RHIGlobals.h"
#include "Camera/CameraComponent.h"
#include "Components/SceneComponent.h"
#include "GameFramework/PlayerController.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "InputCoreTypes.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Engine/GameViewportClient.h"
#include "HAL/FileManager.h"
#include "Editor/EditorPerformanceSettings.h"
#include "Editor.h"
#include "Containers/Ticker.h"

ASanctaVFXReviewGameMode::ASanctaVFXReviewGameMode()
{
    DefaultPawnClass = nullptr;
    HUDClass = ASanctaVFXReviewHUD::StaticClass();
}

ASanctaVFXReviewActor::ASanctaVFXReviewActor()
{
    PrimaryActorTick.bCanEverTick = true;
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("ReviewRoot"));
    Effect = CreateDefaultSubobject<UNiagaraComponent>(TEXT("Effect"));
    Effect->SetupAttachment(RootComponent);
    Effect->SetAutoActivate(false);
    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("ReviewCamera"));
    Camera->SetupAttachment(RootComponent);
    Camera->FieldOfView = 55;
    auto& PP = Camera->PostProcessSettings;
    PP.bOverride_AutoExposureMethod = true;
    PP.AutoExposureMethod = EAutoExposureMethod::AEM_Manual;
    PP.bOverride_AutoExposureApplyPhysicalCameraExposure = true;
    PP.AutoExposureApplyPhysicalCameraExposure = false;
    PP.bOverride_AutoExposureBias = true;
    PP.AutoExposureBias = 0;
    PP.bOverride_BloomIntensity = true;
    PP.BloomIntensity = .55f;
    PP.bOverride_MotionBlurAmount = true;
    PP.MotionBlurAmount = 0;
}

void ASanctaVFXReviewActor::BeginPlay()
{
    Super::BeginPlay();
    // Keep the review animation responsive when the user consults another
    // window. This is process-local: no editor preference is saved to disk.
    GetMutableDefault<UEditorPerformanceSettings>()->bThrottleCPUWhenNotForeground = false;
    Camera->SetRelativeLocation(CameraPosition);
    Camera->SetRelativeRotation((CameraTarget-CameraPosition).Rotation());
    Effect->SetRelativeLocation(FVector(0,0,EffectHeight));
    Effect->SetAsset(System);
    Effect->SetAllowScalability(false);
    // The staging port deforms meshes beyond their recorded spawn origins.
    // Keep review-only culling bounds generous; source assets stay untouched.
    Effect->SetSystemFixedBounds(FBox(FVector(-16000,-16000,-2000),FVector(16000,16000,10000)));
    Effect->SetCastShadow(false);
    // Niagara custom time dilation requires a solo system instance.
    Effect->SetForceSolo(true);
    // Loading a saved map can leave Niagara's on-demand compile request deferred.
    // The viewer must submit it, rather than waiting forever for IsReadyToRun.
    if (System) System->RequestCompile(false);
    bAudit = FParse::Param(FCommandLine::Get(), TEXT("SanctaReviewAudit"));
    bAuditAll = FParse::Param(FCommandLine::Get(), TEXT("SanctaReviewAuditAll"));
    bQuality = FParse::Param(FCommandLine::Get(), TEXT("SanctaReviewQuality"));
    bLoopCheck = FParse::Param(FCommandLine::Get(), TEXT("SanctaReviewLoopCheck"));
    bAuditAll |= bQuality;
    bAudit |= bAuditAll;
    // The interactive viewer starts at normal speed. The explicit loop check
    // retains its slow-playback coverage, and capture runs use normal time.
    bSlow = bLoopCheck && !bAuditAll;
    Effect->SetCustomTimeDilation(bSlow ? 1.f/3.f : 1.f);
    UE_LOG(LogTemp,Display,TEXT("SanctaReview playback initialized: rate=%.3f slow=%d quality=%d loop_check=%d"),
        Effect->GetCustomTimeDilation(),bSlow,bQuality,bLoopCheck);
}

void ASanctaVFXReviewActor::Repeat()
{
    Effect->SetPaused(false);
    Effect->ReinitializeSystem();
    Effect->Activate(true);
    Effect->SetCustomTimeDilation(bSlow ? 1.f/3.f : 1.f);
    Effect->SetPaused(bPaused);
    PlaybackTime = 0;
    CompletionHold = 0;
    if (bLoopCheck) UE_LOG(LogTemp,Display,TEXT("SanctaLoop repeat: %d | real_time=%.3f | rate=%.3f | %s"),++RepeatCount,GetWorld()->GetRealTimeSeconds(),Effect->GetCustomTimeDilation(),*SkillTitle);
}

void ASanctaVFXReviewActor::FinishReview()
{
    GEditor->RequestEndPlayMap();
    FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([](float){
        if (GEditor && GEditor->IsPlaySessionInProgress()) return true;
        FPlatformMisc::RequestExit(false);
        return false;
    }),.5f);
}

void ASanctaVFXReviewActor::TogglePause()
{
    bPaused = !bPaused;
    Effect->SetPaused(bPaused);
}

void ASanctaVFXReviewActor::ToggleSlow()
{
    bSlow = !bSlow;
    Effect->SetCustomTimeDilation(bSlow ? 1.f/3.f : 1.f);
}

void ASanctaVFXReviewActor::OpenIndex(int32 Index)
{
    if (CatalogMaps.IsEmpty()) return;
    Index = (Index % CatalogMaps.Num() + CatalogMaps.Num()) % CatalogMaps.Num();
    UGameplayStatics::OpenLevel(this, FName(*CatalogMaps[Index]));
}

void ASanctaVFXReviewActor::CaptureAudit()
{
    const FString Directory = FPaths::ProjectSavedDir()/TEXT("ReviewCaptures");
    IFileManager::Get().MakeDirectory(*Directory, true);
    const FString Name = FString::Printf(TEXT("%03d_%d.png"),CatalogIndex,AuditPhase);
    FScreenshotRequest::RequestScreenshot(Directory/Name, true, false);
    float ActualAge = 0;
    if (auto Controller = Effect->GetSystemInstanceController()) {
        if (auto* Instance = Controller->GetSystemInstance_Unsafe()) ActualAge = Instance->GetAge();
    }
    UE_LOG(LogTemp, Display, TEXT("SanctaReview capture requested: %s | %s | age=%.3f | NiagaraAge=%.3f | rate=%.3f"), *Name, *SkillTitle, PlaybackTime, ActualAge, Effect->GetCustomTimeDilation());
    ++AuditPhase;
}

void ASanctaVFXReviewActor::CaptureQuality(const FString& Suffix)
{
    const FString Directory=FPaths::ProjectSavedDir()/TEXT("QualityCaptures");
    IFileManager::Get().MakeDirectory(*Directory,true);
    const FString Name=FString::Printf(TEXT("%03d_%s.png"),CatalogIndex,*Suffix);
    FScreenshotRequest::RequestScreenshot(Directory/Name,true,false);
    UE_LOG(LogTemp,Display,TEXT("SanctaQuality capture: %s | %s | %s"),*Name,*SkillTitle,*System->GetPathName());
}

void ASanctaVFXReviewActor::TickQuality(float DeltaSeconds, float ActualAge)
{
    AuditHoldTime+=DeltaSeconds;
    if (QualityStage==0) {
        Effect->SetVisibility(false,true);
        Effect->SetPaused(true);
        CaptureQuality(TEXT("baseline"));
        AuditHoldTime=0;
        QualityStage=1;
    } else if (QualityStage==1 && AuditHoldTime>.3f) {
        Effect->SetVisibility(true,true);
        Repeat();
        Effect->SetPaused(true);
        QualityStage=2;
        AuditHoldTime=0;
    } else if (QualityStage==2) {
        if (ReviewSampleTimes.IsValidIndex(AuditPhase)) {
            if (AuditHoldTime>.04f) {
                const float TargetAge=ReviewSampleTimes[AuditPhase];
                Effect->SetPaused(false);
                Effect->AdvanceSimulationByTime(FMath::Max(0.f,TargetAge-ActualAge),1.f/120.f);
                Effect->SetPaused(true);
                CaptureQuality(FString::Printf(TEXT("t%d"),AuditPhase++));
                float SampleAge=0;
                if (auto Controller=Effect->GetSystemInstanceController()) {
                    if (auto* Instance=Controller->GetSystemInstance_Unsafe()) SampleAge=Instance->GetAge();
                }
                const bool bComplete=Effect->IsComplete();
                if (bComplete && QualityCompletionAge<=0.f) QualityCompletionAge=SampleAge;
                UE_LOG(LogTemp,Display,TEXT("SanctaQuality sample age: target=%.4f actual=%.4f complete=%d"),TargetAge,SampleAge,bComplete?1:0);
                AuditHoldTime=0;
            }
        } else if (AuditHoldTime>.3f) {
            Repeat();
            Effect->SetPaused(false);
            // A finite visual cue may expire well before the conservative
            // catalog duration. Orbit a live moment, then keep moving even
            // if the system has naturally completed.
            const float AngleAge=QualityCompletionAge>0.f && ReviewPeakTime>=QualityCompletionAge ? QualityCompletionAge*.6f : ReviewPeakTime;
            Effect->AdvanceSimulationByTime(AngleAge,1.f/120.f);
            Effect->SetPaused(true);
            QualityStage=3;
            AuditHoldTime=0;
        }
    } else if (QualityStage==3 && AuditHoldTime>.04f) {
        Effect->SetPaused(true);
        const FVector Offset=(CameraPosition-CameraTarget).RotateAngleAxis(45.f,FVector::UpVector);
        Camera->SetRelativeLocation(CameraTarget+Offset);
        Camera->SetRelativeRotation((-Offset).Rotation());
        CaptureQuality(TEXT("angle1"));
        AuditHoldTime=0;
        QualityStage=4;
    } else if (QualityStage==4 && AuditHoldTime>.15f) {
        const FVector Offset=(CameraPosition-CameraTarget).RotateAngleAxis(-45.f,FVector::UpVector);
        Camera->SetRelativeLocation(CameraTarget+Offset);
        Camera->SetRelativeRotation((-Offset).Rotation());
        CaptureQuality(TEXT("angle2"));
        AuditHoldTime=0;
        QualityStage=5;
    } else if (QualityStage==5 && AuditHoldTime>.5f) {
        UE_LOG(LogTemp,Display,TEXT("SanctaQuality complete: %d/%d | %s | %s"),CatalogIndex+1,CatalogMaps.Num(),*SkillTitle,*System->GetPathName());
        int32 EndIndex=CatalogMaps.Num()-1;
        FParse::Value(FCommandLine::Get(),TEXT("SanctaReviewEndIndex="),EndIndex);
        int32 NextIndex=CatalogIndex+1;
        FString Requested;
        if (FParse::Value(FCommandLine::Get(),TEXT("SanctaReviewQualityIndices="),Requested,false)) {
            NextIndex=INDEX_NONE;
            TArray<FString> Tokens;
            Requested.ParseIntoArray(Tokens,TEXT(","),true);
            for (const FString& Token:Tokens) {
                const int32 Candidate=FCString::Atoi(*Token);
                if (Candidate>CatalogIndex && Candidate<=EndIndex && CatalogMaps.IsValidIndex(Candidate) && (NextIndex==INDEX_NONE || Candidate<NextIndex)) NextIndex=Candidate;
            }
        }
        if (NextIndex!=INDEX_NONE && NextIndex<CatalogMaps.Num() && NextIndex<=EndIndex) OpenIndex(NextIndex);
        else {
            QualityStage=6;
            // Let the editor deinitialize the play world before ordinary shutdown.
            FinishReview();
        }
    }
}

void ASanctaVFXReviewActor::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    auto* PC = UGameplayStatics::GetPlayerController(this, 0);
    if (!bControllerReady && PC) {
        PC->SetViewTarget(this);
        PC->ClientSetHUD(ASanctaVFXReviewHUD::StaticClass());
        PC->bShowMouseCursor = true;
        PC->bEnableClickEvents = true;
        FInputModeGameAndUI Input;
        Input.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
        Input.SetHideCursorDuringCapture(false);
        PC->SetInputMode(Input);
        bControllerReady = true;
    }
    if (!bReady) {
        LoadingTime += DeltaSeconds;
        bool MaterialsReady = true;
        if (System) {
            System->PollForCompilationComplete();
            for (const auto& Handle : System->GetEmitterHandles()) {
                if (const auto* Data = Handle.GetInstance().GetEmitterData()) {
                    for (const auto* Renderer : Data->GetRenderers()) {
                        TArray<UMaterialInterface*> Materials;
                        Renderer->GetUsedMaterials(nullptr, Materials);
                        for (auto* Material : Materials) {
                            auto* Resource = Material ? Material->GetMaterialResource(GShaderPlatformForFeatureLevel[GetWorld()->GetFeatureLevel()]) : nullptr;
                            if (Resource && !Resource->IsCompilationFinished()) MaterialsReady = false;
                        }
                    }
                }
            }
        }
        if (System && System->IsReadyToRun() && MaterialsReady && LoadingTime > .5f) {
            bReady = true;
            Repeat();
            UE_LOG(LogTemp, Display, TEXT("SanctaReview ready: %d/%d | %s | %s"), CatalogIndex+1, CatalogMaps.Num(), *SkillTitle, *System->GetPathName());
        }
        return;
    }
    if (PC) {
        if (PC->WasInputKeyJustPressed(EKeys::Right)) { OpenIndex(CatalogIndex+1); return; }
        if (PC->WasInputKeyJustPressed(EKeys::Left)) { OpenIndex(CatalogIndex-1); return; }
        if (PC->WasInputKeyJustPressed(EKeys::R)) Repeat();
        if (PC->WasInputKeyJustPressed(EKeys::SpaceBar)) TogglePause();
        if (PC->WasInputKeyJustPressed(EKeys::S)) ToggleSlow();
    }
    if (!bPaused) PlaybackTime += DeltaSeconds * (bSlow ? 1.f/3.f : 1.f);
    float ActualAge = 0;
    if (auto Controller = Effect->GetSystemInstanceController()) {
        if (auto* Instance = Controller->GetSystemInstance_Unsafe()) ActualAge = Instance->GetAge();
    }
    if (bQuality) { TickQuality(DeltaSeconds,ActualAge); return; }
    if (!bAudit && !bPaused && Effect->IsComplete()) {
        CompletionHold+=DeltaSeconds;
        if (CompletionHold>=.25f) {
            Repeat();
            if (bLoopCheck && RepeatCount>=4) {
                UE_LOG(LogTemp,Display,TEXT("SanctaLoop complete: four repeats in real game playback"));
                bLoopCheck=false;
                FinishReview();
            }
        }
        return;
    }
    if (bAudit && AuditPhase < 5) {
        const float PhaseTimes[] = {.1f,.3f,.6f,1.2f,FMath::Max(1.5f,CycleDuration*.8f)};
        if (ActualAge >= PhaseTimes[AuditPhase] || PlaybackTime >= CycleDuration + .35f) CaptureAudit();
    }
    if (bAuditAll && AuditPhase >= 5) {
        // Keep actual world playback for material-age bindings and allow the
        // final requested image to finish before moving to the next scene.
        AuditHoldTime += DeltaSeconds;
        if (AuditHoldTime > .15f && CatalogIndex+1 < CatalogMaps.Num()) { OpenIndex(CatalogIndex+1); return; }
    }
    if (!bPaused && PlaybackTime >= CycleDuration + .35f && (ActualAge >= CycleDuration || Effect->IsComplete())) {
        if (bAuditAll && AuditPhase >= 5 && CatalogIndex+1 < CatalogMaps.Num()) { OpenIndex(CatalogIndex+1); return; }
        Repeat();
    }
}

ASanctaVFXReviewActor* ASanctaVFXReviewHUD::Stage() const
{
    for (TActorIterator<ASanctaVFXReviewActor> It(GetWorld()); It; ++It) return *It;
    return nullptr;
}

void ASanctaVFXReviewHUD::Button(FName Id, const FString& Label, float X, float Y, float Width)
{
    DrawRect(FLinearColor(.075,.09,.12,.96),X,Y,Width,34);
    DrawText(Label,FLinearColor(.92,.95,1),X+10,Y+8,nullptr,.95f);
    AddHitBox(FVector2D(X,Y),FVector2D(Width,34),Id,true);
}

void ASanctaVFXReviewHUD::DrawHUD()
{
    Super::DrawHUD();
    auto* A = Stage();
    if (!Canvas || !A) return;
    const float W = Canvas->SizeX, H = Canvas->SizeY;
    DrawRect(FLinearColor(.012,.018,.025,.94),0,0,W,82);
    DrawText(FString::Printf(TEXT("%d / %d   %s"),A->CatalogIndex+1,A->CatalogMaps.Num(),*A->SkillTitle), FLinearColor::White,24,16,nullptr,1.5f);
    DrawText(A->SkillClass + TEXT("   |   ") + (A->bReady ? (A->bPaused ? TEXT("Pausa") : TEXT("Reproducao em ciclo")) : TEXT("A preparar o efeito...")),FLinearColor(.65,.72,.8),24,51,nullptr,1);
    const float Y=H-53;
    DrawRect(FLinearColor(.012,.018,.025,.94),0,H-66,W,66);
    Button(TEXT("Previous"),TEXT("< Anterior"),18,Y,112);
    Button(TEXT("Next"),TEXT("Seguinte >"),138,Y,112);
    Button(TEXT("Repeat"),TEXT("Repetir (R)"),258,Y,120);
    Button(TEXT("Pause"),A->bPaused ? TEXT("Continuar") : TEXT("Pausa"),386,Y,110);
    Button(TEXT("Slow"),A->bSlow ? TEXT("Velocidade 1/3") : TEXT("Velocidade normal"),504,Y,155);
    Button(TEXT("List"),TEXT("Todas as skills"),667,Y,160);
    Button(TEXT("ZoomIn"),TEXT("Zoom +"),835,Y,100);
    Button(TEXT("ZoomOut"),TEXT("Zoom -"),943,Y,100);
    Button(TEXT("ZoomReset"),TEXT("Repor vista"),1051,Y,130);
    if (!bList) return;
    const float Left=20, Top=94, PanelW=FMath::Min(W-40,1000.f);
    DrawRect(FLinearColor(.02,.027,.04,.99),Left,Top,PanelW,H-170);
    const int32 Rows=FMath::Max(1,FMath::Min(16,FMath::FloorToInt((H-250)/31)));
    const int32 PageSize=Rows*2;
    const int32 Pages=FMath::Max(1,FMath::DivideAndRoundUp(A->CatalogMaps.Num(),PageSize));
    ListPage=FMath::Clamp(ListPage,0,Pages-1);
    DrawText(FString::Printf(TEXT("Escolhe uma skill   |   pagina %d/%d"),ListPage+1,Pages),FLinearColor::White,Left+15,Top+12,nullptr,1.05f);
    for (int32 Slot=0;Slot<PageSize;++Slot) {
        const int32 Index=ListPage*PageSize+Slot;
        if (!A->CatalogMaps.IsValidIndex(Index)) break;
        const float X=Left+12+(Slot/Rows)*(PanelW*.5f);
        const float RowY=Top+43+(Slot%Rows)*31;
        const FString Label=FString::Printf(TEXT("%03d  %s"),Index+1,*A->CatalogTitles[Index]);
        DrawRect(FLinearColor(.075,.09,.12),X,RowY,PanelW*.5f-24,28);
        DrawText(Label,FLinearColor(.92,.95,1),X+7,RowY+6,nullptr,.85f);
        AddHitBox(FVector2D(X,RowY),FVector2D(PanelW*.5f-24,28),FName(*FString::Printf(TEXT("Entry_%d"),Index)),true);
    }
    Button(TEXT("PagePrevious"),TEXT("< Pagina"),Left+12,H-118,110);
    Button(TEXT("PageNext"),TEXT("Pagina >"),Left+130,H-118,110);
    Button(TEXT("CloseList"),TEXT("Fechar lista"),Left+248,H-118,125);
}

void ASanctaVFXReviewHUD::NotifyHitBoxClick(FName BoxName)
{
    auto* A=Stage(); if (!A) return;
    if (BoxName==TEXT("Previous")) A->OpenIndex(A->CatalogIndex-1);
    else if (BoxName==TEXT("Next")) A->OpenIndex(A->CatalogIndex+1);
    else if (BoxName==TEXT("Repeat")) A->Repeat();
    else if (BoxName==TEXT("Pause")) A->TogglePause();
    else if (BoxName==TEXT("Slow")) A->ToggleSlow();
    else if (BoxName==TEXT("ZoomIn")) A->Camera->SetFieldOfView(FMath::Max(20.f,A->Camera->FieldOfView-10.f));
    else if (BoxName==TEXT("ZoomOut")) A->Camera->SetFieldOfView(FMath::Min(100.f,A->Camera->FieldOfView+10.f));
    else if (BoxName==TEXT("ZoomReset")) A->Camera->SetFieldOfView(55.f);
    else if (BoxName==TEXT("List")) { bList=!bList; ListPage=0; }
    else if (BoxName==TEXT("CloseList")) bList=false;
    else if (BoxName==TEXT("PagePrevious")) --ListPage;
    else if (BoxName==TEXT("PageNext")) ++ListPage;
    else if (BoxName.ToString().StartsWith(TEXT("Entry_"))) A->OpenIndex(FCString::Atoi(*BoxName.ToString().Mid(6)));
}
