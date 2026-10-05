#pragma once
#include "CoreMinimal.h"
#include "SanctaVFXReviewActor.h"
#include "SanctaVFXPresentation.h"
#include "SanctaVFXRuntimeReview.generated.h"
class ASanctaVFXTerrain;

/** Lab-only real game world captures through the presentation API. */
UCLASS()
class SANCTAVFXBRIDGE_API ASanctaVFXRuntimeReview : public ASanctaVFXReviewActor
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FString CasesJSON;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) bool bInteractive=false;
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void Repeat() override;
    virtual void TogglePause() override;
    virtual void ToggleSlow() override;
    virtual void OpenIndex(int32 Index) override;
private:
    UPROPERTY(Transient) TObjectPtr<USanctaVFXPresentationComponent> Presentation;
    UPROPERTY(Transient) TObjectPtr<AActor> TestSource;
    UPROPERTY(Transient) TObjectPtr<AActor> TestTarget;
    UPROPERTY(Transient) TObjectPtr<AActor> TestProjectile;
    UPROPERTY(Transient) TObjectPtr<ASanctaVFXTerrain> ReviewTerrain;
    TArray<TSharedPtr<FJsonValue>> Cases;
    TArray<FSanctaVFXEvent> BatchInputs;
    TArray<double> GPUFrames,InputUpdates;
    TArray<TSharedPtr<FJsonValue>> PerfResults;
    TArray<TSharedPtr<FJsonValue>> CaptureResults;
    bool CaptureSucceeded=true;
    bool RenderWarmed=false;
    UPROPERTY(Transient) TArray<TObjectPtr<AActor>> BatchActors;
    FSanctaVFXEvent Inputs;
    int32 CaseIndex=0;
    float Wait=0;
    bool Started=false, Captured=false, ViewReady=false, CompileRequested=false;
    int32 PerfFrames=0,PerfTarget=0;
    double SpawnMilliseconds=0;
    bool ViewerAudit=false,ViewerAuditPassed=true;
    int32 ViewerAuditStep=0;
    float ViewerPausedAge=0;
};
