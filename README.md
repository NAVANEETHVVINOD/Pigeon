# Pigeon (formerly OpenMail Hub)

A modern open-source email client designed for privacy, speed, and local connectivity. Features AirDrop-style secure file transfer (LocalDrop) and an offline MediaVault.

## Repository
**GitHub**: [https://github.com/NAVANEETHVVINOD/Pigeon](https://github.com/NAVANEETHVVINOD/Pigeon)

## Project Status
- **Current Phase**: Phase 8 (Refinement & Security Upgrade)
- **Completed**:
    - Core Email (IMAP/SMTP)
    - LocalDrop (P2P Encrypted Transfer)
    - MediaVault (Attachment Gallery)
    - Desktop Bundling (Tauri + Python Sidecar)
- **In Progress**:
    - Market Differentiation (PegionDrop Links)
    - Final Polish for Open Source Launch

## Tech Stack
- **Frontend**: Next.js 14, Tailwind CSS, shadcn/ui
- **Backend**: Python FastAPI, SQLite, Mutable Security (X25519/AES-GCM)
- **Desktop**: Tauri (Rust) v2

## Architecture

```mermaid
graph TD
    User[User Desktop] -->|run| Tauri Shell
    subgraph "Pigeon App"
        Tauri Shell -->|embeds| WebView[Next.js Frontend]
        Tauri Shell -->|manages| Sidecar[Python API Sidecar]
        
        WebView <-->|HTTP/WS| Sidecar
        
        Sidecar -->|IMAP/SMTP| MailServer[Email Provider]
        Sidecar -->|mDNS/WS| Peer[Local Peer (LocalDrop)]
        Sidecar -->|SQL| DB[(SQLite Database)]
        Sidecar -->|Files| Vault[(Media Vault)]
    end
```

## Setup & Development

### 1. Backend (Python)
```bash
cd apps/api
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
# Run Dev Server
uvicorn main:app --reload --port 8000
```

### 2. Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
# App running at http://localhost:3000
```

### 3. Desktop Bundle (Tauri)
```bash
cd apps/web
# Ensure backend sidecar is built (see apps/api/build_sidecar.ps1)
npm run tauri dev
```

