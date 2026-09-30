#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "SanctaVFXLabLibrary.generated.h"
class UNiagaraSystem;
class UWorld;
UCLASS()
class USanctaVFXLabLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool SetUserFloat(UNiagaraSystem* System, FString Name, float Value);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString InspectSystem(UNiagaraSystem* System);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static FString SimulateSystem(UNiagaraSystem* System, UWorld* World, TArray<float> Times);
    UFUNCTION(BlueprintCallable, Category="SanctaVFXLab")
    static bool CaptureSystem(UNiagaraSystem* System, UWorld* World, float Time, FString Directory, FString FileName);
};
