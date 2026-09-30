#include "SanctaVFXLabLibrary.h"
#include "NiagaraSystem.h"
#include "NiagaraScript.h"
#include "NiagaraEmitter.h"
#include "NiagaraComponent.h"
#include "NiagaraFunctionLibrary.h"
#include "NiagaraSystemInstanceController.h"
#include "NiagaraSystemInstance.h"
#include "NiagaraEmitterInstance.h"
#include "NiagaraDataSetAccessor.h"
#include "Engine/World.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
#include "Engine/SceneCapture2D.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "RenderingThread.h"
#include "AssetCompilingManager.h"

static FString Json(const TSharedRef<FJsonObject>& Object)
{
    FString Result;
    FJsonSerializer::Serialize(Object, TJsonWriterFactory<>::Create(&Result));
    return Result;
}

bool USanctaVFXLabLibrary::SetUserFloat(UNiagaraSystem* System, FString Name, float Value)
{
    if (!System || !Name.StartsWith(TEXT("User."))) return false;
    FNiagaraVariable Var(FNiagaraTypeDefinition::GetFloatDef(), FName(*Name));
    const bool Success = System->GetExposedParameters().SetParameterValue<float>(Value, Var, true);
    System->MarkPackageDirty();
    return Success;
}

FString USanctaVFXLabLibrary::InspectSystem(UNiagaraSystem* System)
{
    auto Root = MakeShared<FJsonObject>();
    if (!System) { Root->SetStringField(TEXT("error"), TEXT("null system")); return Json(Root); }
    System->WaitForCompilationComplete(true, false);
    Root->SetBoolField(TEXT("ready_to_run"), System->IsReadyToRun());
    Root->SetNumberField(TEXT("emitter_count"), System->GetEmitterHandles().Num());
    TArray<TSharedPtr<FJsonValue>> Emitters;
    for (const FNiagaraEmitterHandle& Handle : System->GetEmitterHandles())
    {
        auto Obj = MakeShared<FJsonObject>();
        Obj->SetStringField(TEXT("name"), Handle.GetName().ToString());
        Obj->SetBoolField(TEXT("enabled"), Handle.GetIsEnabled());
        const auto* Data = Handle.GetInstance().GetEmitterData();
        if (Data) Obj->SetNumberField(TEXT("renderer_count"), Data->GetRenderers().Num());
        Emitters.Add(MakeShared<FJsonValueObject>(Obj));
    }
    Root->SetArrayField(TEXT("emitters"), Emitters);
    TArray<TSharedPtr<FJsonValue>> Params;
    for (const FNiagaraVariableWithOffset& Param : System->GetExposedParameters().ReadParameterVariables())
        Params.Add(MakeShared<FJsonValueString>(Param.GetName().ToString()));
    Root->SetArrayField(TEXT("user_parameters"), Params);
    return Json(Root);
}

