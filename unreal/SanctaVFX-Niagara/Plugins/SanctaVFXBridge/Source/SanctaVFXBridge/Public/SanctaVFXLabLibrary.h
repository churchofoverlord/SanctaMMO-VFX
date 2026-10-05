#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "SanctaVFXLabLibrary.generated.h"
class UNiagaraSystem;
class UWorld;
class UMaterialInterface;
class UStaticMesh;
class USanctaVFXDefinition;
struct FSanctaVFXEvent;
UCLASS()
class USanctaVFXLabLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString ValidatePresentationRuntime(UNiagaraSystem* System, UWorld* World);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static int32 ConfigureRuntimeMaterials(UNiagaraSystem* System);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString ValidateRuntimeBindings(USanctaVFXDefinition* Definition, UWorld* World);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool ConfigureTerrainMesh(UStaticMesh* Mesh, TArray<FVector> Vertices);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString ValidateTerrain(UStaticMesh* Mesh, UMaterialInterface* Material, UWorld* World);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool CaptureRuntimeDefinition(USanctaVFXDefinition* Definition, UWorld* World, FSanctaVFXEvent Inputs, FString Directory, FString FileName);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool CreateReviewMap(FString MapPath, UNiagaraSystem* System, FString Title, FString SkillClass, float Duration, FVector CameraPosition, FVector CameraTarget, float EffectHeight, TArray<FString> Maps, TArray<FString> Titles, int32 Index, UStaticMesh* Body, UMaterialInterface* FloorMaterial, UMaterialInterface* BodyMaterial, TArray<FVector> ActorPositions, TArray<float> SampleTimes, float PeakTime);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString ValidateMaterial(UMaterialInterface* Material, UWorld* World);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool SetUserFloat(UNiagaraSystem* System, FString Name, float Value);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString InspectSystem(UNiagaraSystem* System);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString SimulateSystem(UNiagaraSystem* System, UWorld* World, TArray<float> Times);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString SimulateSystemInputs(UNiagaraSystem* System, UWorld* World, TArray<float> Times, TArray<FString> ParameterNames, TArray<float> ParameterValues);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool CaptureSystem(UNiagaraSystem* System, UWorld* World, float Time, FString Directory, FString FileName);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString MeasureSimulationCost(UNiagaraSystem* System, UWorld* World, int32 CastCount, int32 TickCount);
};
