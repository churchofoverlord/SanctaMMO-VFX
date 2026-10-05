#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "SanctaVFXTerrain.generated.h"
class UStaticMeshComponent;
class UStaticMesh;
class UMaterialInterface;
class UMaterialInstanceDynamic;

// Gameplay owns health/duration. This actor provides the actual blocking body and its appearance.
UCLASS(BlueprintType)
class SANCTAVFXRUNTIME_API ASanctaVFXTerrain : public AActor
{
    GENERATED_BODY()
public:
    ASanctaVFXTerrain();
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Body;
    UPROPERTY(ReplicatedUsing=ApplyState, EditAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMesh> TerrainMesh;
    UPROPERTY(ReplicatedUsing=ApplyState, EditAnywhere, BlueprintReadOnly) TObjectPtr<UMaterialInterface> TerrainMaterial;
    UPROPERTY(ReplicatedUsing=ApplyState, BlueprintReadOnly) bool bTerrainActive = false;
    UPROPERTY(ReplicatedUsing=ApplyState, BlueprintReadOnly) float Integrity = 1.f;
    UPROPERTY(ReplicatedUsing=ApplyState, BlueprintReadOnly) FVector TerrainScale = FVector::OneVector;
    UFUNCTION(BlueprintCallable, BlueprintAuthorityOnly) void InitializeTerrain(UStaticMesh* Mesh, UMaterialInterface* Material, FVector Scale);
    UFUNCTION(BlueprintCallable, BlueprintAuthorityOnly) void SetIntegrity(float Fraction);
    UFUNCTION(BlueprintCallable, BlueprintAuthorityOnly) void RemoveTerrain();
    UFUNCTION() void ApplyState();
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
private:
    UPROPERTY(Transient) TObjectPtr<UMaterialInstanceDynamic> Instance;
};
