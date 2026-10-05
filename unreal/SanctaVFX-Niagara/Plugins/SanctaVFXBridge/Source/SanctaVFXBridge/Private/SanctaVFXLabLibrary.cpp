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
#include "Materials/MaterialInterface.h"
#include "Materials/Material.h"
#include "UObject/UObjectIterator.h"
#include "MaterialShared.h"
#include "RHIGlobals.h"
#include "ShaderCore.h"
#include "SanctaVFXReviewActor.h"
#include "Camera/CameraComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/StaticMeshActor.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/WorldSettings.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Misc/PackageName.h"
#include "UObject/SavePackage.h"
#include "HAL/FileManager.h"

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
        if (Data) {
            Obj->SetNumberField(TEXT("renderer_count"), Data->GetRenderers().Num());
            Obj->SetStringField(TEXT("simulation_target"), Data->SimTarget == ENiagaraSimTarget::CPUSim ? TEXT("CPU") : TEXT("GPU"));
        }
        Emitters.Add(MakeShared<FJsonValueObject>(Obj));
    }
    Root->SetArrayField(TEXT("emitters"), Emitters);
    TArray<TSharedPtr<FJsonValue>> Params;
    for (const FNiagaraVariableWithOffset& Param : System->GetExposedParameters().ReadParameterVariables())
        Params.Add(MakeShared<FJsonValueString>(Param.GetName().ToString()));
    Root->SetArrayField(TEXT("user_parameters"), Params);
    return Json(Root);
}

FString USanctaVFXLabLibrary::ValidateMaterial(UMaterialInterface* Material, UWorld* World)
{
    auto Root = MakeShared<FJsonObject>();
    Root->SetBoolField(TEXT("passed"), false);
    if (!Material || !World) { Root->SetStringField(TEXT("error"), TEXT("null material/world")); return Json(Root); }
    auto* Resource = Material->GetMaterialResource(GShaderPlatformForFeatureLevel[World->GetFeatureLevel()]);
    if (!Resource) { Root->SetStringField(TEXT("error"), TEXT("material resource missing")); return Json(Root); }
    Resource->FinishCacheShaders();
    Resource->SubmitCompileJobs_GameThread(EShaderCompileJobPriority::ForceLocal);
    if (!Resource->IsCompilationFinished()) {
        TArray<FMaterial*> Materials; Materials.Add(Resource);
        FMaterial::FinishCompilation(TEXT("SanctaReferencePort"), Materials);
    }
    TArray<TSharedPtr<FJsonValue>> Errors;
    for (const FString& Error : Resource->GetCompileErrors()) Errors.Add(MakeShared<FJsonValueString>(Error));
    Root->SetArrayField(TEXT("errors"), Errors);
    Root->SetBoolField(TEXT("passed"), Resource->IsCompilationFinished() && Errors.IsEmpty());
    Root->SetStringField(TEXT("material"), Material->GetPathName());
    return Json(Root);
}