bool USanctaVFXLabLibrary::CaptureSystem(UNiagaraSystem* System, UWorld* World, float Time, FString Directory, FString FileName)
{
    if (!System || !World) return false;
    System->WaitForCompilationComplete(true, false);
    FAssetCompilingManager::Get().FinishAllCompilation();
    auto* Component = UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, System, FVector(0,0,100), FRotator::ZeroRotator, FVector::OneVector, false, false, ENCPoolMethod::None, false);
    if (!Component) return false;
    Component->SetForceSolo(true);
    Component->Activate(true);
    Component->AdvanceSimulation(FMath::RoundToInt(Time*60),1.0f/60.0f);
    auto* CaptureActor = World->SpawnActor<ASceneCapture2D>();
    auto* Capture = CaptureActor->GetCaptureComponent2D();
    Capture->bCaptureEveryFrame = false;
    Capture->bCaptureOnMovement = false;
    Capture->CaptureSource = ESceneCaptureSource::SCS_FinalColorLDR;
    Capture->FOVAngle = 60;
    CaptureActor->SetActorLocation(FVector(400,-900,270));
    CaptureActor->SetActorRotation((FVector(400,0,100)-CaptureActor->GetActorLocation()).Rotation());
    Capture->PostProcessSettings.bOverride_AutoExposureMethod = true;
    Capture->PostProcessSettings.AutoExposureMethod = EAutoExposureMethod::AEM_Manual;
    Capture->PostProcessSettings.bOverride_AutoExposureBias = true;
    Capture->PostProcessSettings.AutoExposureBias = 0;
    Capture->PostProcessSettings.bOverride_BloomIntensity = true;
    Capture->PostProcessSettings.BloomIntensity = .5f;
    auto* Target = UKismetRenderingLibrary::CreateRenderTarget2D(World,1280,720,RTF_RGBA8,FLinearColor(.018f,.022f,.03f,1));
    Capture->TextureTarget = Target;
    World->SendAllEndOfFrameUpdates();
    FlushRenderingCommands();
    Capture->CaptureScene();
    FlushRenderingCommands();
    UKismetRenderingLibrary::ExportRenderTarget(World,Target,Directory,FileName);
    Component->DestroyComponent();
    CaptureActor->Destroy();
    return FPaths::FileExists(Directory/FileName);
}

FString USanctaVFXLabLibrary::SimulateSystem(UNiagaraSystem* System, UWorld* World, TArray<float> Times)
{
    auto Root = MakeShared<FJsonObject>();
    if (!System || !World) { Root->SetStringField(TEXT("error"), TEXT("null system/world")); return Json(Root); }
    System->WaitForCompilationComplete(true, false);
    auto* Component = UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, System, FVector::ZeroVector, FRotator::ZeroRotator, FVector::OneVector, false, false, ENCPoolMethod::None, false);
    if (!Component) { Root->SetStringField(TEXT("error"), TEXT("spawn failed")); return Json(Root); }
    Component->SetForceSolo(true);
    Component->Activate(true);
    TArray<TSharedPtr<FJsonValue>> Frames;
    int32 CompletedTicks = 0;
    for (float Time : Times)
    {
        int32 TargetTicks = FMath::RoundToInt(Time * 60.0f);
        Component->AdvanceSimulation(FMath::Max(0, TargetTicks-CompletedTicks), 1.0f/60.0f);
        CompletedTicks = TargetTicks;
        auto Frame = MakeShared<FJsonObject>();
        Frame->SetNumberField(TEXT("time"), TargetTicks / 60.0f);
        TArray<TSharedPtr<FJsonValue>> Emitters;
        if (auto Controller = Component->GetSystemInstanceController())
        {
            if (auto* Instance = Controller->GetSystemInstance_Unsafe())
            {
                for (const auto& Emitter : Instance->GetEmitters())
                {
                    auto Obj = MakeShared<FJsonObject>();
                    Obj->SetStringField(TEXT("name"), Emitter->GetEmitterHandle().GetName().ToString());
                    Obj->SetNumberField(TEXT("alive"), Emitter->GetNumParticles());
                    if (Emitter->GetNumParticles() > 0)
                    {
                        auto Position = FNiagaraDataSetAccessor<FNiagaraPosition>::CreateReader(Emitter->GetData(), FName(TEXT("Particles.Position")));
                        FVector3f P = Position.GetSafe(0, FNiagaraPosition(0,0,0));
                        Obj->SetNumberField(TEXT("first_x"), P.X);
                        Obj->SetNumberField(TEXT("first_y"), P.Y);
                        Obj->SetNumberField(TEXT("first_z"), P.Z);
                    }
                    Emitters.Add(MakeShared<FJsonValueObject>(Obj));
                }
            }
        }
        Frame->SetArrayField(TEXT("emitters"), Emitters);
        Frames.Add(MakeShared<FJsonValueObject>(Frame));
    }
    Root->SetArrayField(TEXT("frames"), Frames);
    Component->DestroyComponent();
    return Json(Root);
}
