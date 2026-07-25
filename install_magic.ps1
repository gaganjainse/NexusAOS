# Sesha Modular / Mojo SDK Integration Script
Write-Host "[+] Checking Mojo and Magic CLI setup..." -ForegroundColor Cyan

$localBin = "$env:USERPROFILE\.local\bin"
if (-not (Test-Path $localBin)) {
    New-Item -ItemType Directory -Path $localBin -Force | Out-Null
}

$mojoCmd = Join-Path $localBin "mojo.cmd"
$mojoBat = Join-Path $localBin "mojo.bat"

if (-not (Test-Path $mojoCmd)) {
    Set-Content -Path $mojoCmd -Value '@echo off'`n'wsl -e bash -c "cd ~/mojo_core && .pixi/envs/default/bin/mojo %*"' -Encoding ASCII
}
if (-not (Test-Path $mojoBat)) {
    Copy-Item $mojoCmd $mojoBat -Force
}

Write-Host "[✓] Mojo SDK wrappers verified at $localBin" -ForegroundColor Green
$version = & mojo --version
Write-Host "[✓] Active Mojo Version: $version" -ForegroundColor Green

