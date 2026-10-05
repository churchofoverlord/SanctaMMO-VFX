#include "SanctaVFXTerrain.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Net/UnrealNetwork.h"

ASanctaVFXTerrain::ASanctaVFXTerrain()
{
    bReplicates=true;SetReplicateMovement(true);
    Body=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("IcebergBody"));SetRootComponent(Body);
    Body->SetMobility(EComponentMobility::Movable);
    Body->SetCollisionObjectType(ECC_WorldDynamic);
    Body->SetCollisionResponseToAllChannels(ECR_Block);
    Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    Body->SetCanEverAffectNavigation(true);
}
void ASanctaVFXTerrain::InitializeTerrain(UStaticMesh* Mesh, UMaterialInterface* Material, FVector Scale)
{
    if (!HasAuthority() || !Mesh || Scale.ContainsNaN() || Scale.GetMin()<=0) return;
    TerrainMesh=Mesh;TerrainMaterial=Material;TerrainScale=Scale;Integrity=1.f;bTerrainActive=true;ApplyState();ForceNetUpdate();
}
void ASanctaVFXTerrain::SetIntegrity(float Fraction)
{
    if (!HasAuthority() || !FMath::IsFinite(Fraction)) return;
    Integrity=FMath::Clamp(Fraction,0.f,1.f);ApplyState();ForceNetUpdate();
}
void ASanctaVFXTerrain::RemoveTerrain()
{
    if (!HasAuthority()) return;
    bTerrainActive=false;ApplyState();Destroy();
}
void ASanctaVFXTerrain::ApplyState()
{
    Body->SetStaticMesh(TerrainMesh);
    SetActorScale3D(TerrainScale);
    if (TerrainMaterial && (!Instance || Instance->Parent!=TerrainMaterial)) { Instance=UMaterialInstanceDynamic::Create(TerrainMaterial,this);Body->SetMaterial(0,Instance); }
    if (Instance) Instance->SetScalarParameterValue(TEXT("TerrainIntegrity"),Integrity);
    Body->SetVisibility(bTerrainActive,true);
    Body->SetCollisionEnabled(bTerrainActive ? ECollisionEnabled::QueryAndPhysics : ECollisionEnabled::NoCollision);
}
void ASanctaVFXTerrain::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(ASanctaVFXTerrain,TerrainMesh);DOREPLIFETIME(ASanctaVFXTerrain,TerrainMaterial);
    DOREPLIFETIME(ASanctaVFXTerrain,bTerrainActive);DOREPLIFETIME(ASanctaVFXTerrain,Integrity);
    DOREPLIFETIME(ASanctaVFXTerrain,TerrainScale);
}