bool USanctaVFXLabLibrary::CreateReviewMap(FString MapPath, UNiagaraSystem* System, FString Title, FString SkillClass, float Duration, FVector CameraPosition, FVector CameraTarget, float EffectHeight, TArray<FString> Maps, TArray<FString> Titles, int32 Index, UStaticMesh* Body, UMaterialInterface* FloorMaterial, UMaterialInterface* BodyMaterial, TArray<FVector> ActorPositions, TArray<float> SampleTimes, float PeakTime)
{
    if (!System || !MapPath.StartsWith(TEXT("/Game/VFXLab/Review/Scenes/")) || Maps.Num()!=Titles.Num() || !Maps.IsValidIndex(Index)) return false;
    auto* Package = CreatePackage(*MapPath);
    // These maps are owned by this generator and replaced in full. An existing
    // file otherwise leaves a new package partially loaded and SavePackage refuses it.
    Package->MarkAsFullyLoaded();
    auto* World = UWorld::CreateWorld(EWorldType::Editor,false,FName(*FPackageName::GetShortName(MapPath)),Package,true);
    if (!World) return false;
    World->SetFlags(RF_Public|RF_Standalone);
    World->GetWorldSettings()->DefaultGameMode = ASanctaVFXReviewGameMode::StaticClass();
    auto* Stage=World->SpawnActor<ASanctaVFXReviewActor>();
    Stage->System=System;
    Stage->SkillTitle=Title;
    Stage->SkillClass=SkillClass;
    Stage->CycleDuration=FMath::Max(Duration,1.f);
    Stage->CameraPosition=CameraPosition;
    Stage->CameraTarget=CameraTarget;
    Stage->EffectHeight=EffectHeight;
    Stage->ReviewSampleTimes=SampleTimes;
    Stage->ReviewPeakTime=PeakTime;
    Stage->CatalogMaps=Maps;
    Stage->CatalogTitles=Titles;
    Stage->CatalogIndex=Index;
    Stage->SetActorLabel(Title);
    Stage->Camera->SetRelativeLocation(CameraPosition);
    Stage->Camera->SetRelativeRotation((CameraTarget-CameraPosition).Rotation());
    auto* Light=World->SpawnActor<ADirectionalLight>(FVector(0,0,1500),FRotator(-55,-30,0));
    Light->SetActorLabel(TEXT("Review_Light"));
    Light->GetLightComponent()->SetMobility(EComponentMobility::Movable);
    Light->GetLightComponent()->SetIntensity(3.f);
    auto* Plane=World->SpawnActor<AStaticMeshActor>(FVector(CameraTarget.X,CameraTarget.Y,-2),FRotator::ZeroRotator);
    Plane->SetActorLabel(TEXT("Review_Floor"));
    Plane->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Plane.Plane")));
    if (FloorMaterial) Plane->GetStaticMeshComponent()->SetMaterial(0,FloorMaterial);
    Plane->SetActorScale3D(FVector(50,50,1));
    Plane->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    if (Body && BodyMaterial) {
        for (const FVector& Position : ActorPositions) {
            auto* Dummy=World->SpawnActor<AStaticMeshActor>(Position,FRotator::ZeroRotator);
            Dummy->SetActorLabel(TEXT("Review_ScaleReference"));
            Dummy->GetStaticMeshComponent()->SetStaticMesh(Body);
            Dummy->GetStaticMeshComponent()->SetMaterial(0,BodyMaterial);
            Dummy->GetStaticMeshComponent()->SetCastShadow(false);
            Dummy->GetStaticMeshComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        }
    }
    Package->MarkPackageDirty();
    FAssetRegistryModule::AssetCreated(World);
    const FString File=FPackageName::LongPackageNameToFilename(MapPath,FPackageName::GetMapPackageExtension());
    IFileManager::Get().MakeDirectory(*FPaths::GetPath(File),true);
    FSavePackageArgs Args;
    Args.TopLevelFlags=RF_Public|RF_Standalone;
    Args.SaveFlags=SAVE_None;
    const bool Saved=UPackage::SavePackage(Package,World,*File,Args);
    World->DestroyWorld(false);
    World->ClearFlags(RF_Standalone);
    World->MarkAsGarbage();
    UE_LOG(LogTemp,Display,TEXT("SanctaReview map %s: %s"),*MapPath,Saved?TEXT("saved"):TEXT("FAILED"));
    return Saved;
}

