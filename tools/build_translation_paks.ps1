param(
  [Parameter(Mandatory=$true)][string]$FullPakRoot,
  [string]$TranslationRoot = 'translations/v11-quality',
  [string]$WorkRoot = 'work/build-v11',
  [string]$OutputRoot = 'outputs',
  [string]$Repak = 'work/repak/target/release/repak.exe',
  [string]$AesKeyFile = 'work/.architect-aes-key',
  [string]$PakVersion = 'V11',
  [uint32]$PathHashSeed = 3911529124
)
$ErrorActionPreference = 'Stop'
$relative = 'ProjectTT/Content/TT/Data/CSV/L10N/en'
$source = Join-Path $TranslationRoot $relative
if (!(Test-Path -LiteralPath $source)) { throw "Pasta CSV não encontrada em $source" }
if (!(Test-Path -LiteralPath $FullPakRoot)) { throw "Árvore completa extraída não encontrada: $FullPakRoot" }
if (!(Test-Path -LiteralPath $Repak)) { throw "repak não encontrado: $Repak" }
if (!(Test-Path -LiteralPath $AesKeyFile)) { throw "Chave AES local não encontrada: $AesKeyFile" }
$aesKey = (Get-Content -LiteralPath $AesKeyFile -Raw).Trim()
if ($aesKey -notmatch '^(0x)?[0-9a-fA-F]{64}$') { throw 'A chave deve conter 64 caracteres hexadecimais.' }
$runRoot = Join-Path $WorkRoot (Get-Date -Format 'yyyyMMdd-HHmmss')
$fullStage = Join-Path $runRoot 'full'
$overrideStage = Join-Path $runRoot 'override'
$fullCsv = Join-Path $fullStage $relative
$overrideCsv = Join-Path $overrideStage $relative
$outFull = Join-Path $OutputRoot 'pakchunk0-Windows-ptbr.pak'
$outOverride = Join-Path $OutputRoot 'pakchunk9999-Windows_1_P-ptbr.pak'
New-Item -ItemType Directory -Force -Path $runRoot,$OutputRoot,$fullCsv,$overrideCsv | Out-Null
try {
  Copy-Item -Path (Join-Path $FullPakRoot '*') -Destination $fullStage -Recurse -Force
  Get-ChildItem -LiteralPath $source -Filter '*.csv' -File | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $fullCsv -Force
    Copy-Item -LiteralPath $_.FullName -Destination $overrideCsv -Force
  }
  & $Repak --aes-key $aesKey pack $fullStage $outFull --version $PakVersion --compression Zlib --path-hash-seed $PathHashSeed --quiet
  if ($LASTEXITCODE -ne 0) { throw "Falha ao criar pacote principal (código $LASTEXITCODE)." }
  & $Repak --aes-key $aesKey pack $overrideStage $outOverride --version $PakVersion --path-hash-seed $PathHashSeed --quiet
  if ($LASTEXITCODE -ne 0) { throw "Falha ao criar pacote de localização (código $LASTEXITCODE)." }
  & $Repak --aes-key $aesKey info $outFull
  if ($LASTEXITCODE -ne 0) { throw 'O pacote principal não passou pela leitura do índice.' }
  & $Repak --aes-key $aesKey info $outOverride
  if ($LASTEXITCODE -ne 0) { throw 'O pacote de localização não passou pela leitura do índice.' }
  Write-Host "Pacotes preparados: $outFull e $outOverride"
}
finally { Remove-Variable aesKey -ErrorAction SilentlyContinue }
