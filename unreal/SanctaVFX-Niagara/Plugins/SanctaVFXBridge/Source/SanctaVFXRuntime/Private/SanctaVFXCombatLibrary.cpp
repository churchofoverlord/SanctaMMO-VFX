#include "SanctaVFXCombatLibrary.h"
FName USanctaVFXCombatLibrary::BasicPresentationId(ESanctaVFXWeapon Weapon,ESanctaVFXPrimary Primary)
{
    static const TCHAR* Names[]={TEXT("Sword"),TEXT("Axe"),TEXT("Club"),TEXT("Wand"),TEXT("Rapier"),TEXT("DualDaggers"),TEXT("FistsGauntlets"),TEXT("GreatClub"),TEXT("Staff"),TEXT("Crossbow"),TEXT("Greatsword"),TEXT("Greataxe"),TEXT("Bow"),TEXT("Spear")};
    if (uint8(Weapon)>=UE_ARRAY_COUNT(Names) || uint8(Primary)>uint8(ESanctaVFXPrimary::Mystic)) return NAME_None;
    const TCHAR* Channel=(Primary==ESanctaVFXPrimary::Fighter || Primary==ESanctaVFXPrimary::Scout) ? TEXT("Physical") : TEXT("Magical");
    return FName(*FString::Printf(TEXT("Combat.Basic.%s.%s"),Names[uint8(Weapon)],Channel));
}
bool USanctaVFXCombatLibrary::IsRangedPresentation(ESanctaVFXWeapon W)
{
    return W==ESanctaVFXWeapon::Wand || W==ESanctaVFXWeapon::Staff || W==ESanctaVFXWeapon::Bow || W==ESanctaVFXWeapon::Crossbow;
}
