#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/HUD.h"
#include "GameFramework/GameModeBase.h"
#include "SanctaVFXReviewActor.generated.h"

class UNiagaraComponent;
class UNiagaraSystem;
class UCameraComponent;

/** Persistent review stage. Playback runs in the game world, rather than editor Python ticks. */
UCLASS()
class SANCTAVFXBRIDGE_API ASanctaVFXReviewActor : public AActor
{
    GENERATED_BODY()
public:
    ASanctaVFXReviewActor();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") TObjectPtr<UNiagaraSystem> System;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") FString SkillTitle;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") FString SkillClass;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") int32 CatalogIndex = 0;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") TArray<FString> CatalogMaps;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") TArray<FString> CatalogTitles;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") float CycleDuration = 3.1f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") FVector CameraPosition = FVector(400,-1250,360);
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") FVector CameraTarget = FVector(400,0,100);
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") float EffectHeight = 0.f;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") TArray<float> ReviewSampleTimes;
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="Review") float ReviewPeakTime = .3f;
    UPROPERTY(VisibleAnywhere, Category="Review") TObjectPtr<UNiagaraComponent> Effect;
    UPROPERTY(VisibleAnywhere, Category="Review") TObjectPtr<UCameraComponent> Camera;
    bool bPaused = false;
    bool bSlow = false;
    bool bReady = false;
    float PlaybackTime = 0;
    virtual void Repeat();
    virtual void TogglePause();
    virtual void ToggleSlow();
    virtual void OpenIndex(int32 Index);
private:
    bool bControllerReady = false;
    float LoadingTime = 0;
    int32 AuditPhase = 0;
    bool bAudit = false;
    bool bAuditAll = false;
    float AuditHoldTime = 0;
    bool bQuality = false;
    int32 QualityStage = 0;
    float QualityCompletionAge = 0.f;
    float CompletionHold = 0.f;
    int32 RepeatCount = 0;
    bool bLoopCheck = false;
    void FinishReview();
    void CaptureQuality(const FString& Suffix);
    void TickQuality(float DeltaSeconds, float ActualAge);
    void CaptureAudit();
};

/** Clickable controls and a paged list of every review scene, with no Niagara knowledge required. */
UCLASS()
class SANCTAVFXBRIDGE_API ASanctaVFXReviewHUD : public AHUD
{
    GENERATED_BODY()
public:
    virtual void DrawHUD() override;
    virtual void NotifyHitBoxClick(FName BoxName) override;
private:
    bool bList = false;
    int32 ListPage = 0;
    ASanctaVFXReviewActor* Stage() const;
    void Button(FName Id, const FString& Label, float X, float Y, float Width);
};

UCLASS()
class SANCTAVFXBRIDGE_API ASanctaVFXReviewGameMode : public AGameModeBase
{
    GENERATED_BODY()
public:
    ASanctaVFXReviewGameMode();
};
