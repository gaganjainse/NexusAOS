# Sesha Modular / Mojo SDK Integration Script
Write-Host "[+] Checking Mojo and Magic CLI setup..." -ForegroundColor Cyan

$wslUncSdk = "\\wsl.localhost\Ubuntu\home\gaganjainse\mojo_core\.pixi\envs\default"
if (Test-Path $wslUncSdk) {
    Write-Host "[OK] Native WSL EXT4 SDK Path Verified: $wslUncSdk (High IOPS Performance)" -ForegroundColor Green
} else {
    Write-Host "[WARN] Native WSL SDK path not accessible via UNC." -ForegroundColor Yellow
}

$localBin = "$env:USERPROFILE\.local\bin"
if (-not (Test-Path $localBin)) {
    New-Item -ItemType Directory -Path $localBin -Force | Out-Null
}

$mojoCmd = Join-Path $localBin "mojo.cmd"
$mojoBat = Join-Path $localBin "mojo.bat"

if (-not (Test-Path $mojoCmd)) {
    Set-Content -Path $mojoCmd -Value "@echo off`nwsl -e bash -c `"cd ~/mojo_core && .pixi/envs/default/bin/mojo %*`"" -Encoding ASCII
}
if (-not (Test-Path $mojoBat)) {
    Copy-Item $mojoCmd $mojoBat -Force
}

Write-Host "[OK] Mojo SDK wrappers verified at $localBin" -ForegroundColor Green
$version = & mojo --version
Write-Host "[OK] Active Mojo Version: $version" -ForegroundColor Green



