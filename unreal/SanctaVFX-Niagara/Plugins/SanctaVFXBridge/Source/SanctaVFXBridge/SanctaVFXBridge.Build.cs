using UnrealBuildTool;

public class SanctaVFXBridge : ModuleRules
{
    public SanctaVFXBridge(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] {
            "Core", "CoreUObject", "Engine", "AssetRegistry", "NiagaraCore",
            "Niagara", "NiagaraEditor", "Slate", "SlateCore", "PythonScriptPlugin"
        });
        PrivateDependencyModuleNames.AddRange(new[] {
            "MessageLog", "Json", "SlateNullRenderer", "RenderCore", "RHI"
        });
        PublicIncludePathModuleNames.Add("Sequencer");
    }
}
