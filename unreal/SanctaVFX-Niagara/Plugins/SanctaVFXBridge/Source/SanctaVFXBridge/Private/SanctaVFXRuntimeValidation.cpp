#include "SanctaVFXLabLibrary.h"
#include "SanctaVFXPresentation.h"
#include "NiagaraComponent.h"
#include "NiagaraSystem.h"
#include "NiagaraEmitter.h"
#include "NiagaraMeshRendererProperties.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "SanctaVFXTerrain.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "PhysicsEngine/BodySetup.h"
#include "Engine/SceneCapture2D.h"
#include "Components/SceneCaptureComponent2D.h"
#include "Engine/TextureRenderTarget2D.h"
#include "Kismet/KismetRenderingLibrary.h"
#include "RenderingThread.h"
#include "Misc/Paths.h"
#include "Engine/World.h"
#include "Components/SceneComponent.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"

int32 USanctaVFXLabLibrary::ConfigureRuntimeMaterials(UNiagaraSystem* System)
{
    if (!System) return 0;
    int32 Count=0;
    for (auto& Handle : System->GetEmitterHandles()) if (auto* Data=Handle.GetInstance().GetEmitterData()) {
        for (auto* Renderer : Data->GetRenderers()) if (auto* Mesh=Cast<UNiagaraMeshRendererProperties>(Renderer)) {
            for (auto& Override : Mesh->OverrideMaterials) if (Override.ExplicitMat) {
                const FName Name(*FString::Printf(TEXT("User.RuntimeMaterial%d"),Count++));
                FNiagaraVariable Param(FNiagaraTypeDefinition(UMaterialInterface::StaticClass()),Name);
                System->GetExposedParameters().AddParameter(Param);
                System->GetExposedParameters().SetUObject(Override.ExplicitMat.Get(),Param);
                Override.UserParamBinding.Parameter=Param;
            }
        }
    }
    System->MarkPackageDirty(); return Count;
}

bool USanctaVFXLabLibrary::ConfigureTerrainMesh(UStaticMesh* Mesh,TArray<FVector> Vertices)
{
    if (!Mesh || Vertices.Num()<8) return false;
    Mesh->CreateBodySetup();auto* Body=Mesh->GetBodySetup();if (!Body) return false;
    Body->AggGeom.EmptyElements();FKConvexElem Convex;Convex.VertexData=MoveTemp(Vertices);Convex.UpdateElemBox();Body->AggGeom.ConvexElems.Add(MoveTemp(Convex));
    Body->CollisionTraceFlag=CTF_UseSimpleAsComplex;Body->InvalidatePhysicsData();Body->CreatePhysicsMeshes();Mesh->MarkPackageDirty();return true;
}
FString USanctaVFXLabLibrary::ValidateTerrain(UStaticMesh* Mesh,UMaterialInterface* Material,UWorld* W)
{
    auto R=MakeShared<FJsonObject>();bool Ok=Mesh && W && Mesh->GetBodySetup() && Mesh->GetBodySetup()->AggGeom.ConvexElems.Num()>0;
    if (Ok) {
        auto* A=W->SpawnActor<ASanctaVFXTerrain>(FVector(5000,5000,0),FRotator::ZeroRotator);
        A->InitializeTerrain(Mesh,Material,FVector::OneVector);
        FHitResult Hit;FCollisionQueryParams Query;
        const bool LOS=W->LineTraceSingleByChannel(Hit,FVector(5000,4500,60),FVector(5000,5500,60),ECC_Visibility,Query) && Hit.GetActor()==A;
        R->SetBoolField(TEXT("los_trace_hits_actual_terrain"),LOS);Ok&=LOS;
        const bool Pawn=A->Body->GetCollisionResponseToChannel(ECC_Pawn)==ECR_Block;
        const bool Projectile=A->Body->GetCollisionResponseToChannel(ECC_WorldDynamic)==ECR_Block;
        R->SetBoolField(TEXT("pawn_and_dynamic_projectile_channels_blocked"),Pawn && Projectile);Ok&=Pawn && Projectile;
        A->SetIntegrity(.25f);R->SetBoolField(TEXT("integrity_presentation_update"),A->Integrity==.25f);Ok&=A->Integrity==.25f;
        float MaterialIntegrity=0;auto* Bound=Cast<UMaterialInstanceDynamic>(A->Body->GetMaterial(0));
        const bool MaterialUpdated=Bound&&Bound->GetScalarParameterValue(FMaterialParameterInfo(TEXT("TerrainIntegrity")),MaterialIntegrity)&&FMath::IsNearlyEqual(MaterialIntegrity,.25f);
        R->SetBoolField(TEXT("actual_terrain_material_receives_integrity"),MaterialUpdated);Ok&=MaterialUpdated;
        A->RemoveTerrain();R->SetBoolField(TEXT("removal_disables_collision"),A->Body->GetCollisionEnabled()==ECollisionEnabled::NoCollision);Ok&=A->Body->GetCollisionEnabled()==ECollisionEnabled::NoCollision;
    }
    R->SetBoolField(TEXT("passed"),Ok);R->SetStringField(TEXT("scope"),TEXT("Native blocking mesh/LOS and lifecycle; actual Foundation projectile channel and authority transport need game wiring."));
    FString Out;FJsonSerializer::Serialize(R,TJsonWriterFactory<>::Create(&Out));return Out;
}