bool USanctaVFXLabLibrary::CaptureSystem(UNiagaraSystem* System, UWorld* World, float Time, FString Directory, FString FileName)
{
    if (!System || !World) return false;
    System->WaitForCompilationComplete(true, false);
    // A standalone game-view capture does not use editor gizmos or debug-view
    // materials. Cancel only their transient jobs in this commandlet process.
    if (IsRunningCommandlet()) {
        for (TObjectIterator<UMaterial> It; It; ++It) {
            const FString Path = It->GetPathName();
            if (Path.StartsWith(TEXT("/Engine/EditorMaterials/")) || Path.StartsWith(TEXT("/Engine/EngineDebugMaterials/")) || Path.StartsWith(TEXT("/Engine/EngineMaterials/DefaultTextMaterial"))) {
                if (auto* Resource = It->GetMaterialResource(GShaderPlatformForFeatureLevel[World->GetFeatureLevel()])) {
                    if (!Resource->IsCompilationFinished()) {
                        Resource->CancelCompilation();
                        UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture: skipped unused editor material %s"), *Path);
                    }
                }
            }
        }
    }
    TArray<FMaterial*> MaterialsToCompile;
    for (const auto& Handle : System->GetEmitterHandles()) {
        if (const auto* Data = Handle.GetInstance().GetEmitterData()) {
            for (const auto* Renderer : Data->GetRenderers()) {
                TArray<UMaterialInterface*> Materials;
                Renderer->GetUsedMaterials(nullptr, Materials);
                for (auto* Material : Materials) {
                    if (Material) {
                        if (auto* Resource = Material->GetMaterialResource(GShaderPlatformForFeatureLevel[World->GetFeatureLevel()])) {
                            Resource->FinishCacheShaders();
                            Resource->SubmitCompileJobs_GameThread(EShaderCompileJobPriority::ForceLocal);
                            UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture material: %s, ready=%d"), *Material->GetName(), Resource->IsCompilationFinished());
                            if (!Resource->IsCompilationFinished()) MaterialsToCompile.AddUnique(Resource);
                        }
                    }
                }
            }
        }
    }
    UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture: compiling %d material resources"), MaterialsToCompile.Num());
    if (!MaterialsToCompile.IsEmpty()) FMaterial::FinishCompilation(TEXT("SanctaVFXCapture"), MaterialsToCompile);
    UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture: materials ready"));
    auto* Component = UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, System, FVector(0,0,100), FRotator::ZeroRotator, FVector::OneVector, false, false, ENCPoolMethod::None, false);
    if (!Component) return false;
    Component->SetForceSolo(true);
    Component->SetAllowScalability(false);
    Component->InitializeSystem();
    Component->Activate(true);
    Component->TickComponent(0.0f, LEVELTICK_All, nullptr);
    Component->SetActiveFlag(true);
    Component->SetRenderingEnabled(true);
    Component->AdvanceSimulation(FMath::RoundToInt(Time*60),1.0f/60.0f);
    UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture: simulation ready"));
    Component->MarkRenderStateDirty();
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
    Capture->PostProcessSettings.bOverride_AutoExposureApplyPhysicalCameraExposure = true;
    Capture->PostProcessSettings.AutoExposureApplyPhysicalCameraExposure = false;
    Capture->PostProcessSettings.bOverride_AutoExposureBias = true;
    Capture->PostProcessSettings.AutoExposureBias = 0;
    Capture->PostProcessSettings.bOverride_BloomIntensity = true;
    Capture->PostProcessSettings.BloomIntensity = .5f;
    auto* Target = UKismetRenderingLibrary::CreateRenderTarget2D(World,1280,720,RTF_RGBA8,FLinearColor(.018f,.022f,.03f,1));
    Capture->TextureTarget = Target;
    World->SendAllEndOfFrameUpdates();
    FlushRenderingCommands();
    // AdvanceSimulation runs outside the normal world's end-of-frame tick.
    // Publish its current particle data after the recreated scene proxy exists.
    Component->MarkRenderDynamicDataDirty();
    World->SendAllEndOfFrameUpdates();
    FlushRenderingCommands();
    Capture->CaptureScene();
    FlushRenderingCommands();
    UKismetRenderingLibrary::ExportRenderTarget(World,Target,Directory,FileName);
    Component->DestroyComponent();
    CaptureActor->Destroy();
    UE_LOG(LogTemp, Display, TEXT("SanctaVFX capture: exported %s"), *FileName);
    return FPaths::FileExists(Directory/FileName);
}

