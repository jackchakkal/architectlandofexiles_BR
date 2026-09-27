param(
  [Parameter(Mandatory=$true)][string[]]$Pak,
  [Parameter(Mandatory=$true)][string]$OutputRoot,
  [string]$Repak = 'work/repak/target/release/repak.exe',
  [string]$AesKeyFile = 'work/.architect-aes-key'
)
$ErrorActionPreference = 'Stop'
if (!(Test-Path -LiteralPath $Repak)) { throw "repak não encontrado: $Repak" }
if (!(Test-Path -LiteralPath $AesKeyFile)) { throw "Chave AES local não encontrada: $AesKeyFile" }
$aesKey = (Get-Content -LiteralPath $AesKeyFile -Raw).Trim()
if ($aesKey -notmatch '^(0x)?[0-9a-fA-F]{64}$') { throw 'A chave deve conter 64 caracteres hexadecimais.' }
try {
  foreach ($pakPath in $Pak) {
    if (!(Test-Path -LiteralPath $pakPath)) { throw "PAK não encontrado: $pakPath" }
    $name = [IO.Path]::GetFileNameWithoutExtension($pakPath)
    $destination = Join-Path $OutputRoot $name
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    & $Repak --aes-key $aesKey unpack -o $destination $pakPath
    if ($LASTEXITCODE -ne 0) { throw "repak falhou ao extrair $pakPath (código $LASTEXITCODE)." }
  }
}
finally { Remove-Variable aesKey -ErrorAction SilentlyContinue }
