# Build the Tauri App (MSI/EXE)
cd apps/web/src-tauri

# Ensure sidecar exists
if (!(Test-Path "binaries/api-sidecar-x86_64-pc-windows-msvc.exe")) {
    Write-Error "Sidecar binary missing! Run apps/api/build_sidecar.ps1 first."
    exit 1
}

# Run Tauri Build
npx tauri build

Write-Host "Build complete! Check apps/web/src-tauri/target/release/bundle"