FString USanctaVFXLabLibrary::ValidateRuntimeBindings(USanctaVFXDefinition* D,UWorld* W)
{
    auto R=MakeShared<FJsonObject>();bool Passed=D && W && D->Phases.Num()>0;
    TArray<TSharedPtr<FJsonValue>> Tests;
    auto Check=[&](const TCHAR* Name,bool Ok){auto T=MakeShared<FJsonObject>();T->SetStringField(TEXT("test"),Name);T->SetBoolField(TEXT("passed"),Ok);Tests.Add(MakeShared<FJsonValueObject>(T));Passed&=Ok;};
    if (Passed) {
        auto Spawn=[&](FVector P){auto* A=W->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);A->SetRootComponent(Root);Root->RegisterComponentWithWorld(W);A->SetActorLocation(P);return A;};
        auto* S=Spawn(FVector(10,20,0));auto* T=Spawn(FVector(600,200,0));auto* P=Spawn(FVector(350,100,100));
        auto* C=NewObject<USanctaVFXPresentationComponent>(S);C->RegisterComponentWithWorld(W);C->Definitions.Add(D);
        auto* TC=NewObject<USanctaVFXPresentationComponent>(T);TC->RegisterComponentWithWorld(W);TC->LifeId=FGuid::NewGuid();
        FSanctaVFXEvent E;E.FormId=D->FormId;E.Phase=D->Phases[0].Phase;E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Source=S;E.Target=T;E.Projectile=P;E.TargetLifeId=TC->LifeId;
        E.bAdmitted=E.bApplied=E.bConfirmedHit=true;E.ConfirmedProcMask=MAX_int32;E.Endpoint=FVector(600,200,100);E.CastProgress=.2;E.OccupiedMask=0;E.ElementA=-1;E.ElementB=-1;E.Surface=D->Phases[0].RequiredSurface;
        E.ModeSnapshot=D->Phases[0].RequiredModeSnapshot;E.StanceSnapshot=D->Phases[0].RequiredStanceSnapshot;E.Relation=D->Phases[0].RequiredRelation;
        Check(TEXT("Real runtime component admitted"),C->Present(E)>0);
        auto* N=C->GetActiveComponent(D->Phases[0].ComponentKey);
        TArray<UMaterialInstanceDynamic*> Private;
        if (N) for (const auto& H : D->Phases[0].System->GetEmitterHandles()) if (const auto* Data=H.GetInstance().GetEmitterData()) {
            for (const auto* Renderer : Data->GetRenderers()) if (const auto* Mesh=Cast<UNiagaraMeshRendererProperties>(Renderer)) for (const auto& O : Mesh->OverrideMaterials) {
                if (auto* M=Cast<UMaterialInstanceDynamic>(N->GetOverrideParameters().GetUObject(O.UserParamBinding.Parameter))) Private.Add(M);
            }
        }
        Check(TEXT("All renderer user-material bindings are private dynamic instances"),N && Private.Num()==D->Phases[0].System->GetEmitterHandles().Num());
        auto Scalar=[](UMaterialInstanceDynamic* M,const TCHAR* Name,float V){float Actual=0;return M->GetScalarParameterValue(FMaterialParameterInfo(Name),Actual) && FMath::IsNearlyEqual(Actual,V,.0001f);};
        bool Empty=Private.Num()>0;
        for (auto* M : Private) Empty &= Scalar(M,TEXT("RuntimeEnabled"),1) && Scalar(M,TEXT("RuntimeCount"),0) && Scalar(M,TEXT("RuntimeOccupied"),0) && Scalar(M,TEXT("RuntimeCastProgress"),.2);
        Check(TEXT("Empty resource and hold inputs reach actual bound material"),Empty);
        E.ResourceCount=10;E.OccupiedMask=3;E.ElementA=0;E.ElementB=2;E.CastProgress=.75;E.PhaseAge=.5;C->UpdatePresentation(E);
        bool Changed=Private.Num()>0;
        for (auto* M : Private) Changed &= Scalar(M,TEXT("RuntimeCount"),10) && Scalar(M,TEXT("RuntimeOccupied"),3) && Scalar(M,TEXT("RuntimeElementB"),2) && Scalar(M,TEXT("RuntimeCastProgress"),.75);
        Check(TEXT("Live resource/colour/hold update changes bound materials"),Changed);
        E.EventSequence++;C->Present(E);E.ResourceCount=2;C->Present(E);
        bool DuplicateRefresh=Private.Num()>0;for(auto* M:Private)DuplicateRefresh&=Scalar(M,TEXT("RuntimeCount"),10);
        Check(TEXT("Duplicate state refresh cannot rewind count or replay its gain pulse"),DuplicateRefresh);
        C->ResetForLife(FGuid::NewGuid());E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.ResourceCount=0;E.OccupiedMask=0;C->Present(E);
        auto* New=C->GetActiveComponent(D->Phases[0].ComponentKey);bool Reset=New!=nullptr;
        if (New) for (const auto& H : D->Phases[0].System->GetEmitterHandles()) if (const auto* Data=H.GetInstance().GetEmitterData()) {
            for (const auto* Renderer : Data->GetRenderers()) if (const auto* Mesh=Cast<UNiagaraMeshRendererProperties>(Renderer)) for (const auto& O : Mesh->OverrideMaterials) {
                auto* M=Cast<UMaterialInstanceDynamic>(New->GetOverrideParameters().GetUObject(O.UserParamBinding.Parameter));
                Reset &= M && !Private.Contains(M) && Scalar(M,TEXT("RuntimeCount"),0) && Scalar(M,TEXT("RuntimeOccupied"),0);
            }
        }
        Check(TEXT("Reuse/reset does not leak resources or a previous material instance"),Reset);
        E.ReleaseAge=.2f;E.GainAge=.1f;E.PhaseAge=0;C->UpdatePresentation(E);
        // Advance only the local test clock, without ticking unrelated editor actors.
        const double Before=W->GetTimeSeconds();W->TimeSeconds+=.15;C->TickComponent(0,LEVELTICK_All,nullptr);
        const float Elapsed=W->GetTimeSeconds()-Before;bool Clocks=Elapsed>0;
        if(New)for(const auto& H:D->Phases[0].System->GetEmitterHandles())if(const auto* Data=H.GetInstance().GetEmitterData())for(const auto* Renderer:Data->GetRenderers())if(const auto* Mesh=Cast<UNiagaraMeshRendererProperties>(Renderer))for(const auto& O:Mesh->OverrideMaterials){
            auto* M=Cast<UMaterialInstanceDynamic>(New->GetOverrideParameters().GetUObject(O.UserParamBinding.Parameter));
            Clocks&=M&&Scalar(M,TEXT("RuntimeReleaseAge"),.2f+Elapsed)&&Scalar(M,TEXT("RuntimeGainAge"),.1f+Elapsed);
        }
        Check(TEXT("Release and gain visual clocks advance without a repeated gameplay event"),Clocks);
        W->TimeSeconds=Before;
        // Editor commandlet components have not begun play, so DestroyComponent
        // does not invoke the presentation EndPlay cleanup used in a game world.
        C->ResetForLife(FGuid::NewGuid());
        C->DestroyComponent();TC->DestroyComponent();W->DestroyActor(S);W->DestroyActor(T);W->DestroyActor(P);
        FlushRenderingCommands();
    }
    R->SetBoolField(TEXT("passed"),Passed);R->SetArrayField(TEXT("tests"),Tests);R->SetStringField(TEXT("scope"),TEXT("Reads actual Niagara user material objects and their dynamic parameters; GPU image/collision/transport require separate tests."));
    FString Out;FJsonSerializer::Serialize(R,TJsonWriterFactory<>::Create(&Out));return Out;
}