static FString SimulateWithInputs(UNiagaraSystem* System, UWorld* World, const TArray<float>& Times, const TArray<FString>& ParameterNames, const TArray<float>& ParameterValues)
{
    auto Root = MakeShared<FJsonObject>();
    if (!System || !World) { Root->SetStringField(TEXT("error"), TEXT("null system/world")); return Json(Root); }
    if (ParameterValues.Num() != Times.Num()*ParameterNames.Num()) {
        Root->SetStringField(TEXT("error"), TEXT("parameter values must contain one row per sample")); return Json(Root);
    }
    for (const FString& Name : ParameterNames) {
        if (!Name.StartsWith(TEXT("User."))) { Root->SetStringField(TEXT("error"), TEXT("only User parameters are accepted")); return Json(Root); }
    }
    System->WaitForCompilationComplete(true, false);
    auto* Component = UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, System, FVector::ZeroVector, FRotator::ZeroRotator, FVector::OneVector, false, false, ENCPoolMethod::None, false);
    if (!Component) { Root->SetStringField(TEXT("error"), TEXT("spawn failed")); return Json(Root); }
    Component->SetForceSolo(true);
    Component->SetAllowScalability(false);
    Root->SetNumberField(TEXT("world_type"), static_cast<int32>(World->WorldType));
    Root->SetBoolField(TEXT("initialized"), Component->InitializeSystem());
    Component->Activate(true);
    Component->TickComponent(0.0f, LEVELTICK_All, nullptr);
    TArray<TSharedPtr<FJsonValue>> Frames;
    int32 CompletedTicks = 0;
    int32 SampleIndex = 0;
    for (float Time : Times)
    {
        for (int32 Parameter = 0; Parameter < ParameterNames.Num(); ++Parameter) {
            Component->SetVariableFloat(FName(*ParameterNames[Parameter]), ParameterValues[SampleIndex*ParameterNames.Num()+Parameter]);
        }
        int32 TargetTicks = FMath::RoundToInt(Time * 60.0f);
        Component->AdvanceSimulation(FMath::Max(0, TargetTicks-CompletedTicks), 1.0f/60.0f);
        CompletedTicks = TargetTicks;
        auto Frame = MakeShared<FJsonObject>();
        Frame->SetNumberField(TEXT("time"), TargetTicks / 60.0f);
        Frame->SetBoolField(TEXT("component_active"), Component->IsActive());
        Frame->SetNumberField(TEXT("execution_state"), static_cast<int32>(Component->GetExecutionState()));
        Frame->SetBoolField(TEXT("controller_present"), Component->GetSystemInstanceController().IsValid());
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
                        auto Position = FNiagaraDataSetAccessor<FNiagaraPosition>::CreateReader(Emitter->GetParticleData(), FName(TEXT("Position")));
                        if (!Position.IsValid()) Position = FNiagaraDataSetAccessor<FNiagaraPosition>::CreateReader(Emitter->GetParticleData(), FName(TEXT("Particles.Position")));
                        Obj->SetBoolField(TEXT("position_readable"), Position.IsValid());
                        if (!Position.IsValid()) {
                            TArray<TSharedPtr<FJsonValue>> Variables;
                            for (const auto& Variable : Emitter->GetParticleData().GetVariables()) Variables.Add(MakeShared<FJsonValueString>(Variable.GetName().ToString()));
                            Obj->SetArrayField(TEXT("data_variables"), Variables);
                        }
                        FVector3f P = Position.GetSafe(0, FNiagaraPosition(0,0,0));
                        Obj->SetNumberField(TEXT("first_x"), P.X);
                        Obj->SetNumberField(TEXT("first_y"), P.Y);
                        Obj->SetNumberField(TEXT("first_z"), P.Z);
                        auto Age = FNiagaraDataSetAccessor<float>::CreateReader(Emitter->GetParticleData(), FName(TEXT("Age")));
                        auto Lifetime = FNiagaraDataSetAccessor<float>::CreateReader(Emitter->GetParticleData(), FName(TEXT("Lifetime")));
                        auto NormalizedAge = FNiagaraDataSetAccessor<float>::CreateReader(Emitter->GetParticleData(), FName(TEXT("NormalizedAge")));
                        Obj->SetBoolField(TEXT("age_readable"), Age.IsValid() && Lifetime.IsValid() && NormalizedAge.IsValid());
                        if (Age.IsValid() && Lifetime.IsValid() && NormalizedAge.IsValid()) {
                            Obj->SetNumberField(TEXT("first_age"), Age.GetSafe(0, 0.0f));
                            Obj->SetNumberField(TEXT("first_lifetime"), Lifetime.GetSafe(0, 0.0f));
                            Obj->SetNumberField(TEXT("first_normalized_age"), NormalizedAge.GetSafe(0, 0.0f));
                        }
                        auto ReferenceData = FNiagaraDataSetAccessor<FVector4f>::CreateReader(Emitter->GetParticleData(), FName(TEXT("DynamicMaterialParameter")));
                        Obj->SetBoolField(TEXT("reference_index_readable"), ReferenceData.IsValid());
                        if (ReferenceData.IsValid()) {
                            bool MatchesSpawnOrder = true;
                            for (int32 Particle = 0; Particle < Emitter->GetNumParticles(); ++Particle) {
                                MatchesSpawnOrder &= FMath::IsNearlyEqual(ReferenceData.GetSafe(Particle, FVector4f(-1,0,0,0)).X, float(Particle), 0.0001f);
                            }
                            Obj->SetBoolField(TEXT("reference_indices_match_spawn_order"), MatchesSpawnOrder);
                            Obj->SetNumberField(TEXT("first_reference_index"), ReferenceData.GetSafe(0, FVector4f(-1,0,0,0)).X);
                            Obj->SetNumberField(TEXT("last_reference_index"), ReferenceData.GetSafe(Emitter->GetNumParticles()-1, FVector4f(-1,0,0,0)).X);
                            const FVector4f Values = ReferenceData.GetSafe(0, FVector4f(-1,0,0,0));
                            TArray<TSharedPtr<FJsonValue>> DynamicValues;
                            DynamicValues.Add(MakeShared<FJsonValueNumber>(Values.X));
                            DynamicValues.Add(MakeShared<FJsonValueNumber>(Values.Y));
                            DynamicValues.Add(MakeShared<FJsonValueNumber>(Values.Z));
                            DynamicValues.Add(MakeShared<FJsonValueNumber>(Values.W));
                            Obj->SetArrayField(TEXT("first_dynamic_material_parameter"), DynamicValues);
                        }
                    }
                    Emitters.Add(MakeShared<FJsonValueObject>(Obj));
                }
            }
        }
        Frame->SetArrayField(TEXT("emitters"), Emitters);
        Frames.Add(MakeShared<FJsonValueObject>(Frame));
        ++SampleIndex;
    }
    Root->SetArrayField(TEXT("frames"), Frames);
    Component->DestroyComponent();
    return Json(Root);
}

