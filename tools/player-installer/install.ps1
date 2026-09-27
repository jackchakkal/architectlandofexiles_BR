# Tradução PT-BR — Architect: Land of Exiles
# Instalador/desinstalador para jogadores. Uso: install.ps1 [-Uninstall] [-GameRoot <pasta do Architect>]
param([switch]$Uninstall, [string]$GameRoot)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Here      = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReleaseFile = Join-Path $Here 'release.json'
if (-not (Test-Path $ReleaseFile)) { Write-Host 'ERRO: release.json não encontrado ao lado do instalador. Extraia o ZIP inteiro.' -ForegroundColor Red; Read-Host 'ENTER para sair' | Out-Null; exit 1 }
$Release   = Get-Content $ReleaseFile -Raw -Encoding UTF8 | ConvertFrom-Json
$PakName   = $Release.pak
$PakSha256 = $Release.sha256.ToUpperInvariant()
$Version   = $Release.version
if ($PakName -cne 'pakchunk9999-Windows_21474835_P.pak' -or $PakSha256 -notmatch '^[0-9A-F]{64}$') {
    Write-Host 'ERRO: release.json contém nome de arquivo ou hash inesperado.' -ForegroundColor Red
    exit 1
}

function Write-Title($t){ Write-Host ''; Write-Host "== $t ==" -ForegroundColor Cyan }
function Fail($m){ Write-Host ''; Write-Host "ERRO: $m" -ForegroundColor Red; Write-Host ''; Read-Host 'Pressione ENTER para sair' | Out-Null; exit 1 }

function Test-GameRoot($p){ if (-not $p) { return $false }; return (Test-Path (Join-Path $p 'ProjectTT\Content\Paks\pakchunk0-Windows.pak')) -and (Test-Path (Join-Path $p 'Architect.exe')) }

function Find-GameRoot {
    # 1) chaves de desinstalação do Windows (launcher pode registrar InstallLocation)
    $keys = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
    foreach ($k in $keys) {
        try { Get-ItemProperty $k -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like '*Architect*' } | ForEach-Object {
            foreach ($c in @($_.InstallLocation, (Split-Path -Parent ($_.DisplayIcon -replace '"','')))) { if (Test-GameRoot $c) { return $c } } } } catch {}
    }
    # 2) pastas comuns em todas as unidades
    $drives = Get-PSDrive -PSProvider FileSystem | ForEach-Object { $_.Root }
    $subs = 'Games\Architect','Architect','DRIMAGE\Architect','DRIMAGE\Games\Architect','Program Files\Architect','Program Files (x86)\Architect','Program Files\DRIMAGE\Architect','Program Files (x86)\DRIMAGE\Architect','Games\DRIMAGE\Architect'
    foreach ($d in $drives) { foreach ($s in $subs) { $c = Join-Path $d $s; if (Test-GameRoot $c) { return $c } } }
    # 3) processo do jogo aberto? (não deveria, mas dá a pasta)
    return $null
}

function Assert-GameClosed {
    $procs = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^(Architect|Architect-Win64-Shipping|ProjectTT|DRIMAGE.*)$' }
    if ($procs) { Fail ("Feche o jogo e o launcher antes de continuar. Em execução: " + (($procs | Select-Object -ExpandProperty ProcessName -Unique) -join ', ')) }
}

Write-Host ''
Write-Host "Tradução PT-BR — Architect: Land of Exiles ($Version)" -ForegroundColor Green
Write-Host 'Projeto comunitário, sem vínculo com a publisher. Uso por sua conta e risco.'

Write-Title 'Localizando o jogo'
if (-not (Test-GameRoot $GameRoot)) { $GameRoot = Find-GameRoot }
while (-not (Test-GameRoot $GameRoot)) {
    Write-Host 'Não encontrei a pasta do jogo automaticamente.' -ForegroundColor Yellow
    Write-Host 'Cole aqui o caminho da pasta que contém Architect.exe (ex.: H:\Games\Architect) e pressione ENTER.'
    $GameRoot = (Read-Host 'Pasta do jogo').Trim('"',' ')
    if (-not $GameRoot) { Fail 'Nenhuma pasta informada.' }
    if (-not (Test-GameRoot $GameRoot)) { Write-Host "Essa pasta não contém Architect.exe + ProjectTT\Content\Paks. Tente de novo." -ForegroundColor Yellow }
}
$PaksDir = Join-Path $GameRoot 'ProjectTT\Content\Paks'
Write-Host "Jogo encontrado em: $GameRoot"

