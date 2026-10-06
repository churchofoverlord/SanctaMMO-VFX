#pragma once
#include "CoreMinimal.h"
#include "SanctaVFXReviewActor.h"
#include "SanctaVFXPresentation.h"
#include "SanctaVFXMannyReview.generated.h"

class USkeletalMeshComponent;
class UAnimSequence;
class ASanctaVFXTerrain;

/** Independent editor-only fixture. Never changes the game rig or approved source effects. */
UCLASS()
class SANCTAVFXMANNYLAB_API ASanctaVFXMannyReview : public ASanctaVFXReviewActor
{
    GENERATED_BODY()
public:
    ASanctaVFXMannyReview();
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FString CasesJSON;
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void Repeat() override;
    virtual void TogglePause() override;
    virtual void ToggleSlow() override;
    virtual void OpenIndex(int32 Index) override;
private:
    UPROPERTY(Transient) TObjectPtr<AActor> SourceActor;
    UPROPERTY(Transient) TObjectPtr<AActor> TargetActor;
    UPROPERTY(Transient) TObjectPtr<AActor> SourceProxy;
    UPROPERTY(Transient) TObjectPtr<AActor> TargetProxy;
    UPROPERTY(Transient) TObjectPtr<AActor> ProjectileProxy;
    UPROPERTY(Transient) TObjectPtr<ASanctaVFXTerrain> ReviewTerrain;
    UPROPERTY(Transient) TObjectPtr<USkeletalMeshComponent> SourceMesh;
    UPROPERTY(Transient) TObjectPtr<USkeletalMeshComponent> TargetMesh;
    UPROPERTY(Transient) TObjectPtr<USanctaVFXPresentationComponent> Presentation;
    UPROPERTY(Transient) TObjectPtr<USanctaVFXPresentationComponent> TargetLife;
    UPROPERTY(Transient) TObjectPtr<USanctaVFXDefinition> Definition;
    UPROPERTY(Transient) TArray<TObjectPtr<UAnimSequence>> Poses;
    TArray<TSharedPtr<FJsonValue>> Cases;
    TArray<TSharedPtr<FJsonValue>> Results;
    FSanctaVFXEvent Inputs;
    int32 CaseIndex=0, PoseIndex=0, ScaleIndex=1, SampleIndex=0, ViewIndex=0, ArmMask=3;
    float Wait=0, PoseTime=0;
    bool Audit=false, Started=false, ViewReady=false, Passed=true, CompileRequested=false;
    bool FullCatalog=false;
    int32 AuditFirst=0, AuditEnd=0;
    FVector Origin=FVector::ZeroVector, Endpoint=FVector::ZeroVector;
    FQuat AnchorRotation=FQuat::Identity;
    void SetPose(float Time);
    void UpdateRig(float Age);
    void ApplyFixtureBasis(UNiagaraComponent* Component);
    void UpdateCamera();
    void RecordSample();
    bool Capture(const FString& Name, bool Baseline);
    void Finish();
    void WriteResults(bool Complete);
    FString CaptureDirectory() const;
};
