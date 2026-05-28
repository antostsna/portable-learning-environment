# Build the packaged Windows app locally.
#
# Mirrors .github/workflows/release.yml so a local build matches CI.
# Run from the repo root in PowerShell:
#
#     .\scripts\build_windows.ps1
#
# Output: dist\Portable Learning Environment\  and  release\*.zip

$ErrorActionPreference = "Stop"

$python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Error "Virtual environment not found at .venv. Create it first:`n  py -m venv .venv`n  .\.venv\Scripts\python -m pip install -r requirements.txt"
}

Write-Host "==> Ensuring PyInstaller is installed"
& $python -m pip install --upgrade pip pyinstaller

Write-Host "==> Refreshing version metadata"
& $python scripts\generate_version_info.py

Write-Host "==> Building with PyInstaller"
& $python -m PyInstaller --noconfirm --windowed `
    --name "Portable Learning Environment" `
    --icon assets\ico.ico `
    --version-file scripts\version_info.txt `
    --paths src `
    --add-data "assets;assets" `
    --add-data "docs;docs" `
    --add-data "src\ple\views\theme\light.qss;ple\views\theme" `
    --add-data "src\ple\views\theme\dark.qss;ple\views\theme" `
    --collect-submodules ple `
    main.py

Write-Host "==> Zipping release"
New-Item -ItemType Directory -Force -Path release | Out-Null
$zip = "release\PortableLearningEnvironment-local-windows.zip"
if (Test-Path $zip) { Remove-Item $zip }
Compress-Archive -Path "dist\Portable Learning Environment\*" -DestinationPath $zip

Write-Host ""
Write-Host "Done."
Write-Host "  App folder: dist\Portable Learning Environment\"
Write-Host "  Zip:        $zip"
Write-Host "Test it by running the .exe in the app folder before distributing."
