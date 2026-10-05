using UnrealBuildTool;
public class SanctaVFXMannyLab : ModuleRules
{
    public SanctaVFXMannyLab(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "SanctaVFXBridge", "SanctaVFXRuntime" });
        PrivateDependencyModuleNames.AddRange(new[] { "Niagara", "Json", "UnrealEd", "InputCore", "RenderCore", "RHI" });
    }
}
