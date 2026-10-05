#include "SanctaVFXRuntimeReview.h"
#include "NiagaraComponent.h"
#include "NiagaraSystem.h"
#include "Camera/CameraComponent.h"
#include "Components/SceneComponent.h"
#include "Engine/World.h"
#include "Engine/GameViewportClient.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "DynamicRHI.h"
#include "HAL/FileManager.h"
#include "Editor.h"
#include "Containers/Ticker.h"
#include "SanctaVFXTerrain.h"
#include "Engine/StaticMeshActor.h"
#include "HAL/IConsoleManager.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "InputCoreTypes.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "ImageUtils.h"
#include "UnrealClient.h"
#include "NiagaraSystemInstanceController.h"
#include "NiagaraSystemInstance.h"
#include "NiagaraEmitterInstance.h"
#include "ShaderCompiler.h"

void ASanctaVFXRuntimeReview::BeginPlay()
{
    Super::BeginPlay(); Effect->SetVisibility(false);Effect->DeactivateImmediate();
    TSharedRef<TJsonReader<>> Reader=TJsonReaderFactory<>::Create(CasesJSON);
    FJsonSerializer::Deserialize(Reader,Cases);
    ViewerAudit=bInteractive&&FParse::Param(FCommandLine::Get(),TEXT("SanctaRuntimeViewerAudit"));
    if(bInteractive){
        CatalogMaps.Reset();CatalogTitles.Reset();bSlow=bPaused=false;
        for(const auto& V:Cases){FString Title;const auto J=V->AsObject();if(!J->TryGetStringField(TEXT("title"),Title))Title=J->GetStringField(TEXT("name"));CatalogMaps.Add(J->GetStringField(TEXT("name")));CatalogTitles.Add(Title);}
        if(!CatalogTitles.IsEmpty())SkillTitle=CatalogTitles[0];SkillClass=TEXT("Fases de integracao | inputs de teste");
    }
    auto Spawn=[&](FVector P){auto* A=GetWorld()->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);A->SetRootComponent(Root);Root->RegisterComponentWithWorld(GetWorld());A->SetActorLocation(P);return A;};
    TestSource=Spawn(FVector::ZeroVector);TestTarget=Spawn(FVector::ZeroVector);TestProjectile=Spawn(FVector(0,0,100));
    Presentation=NewObject<USanctaVFXPresentationComponent>(TestSource);Presentation->RegisterComponentWithWorld(GetWorld());
    auto* TC=NewObject<USanctaVFXPresentationComponent>(TestTarget);TC->RegisterComponentWithWorld(GetWorld());TC->LifeId=FGuid::NewGuid();
    Inputs.Source=TestSource;Inputs.Target=TestTarget;Inputs.Projectile=TestProjectile;Inputs.TargetLifeId=TC->LifeId;
}
void ASanctaVFXRuntimeReview::Repeat()
{
    if(!Presentation)return;
    Presentation->ResetForLife(FGuid::NewGuid());for(auto A:BatchActors)if(A)A->Destroy();BatchActors.Reset();
    if(ReviewTerrain){ReviewTerrain->RemoveTerrain();ReviewTerrain=nullptr;}
    Started=Captured=CompileRequested=bReady=false;Wait=PlaybackTime=0;
}
void ASanctaVFXRuntimeReview::TogglePause(){bPaused=!bPaused;}
void ASanctaVFXRuntimeReview::ToggleSlow(){bSlow=!bSlow;}
void ASanctaVFXRuntimeReview::OpenIndex(int32 Index)
{
    if(Cases.IsEmpty())return;
    Repeat();CaseIndex=CatalogIndex=(Index%Cases.Num()+Cases.Num())%Cases.Num();
    if(CatalogTitles.IsValidIndex(CaseIndex))SkillTitle=CatalogTitles[CaseIndex];
}
void ASanctaVFXRuntimeReview::Tick(float Delta)
{
    // Do not tick the recorded demonstration in the parent review actor.
    if (!ViewReady) if (auto* PC=UGameplayStatics::GetPlayerController(this,0)) {
        PC->SetViewTarget(this);PC->ClientSetHUD(bInteractive?ASanctaVFXReviewHUD::StaticClass():nullptr);
        if(bInteractive){PC->bShowMouseCursor=true;FInputModeGameAndUI Mode;Mode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);Mode.SetHideCursorDuringCapture(false);PC->SetInputMode(Mode);}
        ViewReady=true;
    }
    if(bInteractive)if(auto* PC=UGameplayStatics::GetPlayerController(this,0)){
        if(PC->WasInputKeyJustPressed(EKeys::Right)){OpenIndex(CaseIndex+1);return;}
        if(PC->WasInputKeyJustPressed(EKeys::Left)){OpenIndex(CaseIndex-1);return;}
        if(PC->WasInputKeyJustPressed(EKeys::R))Repeat();
        if(PC->WasInputKeyJustPressed(EKeys::SpaceBar))TogglePause();
        if(PC->WasInputKeyJustPressed(EKeys::S))ToggleSlow();
    }
    Wait+=Delta;
    if (!Cases.IsValidIndex(CaseIndex)) {
        if(bInteractive)return;
        if (Wait<.5f)return;
        FString Out;FJsonSerializer::Serialize(PerfResults,TJsonWriterFactory<>::Create(&Out));
        FFileHelper::SaveStringToFile(Out,*(FPaths::ProjectSavedDir()/TEXT("RuntimeCaptures/frame-costs.json")));
        FString Captures;FJsonSerializer::Serialize(CaptureResults,TJsonWriterFactory<>::Create(&Captures));
        CaptureSucceeded&=FFileHelper::SaveStringToFile(Captures,*(FPaths::ProjectSavedDir()/TEXT("RuntimeCaptures/capture-frames.json")));
        GEditor->RequestEndPlayMap();SetActorTickEnabled(false);
        const uint8 ExitCode=CaptureSucceeded?0:1;
        FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([ExitCode](float){if(GEditor&&GEditor->IsPlaySessionInProgress())return true;FPlatformMisc::RequestExitWithStatus(false,ExitCode);return false;}),.5f);return;
    }
    const auto J=Cases[CaseIndex]->AsObject();
    if (!Started) {
        auto* Def=LoadObject<USanctaVFXDefinition>(nullptr,*J->GetStringField(TEXT("definition")));
        if (!Def){if(bInteractive)SkillClass=TEXT("Definicao em falta — consultar log; Proxima continua disponivel");return;}
        if(!CompileRequested){for(const auto& P:Def->Phases)if(P.System)P.System->RequestCompile(false);CompileRequested=true;}
        bool Ready=true;for(const auto& P:Def->Phases)if(P.System)Ready&=P.System->IsReadyToRun();
        // Niagara readiness does not include asynchronously compiled material
        // shaders. Do not start a phase while its renderer still uses a fallback.
        if (!Ready || (GShaderCompilingManager&&GShaderCompilingManager->IsCompiling()) || Wait<.5f)return;
        Presentation->ResetForLife(FGuid::NewGuid());Presentation->Definitions={Def};
        Inputs.FormId=Def->FormId;Inputs.Phase=FName(*J->GetStringField(TEXT("phase")));Inputs.ExecutionId=FGuid::NewGuid();Inputs.StateId=FGuid::NewGuid();
        auto Number=[&](const TCHAR* Key,double Default){double V;return J->TryGetNumberField(Key,V)?V:Default;};
        bool Decorative=true;J->TryGetBoolField(TEXT("decorative_enabled"),Decorative);Presentation->bDecorativeEnabled=Decorative;
        Inputs.PhaseAge=bInteractive?0:Number(TEXT("age"),.15);Inputs.ResourceCount=Number(TEXT("count"),0);Inputs.ResourceMax=Number(TEXT("max"),10);Inputs.OccupiedMask=Number(TEXT("occupied"),0);
        Inputs.ElementA=Number(TEXT("element_a"),-1);Inputs.ElementB=Number(TEXT("element_b"),-1);Inputs.CastProgress=Number(TEXT("hold"),0);Inputs.ReleaseAge=Number(TEXT("release"),-1);
        Inputs.GainAge=Number(TEXT("gain_age"),-1);Inputs.Pending=Number(TEXT("pending"),0);Inputs.EventSequence=0;
        Inputs.bAdmitted=Inputs.bApplied=Inputs.bConfirmedHit=true;Inputs.bNaturalEnd=Inputs.bCleansed=true;Inputs.ConfirmedProcMask=MAX_int32;
        if(Def->Phases[0].Anchor==ESanctaVFXAnchor::Link)TestTarget->SetActorLocation(FVector(250,0,100));else TestTarget->SetActorLocation(FVector::ZeroVector);
        TestTarget->SetActorLocation(FVector(Number(TEXT("target_x"),TestTarget->GetActorLocation().X),Number(TEXT("target_y"),TestTarget->GetActorLocation().Y),Number(TEXT("target_z"),TestTarget->GetActorLocation().Z)));
        TestProjectile->SetActorLocation(FVector(0,-110,110));
        if(Inputs.Phase==TEXT("Trail"))TestSource->SetActorLocation(FVector(0,-35,120));else TestSource->SetActorLocation(FVector::ZeroVector);
        TestSource->SetActorLocation(FVector(Number(TEXT("source_x"),TestSource->GetActorLocation().X),Number(TEXT("source_y"),TestSource->GetActorLocation().Y),Number(TEXT("source_z"),TestSource->GetActorLocation().Z)));
        const FSanctaVFXPhase* Selected=Def->Phases.FindByPredicate([&](const FSanctaVFXPhase& P){return P.Phase==Inputs.Phase;});
        Inputs.Endpoint=FVector(150,-35,120);Inputs.Position=Selected&&Selected->bContact?FVector(0,-55,110):FVector::ZeroVector;
        Inputs.Position=FVector(Number(TEXT("position_x"),Inputs.Position.X),Number(TEXT("position_y"),Inputs.Position.Y),Number(TEXT("position_z"),Inputs.Position.Z));
        if(Selected){Inputs.Radius=Selected->ReferenceRadius;Inputs.Range=Selected->ReferenceRange;Inputs.ConeAngle=Selected->ReferenceConeAngle;}
        Inputs.Radius=Number(TEXT("radius"),Inputs.Radius);Inputs.Range=Number(TEXT("range"),Inputs.Range);Inputs.ConeAngle=Number(TEXT("cone"),Inputs.ConeAngle);
        if(J->HasField(TEXT("camera_x"))){Camera->SetRelativeLocation(FVector(Number(TEXT("camera_x"),230),Number(TEXT("camera_y"),-480),Number(TEXT("camera_z"),270)));Camera->SetRelativeRotation((FVector(Number(TEXT("look_x"),0),Number(TEXT("look_y"),0),Number(TEXT("look_z"),100))-Camera->GetRelativeLocation()).Rotation());}
        bool Bright=false;J->TryGetBoolField(TEXT("bright"),Bright);
        auto* FloorMaterial=LoadObject<UMaterialInterface>(nullptr,Bright?TEXT("/Game/Sancta/VFX/Review/Common/M_RuntimeFloorBright"):TEXT("/Game/VFXLab/Review/Fixtures/M_ReviewFloor"));
        TArray<AActor*> Floors;UGameplayStatics::GetAllActorsOfClass(GetWorld(),AStaticMeshActor::StaticClass(),Floors);
        for(auto* A:Floors)if(A->ActorHasTag(TEXT("RuntimeFloor")))Cast<AStaticMeshActor>(A)->GetStaticMeshComponent()->SetMaterial(0,FloorMaterial);
        bool Terrain=false;J->TryGetBoolField(TEXT("terrain"),Terrain);
        if(Terrain){
            ReviewTerrain=GetWorld()->SpawnActor<ASanctaVFXTerrain>();ReviewTerrain->SetActorLocation(Inputs.Position);
            ReviewTerrain->InitializeTerrain(LoadObject<UStaticMesh>(nullptr,TEXT("/Game/Sancta/VFX/Terrain/Iceberg/SM_IcebergBody")),LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Sancta/VFX/Terrain/Iceberg/M_IcebergBody")),FVector::OneVector);
            ReviewTerrain->SetIntegrity(Number(TEXT("integrity"),1));
        }
        Inputs.ModeSnapshot=Def->Phases[0].RequiredModeSnapshot;Inputs.StanceSnapshot=Def->Phases[0].RequiredStanceSnapshot;Inputs.Relation=Def->Phases[0].RequiredRelation;
        FString Surface;Inputs.Surface=J->TryGetStringField(TEXT("surface"),Surface)?FName(*Surface):NAME_None;
        PerfTarget=Number(TEXT("perf_frames"),0);PerfFrames=0;GPUFrames.Reset();InputUpdates.Reset();BatchInputs.Reset();
        const int32 InstanceCount=Number(TEXT("instances"),1);
        const double SpawnStart=FPlatformTime::Seconds();int32 Created=0;
        for(int32 Index=0;Index<InstanceCount;++Index){
            auto E=Inputs;E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();
            if(InstanceCount>1){
                const FVector Position((Index%8-3.5f)*130,(Index/8-2.5f)*130,0);
                auto* A=GetWorld()->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);A->SetRootComponent(Root);Root->RegisterComponentWithWorld(GetWorld());A->SetActorLocation(Position);
                E.Source=A;E.Position=Position;BatchActors.Add(A);
            }
            if(Selected&&Selected->Gate==ESanctaVFXGate::NaturalEnd)Presentation->EndState(E.StateId,ESanctaVFXEndReason::Natural);
            if(Selected&&Selected->Gate==ESanctaVFXGate::Cleanse)Presentation->EndState(E.StateId,ESanctaVFXEndReason::Cleanse);
            Created+=Presentation->Present(E);BatchInputs.Add(E);
        }
        SpawnMilliseconds=(FPlatformTime::Seconds()-SpawnStart)*1000;
        if(PerfTarget>0){Camera->SetRelativeLocation(FVector(600,-1700,1100));Camera->SetRelativeRotation((FVector(0,0,100)-Camera->GetRelativeLocation()).Rotation());}
        for(const auto& P:Def->Phases)if(auto* N=Presentation->GetActiveComponent(P.ComponentKey)){N->SetForceSolo(true);N->SetAllowScalability(false);N->SetCastShadow(false);if(PerfTarget==0){N->SetVariableFloat(TEXT("User.CueLifetime"),bInteractive?1.e9f:30.f);N->ReinitializeSystem();}N->SetPaused(false);}
        RenderWarmed=false;
        UE_LOG(LogTemp,Display,TEXT("SanctaRuntimeReview admitted: %s count=%d"),*J->GetStringField(TEXT("name")),Created);
        Started=bReady=true;Wait=0;PlaybackTime=0;
    }
    if(bInteractive){
        if(!bPaused&&RenderWarmed)PlaybackTime+=Delta*(bSlow?1.f/3.f:1.f);
        const auto* Def=Presentation->Definitions[0].Get();const auto* Selected=Def->Phases.FindByPredicate([&](const FSanctaVFXPhase& P){return P.Phase==Inputs.Phase;});
        if(Selected&&Selected->Anchor==ESanctaVFXAnchor::Projectile)TestProjectile->SetActorLocation(FVector(-180.f+FMath::Fmod(PlaybackTime,1.2f)*350.f,-110,110));
        if(Inputs.Phase==TEXT("Trail")){
            const float A=FMath::Lerp(-1.2f,1.2f,FMath::Clamp(PlaybackTime/.42f,0.f,1.f));
            TestProjectile->SetActorLocation(TestSource->GetActorLocation()+FVector(FMath::Cos(A)*150,FMath::Sin(A)*150,15));
            for(auto& E:BatchInputs)E.EndpointActor=TestProjectile;
        }
        for(auto& E:BatchInputs){
            E.PhaseAge=PlaybackTime;
            if(E.Phase==TEXT("Hold")){E.CastProgress=FMath::Clamp(PlaybackTime/1.5f,0.f,1.f);E.GainAge=PlaybackTime>=1.5f?PlaybackTime-1.5f:-1.f;if(SkillTitle.Contains(TEXT("Volley"))){E.Range=1800.f*(.5f+.5f*E.CastProgress);E.ConeAngle=50.f*(1.f-E.CastProgress);}}
            if(E.Phase==TEXT("End"))E.ReleaseAge=PlaybackTime;
            if(SkillTitle.Contains(TEXT("Arcane"))&&SkillTitle.Contains(TEXT("Weaving"))){E.ResourceCount=FMath::Min(E.ResourceMax,int32(PlaybackTime/.65f));E.GainAge=FMath::Fmod(PlaybackTime,.65f);}
            if(SkillTitle.Contains(TEXT("Elemental"))){E.OccupiedMask=PlaybackTime<.8f?0:PlaybackTime<1.6f?1:3;E.ElementA=int32(PlaybackTime/2.4f)%3;E.ElementB=J->GetStringField(TEXT("name")).Contains(TEXT("WeaverIi"))?(E.ElementA+1)%3:E.ElementA;}
        }
        if(Selected&&PlaybackTime>(Selected->bPersistent?8.f:Selected->Duration+.35f)){Repeat();return;}
    }
    // Keep the material snapshot fixed while the real Niagara render thread warms.
    const double UpdateStart=FPlatformTime::Seconds();
    for(const auto& E:BatchInputs)Presentation->UpdatePresentation(E);
    const double UpdateMs=(FPlatformTime::Seconds()-UpdateStart)*1000;
    // The material clock owns the snapshot/pause. Keep Niagara ticking so each
    // render frame receives current mesh data, even after asynchronous warmup.
    // Shader jobs can also be queued when a renderer is first instantiated.
    // Restart the warmup after these jobs finish; the snapshot stays fixed.
    if(GShaderCompilingManager&&GShaderCompilingManager->IsCompiling()){
        RenderWarmed=false;Wait=0;return;
    }
    if(PerfTarget==0&&!RenderWarmed&&Wait>.4f)RenderWarmed=true;
    if(bInteractive){
        if(ViewerAudit){
            ASanctaVFXReviewActor* Controls=this; // Same virtual dispatch as HUD buttons.
            if(ViewerAuditStep==0&&PlaybackTime>.1f){ViewerAuditPassed&=!bSlow;Controls->TogglePause();ViewerPausedAge=PlaybackTime;ViewerAuditStep=1;Wait=0;}
            else if(ViewerAuditStep==1&&Wait>.2f){
                ViewerAuditPassed&=bPaused&&FMath::IsNearlyEqual(PlaybackTime,ViewerPausedAge);
                Controls->TogglePause();Controls->ToggleSlow();ViewerAuditPassed&=bSlow;Controls->ToggleSlow();
                Controls->OpenIndex(CaseIndex+1);ViewerAuditPassed&=CaseIndex==1&&Presentation->GetActiveCount()==0;ViewerAuditStep=2;
            }else if(ViewerAuditStep==2&&PlaybackTime>.1f){
                Controls->Repeat();ViewerAuditPassed&=PlaybackTime==0&&Presentation->GetActiveCount()==0;
                auto R=MakeShared<FJsonObject>();R->SetBoolField(TEXT("passed"),ViewerAuditPassed);R->SetNumberField(TEXT("default_playback_rate"),1);R->SetNumberField(TEXT("catalog_cases"),Cases.Num());
                R->SetStringField(TEXT("scope"),TEXT("PIE runtime viewer: actual HUD control method dispatch, normal startup rate, pause, slow toggle, next phase, repeat and old-component cleanup. Mouse/key delivery remains a user interaction check."));
                FString Out;FJsonSerializer::Serialize(R,TJsonWriterFactory<>::Create(&Out));FFileHelper::SaveStringToFile(Out,*(FPaths::ProjectDir()/TEXT("Evidence/gameplay-runtime-viewer-validation.json")));
                UE_LOG(LogTemp,Display,TEXT("SanctaRuntimeViewer audit passed=%d"),ViewerAuditPassed);SetActorTickEnabled(false);GEditor->RequestEndPlayMap();
                const uint8 ExitCode=ViewerAuditPassed?0:1;
                FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([ExitCode](float){if(GEditor&&GEditor->IsPlaySessionInProgress())return true;FPlatformMisc::RequestExitWithStatus(false,ExitCode);return false;}),.5f);
            }
        }
        return;
    }
    if(PerfTarget>0 && Wait>1.f){
        ++PerfFrames;InputUpdates.Add(UpdateMs);
        const uint32 Cycles=RHIGetGPUFrameCycles();if(Cycles>0)GPUFrames.Add(FPlatformTime::ToMilliseconds(Cycles));
    }
    if (!Captured && Wait>.65f) {
        const FString Dir=FPaths::ProjectSavedDir()/TEXT("RuntimeCaptures");IFileManager::Get().MakeDirectory(*Dir,true);
        const FString Name=J->GetStringField(TEXT("name"))+TEXT(".png");
        // A global screenshot request can be consumed by an editor viewport.
        // Read only the viewport belonging to this PIE world.
        auto* Client=GetWorld()->GetGameViewport();auto* Viewport=Client?Client->Viewport:nullptr;
        // Offscreen Slate windows can leave a cached framebuffer. Draw the
        // owning game viewport explicitly before reading the current snapshot.
        if(Viewport)Viewport->Draw(false);
        TArray<FColor> Pixels;bool Ok=Viewport&&GetViewportScreenShot(Viewport,Pixels);
        if(!Ok&&Wait<5.f)return;
        FIntPoint Size=Viewport?Viewport->GetSizeXY():FIntPoint::ZeroValue;
        if(Ok){for(auto& Pixel:Pixels)Pixel.A=255;TArray64<uint8> PNG;FImageUtils::PNGCompressImageArray(Size.X,Size.Y,Pixels,PNG);Ok=FFileHelper::SaveArrayToFile(PNG,*(Dir/Name));}
        int32 Particles=0;
        for(const auto& P:Presentation->Definitions[0]->Phases)if(auto* N=Presentation->GetActiveComponent(P.ComponentKey))if(auto Controller=N->GetSystemInstanceController())if(auto* Instance=Controller->GetSystemInstance_Unsafe())for(const auto& Emitter:Instance->GetEmitters())Particles+=Emitter->GetNumParticles();
        auto Frame=MakeShared<FJsonObject>();Frame->SetStringField(TEXT("case"),J->GetStringField(TEXT("name")));Frame->SetBoolField(TEXT("saved"),Ok);Frame->SetNumberField(TEXT("width"),Size.X);Frame->SetNumberField(TEXT("height"),Size.Y);Frame->SetNumberField(TEXT("particles"),Particles);Frame->SetNumberField(TEXT("active_components"),Presentation->GetActiveCount());Frame->SetStringField(TEXT("viewport"),TEXT("Owning PIE world GameViewport"));Frame->SetBoolField(TEXT("analytic_snapshot_particle_lifetime_override"),PerfTarget==0);CaptureResults.Add(MakeShared<FJsonValueObject>(Frame));
        CaptureSucceeded&=Ok;
        UE_LOG(LogTemp,Display,TEXT("SanctaRuntimeReview capture: %s saved=%d particles=%d active=%d"),*Name,Ok,Particles,Presentation->GetActiveCount());Captured=true;
    }
    if (Captured && Wait>.5f && (PerfTarget==0 || PerfFrames>=PerfTarget)) {
        if(PerfTarget>0){
            auto R=MakeShared<FJsonObject>();R->SetStringField(TEXT("case"),J->GetStringField(TEXT("name")));R->SetNumberField(TEXT("actual_instances"),Presentation->GetActiveCount());R->SetNumberField(TEXT("spawn_cpu_ms"),SpawnMilliseconds);
            auto Mean=[](const TArray<double>& A){double Sum=0;for(double V:A)Sum+=V;return A.IsEmpty()?0:Sum/A.Num();};
            R->SetNumberField(TEXT("input_update_cpu_ms"),Mean(InputUpdates));R->SetNumberField(TEXT("gpu_frame_ms"),Mean(GPUFrames));R->SetNumberField(TEXT("gpu_samples"),GPUFrames.Num());
            for(const TCHAR* Name:{TEXT("t.IdleWhenNotForeground"),TEXT("Slate.bAllowThrottling"),TEXT("r.VSync")})if(auto* V=IConsoleManager::Get().FindConsoleVariable(Name))R->SetNumberField(Name,V->GetInt());
            R->SetStringField(TEXT("scope"),TEXT("Total lab PIE viewport GPU frame, not isolated effect cost. Input update excludes Niagara simulation/render work. Compare baseline/1/16/48; shipping target and multiplayer still require profiling."));
            PerfResults.Add(MakeShared<FJsonValueObject>(R));
        }
        Presentation->ResetForLife(FGuid::NewGuid());for(auto A:BatchActors)if(A)A->Destroy();BatchActors.Reset();
        if(ReviewTerrain){ReviewTerrain->RemoveTerrain();ReviewTerrain=nullptr;}
        ++CaseIndex;Started=Captured=CompileRequested=false;Wait=0;
    }
}
