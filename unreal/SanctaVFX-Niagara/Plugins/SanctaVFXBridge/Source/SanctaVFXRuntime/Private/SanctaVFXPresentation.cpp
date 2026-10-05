#include "SanctaVFXPresentation.h"
#include "NiagaraComponent.h"
#include "NiagaraSystem.h"
#include "NiagaraEmitter.h"
#include "NiagaraMeshRendererProperties.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Components/MeshComponent.h"
#include "Engine/World.h"

USanctaVFXPresentationComponent::USanctaVFXPresentationComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.bAllowTickOnDedicatedServer = false;
}

static FVector SocketPosition(AActor* Actor, FName Socket, const FVector& Fallback)
{
    if (!IsValid(Actor)) return Fallback;
    if (!Socket.IsNone()) {
        TInlineComponentArray<UMeshComponent*> Meshes(Actor);
        for (UMeshComponent* Mesh : Meshes) if (Mesh->DoesSocketExist(Socket)) return Mesh->GetSocketLocation(Socket);
    }
    return Actor->GetActorLocation();
}

static bool ValidInputs(const FSanctaVFXEvent& E)
{
    return FMath::IsFinite(E.PhaseAge) && FMath::IsFinite(E.CastProgress) && FMath::IsFinite(E.Radius) && FMath::IsFinite(E.Range) && FMath::IsFinite(E.ConeAngle) && FMath::IsFinite(E.ReleaseAge) && FMath::IsFinite(E.GainAge) && FMath::IsFinite(E.EventWorldTime) && !E.Direction.ContainsNaN() && !E.Position.ContainsNaN() && !E.Endpoint.ContainsNaN();
}

bool USanctaVFXPresentationComponent::Accept(const FSanctaVFXEvent& E, const FSanctaVFXPhase& P) const
{
    if (!E.ExecutionId.IsValid() || E.EventSequence < 0 || !P.System) return false;
    const double Now=GetWorld()->GetTimeSeconds();
    if (E.EventWorldTime >= 0 && (E.EventWorldTime < Now-HistorySeconds || E.EventWorldTime > Now+5)) return false;
    const bool Terminal=P.Gate==ESanctaVFXGate::NaturalEnd || P.Gate==ESanctaVFXGate::Cleanse;
    const auto* Closed=E.StateId.IsValid() ? ClosedStates.Find(E.StateId) : ClosedExecutions.Find(E.ExecutionId);
    if (Terminal) {
        const auto Required=P.Gate==ESanctaVFXGate::NaturalEnd ? ESanctaVFXEndReason::Natural : ESanctaVFXEndReason::Cleanse;
        if (!Closed || Closed->Reason!=Required || P.bPersistent) return false;
    } else if (Closed || (ClosedExecutions.Contains(E.ExecutionId) && (!E.StateId.IsValid() || !P.bStateOwned))) return false;
    if (P.bPersistent && !E.StateId.IsValid()) return false;
    if ((P.Anchor==ESanctaVFXAnchor::Source || P.Anchor==ESanctaVFXAnchor::Link) && !IsValid(E.Source)) return false;
    if (P.Anchor==ESanctaVFXAnchor::Target && !IsValid(E.Target)) return false;
    if (P.Anchor==ESanctaVFXAnchor::Projectile && !IsValid(E.Projectile)) return false;
    if (!ValidInputs(E)) return false;
    if (!bDecorativeEnabled && P.Importance == ESanctaVFXImportance::Decorative) return false;
    if (E.bReconstructActive && !P.bPersistent) return false;
    if ((E.ConfirmedProcMask & P.RequiredProcMask) != P.RequiredProcMask) return false;
    if (!P.RequiredSurface.IsNone() && P.RequiredSurface!=E.Surface) return false;
    if (!P.RequiredModeSnapshot.IsNone() && P.RequiredModeSnapshot!=E.ModeSnapshot) return false;
    if (!P.RequiredStanceSnapshot.IsNone() && P.RequiredStanceSnapshot!=E.StanceSnapshot) return false;
    if (!P.RequiredRelation.IsNone() && P.RequiredRelation!=E.Relation) return false;
    if (P.bBindTargetLife) {
        if (!IsValid(E.Target) || !E.TargetLifeId.IsValid()) return false;
        const auto* Host = E.Target->FindComponentByClass<USanctaVFXPresentationComponent>();
        if (!Host || Host->LifeId != E.TargetLifeId) return false;
    }
    switch (P.Gate) {
    case ESanctaVFXGate::Admission: return E.bAdmitted;
    case ESanctaVFXGate::ConfirmedHit: return E.bConfirmedHit && !E.bTargetedMiss;
    case ESanctaVFXGate::Applied: return E.bApplied && !E.bTargetedMiss;
    case ESanctaVFXGate::NaturalEnd: return E.bNaturalEnd;
    case ESanctaVFXGate::Cleanse: return E.bCleansed;
    default: return true;
    }
}

