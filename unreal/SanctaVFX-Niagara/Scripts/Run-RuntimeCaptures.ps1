[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[string]$LogName='Runtime-game-captures.log',[ValidateRange(15,60)][int]$CaptureTickFPS=15,[string]$Map='/Game/Sancta/VFX/Review/L_RuntimeAudit',[ValidateSet('Default','Low')][string]$Quality='Default')
$ErrorActionPreference='Stop'
$taskRuntimeRoot=Split-Path -Parent $PSScriptRoot
$taskConsole='t.IdleWhenNotForeground 0, Slate.bAllowThrottling 0, r.VSync 0, t.MaxFPS 0'
if($Quality -eq 'Low'){$taskConsole+=', sg.EffectsQuality 0, fx.Niagara.QualityLevel 0'}
$taskRuntimeArgs=@("$taskRuntimeRoot\SanctaVFXLab.uproject",$Map,'-d3d11','-RenderOffscreen','-unattended','-nosplash','-NoSound','-ddc=NoZenLocalFallback','-SanctaReview','-UseFixedTimeStep',"-FPS=$CaptureTickFPS",'-ini:EditorSettings:[/Script/UnrealEd.EditorPerformanceSettings]:bThrottleCPUWhenNotForeground=False',"-ExecCmds=`"$taskConsole`"","-LocalDataCachePath=$taskRuntimeRoot\Saved\LocalDDC","-AbsLog=$taskRuntimeRoot\Saved\$LogName")
$taskRuntimeProc=Start-Process -FilePath (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe') -ArgumentList $taskRuntimeArgs -WindowStyle Hidden -PassThru
Write-Output "Capturas runtime: PID $($taskRuntimeProc.Id); Saved\RuntimeCaptures."
$taskRuntimeProc.WaitForExit()
if($taskRuntimeProc.ExitCode -ne 0){throw "Falha de captura: $($taskRuntimeProc.ExitCode)."}
