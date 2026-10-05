#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "SanctaVFXCombatLibrary.generated.h"
UENUM(BlueprintType)
enum class ESanctaVFXPrimary : uint8 { Fighter, Scout, Mage, Mystic };
UENUM(BlueprintType)
enum class ESanctaVFXWeapon : uint8 { Sword, Axe, Club, Wand, Rapier, DualDaggers, FistsGauntlets, GreatClub, Staff, Crossbow, Greatsword, Greataxe, Bow, Spear };
UCLASS()
class SANCTAVFXRUNTIME_API USanctaVFXCombatLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintPure) static FName BasicPresentationId(ESanctaVFXWeapon Weapon, ESanctaVFXPrimary Primary);
    UFUNCTION(BlueprintPure) static bool IsRangedPresentation(ESanctaVFXWeapon Weapon);
};