FString USanctaVFXPresentationComponent::InstanceKey(const FSanctaVFXEvent& E, const FSanctaVFXPhase& P) const
{
    const FGuid Owner = E.StateId.IsValid() ? E.StateId : E.ExecutionId;
    FString Key=Owner.ToString() + TEXT("/") + E.FormId.ToString() + TEXT("/") + P.ComponentKey.ToString() + TEXT("/") + GetPathNameSafe(E.Target);
    if(P.Anchor==ESanctaVFXAnchor::Projectile)Key+=TEXT("/Projectile/")+GetPathNameSafe(E.Projectile);
    return Key;
}

int32 USanctaVFXPresentationComponent::Present(const FSanctaVFXEvent& E)
{
    if (!GetWorld() || GetWorld()->GetNetMode()==NM_DedicatedServer) return 0;
    PruneHistory();
    if (GetHistoryCount() >= MaxHistoryEntries) return 0;
    USanctaVFXDefinition* Def = nullptr;
    for (const auto& Candidate : Definitions) if (Candidate && Candidate->FormId == E.FormId) { Def = Candidate.Get(); break; }
    if (!Def) return 0;
    const FString EventKey = E.ExecutionId.ToString() + TEXT("/") + E.StateId.ToString() + TEXT("/") + E.FormId.ToString() + TEXT("/") + E.Phase.ToString() + TEXT("/") + GetPathNameSafe(E.Target) + TEXT("/") + GetPathNameSafe(E.Projectile) + TEXT("/") + LexToString(E.EventSequence);
    if (SeenEvents.Contains(EventKey)) return 0;
    int32 BestContact = MIN_int32;
    for (const auto& P : Def->Phases) if (P.Phase == E.Phase && P.bContact && Accept(E,P)) BestContact = FMath::Max(BestContact,P.ContactPriority);
    int32 Count = 0;
    bool AcceptedUpdate=false;
    bool ContactPlayed=false;
    for (const auto& P : Def->Phases) {
        if (P.Phase != E.Phase || !Accept(E,P) || (P.bContact && P.ContactPriority != BestContact)) continue;
        if (P.bContact && ContactPlayed) continue;
        // A state owns one persistent cue, but can produce multiple finite
        // confirmed results while that state is alive (ticks, attacks, procs).
        const FString Key = InstanceKey(E,P) + (!P.bPersistent ? TEXT("/Occurrence/")+LexToString(E.EventSequence) : TEXT(""));
        // Active reconstruction/refresh updates an existing state without repeating its entry burst.
        if (auto* Existing = Instances.Find(Key)) {
            const FName Mode=Existing->Event.ModeSnapshot, Stance=Existing->Event.StanceSnapshot, Relation=Existing->Event.Relation;
            Existing->Event = E; Existing->Event.ModeSnapshot=Mode; Existing->Event.StanceSnapshot=Stance; Existing->Event.Relation=Relation;
            Existing->InputReceiptTime=GetWorld()->GetTimeSeconds();
            if(E.bReconstructActive)Existing->StartTime=GetWorld()->GetTimeSeconds()-FMath::Max(0.f,E.PhaseAge);
            ApplyInputs(*Existing);AcceptedUpdate=true;continue;
        }
        auto* C = NewObject<UNiagaraComponent>(GetOwner());
        C->SetAutoActivate(false); C->SetAutoDestroy(false); C->SetAsset(P.System);
        C->RegisterComponentWithWorld(GetWorld());
        FSanctaVFXInstance I; I.Component = C; I.Event = E; I.Phase = P;
        I.StartTime = GetWorld()->GetTimeSeconds() - FMath::Max(0.f,E.PhaseAge);
        I.InputReceiptTime=GetWorld()->GetTimeSeconds();
        // All renderer materials get private instances: no state leaks between casts or targets.
        for (const auto& Handle : P.System->GetEmitterHandles()) if (const auto* Data=Handle.GetInstance().GetEmitterData()) {
            for (auto* Renderer : Data->GetRenderers()) if (const auto* Mesh=Cast<UNiagaraMeshRendererProperties>(Renderer)) {
                for (const auto& Override : Mesh->OverrideMaterials) if (Override.ExplicitMat && Override.UserParamBinding.Parameter.IsValid()) {
                    auto* D=UMaterialInstanceDynamic::Create(Override.ExplicitMat,C);
                    C->SetVariableMaterial(Override.UserParamBinding.Parameter.GetName(),D); I.Materials.Add(D);
                }
            }
        }
        for (const auto& Pair : P.ScalarDefaults) C->SetVariableFloat(Pair.Key,Pair.Value);
        C->SetVariableFloat(TEXT("User.PlaybackRate"),1.f);
        C->SetVariableFloat(TEXT("User.CueLifetime"), P.Duration);
        Instances.Add(Key,MoveTemp(I)); ApplyInputs(Instances[Key]); C->Activate(true); ++Count;
        ContactPlayed |= P.bContact;
    }
    // Accepted reconstruction also has a sequence identity, even when it creates no new component.
    if (Count > 0 || AcceptedUpdate || E.bReconstructActive) SeenEvents.Add(EventKey,GetWorld()->GetTimeSeconds());
    return Count;
}

