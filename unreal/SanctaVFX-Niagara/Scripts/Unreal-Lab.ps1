[CmdletBinding()]
param(
    [ValidateSet('Check','Build','Prepare','Rebuild','Validate','Open','OpenLatest','OpenReview')]
    [string]$Action = 'Check',
    [string]$EngineRoot = $env:UE_ENGINE_ROOT,
    [switch]$SkipDeploy,
    [switch]$AuditReview
)
$ErrorActionPreference = 'Stop'
$labRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($EngineRoot)) { $EngineRoot = 'C:\UE_5.8' }
$EngineRoot = (Resolve-Path -LiteralPath $EngineRoot).Path
$editor = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$commandlet = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$version = Get-Content -LiteralPath (Join-Path $EngineRoot 'Engine\Build\Build.version') -Raw | ConvertFrom-Json
if ($version.MajorVersion -ne 5 -or $version.MinorVersion -ne 8 -or $version.PatchVersion -notin @(2,3)) {
    throw 'Este laboratorio aceita UE 5.8.2 ou 5.8.3. Nao atualize o Engine automaticamente.'
}
foreach ($required in @($editor,$commandlet)) {
    if (-not (Test-Path -LiteralPath $required)) { throw "Ficheiro em falta: $required" }
}
$nativeConverter = Join-Path $EngineRoot 'Engine\Plugins\FX\CascadeToNiagaraConverter\Binaries\Win64'
$nativeManifest = Get-Content -LiteralPath (Join-Path $nativeConverter 'UnrealEditor.modules') -Raw | ConvertFrom-Json
$editorManifest = Get-Content -LiteralPath (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.modules') -Raw | ConvertFrom-Json
if ($nativeManifest.BuildId -ne $editorManifest.BuildId) { throw 'Conversor nativo incompatível com o Editor. Não alterar BuildIds.' }
if (-not (Test-Path -LiteralPath (Join-Path $nativeConverter 'UnrealEditor-CascadeToNiagaraConverter.dll'))) { throw 'DLL do conversor nativo em falta.' }
if ($Action -eq 'Check') {
    Write-Output "Engine encontrado: $EngineRoot (UE 5.8.$($version.PatchVersion)). Conversor nativo sera usado. Nenhum editor ou compilador foi iniciado."
    exit 0
}
$env:UE_SKIP_UBT_SDK_SETUP = '1'
$project = Join-Path $labRoot 'SanctaVFXLab.uproject'
$plugin = Join-Path $labRoot 'Plugins\SanctaVFXBridge'
$saved = Join-Path $labRoot 'Saved'
New-Item -ItemType Directory -Path $saved -Force | Out-Null

function Copy-ChangedFile([string]$From,[string]$To) {
    if ((Test-Path -LiteralPath $To) -and ((Get-FileHash -LiteralPath $From).Hash -eq (Get-FileHash -LiteralPath $To).Hash)) { return }
    New-Item -ItemType Directory -Path (Split-Path -Parent $To) -Force | Out-Null
    Copy-Item -LiteralPath $From -Destination $To -Force
}
if ($Action -eq 'Build') {
    $hostRoot = Join-Path $labRoot 'BuildHost'
    $hostPlugin = Join-Path $hostRoot 'Plugins\SanctaVFXBridge'
    foreach ($relativeRoot in @('Source')) {
        $sourceRoot = Join-Path $plugin $relativeRoot
        foreach ($file in (Get-ChildItem -LiteralPath $sourceRoot -File -Recurse)) {
            $relative = $file.FullName.Substring($plugin.Length+1)
            Copy-ChangedFile $file.FullName (Join-Path $hostPlugin $relative)
        }
    }
    Copy-ChangedFile (Join-Path $plugin 'SanctaVFXBridge.uplugin') (Join-Path $hostPlugin 'SanctaVFXBridge.uplugin')
    $dotnet = Join-Path $EngineRoot 'Engine\Binaries\ThirdParty\DotNet\10.0\win-x64\dotnet.exe'
    $ubt = Join-Path $EngineRoot 'Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.dll'
    if (-not (Test-Path -LiteralPath $dotnet) -or -not (Test-Path -LiteralPath $ubt)) {
        throw 'Falta o runtime DotNet/UnrealBuildTool do Engine transferido.'
    }
    & $dotnet $ubt VFXBuildEditor Win64 Development "-Project=$(Join-Path $hostRoot 'VFXBuild.uproject')" -NoEngineChanges -NoHotReload -UsePrecompiled -NoUBA -NoXGE -WaitMutex "-Log=$(Join-Path $saved 'Bridge-build.log')"
    if ($LASTEXITCODE -ne 0) { throw "Falhou a compilacao do plugin: $LASTEXITCODE" }
    $compiled = Join-Path $hostPlugin 'Binaries\Win64'
    if (-not (Test-Path -LiteralPath (Join-Path $compiled 'UnrealEditor-SanctaVFXBridge.dll'))) { throw 'A compilacao nao produziu a DLL esperada.' }
    if ($SkipDeploy) {
        Write-Output 'Plugin compilado no BuildHost; a ponte do laboratorio em execucao foi preservada.'
        exit 0
    }
    New-Item -ItemType Directory -Path (Join-Path $plugin 'Binaries\Win64') -Force | Out-Null
    Get-ChildItem -LiteralPath $compiled -File | ForEach-Object { Copy-ChangedFile $_.FullName (Join-Path $plugin ('Binaries\Win64\'+$_.Name)) }
    Write-Output 'Plugin compilado. Proximo passo: Retomar-Preparacao.cmd.'
    exit 0
}

$engineManifest = Get-Content -LiteralPath (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.modules') -Raw | ConvertFrom-Json
$pluginManifestPath = Join-Path $plugin 'Binaries\Win64\UnrealEditor.modules'
if (-not (Test-Path -LiteralPath $pluginManifestPath)) { throw 'Compilar primeiro com Compilar-Ponte.cmd.' }
$pluginManifest = Get-Content -LiteralPath $pluginManifestPath -Raw | ConvertFrom-Json
if ($pluginManifest.BuildId -ne $engineManifest.BuildId) { throw 'Plugin de outra compilacao. Execute Compilar-Ponte.cmd. Nunca altere o BuildId manualmente.' }
$systemFile = Join-Path $labRoot 'Content\VFXLab\FireBoltI\NS_FireBoltI.uasset'
$commonArguments = @($project,'-d3d11','-ddc=NoZenLocalFallback',"-LocalDataCachePath=$(Join-Path $saved 'LocalDDC')","-ShaderWorkingDir=$(Join-Path $saved 'ShaderWork')")
if ($Action -in @('Open','OpenLatest','OpenReview')) {
    if (-not (Test-Path -LiteralPath $systemFile)) { throw 'NS_FireBoltI ainda nao foi criado. Execute Retomar-Preparacao.cmd.' }
    if ($Action -eq 'OpenReview') {
        $sceneReportPath = Join-Path $labRoot 'Evidence\review-scenes.json'
        if (-not (Test-Path -LiteralPath $sceneReportPath)) { throw 'Os cenarios de revisao ainda nao foram gerados.' }
        $sceneReport = Get-Content -LiteralPath $sceneReportPath -Raw | ConvertFrom-Json
        if ($sceneReport.status -ne 'saved' -or $sceneReport.scenes.Count -ne $sceneReport.total -or $sceneReport.failures.Count -gt 0) { throw 'A geracao dos cenarios nao foi concluida. Consultar Evidence\review-scenes.json.' }
        Write-Output "A abrir $($sceneReport.total) skills. No visualizador, usar os botoes Anterior, Seguinte e Todas as skills."
        $reviewArguments = @('-SanctaReview','-ExecCmds=r.ShadowQuality 0,r.AmbientOcclusionLevels 0')
        if ($AuditReview) { $reviewArguments += @('-SanctaReviewAuditAll',"-AbsLog=$(Join-Path $saved 'Review-native-audit.log')") }
        # UE's editor map argument must precede the switches.
        $reviewLaunchArguments = @($project,$sceneReport.scenes[0].map) + $commonArguments[1..($commonArguments.Count-1)] + $reviewArguments
        & $editor @reviewLaunchArguments
        exit $LASTEXITCODE
    }
    $openScript = if ($Action -eq 'OpenLatest') { 'abrir_latest_vfx.py' } else { 'abrir_firebolt.py' }
    & $editor @commonArguments "-ExecutePythonScript=$(Join-Path $PSScriptRoot $openScript)"
    exit $LASTEXITCODE
}
if ($Action -eq 'Validate' -and -not (Test-Path -LiteralPath $systemFile)) { throw 'Sistema em falta. Execute Retomar-Preparacao.cmd.' }
$scriptName = if ($Action -eq 'Rebuild') { 'build_firebolt.py' } elseif ($Action -eq 'Validate' -or (Test-Path -LiteralPath $systemFile)) { 'validate_firebolt.py' } else { 'build_firebolt.py' }
Write-Output 'A iniciar a preparacao/validacao no UE. A primeira compilacao de shaders pode demorar.'
& $commandlet @commonArguments '-run=pythonscript' "-script=$(Join-Path $PSScriptRoot $scriptName)" '-unattended' '-nosplash' '-NoSound' '-AllowCommandletRendering' '-RenderOffscreen' '-stdout' '-FullStdOutLogOutput' *> (Join-Path $saved 'Preparacao.log')
if ($LASTEXITCODE -ne 0) { throw "O Unreal terminou com erro $LASTEXITCODE. Consultar Saved\Preparacao.log." }
$validationPath = Join-Path $labRoot 'VFX-validation-report.json'
if (-not (Test-Path -LiteralPath $validationPath)) { throw 'Nao foi produzido um relatorio de validacao. Consultar VFX-build-report.json e Saved\Preparacao.log.' }
$validation = Get-Content -LiteralPath $validationPath -Raw | ConvertFrom-Json
if ($validation.status -ne 'passed') { throw 'Validacao falhou. Consultar VFX-validation-report.json.' }
Write-Output 'Simulacao validada. Inspecionar as capturas em Previews e abrir o efeito com Abrir-Laboratorio.cmd.'