bool USanctaVFXLabLibrary::CaptureRuntimeDefinition(USanctaVFXDefinition* D,UWorld* W,FSanctaVFXEvent E,FString Directory,FString FileName)
{
    if (!D || !W || D->Phases.IsEmpty()) return false;
    auto Spawn=[&](FVector P){auto* A=W->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);A->SetRootComponent(Root);Root->RegisterComponentWithWorld(W);A->SetActorLocation(P);return A;};
    auto* Source=Spawn(FVector::ZeroVector);auto* Target=Spawn(FVector::ZeroVector);auto* Projectile=Spawn(FVector(0,0,100));
    auto* C=NewObject<USanctaVFXPresentationComponent>(Source);C->RegisterComponentWithWorld(W);C->Definitions.Add(D);
    auto* T=NewObject<USanctaVFXPresentationComponent>(Target);T->RegisterComponentWithWorld(W);T->LifeId=FGuid::NewGuid();
    E.FormId=D->FormId;E.Phase=D->Phases[0].Phase;E.Source=Source;E.Target=Target;E.Projectile=Projectile;E.TargetLifeId=T->LifeId;E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();
    E.bAdmitted=E.bApplied=E.bConfirmedHit=true;E.Endpoint=FVector(100,0,120);E.Position=FVector::ZeroVector;E.Surface=D->Phases[0].RequiredSurface;
    bool Ok=C->Present(E)>0;
    if (Ok) {
        auto* N=C->GetActiveComponent(D->Phases[0].ComponentKey);N->SetForceSolo(true);N->SetAllowScalability(false);N->SetCastShadow(false);N->InitializeSystem();N->Activate(true);N->TickComponent(0,LEVELTICK_All,nullptr);N->AdvanceSimulation(3,1.f/60.f);
        auto* A=W->SpawnActor<ASceneCapture2D>();auto* Capture=A->GetCaptureComponent2D();Capture->bCaptureEveryFrame=false;Capture->bCaptureOnMovement=false;Capture->CaptureSource=ESceneCaptureSource::SCS_FinalColorLDR;Capture->FOVAngle=55;
        A->SetActorLocation(FVector(230,-480,270));A->SetActorRotation((FVector(0,0,105)-A->GetActorLocation()).Rotation());
        auto& PP=Capture->PostProcessSettings;PP.bOverride_AutoExposureMethod=true;PP.AutoExposureMethod=EAutoExposureMethod::AEM_Manual;PP.bOverride_AutoExposureApplyPhysicalCameraExposure=true;PP.AutoExposureApplyPhysicalCameraExposure=false;PP.bOverride_BloomIntensity=true;PP.BloomIntensity=.4f;
        auto* RT=UKismetRenderingLibrary::CreateRenderTarget2D(W,960,640,RTF_RGBA8,FLinearColor(.018,.022,.03,1));Capture->TextureTarget=RT;
        N->MarkRenderStateDirty();W->SendAllEndOfFrameUpdates();FlushRenderingCommands();N->MarkRenderDynamicDataDirty();W->SendAllEndOfFrameUpdates();FlushRenderingCommands();Capture->CaptureScene();FlushRenderingCommands();
        UKismetRenderingLibrary::ExportRenderTarget(W,RT,Directory,FileName);Ok=FPaths::FileExists(Directory/FileName);A->Destroy();
    }
    C->DestroyComponent();T->DestroyComponent();W->DestroyActor(Projectile);W->DestroyActor(Target);W->DestroyActor(Source);return Ok;
}