void USanctaVFXPresentationComponent::ApplyInputs(FSanctaVFXInstance& I)
{
    auto* C=I.Component.Get(); if (!C) return;
    const auto& E=I.Event; const auto& P=I.Phase;
    FVector Origin=E.Position;
    if (P.Anchor==ESanctaVFXAnchor::Source || P.Anchor==ESanctaVFXAnchor::Link) Origin=SocketPosition(E.Source,E.SourceSocket,E.Position);
    if (P.Anchor==ESanctaVFXAnchor::Target) Origin=SocketPosition(E.Target,E.TargetSocket,E.Position);
    if (P.Anchor==ESanctaVFXAnchor::Projectile && IsValid(E.Projectile)) Origin=E.Projectile->GetActorLocation();
    FVector Direction=E.Direction.GetSafeNormal(UE_SMALL_NUMBER,FVector::ForwardVector);
    if (P.Anchor==ESanctaVFXAnchor::Projectile && IsValid(E.Projectile)) Direction=E.Projectile->GetActorForwardVector();
    if (P.Anchor==ESanctaVFXAnchor::Source && IsValid(E.Source)) Direction=E.Source->GetActorForwardVector();
    const FQuat Rotation=Direction.Rotation().Quaternion();
    C->SetWorldLocationAndRotation(Origin,Rotation);
    const float Scale=P.bUseRadius ? FMath::Max(1.f,E.Radius)/FMath::Max(1.f,P.ReferenceRadius) : 1.f;
    const float RangeScale=P.bUseRange ? FMath::Max(1.f,E.Range)/FMath::Max(1.f,P.ReferenceRange) : Scale;
    const float ConeScale=P.bUseConeAngle ? FMath::Tan(FMath::DegreesToRadians(FMath::Clamp(E.ConeAngle,1.f,175.f)*.5f))/FMath::Max(.001f,FMath::Tan(FMath::DegreesToRadians(P.ReferenceConeAngle*.5f))) : 1.f;
    const FVector X=Rotation.GetAxisX()*RangeScale, Y=Rotation.GetAxisY()*RangeScale*ConeScale, Z=Rotation.GetAxisZ();
    const FVector Endpoint=IsValid(E.EndpointActor) ? SocketPosition(E.EndpointActor,E.EndpointSocket,E.Endpoint) :
        (P.Anchor==ESanctaVFXAnchor::Link ? SocketPosition(E.Target,E.TargetSocket,E.Endpoint) : E.Endpoint);
    const FVector LocalDelta=Rotation.UnrotateVector(Endpoint-Origin);
    const FVector Delta(LocalDelta.X/RangeScale,LocalDelta.Y/(RangeScale*ConeScale),LocalDelta.Z);
    FVector BoundsExtent(P.Anchor==ESanctaVFXAnchor::World?1200.f:400.f,P.Anchor==ESanctaVFXAnchor::World?1200.f:400.f,700.f);
    if(P.bUseRadius){BoundsExtent.X=BoundsExtent.Y=FMath::Max(400.f,E.Radius+150.f);}
    if(P.bUseRange){BoundsExtent.X=FMath::Max(400.f,E.Range+150.f);BoundsExtent.Y=FMath::Max(400.f,E.Range*FMath::Tan(FMath::DegreesToRadians(FMath::Clamp(E.ConeAngle,1.f,175.f)*.5f))+150.f);}
    FBox Bounds(-BoundsExtent,BoundsExtent);
    if(P.bUseEndpoint || P.Anchor==ESanctaVFXAnchor::Link){Bounds+=LocalDelta-FVector(200);Bounds+=LocalDelta+FVector(200);}
    if (!(C->GetSystemFixedBounds()==Bounds)) C->SetSystemFixedBounds(Bounds);
    const FVector ThreeEndpoint(Delta.Y/100.f,Delta.Z/100.f,-Delta.X/100.f);
    const float Age=FMath::Max(0.,GetWorld()->GetTimeSeconds()-I.StartTime);
    const float SinceInput=FMath::Max(0.,GetWorld()->GetTimeSeconds()-I.InputReceiptTime);
    const float ReleaseAge=E.ReleaseAge>=0 ? E.ReleaseAge+SinceInput : -1.f;
    const float GainAge=E.GainAge>=0 ? E.GainAge+SinceInput : -1.f;
    C->SetVariableFloat(TEXT("User.CastProgress"),FMath::Clamp(E.CastProgress,0.f,1.f));
    C->SetVariableFloat(TEXT("User.ReleaseAge"),ReleaseAge);
    C->SetVariableFloat(TEXT("User.AutoPreview"),0.f);
    C->SetVariableFloat(TEXT("User.ElementA"),E.ElementA); C->SetVariableFloat(TEXT("User.ElementB"),E.ElementB);
    C->SetVariableFloat(TEXT("User.RuntimeAge"),Age);
    C->SetVariableFloat(TEXT("User.ResourceCount"),FMath::Clamp(E.ResourceCount,0,FMath::Max(0,E.ResourceMax)));
    C->SetVariableFloat(TEXT("User.OccupiedMask"),E.OccupiedMask & 3);
    auto VectorColor=[](const FVector& V){return FLinearColor(V.X,V.Y,V.Z,0);};
    for (auto Weak : I.Materials) if (auto* M=Weak.Get()) {
        M->SetScalarParameterValue(TEXT("RuntimeEnabled"),1.f);
        M->SetScalarParameterValue(TEXT("RuntimeAge"),Age);
        M->SetVectorParameterValue(TEXT("RuntimeBasisX"),VectorColor(X));
        M->SetVectorParameterValue(TEXT("RuntimeBasisY"),VectorColor(Y));
        M->SetVectorParameterValue(TEXT("RuntimeBasisZ"),VectorColor(Z));
        M->SetVectorParameterValue(TEXT("RuntimeEndpoint"),VectorColor(ThreeEndpoint));
        M->SetScalarParameterValue(TEXT("RuntimeCount"),FMath::Clamp(E.ResourceCount,0,FMath::Max(0,E.ResourceMax)));
        M->SetScalarParameterValue(TEXT("RuntimeMax"),FMath::Max(1,E.ResourceMax));
        M->SetScalarParameterValue(TEXT("RuntimeElementA"),E.ElementA);
        M->SetScalarParameterValue(TEXT("RuntimeElementB"),E.ElementB);
        M->SetScalarParameterValue(TEXT("RuntimeOccupied"),E.OccupiedMask & 3);
        M->SetScalarParameterValue(TEXT("RuntimeGainAge"),GainAge);
        M->SetScalarParameterValue(TEXT("RuntimePending"),E.Pending);
        M->SetScalarParameterValue(TEXT("RuntimeCastProgress"),FMath::Clamp(E.CastProgress,0.f,1.f));
        M->SetScalarParameterValue(TEXT("RuntimeReleaseAge"),ReleaseAge);
        M->SetScalarParameterValue(TEXT("RuntimeAimHalfAngle"),FMath::DegreesToRadians(FMath::Clamp(E.ConeAngle,0.f,175.f)*.5f));
    }
}

