[CmdletBinding()]
param([string]$EngineRoot='C:\UE_5.8',[ValidateRange(1,25)][int]$BatchSize=25,[switch]$Revalidate)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$taskDefinitions=Get-Content -LiteralPath (Join-Path $taskRoot 'Evidence/gameplay-runtime-definitions.json') -Raw | ConvertFrom-Json
$taskDefinitionCount=$taskDefinitions.definitions.Count
$taskSubsetPath='Saved/runtime-material-subset.json'
if($Revalidate){
    $taskPlan=Get-Content -LiteralPath (Join-Path $taskRoot 'Saved/runtime-bindings-revalidation-plan.json') -Raw | ConvertFrom-Json
    $taskDefinitionCount=$taskPlan.revalidate.Count
    $taskSubsetPath='Saved/runtime-material-revalidation.json'
    $env:SANCTA_BINDINGS_REVALIDATE='1'
}
$taskResults=@{}
$taskRuns=@()
try {
    for($taskOffset=0;$taskOffset -lt $taskDefinitionCount;$taskOffset+=$BatchSize){
        $env:SANCTA_BINDINGS_OFFSET=[string]$taskOffset
        $env:SANCTA_BINDINGS_LIMIT=[string]$BatchSize
        $taskLog=if($Revalidate){"Runtime-material-revalidation-$taskOffset.log"}else{"Runtime-material-batch-$taskOffset.log"}
        & (Join-Path $PSScriptRoot 'Run-LabScript.ps1') -Script validate_runtime_materials.py -LogName $taskLog -EngineRoot $EngineRoot
        $taskSubset=Get-Content -LiteralPath (Join-Path $taskRoot $taskSubsetPath) -Raw | ConvertFrom-Json
        if(-not $taskSubset.passed -or $taskSubset.offset -ne $taskOffset){throw 'Material batch failed or stale report.'}
        foreach($taskProperty in $taskSubset.results.PSObject.Properties){$taskResults[$taskProperty.Name]=$taskProperty.Value}
        $taskRuns+=@{offset=$taskOffset;limit=$BatchSize;definitions_tested=$taskSubset.definitions_tested;process_exit_code=0;log="Saved/$taskLog"}
        Write-Output "Material bindings: $($taskResults.Count) passed."
    }
    $taskReport=@{passed=$true;definitions_tested=$taskResults.Count;results=$taskResults;runs=$taskRuns;scope='First phase of every saved definition whose first phase is not terminal. Separate bounded UE processes prevent accumulation of transient test actors; all-phase rendering is checked separately.';monolithic_exit_anomaly='Preserved in Saved/Runtime-finalize-20261005.log: result 0 and no logged errors, process exit 3. No monolithic run is accepted as successful.'}
    $taskOutput=if($Revalidate){'Saved/runtime-material-revalidation.json'}else{'Evidence/gameplay-runtime-material-validation.json'}
    $taskReport | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath (Join-Path $taskRoot $taskOutput) -Encoding utf8
} finally {
    Remove-Item Env:SANCTA_BINDINGS_OFFSET -ErrorAction SilentlyContinue
    Remove-Item Env:SANCTA_BINDINGS_LIMIT -ErrorAction SilentlyContinue
    if($Revalidate){Remove-Item Env:SANCTA_BINDINGS_REVALIDATE -ErrorAction SilentlyContinue}
}
