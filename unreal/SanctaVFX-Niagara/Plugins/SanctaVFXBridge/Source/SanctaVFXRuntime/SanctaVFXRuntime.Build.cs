using UnrealBuildTool;
public class SanctaVFXRuntime : ModuleRules
{
    public SanctaVFXRuntime(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "Niagara", "NiagaraCore" });
    }
}