int32 USanctaVFXPresentationComponent::UpdatePresentation(const FSanctaVFXEvent& E)
{
    if (!GetWorld() || GetWorld()->GetNetMode()==NM_DedicatedServer || !ValidInputs(E)) return 0;
    int32 Count=0;
    for (auto& Pair : Instances) {
        auto& I=Pair.Value;
        if (I.Event.ExecutionId!=E.ExecutionId || I.Event.StateId!=E.StateId || I.Event.FormId!=E.FormId || I.Event.Target!=E.Target) continue;
        if (!E.Phase.IsNone() && I.Phase.Phase!=E.Phase) continue;
        if (I.Phase.Anchor==ESanctaVFXAnchor::Projectile && I.Event.Projectile!=E.Projectile) continue;
        // One finite impact cannot rewind other occurrences from the same state.
        if (!I.Phase.bPersistent && I.Event.EventSequence!=E.EventSequence) continue;
        if (I.Phase.bBindTargetLife && I.Event.TargetLifeId!=E.TargetLifeId) continue;
        if (E.EventWorldTime>=0 && I.Event.EventWorldTime>=0 && E.EventWorldTime<I.Event.EventWorldTime) continue;
        const FName Mode=I.Event.ModeSnapshot, Stance=I.Event.StanceSnapshot, Relation=I.Event.Relation;
        I.Event=E; I.Event.ModeSnapshot=Mode; I.Event.StanceSnapshot=Stance; I.Event.Relation=Relation;
        I.InputReceiptTime=GetWorld()->GetTimeSeconds();
        I.StartTime=GetWorld()->GetTimeSeconds()-FMath::Max(0.f,E.PhaseAge); ApplyInputs(I); ++Count;
    }
    return Count;
}

