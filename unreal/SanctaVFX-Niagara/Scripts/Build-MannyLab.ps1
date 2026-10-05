[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8')
$ErrorActionPreference='Stop'
$taskMannyRoot=Split-Path -Parent $PSScriptRoot
$taskMannyPlugin=Join-Path $taskMannyRoot 'Plugins\SanctaVFXMannyLab'
$taskMannyHost=Join-Path $taskMannyRoot 'BuildHost\Plugins\SanctaVFXMannyLab'
foreach($taskMannyFile in Get-ChildItem -LiteralPath $taskMannyPlugin -Recurse -File){
    if($taskMannyFile.FullName -match '\\(Binaries|Intermediate)\\'){continue}
    $taskMannyDestination=Join-Path $taskMannyHost $taskMannyFile.FullName.Substring($taskMannyPlugin.Length+1)
    if((Test-Path -LiteralPath $taskMannyDestination) -and ((Get-FileHash -LiteralPath $taskMannyDestination).Hash -eq (Get-FileHash -LiteralPath $taskMannyFile.FullName).Hash)){continue}
    New-Item -ItemType Directory -Path (Split-Path -Parent $taskMannyDestination) -Force | Out-Null
    Copy-Item -LiteralPath $taskMannyFile.FullName -Destination $taskMannyDestination -Force
}
$env:UE_SKIP_UBT_SDK_SETUP='1'
& "$EngineRoot\Engine\Binaries\ThirdParty\DotNet\10.0\win-x64\dotnet.exe" "$EngineRoot\Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.dll" VFXBuildEditor Win64 Development "-Project=$taskMannyRoot\BuildHost\VFXBuild.uproject" -NoEngineChanges -NoHotReload -UsePrecompiled -NoUBA -NoXGE -WaitMutex "-Log=$taskMannyRoot\Saved\Manny-build.log"
if($LASTEXITCODE -ne 0){throw 'Compilação Manny falhou; consultar Saved/Manny-build.log.'}
New-Item -ItemType Directory -Path "$taskMannyPlugin\Binaries\Win64" -Force | Out-Null
Get-ChildItem -LiteralPath "$taskMannyHost\Binaries\Win64" -File | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination "$taskMannyPlugin\Binaries\Win64\$($_.Name)" -Force}
Write-Output 'Módulo Manny compilado e instalado no laboratório. A ponte existente não foi substituída.'
