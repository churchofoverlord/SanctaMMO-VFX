[CmdletBinding()]
param([Parameter(Mandatory)][string]$Script,[Parameter(Mandatory)][string]$LogName,[string]$EngineRoot='C:\UE_5.8')
$ErrorActionPreference='Stop'
$taskLabRoot=Split-Path -Parent $PSScriptRoot
$taskScriptPath=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $Script)).Path
if (-not $taskScriptPath.StartsWith($PSScriptRoot+[IO.Path]::DirectorySeparatorChar)){throw 'O script deve pertencer ao laboratorio.'}
$taskUnused=[Math]::Max(0,[Environment]::ProcessorCount-2)
$taskOverride="-ini:Engine:[DevOptions.Shaders]:NumUnusedShaderCompilingThreads=$taskUnused,NumUnusedShaderCompilingThreadsDuringGame=$taskUnused,ShaderCompilerCoreCountThreshold=100"
& (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe') (Join-Path $taskLabRoot 'SanctaVFXLab.uproject') '-d3d11' '-ddc=NoZenLocalFallback' $taskOverride "-LocalDataCachePath=$taskLabRoot\Saved\LocalDDC" "-ShaderWorkingDir=$taskLabRoot\Saved\ShaderWork" '-run=pythonscript' "-script=$taskScriptPath" '-unattended' '-nosplash' '-NoSound' '-AllowCommandletRendering' '-RenderOffscreen' '-stdout' '-FullStdOutLogOutput' *> (Join-Path $taskLabRoot "Saved\$LogName")
if($LASTEXITCODE -ne 0){throw "UE terminou com erro $LASTEXITCODE; consultar Saved\$LogName."}
Write-Output "$Script : UE exit 0"
