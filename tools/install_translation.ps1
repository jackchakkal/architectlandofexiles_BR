param(
  [Parameter(Mandatory=$true)][string]$MainPak,
  [Parameter(Mandatory=$true)][string]$OverridePak,
  [string]$GameRoot = 'H:\Games\Architect\ProjectTT',
  [string]$BackupRoot = 'work/backups'
)
$ErrorActionPreference = 'Stop'
$running = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'Architect|ProjectTT' }
if ($running) { throw "Feche o jogo antes de instalar. Processo ativo: $(($running.ProcessName -join ', '))" }
foreach ($candidate in @($MainPak,$OverridePak)) { if (!(Test-Path -LiteralPath $candidate)) { throw "PAK preparado não encontrado: $candidate" } }
$targets = @(
  @{Source=$MainPak; Target=(Join-Path $GameRoot 'Saved/PersistentDownloadDir/DownloadContent/pakchunk0-Windows.pak')},
  @{Source=$OverridePak; Target=(Join-Path $GameRoot 'Content/Paks/pakchunk9999-Windows_1_P.pak')}
)
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
foreach ($entry in $targets) {
  $parent=Split-Path -Parent $entry.Target
  if (!(Test-Path -LiteralPath $parent)) { throw "Pasta de instalação não encontrada: $parent" }
  $backup=Join-Path $BackupRoot ("{0}-{1}.pak" -f ([IO.Path]::GetFileNameWithoutExtension($entry.Target)), $stamp)
  if (Test-Path -LiteralPath $entry.Target) { Copy-Item -LiteralPath $entry.Target -Destination $backup }
  $temporary=Join-Path $parent (([IO.Path]::GetFileName($entry.Target))+'.new')
  Copy-Item -LiteralPath $entry.Source -Destination $temporary -Force
  Move-Item -LiteralPath $temporary -Destination $entry.Target -Force
  $sourceHash=(Get-FileHash -LiteralPath $entry.Source -Algorithm SHA256).Hash
  $installedHash=(Get-FileHash -LiteralPath $entry.Target -Algorithm SHA256).Hash
  if ($sourceHash -ne $installedHash) { throw "Hash diferente após instalar $($entry.Target)" }
  Write-Host "$($entry.Target) instalado; SHA-256 $installedHash; backup $backup"
}
Write-Host 'Instalação concluída. Abra o jogo para conferir a tradução.'
