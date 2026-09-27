<#
Gera o PAK de tradução (override de prioridade alta) e o pacote ZIP para jogadores.

  pwsh -File tools/build_release.ps1 -Version v13 -TranslationRoot translations/v13

Saída: ..\outputs\<Version>\pakchunk9999-Windows_21474835_P.pak, release.json e Architect-PTBR-<Version>.zip
Requer: repak_cli (..\work\repak\target\release\repak.exe) e a chave AES local (work/.architect-aes-key, nunca versionada).
O PAK contém APENAS os 227 CSVs de ProjectTT/Content/TT/Data/CSV/L10N/en — nenhum arquivo do jogo.
#>
param(
  [Parameter(Mandatory)][string]$Version,
  [string]$TranslationRoot = 'translations/v12-corrections',
  [string]$OutputRoot = '',
  [string]$WorkRoot = '..\work\build-release',
  [string]$Repak = '..\work\repak\target\release\repak.exe',
  [string]$AesKeyFile = 'work/.architect-aes-key',
  [string]$PakVersion = 'V11',
  [uint32]$PathHashSeed = 3911529124,
  [string]$PakName = 'pakchunk9999-Windows_21474835_P.pak'
)
$ErrorActionPreference = 'Stop'
if (-not $OutputRoot) { $OutputRoot = "..\outputs\$Version" }
$relative = 'ProjectTT/Content/TT/Data/CSV/L10N/en'
$source = Join-Path $TranslationRoot $relative
if (!(Test-Path -LiteralPath $source)) { throw "Pasta CSV não encontrada em $source" }
if (!(Test-Path -LiteralPath $Repak)) { throw "repak não encontrado: $Repak" }
if (!(Test-Path -LiteralPath $AesKeyFile)) { throw "Chave AES local não encontrada: $AesKeyFile" }
$aesKey = (Get-Content -LiteralPath $AesKeyFile -Raw).Trim()
if ($aesKey -notmatch '^(0x)?[0-9a-fA-F]{64}$') { throw 'A chave deve conter 64 caracteres hexadecimais.' }

$stage = Join-Path $WorkRoot ("$Version-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$stageCsv = Join-Path $stage $relative
$outPak = Join-Path $OutputRoot $PakName
New-Item -ItemType Directory -Force -Path $stageCsv,$OutputRoot | Out-Null
try {
  $csvs = Get-ChildItem -LiteralPath $source -Filter '*.csv' -File
  if ($csvs.Count -ne 227) { Write-Warning "Esperava 227 tabelas, encontrei $($csvs.Count)." }
  $csvs | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $stageCsv -Force }
  & $Repak --aes-key $aesKey pack $stage $outPak --version $PakVersion --path-hash-seed $PathHashSeed --quiet
  if ($LASTEXITCODE -ne 0) { throw "Falha ao criar o PAK (código $LASTEXITCODE)." }
  & $Repak --aes-key $aesKey info $outPak
  if ($LASTEXITCODE -ne 0) { throw 'O PAK gerado não passou pela leitura do índice.' }
} finally { Remove-Variable aesKey -ErrorAction SilentlyContinue }

$hash = (Get-FileHash -LiteralPath $outPak -Algorithm SHA256).Hash
$release = [ordered]@{ version=$Version; pak=$PakName; sha256=$hash; tables=$csvs.Count; translationRoot=$TranslationRoot; builtAt=(Get-Date).ToString('s') }
$releaseJson = Join-Path $OutputRoot 'release.json'
$release | ConvertTo-Json | Set-Content -Encoding UTF8 $releaseJson

# Pacote para jogadores
$zipDir = Join-Path $OutputRoot "Architect-PTBR-$Version"
if (Test-Path $zipDir) { Remove-Item $zipDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
Copy-Item $outPak $zipDir
Copy-Item $releaseJson $zipDir
Copy-Item 'tools/player-installer/install.ps1','tools/player-installer/Instalar-Traducao-PTBR.bat','tools/player-installer/Desinstalar-Traducao-PTBR.bat','tools/player-installer/LEIA-ME.txt' $zipDir
$zip = Join-Path $OutputRoot "Architect-PTBR-$Version.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path $zipDir -DestinationPath $zip
$zipHash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
Write-Host ''
Write-Host "PAK : $outPak"
Write-Host "SHA-256 do PAK: $hash"
Write-Host "ZIP : $zip"
Write-Host "SHA-256 do ZIP: $zipHash"
Write-Host 'Publique o ZIP e os dois hashes na Release do GitHub e em releases/<versão>/manifest.json.'