FString USanctaVFXLabLibrary::SimulateSystem(UNiagaraSystem* System, UWorld* World, TArray<float> Times)
{
    return SimulateWithInputs(System, World, Times, {}, {});
}

FString USanctaVFXLabLibrary::SimulateSystemInputs(UNiagaraSystem* System, UWorld* World, TArray<float> Times, TArray<FString> ParameterNames, TArray<float> ParameterValues)
{
    return SimulateWithInputs(System, World, Times, ParameterNames, ParameterValues);
}

FString USanctaVFXLabLibrary::MeasureSimulationCost(UNiagaraSystem* System, UWorld* World, int32 CastCount, int32 TickCount)
{
    auto Root = MakeShared<FJsonObject>();
    if (!System || !World || CastCount < 1 || CastCount > 128 || TickCount < 1 || TickCount > 600) {
        Root->SetStringField(TEXT("error"), TEXT("Invalid system, world, cast count or tick count"));
        return Json(Root);
    }
    System->WaitForCompilationComplete(true, false);
    TArray<UNiagaraComponent*> Components;
    const double SpawnStart = FPlatformTime::Seconds();
    for (int32 Index = 0; Index < CastCount; ++Index) {
        auto* Component = UNiagaraFunctionLibrary::SpawnSystemAtLocation(World, System, FVector::ZeroVector, FRotator::ZeroRotator, FVector::OneVector, false, false, ENCPoolMethod::None, false);
        if (!Component) continue;
        Component->SetForceSolo(true);
        Component->SetAllowScalability(false);
        Component->SetRenderingEnabled(false);
        Component->InitializeSystem();
        Component->Activate(true);
        Component->TickComponent(0.0f, LEVELTICK_All, nullptr);
        Components.Add(Component);
    }
    Root->SetNumberField(TEXT("spawn_ms"), (FPlatformTime::Seconds()-SpawnStart)*1000.0);
    double TotalMs = 0.0, PeakMs = 0.0;
    int32 PeakParticles = 0;
    for (int32 Tick = 0; Tick < TickCount; ++Tick) {
        const double Start = FPlatformTime::Seconds();
        for (auto* Component : Components) Component->AdvanceSimulation(1, 1.0f/60.0f);
        const double Ms = (FPlatformTime::Seconds()-Start)*1000.0;
        TotalMs += Ms;
        PeakMs = FMath::Max(PeakMs, Ms);
        int32 Particles = 0;
        for (auto* Component : Components) {
            if (auto Controller = Component->GetSystemInstanceController()) {
                if (auto* Instance = Controller->GetSystemInstance_Unsafe()) {
                    for (const auto& Emitter : Instance->GetEmitters()) Particles += Emitter->GetNumParticles();
                }
            }
        }
        PeakParticles = FMath::Max(PeakParticles, Particles);
    }
    for (auto* Component : Components) Component->DestroyComponent();
    Root->SetNumberField(TEXT("cast_count"), Components.Num());
    Root->SetNumberField(TEXT("tick_count"), TickCount);
    Root->SetNumberField(TEXT("simulation_mean_ms_per_tick"), TotalMs/TickCount);
    Root->SetNumberField(TEXT("simulation_peak_ms_per_tick"), PeakMs);
    Root->SetNumberField(TEXT("peak_particles"), PeakParticles);
    Root->SetStringField(TEXT("scope"), TEXT("CPU solo simulation at 60 Hz; rendering disabled; excludes GPU, gameplay, networking and scalability batching"));
    return Json(Root);
}
