[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[int]$Start=0,[int]$BatchSize=40)
$ErrorActionPreference='Stop'
if($BatchSize -lt 1){throw 'BatchSize deve ser positivo.'}
$taskCatalogRoot=Split-Path -Parent $PSScriptRoot
$taskCatalog=Get-Content -LiteralPath "$taskCatalogRoot\Evidence\gameplay-manny-full-cases.json" -Raw | ConvertFrom-Json
for($taskFirst=$Start;$taskFirst -lt $taskCatalog.Count;$taskFirst+=$BatchSize){
    $taskEnd=[Math]::Min($taskFirst+$BatchSize,$taskCatalog.Count)
    $taskRawPath="$taskCatalogRoot\Saved\MannyFullCaptures\rig-results-$taskFirst-$taskEnd.json"
    $taskMetaPath="$taskCatalogRoot\Saved\MannyFullCaptures\batch-$taskFirst-$taskEnd-inputs.json"
    $taskReusable=$false
    if((Test-Path -LiteralPath $taskRawPath) -and (Test-Path -LiteralPath $taskMetaPath)){
        $taskRaw=Get-Content -LiteralPath $taskRawPath -Raw | ConvertFrom-Json
        $taskMeta=Get-Content -LiteralPath $taskMetaPath -Raw | ConvertFrom-Json
        $taskReusable=$taskRaw.complete -and $taskRaw.passed -and $taskRaw.cleanup_passed -and $taskMeta.exit_code -eq 0 -and $taskRaw.samples.Count -eq ($taskEnd-$taskFirst)*24
        $taskRecordedCatalog=$taskRaw.catalog_json | ConvertFrom-Json
        for($taskCaseIndex=$taskFirst;$taskCaseIndex -lt $taskEnd;$taskCaseIndex++){
            $taskRecordedCase=$taskRecordedCatalog[$taskCaseIndex] | ConvertTo-Json -Depth 30 -Compress
            $taskCurrentCase=$taskCatalog[$taskCaseIndex] | ConvertTo-Json -Depth 30 -Compress
            if($taskRecordedCase -ne $taskCurrentCase){$taskReusable=$false}
        }
        foreach($taskInput in $taskMeta.inputs.PSObject.Properties){
            if($taskInput.Name -match '\.umap$'){
                $taskCurrent=(Get-FileHash -LiteralPath (Join-Path $taskCatalogRoot $taskInput.Name) -Algorithm SHA256).Hash.ToLowerInvariant()
                if($taskCurrent -ne $taskInput.Value){
                    $taskMapArchive=Join-Path $taskCatalogRoot "Saved\MannyFullMapArchive\$($taskInput.Value).umap"
                    if(-not(Test-Path -LiteralPath $taskMapArchive)){$taskReusable=$false}
                    elseif((Get-FileHash -LiteralPath $taskMapArchive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskInput.Value){$taskReusable=$false}
                }
            }
            elseif($taskInput.Name -match '\.(cpp|h|cs|dll|ps1)$'){
                $taskCurrent=(Get-FileHash -LiteralPath (Join-Path $taskCatalogRoot $taskInput.Name) -Algorithm SHA256).Hash.ToLowerInvariant()
                if($taskCurrent -ne $taskInput.Value){$taskReusable=$false}
            }
        }
    }
    if($taskReusable){Write-Output "Lote $taskFirst-$taskEnd ja validado; preservado.";continue}
    & "$PSScriptRoot\Open-MannyFullLab.ps1" -EngineRoot $EngineRoot -Audit -Start $taskFirst -Count ($taskEnd-$taskFirst)
}
Write-Output 'Todos os lotes nativos Manny completos. Executar auditoria de imagens e inspecao visual.'