FString USanctaVFXLabLibrary::ValidatePresentationRuntime(UNiagaraSystem* System, UWorld* World)
{
    auto R=MakeShared<FJsonObject>(); TArray<TSharedPtr<FJsonValue>> Tests;
    bool Passed=true;
    auto Check=[&](const TCHAR* Name,bool Ok){auto T=MakeShared<FJsonObject>();T->SetStringField(TEXT("test"),Name);T->SetBoolField(TEXT("passed"),Ok);Tests.Add(MakeShared<FJsonValueObject>(T));Passed&=Ok;};
    if (!System || !World) { R->SetBoolField(TEXT("passed"),false); R->SetStringField(TEXT("error"),TEXT("Missing system/world")); }
    else {
        auto Spawn=[&](FVector P){auto* A=World->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);A->SetRootComponent(Root);Root->RegisterComponentWithWorld(World);A->SetActorLocation(P);return A;};
        auto* Source=Spawn(FVector(100,200,300));auto* Target=Spawn(FVector(600,400,100));auto* Projectile=Spawn(FVector(350,300,150));
        auto* C=NewObject<USanctaVFXPresentationComponent>(Source);C->RegisterComponentWithWorld(World);C->LifeId=FGuid::NewGuid();
        auto* T=NewObject<USanctaVFXPresentationComponent>(Target);T->RegisterComponentWithWorld(World);T->LifeId=FGuid::NewGuid();
        auto* D=NewObject<USanctaVFXDefinition>(C);D->FormId=TEXT("Test.Runtime");C->Definitions.Add(D);
        auto Phase=[&](const TCHAR* N,ESanctaVFXGate G,ESanctaVFXAnchor A,bool Persistent=false){FSanctaVFXPhase P;P.Phase=N;P.ComponentKey=N;P.System=System;P.Gate=G;P.Anchor=A;P.bPersistent=Persistent;P.Duration=.5;P.bBindTargetLife=(A==ESanctaVFXAnchor::Target);D->Phases.Add(P);};
        Phase(TEXT("Flight"),ESanctaVFXGate::Admission,ESanctaVFXAnchor::Projectile,true);D->Phases.Last().bStateOwned=false;
        Phase(TEXT("Active"),ESanctaVFXGate::Applied,ESanctaVFXAnchor::Target,true);
        Phase(TEXT("Impact"),ESanctaVFXGate::ConfirmedHit,ESanctaVFXAnchor::Target);
        Phase(TEXT("NaturalEnd"),ESanctaVFXGate::NaturalEnd,ESanctaVFXAnchor::Target);
        Phase(TEXT("Cleanse"),ESanctaVFXGate::Cleanse,ESanctaVFXAnchor::Target);
        FSanctaVFXEvent E;E.FormId=D->FormId;E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Source=Source;E.Target=Target;E.Projectile=Projectile;E.TargetLifeId=T->LifeId;E.Phase=TEXT("Flight");
        Check(TEXT("Unadmitted flight rejected"),C->Present(E)==0);
        E.bAdmitted=true;Check(TEXT("Admitted flight starts"),C->Present(E)==1);
        Check(TEXT("Duplicate event rejected"),C->Present(E)==0 && C->GetActiveCount()==1);
        Projectile->SetActorLocation(FVector(430,-150,250));C->TickComponent(0,LEVELTICK_All,nullptr);
        Check(TEXT("Flight follows actual owner"),C->GetActiveComponent(TEXT("Flight"))->GetComponentLocation().Equals(Projectile->GetActorLocation(),.01));
        auto* SecondProjectile=Spawn(FVector(430,150,250));E.Projectile=SecondProjectile;
        Check(TEXT("Fan projectiles sharing one cast retain separate flight components"),C->Present(E)==1&&C->GetActiveCount()==2);
        Check(TEXT("Projectile update changes only its own flight"),C->UpdatePresentation(E)==1);E.Projectile=Projectile;
        E.Phase=TEXT("Impact");E.bConfirmedHit=true;E.bTargetedMiss=true;E.EventSequence++;
        Check(TEXT("Targeted Miss suppresses hit"),C->Present(E)==0);
        E.bTargetedMiss=false;E.EventSequence++;Check(TEXT("Confirmed hit admitted"),C->Present(E)==1);
        E.Phase=TEXT("Active");E.StateId=FGuid::NewGuid();E.bApplied=true;E.EventSequence++;
        Check(TEXT("State application admitted"),C->Present(E)==1);
        C->EndExecution(E.ExecutionId,ESanctaVFXEndReason::Natural);
        Check(TEXT("Owned state and confirmed finite impact survive natural execution finish; delivery closes"),C->GetActiveCount()==2 && C->GetActiveComponent(TEXT("Flight"))==nullptr && C->GetActiveComponent(TEXT("Impact"))!=nullptr);
        C->EndPhase(E.ExecutionId,TEXT("Impact"));
        E.bReconstructActive=true;E.EventSequence++;Check(TEXT("Relevance reconstruction does not replay entry"),C->Present(E)==0 && C->GetActiveCount()==1);E.bReconstructActive=false;
        Target->SetActorLocation(FVector(-200,120,180));C->TickComponent(0,LEVELTICK_All,nullptr);
        Check(TEXT("Active follows moving target"),C->GetActiveComponent(TEXT("Active"))->GetComponentLocation().Equals(Target->GetActorLocation(),.01));
        C->EndState(E.StateId,ESanctaVFXEndReason::RangeBreak);
        E.Phase=TEXT("NaturalEnd");E.bNaturalEnd=true;E.EventSequence++;
        Check(TEXT("Range break cannot trigger natural payoff"),C->Present(E)==0 && C->GetActiveCount()==0);
        C->EndState(E.StateId,ESanctaVFXEndReason::Natural);E.EventSequence++;
        Check(TEXT("Duplicate termination cannot replace the original range-break cause"),C->Present(E)==0);
        E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Phase=TEXT("Active");E.EventSequence++;
        C->Present(E);C->EndState(E.StateId,ESanctaVFXEndReason::Natural);E.Phase=TEXT("NaturalEnd");E.EventSequence++;
        Check(TEXT("Natural payoff works after owner removal"),C->Present(E)==1);
        C->EndState(E.StateId,ESanctaVFXEndReason::Natural);
        Check(TEXT("Duplicate removal preserves the already admitted terminal cue"),C->GetActiveCount()==1);
        Check(TEXT("Natural payoff duplicate rejected"),C->Present(E)==0);
        C->ResetForLife(FGuid::NewGuid());E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Phase=TEXT("Active");E.EventSequence++;
        C->Present(E);C->EndState(E.StateId,ESanctaVFXEndReason::Cleanse);E.Phase=TEXT("Cleanse");E.bCleansed=true;E.EventSequence++;
        Check(TEXT("Cleanse has independent terminal presentation"),C->Present(E)==1);
        C->ResetForLife(FGuid::NewGuid());E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Phase=TEXT("Active");E.EventSequence++;C->Present(E);
        T->ResetForLife(FGuid::NewGuid());C->TickComponent(0,LEVELTICK_All,nullptr);
        Check(TEXT("Respawn removes old-life effect"),C->GetActiveCount()==0);
        E.EventSequence++;Check(TEXT("Old-life event rejected"),C->Present(E)==0);
        E.TargetLifeId=T->LifeId;E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Phase=TEXT("Flight");E.EventSequence++;
        C->EndExecution(E.ExecutionId,ESanctaVFXEndReason::Rejected);
        Check(TEXT("Rejected execution cannot produce flight"),C->Present(E)==0);
        C->ResetForLife(FGuid::NewGuid());Check(TEXT("Reset clears components and histories"),C->GetActiveCount()==0 && C->GetHistoryCount()==0);
        // Two potential contacts in the same composition still produce one contact.
        D->Phases[2].bContact=true;D->Phases[2].ContactPriority=1;auto Extra=D->Phases[2];Extra.ComponentKey=TEXT("RedundantFlash");Extra.ContactPriority=0;D->Phases.Add(Extra);
        E.ExecutionId=FGuid::NewGuid();E.Phase=TEXT("Impact");E.EventSequence++;Check(TEXT("Dominant contact suppresses redundant flash"),C->Present(E)==1);
        E.EventSequence++;Check(TEXT("Distinct confirmed occurrences from the same state can coexist"),C->Present(E)==1&&C->GetActiveCount()==2);
        E.PhaseAge=1;Check(TEXT("Finite update changes only its matching occurrence"),C->UpdatePresentation(E)==1);
        C->TickComponent(0,LEVELTICK_All,nullptr);Check(TEXT("Older finite occurrence is not rewound by a later update"),C->GetActiveCount()==1);
        E.EventSequence--;C->UpdatePresentation(E);C->TickComponent(0,LEVELTICK_All,nullptr);Check(TEXT("Finite visual expires without synthesizing payoff"),C->GetActiveCount()==0);
        C->ResetForLife(FGuid::NewGuid());E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.Phase=TEXT("Active");E.PhaseAge=0;
        D->Phases[1].RequiredStanceSnapshot=TEXT("Tank");D->Phases[1].RequiredModeSnapshot=TEXT("Manifest");D->Phases[1].RequiredRelation=TEXT("Enemy");
        E.StanceSnapshot=TEXT("Warrior");E.ModeSnapshot=TEXT("Manifest");E.Relation=TEXT("Enemy");
        Check(TEXT("Wrong admission stance cannot select a variant"),C->Present(E)==0);
        E.StanceSnapshot=TEXT("Tank");E.ModeSnapshot=TEXT("Weave");Check(TEXT("Wrong Mage mode cannot select a variant"),C->Present(E)==0);
        E.ModeSnapshot=TEXT("Manifest");E.Relation=TEXT("Ally");Check(TEXT("Wrong target relation cannot select a variant"),C->Present(E)==0);
        E.Relation=TEXT("Enemy");Check(TEXT("Matching admission snapshots select the variant"),C->Present(E)==1);
        Phase(TEXT("Decoration"),ESanctaVFXGate::Admission,ESanctaVFXAnchor::Source);D->Phases.Last().Importance=ESanctaVFXImportance::Decorative;
        C->bDecorativeEnabled=false;E.Phase=TEXT("Decoration");E.ExecutionId=FGuid::NewGuid();E.StateId=FGuid::NewGuid();E.EventSequence++;
        Check(TEXT("Low presentation profile suppresses decoration"),C->Present(E)==0);
        D->Phases[1].Importance=ESanctaVFXImportance::Essential;E.Phase=TEXT("Active");
        Check(TEXT("Low presentation profile retains essential state"),C->Present(E)==1);
        Phase(TEXT("LinkBounds"),ESanctaVFXGate::Applied,ESanctaVFXAnchor::Link,true);D->Phases.Last().bUseEndpoint=true;
        E.Phase=TEXT("LinkBounds");E.StateId=FGuid::NewGuid();E.Endpoint=Source->GetActorLocation()+FVector(3000,0,0);E.EventSequence++;Target->SetActorLocation(E.Endpoint);
        C->Present(E);auto* Link=C->GetActiveComponent(TEXT("LinkBounds"));
        Check(TEXT("Live link bounds include endpoint beyond recorded preview bounds"),Link&&Link->GetSystemFixedBounds().IsInside(E.Endpoint-Source->GetActorLocation()));
        C->DestroyComponent();T->DestroyComponent();World->DestroyActor(SecondProjectile);World->DestroyActor(Projectile);World->DestroyActor(Target);World->DestroyActor(Source);
        R->SetBoolField(TEXT("passed"),Passed);R->SetArrayField(TEXT("tests"),Tests);
        R->SetStringField(TEXT("scope"),TEXT("Native event routing, ownership and component transforms. Does not certify GPU appearance or game transport."));
    }
    FString Out;FJsonSerializer::Serialize(R,TJsonWriterFactory<>::Create(&Out));return Out;
}
