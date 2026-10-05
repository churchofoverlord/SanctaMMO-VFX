using UnrealBuildTool;

public class SanctaVFXBridge : ModuleRules
{
    public SanctaVFXBridge(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] {
            "Core", "CoreUObject", "Engine", "AssetRegistry", "NiagaraCore",
            "Niagara", "NiagaraEditor", "Slate", "SlateCore", "PythonScriptPlugin", "SanctaVFXRuntime"
        });
        PrivateDependencyModuleNames.AddRange(new[] {
            "MessageLog", "Json", "SlateNullRenderer", "RenderCore", "RHI", "UnrealEd", "InputCore"
        });
        PublicIncludePathModuleNames.Add("Sequencer");
    }
}
