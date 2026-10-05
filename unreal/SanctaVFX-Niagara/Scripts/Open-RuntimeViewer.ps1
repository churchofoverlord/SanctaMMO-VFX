[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[switch]$Audit)
$ErrorActionPreference='Stop'
if($env:UE_ENGINE_ROOT -and -not $PSBoundParameters.ContainsKey('EngineRoot')){$EngineRoot=$env:UE_ENGINE_ROOT}
$taskViewerRoot=Split-Path -Parent $PSScriptRoot
$taskViewerMap=Join-Path $taskViewerRoot 'Content\Sancta\VFX\Review\L_RuntimeViewer.umap'
if(-not(Test-Path -LiteralPath $taskViewerMap)){throw 'O visualizador de fases ainda nao foi preparado.'}
$taskViewerEditor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$taskViewerArgs=@("$taskViewerRoot\SanctaVFXLab.uproject",'/Game/Sancta/VFX/Review/L_RuntimeViewer','-d3d11','-SanctaReview','-nosplash','-NoSound','-ddc=NoZenLocalFallback',"-LocalDataCachePath=$taskViewerRoot\Saved\LocalDDC",'-ExecCmds="t.IdleWhenNotForeground 0, Slate.bAllowThrottling 0, r.VSync 0, r.ShadowQuality 0, r.AmbientOcclusionLevels 0"')
if($Audit){$taskViewerArgs+=@('-RenderOffscreen','-unattended','-SanctaRuntimeViewerAudit',"-AbsLog=$taskViewerRoot\Saved\Runtime-viewer-audit.log")}
$taskViewerProc=Start-Process -FilePath $taskViewerEditor -ArgumentList $taskViewerArgs -WindowStyle Hidden -PassThru
Write-Output 'Visualizador: Anterior / Seguinte / Todas as skills. Espaco pausa; R repete; S alterna 1.0 / 1/3.'
if($Audit){$taskViewerProc.WaitForExit();if($taskViewerProc.ExitCode -ne 0){throw "Auditoria do visualizador terminou com erro $($taskViewerProc.ExitCode)."}}
