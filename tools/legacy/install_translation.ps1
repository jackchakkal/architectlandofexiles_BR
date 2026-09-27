param(
  [string]$MainPak = '..\outputs\v12-corrections\pakchunk0-Windows-ptbr.pak',
  [string]$OverridePak = '..\outputs\v12-corrections\pakchunk9999-Windows_1_P-ptbr.pak',
  [string]$GameRoot = 'H:\Games\Architect\ProjectTT',
  [string]$BackupRoot = '..\work\backups'
)
$ErrorActionPreference = 'Stop'

$running = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'Architect|ProjectTT|DRIMAGE' })
if ($running.Count -gt 0) {
  throw "Feche Architect e o DRIMAGE Launcher antes de instalar. Processo ativo: $($running.ProcessName -join ', ')"
}

$targets = @(
  @{ Name='main'; Source=$MainPak; Target=(Join-Path $GameRoot 'Saved/PersistentDownloadDir/DownloadContent/pakchunk0-Windows.pak') },
  @{ Name='override'; Source=$OverridePak; Target=(Join-Path $GameRoot 'Content/Paks/pakchunk9999-Windows_1_P.pak') }
)

# Preflight every source and destination before making any changes.
foreach ($entry in $targets) {
  if (!(Test-Path -LiteralPath $entry.Source -PathType Leaf)) { throw "PAK preparado não encontrado: $($entry.Source)" }
  $parent = Split-Path -Parent $entry.Target
  if (!(Test-Path -LiteralPath $parent -PathType Container)) { throw "Pasta de instalação não encontrada: $parent" }
  $entry.SourceHash = (Get-FileHash -LiteralPath $entry.Source -Algorithm SHA256).Hash
  $entry.Existed = Test-Path -LiteralPath $entry.Target -PathType Leaf
  if ($entry.Existed) { $entry.PreviousHash = (Get-FileHash -LiteralPath $entry.Target -Algorithm SHA256).Hash }
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = Join-Path $BackupRoot "translation-v12-$stamp"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$committed = [System.Collections.Generic.List[object]]::new()
$manifestPath = Join-Path $backupDir 'install-manifest.json'
$manifest = $null

try {
  # Back up both old files and stage both new files before replacing either target.
  foreach ($entry in $targets) {
    if ($entry.Existed) {
      $entry.Backup = Join-Path $backupDir ([IO.Path]::GetFileName($entry.Target))
      Copy-Item -LiteralPath $entry.Target -Destination $entry.Backup
      $backupHash = (Get-FileHash -LiteralPath $entry.Backup -Algorithm SHA256).Hash
      if ($backupHash -ne $entry.PreviousHash) { throw "Backup falhou na verificação: $($entry.Target)" }
    }
    $entry.Temp = $entry.Target + ".install-$stamp.tmp"
    Copy-Item -LiteralPath $entry.Source -Destination $entry.Temp
    $stagedHash = (Get-FileHash -LiteralPath $entry.Temp -Algorithm SHA256).Hash
    if ($stagedHash -ne $entry.SourceHash) { throw "Cópia temporária falhou na verificação: $($entry.Target)" }
  }

  $manifest = [ordered]@{
    version = 'v12-corrections'
    created_at = (Get-Date).ToString('o')
    game_root = $GameRoot
    files = @($targets | ForEach-Object { [ordered]@{ name=$_.Name; target=$_.Target; source_sha256=$_.SourceHash; existed_before=$_.Existed; previous_sha256=$_.PreviousHash; backup=$_.Backup } })
    status = 'staged'
  }
  $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8

  # Replace as a pair. Any failure restores both prior files (or removes newly created targets).
  foreach ($entry in $targets) {
    $committed.Add($entry)
    Move-Item -LiteralPath $entry.Temp -Destination $entry.Target -Force
    $installedHash = (Get-FileHash -LiteralPath $entry.Target -Algorithm SHA256).Hash
    if ($installedHash -ne $entry.SourceHash) { throw "Hash diferente após instalar $($entry.Target)" }
  }

  $manifest.status = 'installed'
  $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
  foreach ($entry in $targets) { Write-Host "$($entry.Name): $($entry.Target) — SHA-256 $($entry.SourceHash)" }
  Write-Host "Backup e manifesto: $backupDir"
}
catch {
  $failure = $_
  $rollbackErrors = [System.Collections.Generic.List[string]]::new()
  $rollbackEntries = @($committed.ToArray())
  [array]::Reverse($rollbackEntries)
  foreach ($entry in $rollbackEntries) {
    try {
      if ($entry.Existed -and (Test-Path -LiteralPath $entry.Backup)) {
        $rollbackTemp = $entry.Target + ".rollback-$stamp.tmp"
        Copy-Item -LiteralPath $entry.Backup -Destination $rollbackTemp -Force
        Move-Item -LiteralPath $rollbackTemp -Destination $entry.Target -Force
        if ((Get-FileHash -LiteralPath $entry.Target -Algorithm SHA256).Hash -ne $entry.PreviousHash) { throw 'Hash de restauração divergente' }
      } elseif (Test-Path -LiteralPath $entry.Target) {
        [IO.File]::Delete($entry.Target)
      }
    } catch { $rollbackErrors.Add("$($entry.Target): $($_.Exception.Message)") }
  }
  if ($manifest -and (Test-Path -LiteralPath $manifestPath)) {
    $manifest.status = if ($rollbackErrors.Count -eq 0) { 'failed-rolled-back' } else { 'rollback-failed' }
    $manifest.error = $failure.Exception.Message
    $manifest.rollback_errors = @($rollbackErrors)
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding utf8
  }
  if ($rollbackErrors.Count -gt 0) { throw "Instalação falhou e a restauração precisa ser conferida: $($rollbackErrors -join '; ')" }
  throw $failure
}
finally {
  foreach ($entry in $targets) {
    if ($entry.Temp -and (Test-Path -LiteralPath $entry.Temp)) { [IO.File]::Delete($entry.Temp) }
  }
}
