# Pegion (formerly OpenMail Hub)

A modern open-source email client like Gmail/Superhuman, with Thunderbird-level power, plus AirDrop-style LocalDrop attachments and an offline Google Photos-like MediaVault.

## Vision
OpenMail Hub is a privacy-first, offline-first communication hub:
- 📩 Email
- 📎 Instant file transfer inside email (LocalDrop)
- 📸 Offline media sorting (MediaVault)

## Tech Stack
- **Frontend**: Next.js 14, Tailwind CSS, shadcn/ui
- **Backend**: Python FastAPI, SQLite, IMAP/SMTP
- **LocalDrop**: Zeroconf, WebSockets
- **Desktop**: Tauri (Rust)

## Setup
### Backend
```bash
cd apps/api
python -m venv venv
# Activate venv
pip install -r requirements.txt
# Run Migrations
alembic upgrade head
python main.py
```

### Frontend (Web)
```bash
cd apps/web
npm install
npm run dev
```

### Desktop App (Tauri)
**Prerequisites**: Rust, Node.js, and Backend running at `http://localhost:8000`.

```bash
cd apps/web
npm run tauri dev
```

**Build for Production**:
```bash
npm run tauri build
```

## Desktop Features
- **Backend Gate**: Ensures API is running before loading UI.
- **Native Notifications**: System alerts for LocalDrop transfers.
- **Sidecar Roadmap**: Future versions will bundle the Python backend automatically.
