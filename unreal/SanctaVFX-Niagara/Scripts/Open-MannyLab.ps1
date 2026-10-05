[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[switch]$Audit)
$ErrorActionPreference='Stop'
if($env:UE_ENGINE_ROOT -and -not $PSBoundParameters.ContainsKey('EngineRoot')){$EngineRoot=$env:UE_ENGINE_ROOT}
$taskMannyRoot=Split-Path -Parent $PSScriptRoot
if(-not(Test-Path -LiteralPath "$taskMannyRoot\Content\Sancta\VFX\MannyLab\L_MannyReview.umap")){throw 'Preparar o laboratório Manny primeiro: ver MANNY_VFX.md.'}
$taskMannyArgs=@("$taskMannyRoot\SanctaVFXLab.uproject",'/Game/Sancta/VFX/MannyLab/L_MannyReview','-d3d11','-SanctaReview','-nosplash','-NoSound','-ddc=NoZenLocalFallback',"-LocalDataCachePath=$taskMannyRoot\Saved\LocalDDC",'-ExecCmds="t.IdleWhenNotForeground 0, Slate.bAllowThrottling 0, r.VSync 0, r.ShadowQuality 0, r.AmbientOcclusionLevels 0"')
if($Audit){$taskMannyArgs+=@('-RenderOffscreen','-unattended','-SanctaMannyAudit','-UseFixedTimeStep','-FPS=15',"-AbsLog=$taskMannyRoot\Saved\Manny-audit.log")}
$taskMannyProcess=Start-Process -FilePath "$EngineRoot\Engine\Binaries\Win64\UnrealEditor.exe" -ArgumentList $taskMannyArgs -WindowStyle Hidden -PassThru
Write-Output "Manny: PID $($taskMannyProcess.Id). P muda pose; E muda escala; espaço pausa; R repete; S alterna velocidade."
if($Audit){$taskMannyProcess.WaitForExit();if($taskMannyProcess.ExitCode -ne 0){throw "Auditoria Manny terminou com erro $($taskMannyProcess.ExitCode)."}}