Assert-GameClosed

# Só estes nomes foram usados por este projeto. Nunca apagar por curinga.
$knownNames = @($PakName, 'pakchunk9999-Windows_1_P.pak')
$knownFiles = @($knownNames | ForEach-Object { Join-Path $PaksDir $_ } | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf })
if ($Uninstall) {
    Write-Title 'Removendo a tradução'
    if (-not $knownFiles) { Write-Host 'Nenhum arquivo da tradução encontrado. Nada a fazer.' }
    foreach ($file in $knownFiles) { Remove-Item -LiteralPath $file -Force; Write-Host "Removido: $(Split-Path -Leaf $file)" }
    $record = Join-Path $PaksDir 'traducao-ptbr.json'
    if (Test-Path -LiteralPath $record -PathType Leaf) { Remove-Item -LiteralPath $record -Force; Write-Host 'Removido: traducao-ptbr.json' }
    Write-Host ''; Write-Host 'Pronto. O jogo voltou ao idioma original.' -ForegroundColor Green
    Read-Host 'Pressione ENTER para sair' | Out-Null; exit 0
}

Write-Title 'Verificando o arquivo da tradução'
$src = Join-Path $Here $PakName
if (-not (Test-Path $src)) { Fail "Arquivo $PakName não está na mesma pasta deste instalador. Extraia o ZIP inteiro antes de executar." }
$h = (Get-FileHash $src -Algorithm SHA256).Hash
if ($h -ne $PakSha256) { Fail "O arquivo $PakName está corrompido ou não é o oficial desta versão (SHA-256 diferente). Baixe o pacote novamente." }
Write-Host 'Arquivo íntegro (SHA-256 confere).'

Write-Title 'Instalando'
$dst = Join-Path $PaksDir $PakName
$tmp = "$dst.new"
$backup = "$dst.previous-$([guid]::NewGuid().ToString('N'))"
try {
    Copy-Item -LiteralPath $src -Destination $tmp -Force
    if ((Get-FileHash -LiteralPath $tmp -Algorithm SHA256).Hash -ne $PakSha256) { throw 'A cópia falhou na verificação.' }
    if (Test-Path -LiteralPath $dst -PathType Leaf) { Move-Item -LiteralPath $dst -Destination $backup }
    try { Move-Item -LiteralPath $tmp -Destination $dst }
    catch {
        if (Test-Path -LiteralPath $backup -PathType Leaf) { Move-Item -LiteralPath $backup -Destination $dst }
        throw
    }
    if (Test-Path -LiteralPath $backup -PathType Leaf) { Remove-Item -LiteralPath $backup -Force }
} catch {
    if (Test-Path -LiteralPath $tmp -PathType Leaf) { Remove-Item -LiteralPath $tmp -Force }
    Fail $_.Exception.Message
}
$legacy = Join-Path $PaksDir 'pakchunk9999-Windows_1_P.pak'
if (Test-Path -LiteralPath $legacy -PathType Leaf) { Remove-Item -LiteralPath $legacy -Force; Write-Host 'Removida versão antiga deste projeto.' }
Write-Host "Instalado: $dst"
[ordered]@{ version=$Version; pak=$PakName; sha256=$PakSha256; installedAt=(Get-Date).ToString('s') } | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $PaksDir 'traducao-ptbr.json')

Write-Host ''
Write-Host 'Pronto! Abra o jogo normalmente. Nenhum arquivo original foi modificado.' -ForegroundColor Green
Write-Host 'Para remover, execute Desinstalar-Traducao-PTBR.bat.'
Read-Host 'Pressione ENTER para sair' | Out-Null