void USanctaVFXPresentationComponent::Remove(const FString& Key)
{
    if (auto* I=Instances.Find(Key)) if (auto* C=I->Component.Get()) { C->DeactivateImmediate(); C->DestroyComponent(); }
    Instances.Remove(Key);
}
void USanctaVFXPresentationComponent::EndExecution(FGuid Id, ESanctaVFXEndReason Reason)
{
    if (!Id.IsValid()) return;
    if (ClosedExecutions.Contains(Id)) return;
    if (GetHistoryCount() >= MaxHistoryEntries) PruneHistory();
    if (GetHistoryCount() < MaxHistoryEntries || ClosedExecutions.Contains(Id)) ClosedExecutions.Add(Id,{GetWorld()->GetTimeSeconds(),Reason});
    TArray<FString> Keys;
    for (const auto& Pair : Instances) if (Pair.Value.Event.ExecutionId==Id) {
        const auto& P=Pair.Value.Phase;
        if (P.bPersistent && P.bStateOwned) continue;
        // An authoritative natural finish closes delivery/hold, while an
        // already-confirmed finite impact finishes its own visual envelope.
        if (Reason==ESanctaVFXEndReason::Natural && !P.bPersistent) continue;
        Keys.Add(Pair.Key);
    }
    for (const auto& Key : Keys) Remove(Key);
}
void USanctaVFXPresentationComponent::EndState(FGuid Id, ESanctaVFXEndReason Reason)
{
    if (!Id.IsValid()) return;
    if (ClosedStates.Contains(Id)) return;
    if (GetHistoryCount() >= MaxHistoryEntries) PruneHistory();
    if (GetHistoryCount() < MaxHistoryEntries || ClosedStates.Contains(Id)) ClosedStates.Add(Id,{GetWorld()->GetTimeSeconds(),Reason});
    TArray<FString> Keys; for (const auto& Pair : Instances) if (Pair.Value.Event.StateId==Id) Keys.Add(Pair.Key);
    for (const auto& Key : Keys) Remove(Key);
}
void USanctaVFXPresentationComponent::ResetForLife(FGuid Id)
{
    TArray<FString> Keys; Instances.GetKeys(Keys); for (const auto& Key : Keys) Remove(Key);
    SeenEvents.Reset(); ClosedExecutions.Reset(); ClosedStates.Reset(); LifeId=Id;AnimationContext=FSanctaVFXEvent();
}
void USanctaVFXPresentationComponent::EndPhase(FGuid Id,FName Key)
{
    TArray<FString> Keys;
    for (const auto& Pair : Instances) if ((Pair.Value.Event.StateId==Id || Pair.Value.Event.ExecutionId==Id) && Pair.Value.Phase.ComponentKey==Key) Keys.Add(Pair.Key);
    for (const auto& K : Keys) Remove(K);
}
void USanctaVFXPresentationComponent::SetAnimationContext(const FSanctaVFXEvent& E) { AnimationContext=E; }
int32 USanctaVFXPresentationComponent::PresentAnimationPhase(FName Phase,FName Socket,FVector Endpoint)
{
    // Animation can synchronize cosmetic delivery, never confirm a hit, proc or status.
    if (Phase!=TEXT("Cast") && Phase!=TEXT("Release") && Phase!=TEXT("Trail") && Phase!=TEXT("FootContact") && Phase!=TEXT("Start")) return 0;
    AnimationContext.Phase=Phase;AnimationContext.SourceSocket=Socket;AnimationContext.Endpoint=Endpoint;
    AnimationContext.Position=SocketPosition(AnimationContext.Source,Socket,AnimationContext.Position);
    AnimationContext.EventSequence++;AnimationContext.EventWorldTime=GetWorld()->GetTimeSeconds();
    AnimationContext.bConfirmedHit=false;AnimationContext.bApplied=false;AnimationContext.ConfirmedProcMask=0;
    return Present(AnimationContext);
}
UNiagaraComponent* USanctaVFXPresentationComponent::GetActiveComponent(FName Key) const
{
    for (const auto& Pair : Instances) if (Pair.Value.Phase.ComponentKey==Key) return Pair.Value.Component.Get();
    return nullptr;
}
void USanctaVFXPresentationComponent::TickComponent(float Delta, ELevelTick Type, FActorComponentTickFunction* Tick)
{
    Super::TickComponent(Delta,Type,Tick);
    PruneHistory();
    TArray<FString> RemoveKeys;
    for (auto& Pair : Instances) {
        auto& I=Pair.Value;
        if (!I.Component.IsValid() || (!I.Phase.bPersistent && GetWorld()->GetTimeSeconds()-I.StartTime > I.Phase.Duration)) { RemoveKeys.Add(Pair.Key); continue; }
        if (I.Phase.bBindTargetLife) {
            auto* Host=IsValid(I.Event.Target) ? I.Event.Target->FindComponentByClass<USanctaVFXPresentationComponent>() : nullptr;
            if (!Host || Host->LifeId!=I.Event.TargetLifeId) { RemoveKeys.Add(Pair.Key); continue; }
        }
        if ((I.Phase.Anchor==ESanctaVFXAnchor::Target && !IsValid(I.Event.Target)) || (I.Phase.Anchor==ESanctaVFXAnchor::Projectile && !IsValid(I.Event.Projectile)) ||
            ((I.Phase.Anchor==ESanctaVFXAnchor::Source || I.Phase.Anchor==ESanctaVFXAnchor::Link) && !IsValid(I.Event.Source))) { RemoveKeys.Add(Pair.Key); continue; }
        ApplyInputs(I);
    }
    for (const auto& Key : RemoveKeys) Remove(Key);
}
int32 USanctaVFXPresentationComponent::GetHistoryCount() const
{
    return SeenEvents.Num()+ClosedExecutions.Num()+ClosedStates.Num();
}
void USanctaVFXPresentationComponent::PruneHistory()
{
    const double Before=GetWorld()->GetTimeSeconds()-HistorySeconds;
    for (auto It=SeenEvents.CreateIterator(); It; ++It) if (It.Value()<Before) It.RemoveCurrent();
    for (auto It=ClosedExecutions.CreateIterator(); It; ++It) if (It.Value().Time<Before) It.RemoveCurrent();
    for (auto It=ClosedStates.CreateIterator(); It; ++It) if (It.Value().Time<Before) It.RemoveCurrent();
}
void USanctaVFXPresentationComponent::EndPlay(const EEndPlayReason::Type Reason)
{
    ResetForLife(FGuid()); Super::EndPlay(Reason);
}
