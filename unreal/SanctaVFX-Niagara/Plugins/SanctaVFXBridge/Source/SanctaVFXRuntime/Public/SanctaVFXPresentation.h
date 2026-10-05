#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Components/ActorComponent.h"
#include "SanctaVFXPresentation.generated.h"

class UNiagaraSystem;
class UNiagaraComponent;
class UMaterialInstanceDynamic;

UENUM(BlueprintType)
enum class ESanctaVFXAnchor : uint8 { Source, Target, Projectile, World, Link };
UENUM(BlueprintType)
enum class ESanctaVFXGate : uint8 { Admission, ConfirmedHit, Applied, NaturalEnd, Cleanse, Cosmetic };
UENUM(BlueprintType)
enum class ESanctaVFXEndReason : uint8 { Natural, Cancel, Interrupt, Miss, RangeBreak, Cleanse, Death, Rejected, Relevance, Consumed, Replaced };
UENUM(BlueprintType)
enum class ESanctaVFXImportance : uint8 { Essential, Gameplay, Decorative };

// IDs are supplied by gameplay. Display names and asset paths are not execution IDs.
USTRUCT(BlueprintType)
struct SANCTAVFXRUNTIME_API FSanctaVFXEvent
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName FormId;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Phase;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FGuid ExecutionId;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FGuid StateId;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int64 EventSequence = 0;
    // Stamp on receipt in the local presentation clock. Reject stale replay after history eviction.
    UPROPERTY(EditAnywhere, BlueprintReadWrite) double EventWorldTime = -1;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<AActor> Source = nullptr;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<AActor> Target = nullptr;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<AActor> Projectile = nullptr;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TObjectPtr<AActor> EndpointActor = nullptr;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FGuid TargetLifeId;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName SourceSocket;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName TargetSocket;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName EndpointSocket;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FVector Position = FVector::ZeroVector;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FVector Endpoint = FVector::ZeroVector;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FVector Direction = FVector::ForwardVector;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FVector HitNormal = FVector::UpVector;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float Radius = 100.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float Range = 100.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float ConeAngle = 90.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float PhaseAge = 0.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float CastProgress = 0.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float ReleaseAge = -1.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 ResourceCount = 0;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 ResourceMax = 10;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 ElementA = -1;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 ElementB = -1;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 OccupiedMask = 0;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) float GainAge = -1.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Pending = 0;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 ConfirmedProcMask = 0;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bAdmitted = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bConfirmedHit = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bApplied = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bTargetedMiss = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bNaturalEnd = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bCleansed = false;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bReconstructActive = false;
    // Variants are captured at admission. Updating position/resources does not change them.
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName ModeSnapshot;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName StanceSnapshot;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Relation;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Surface;
};

USTRUCT(BlueprintType)
struct SANCTAVFXRUNTIME_API FSanctaVFXPhase
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName Phase;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName ComponentKey;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) TObjectPtr<UNiagaraSystem> System = nullptr;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) ESanctaVFXAnchor Anchor = ESanctaVFXAnchor::Source;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) ESanctaVFXGate Gate = ESanctaVFXGate::Admission;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) ESanctaVFXImportance Importance = ESanctaVFXImportance::Gameplay;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bPersistent = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bStateOwned = true;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bBindTargetLife = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bUseRadius = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bUseEndpoint = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bUseRange = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bUseConeAngle = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) bool bContact = false;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) int32 ContactPriority = 0;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) int32 RequiredProcMask = 0;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName RequiredSurface;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName RequiredModeSnapshot;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName RequiredStanceSnapshot;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName RequiredRelation;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) float Duration = .5f;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) float ReferenceRadius = 100.f;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) float ReferenceRange = 100.f;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) float ReferenceConeAngle = 90.f;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) TMap<FName, float> ScalarDefaults;
};

UCLASS(BlueprintType)
class SANCTAVFXRUNTIME_API USanctaVFXDefinition : public UPrimaryDataAsset
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName FormId;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) int32 CompositionVersion = 1;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FString SourceHash;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) TArray<FSanctaVFXPhase> Phases;
};

USTRUCT()
struct FSanctaVFXInstance
{
    GENERATED_BODY()
    UPROPERTY(Transient) TWeakObjectPtr<UNiagaraComponent> Component;
    UPROPERTY(Transient) TArray<TWeakObjectPtr<UMaterialInstanceDynamic>> Materials;
    UPROPERTY(Transient) FSanctaVFXEvent Event;
    UPROPERTY(Transient) FSanctaVFXPhase Phase;
    double StartTime = 0;
    double InputReceiptTime = 0;
};

// Presentation only: never deals damage, selects targets, refreshes CC, counts skills or sends RPCs.
UCLASS(ClassGroup=(Sancta), BlueprintType, meta=(BlueprintSpawnableComponent))
class SANCTAVFXRUNTIME_API USanctaVFXPresentationComponent : public UActorComponent
{
    GENERATED_BODY()
public:
    USanctaVFXPresentationComponent();
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TArray<TObjectPtr<USanctaVFXDefinition>> Definitions;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FGuid LifeId;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bDecorativeEnabled = true;
    UFUNCTION(BlueprintCallable) int32 Present(const FSanctaVFXEvent& Event);
    UFUNCTION(BlueprintCallable) int32 UpdatePresentation(const FSanctaVFXEvent& Event);
    UFUNCTION(BlueprintCallable) void EndExecution(FGuid ExecutionId, ESanctaVFXEndReason Reason);
    UFUNCTION(BlueprintCallable) void EndState(FGuid StateId, ESanctaVFXEndReason Reason);
    UFUNCTION(BlueprintCallable) void ResetForLife(FGuid NewLifeId);
    UFUNCTION(BlueprintCallable) void EndPhase(FGuid OwnerId, FName ComponentKey);
    UFUNCTION(BlueprintCallable) void SetAnimationContext(const FSanctaVFXEvent& Event);
    UFUNCTION(BlueprintCallable) int32 PresentAnimationPhase(FName Phase, FName Socket, FVector Endpoint);
    UFUNCTION(BlueprintPure) int32 GetActiveCount() const { return Instances.Num(); }
    UFUNCTION(BlueprintPure) UNiagaraComponent* GetActiveComponent(FName ComponentKey) const;
    UFUNCTION(BlueprintPure) int32 GetHistoryCount() const;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
private:
    UPROPERTY(Transient) TMap<FString, FSanctaVFXInstance> Instances;
    UPROPERTY(Transient) FSanctaVFXEvent AnimationContext;
    struct FClosedOwner { double Time; ESanctaVFXEndReason Reason; };
    TMap<FString, double> SeenEvents;
    TMap<FGuid, FClosedOwner> ClosedExecutions;
    TMap<FGuid, FClosedOwner> ClosedStates;
    static constexpr int32 MaxHistoryEntries = 32768;
    static constexpr double HistorySeconds = 120;
    void PruneHistory();
    bool Accept(const FSanctaVFXEvent& Event, const FSanctaVFXPhase& Phase) const;
    void ApplyInputs(FSanctaVFXInstance& Instance);
    void Remove(const FString& Key);
    FString InstanceKey(const FSanctaVFXEvent& Event, const FSanctaVFXPhase& Phase) const;
};
