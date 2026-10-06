[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[switch]$Audit,[int]$Start=0,[int]$Count=40)
$ErrorActionPreference='Stop'
if($env:UE_ENGINE_ROOT -and -not $PSBoundParameters.ContainsKey('EngineRoot')){$EngineRoot=$env:UE_ENGINE_ROOT}
$taskFullRoot=Split-Path -Parent $PSScriptRoot
$taskFullOutput=Join-Path $taskFullRoot 'Saved\MannyFullCaptures'
$taskFullMap=Join-Path $taskFullRoot 'Content\Sancta\VFX\MannyLab\L_MannyFullReview.umap'
if(-not(Test-Path -LiteralPath $taskFullMap)){throw 'Preparar o palco completo Manny primeiro.'}
$taskFullCases=Get-Content -LiteralPath (Join-Path $taskFullRoot 'Evidence\gameplay-manny-full-cases.json') -Raw | ConvertFrom-Json
if($Start -lt 0 -or $Start -ge $taskFullCases.Count -or $Count -lt 1){throw 'Intervalo de auditoria invalido.'}
$taskFullEnd=[Math]::Min($taskFullCases.Count,$Start+$Count)
$taskFullRenderSettings='t.IdleWhenNotForeground 0, Slate.bAllowThrottling 0, r.VSync 0, r.ShadowQuality 0, r.AmbientOcclusionLevels 0, r.AntiAliasingMethod 0, r.MotionBlurQuality 0'
$taskFullArgs=@("$taskFullRoot\SanctaVFXLab.uproject",'/Game/Sancta/VFX/MannyLab/L_MannyFullReview','-d3d11','-SanctaReview','-nosplash','-NoSound','-ddc=NoZenLocalFallback',"-LocalDataCachePath=$taskFullRoot\Saved\LocalDDC",('-ExecCmds="'+$taskFullRenderSettings+'"'))
if($Audit){
    New-Item -ItemType Directory -Path $taskFullOutput -Force | Out-Null
    $taskFullHashes=@{}
    $taskFullPaths=@('Scripts/Open-MannyFullLab.ps1','Evidence/gameplay-manny-full-cases.json','Content/Sancta/VFX/MannyLab/L_MannyFullReview.umap','Plugins/SanctaVFXMannyLab/Binaries/Win64/UnrealEditor-SanctaVFXMannyLab.dll')
    foreach($taskFullSource in Get-ChildItem -LiteralPath "$taskFullRoot\Plugins\SanctaVFXMannyLab\Source" -Recurse -File){$taskFullPaths+=$taskFullSource.FullName.Substring($taskFullRoot.Length+1).Replace('\','/')}
    foreach($taskFullPath in $taskFullPaths){$taskFullHashes[$taskFullPath]=(Get-FileHash -LiteralPath (Join-Path $taskFullRoot $taskFullPath) -Algorithm SHA256).Hash.ToLowerInvariant()}
    @{first=$Start;end=$taskFullEnd;inputs=$taskFullHashes;render_settings=$taskFullRenderSettings;started_at_utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskFullOutput "batch-$Start-$taskFullEnd-inputs.json") -Encoding utf8
    $taskFullArgs+=@('-RenderOffscreen','-unattended','-SanctaMannyAudit',"-SanctaMannyStart=$Start","-SanctaMannyCount=$Count",'-UseFixedTimeStep','-FPS=15',"-AbsLog=$taskFullOutput\audit-$Start-$taskFullEnd.log")
}
$taskFullProcess=Start-Process -FilePath "$EngineRoot\Engine\Binaries\Win64\UnrealEditor.exe" -ArgumentList $taskFullArgs -WindowStyle Hidden -PassThru
Write-Output "Manny completo: PID $($taskFullProcess.Id); cenarios $Start a $($taskFullEnd-1). P: pose; E: escala; V: vista; B: bracos."
if($Audit){
    $taskFullProcess.WaitForExit()
    if($taskFullProcess.ExitCode -ne 0){throw "Auditoria Manny terminou com erro $($taskFullProcess.ExitCode)."}
    $taskFullRaw=Get-Content -LiteralPath (Join-Path $taskFullOutput "rig-results-$Start-$taskFullEnd.json") -Raw | ConvertFrom-Json
    if(-not $taskFullRaw.complete -or -not $taskFullRaw.passed -or $taskFullRaw.samples.Count -ne ($taskFullEnd-$Start)*24){throw 'O lote nao produziu todas as amostras esperadas.'}
    $taskFullBatch=Get-Content -LiteralPath (Join-Path $taskFullOutput "batch-$Start-$taskFullEnd-inputs.json") -Raw | ConvertFrom-Json
    $taskFullBatch | Add-Member -NotePropertyName exit_code -NotePropertyValue 0 -Force
    $taskFullBatch | Add-Member -NotePropertyName completed_at_utc -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
    $taskFullBatch | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskFullOutput "batch-$Start-$taskFullEnd-inputs.json") -Encoding utf8
    Write-Output "Lote Manny $Start-$taskFullEnd concluido: $($taskFullRaw.samples.Count) amostras; UE exit 0."
}
