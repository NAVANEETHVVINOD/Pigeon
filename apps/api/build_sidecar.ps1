# Build the sidecar
pyinstaller --name api-sidecar --onefile --clean --hidden-import=uvicorn.logging --hidden-import=uvicorn.loops --hidden-import=uvicorn.loops.auto --hidden-import=uvicorn.protocols --hidden-import=uvicorn.protocols.http --hidden-import=uvicorn.protocols.http.auto --hidden-import=uvicorn.protocols.websockets --hidden-import=uvicorn.protocols.websockets.auto --hidden-import=uvicorn.lifespan --hidden-import=uvicorn.lifespan.on --hidden-import=engineio.async_drivers.aiohttp server.py

# Create destination directory if it doesn't exist
$destDir = "..\web\src-tauri\binaries"
if (!(Test-Path -Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir
}

# Move and rename (Windows x64)
Move-Item -Path "dist\api-sidecar.exe" -Destination "$destDir\api-sidecar-x86_64-pc-windows-msvc.exe" -Force

Write-Host "Sidecar built and placed in src-tauri/binaries"
