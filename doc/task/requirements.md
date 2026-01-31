# OpenMail Hub - MVP Requirements & Technical Specifications

## 1. Core Vision
OpenMail Hub is a privacy-first, offline-first email client designed for high-performance and local sharing. It combines Thunderbird's power with Superhuman's aesthetics.

## 2. Technical Stack (Strict)
- **Frontend**: Next.js 14 (App Router), Tailwind CSS, shadcn/ui.
- **Backend**: Python FastAPI (Async), SQLModel (SQLite), Pydantic.
- **Protocols**: IMAP (fetching), SMTP (sending), Zeroconf (discovery), WebSockets (transfer).
- **Storage**: Local filesystem (`media_vault/`) + SQLite (`database.db`).

## 3. MVP Feature Scope & Completion Criteria

### 3.1 Authentication & Security
- **Goal**: Securely store credentials for session duration.
- **Tech**: In-memory or encrypted local storage (Simulated for Hackathon).
- **Completion Criteria**:
  - [x] POST /auth/login accepts email/password/server.
  - [x] Returns session token.
  - [ ] Credential encryption at rest (Nice to have).

### 3.2 Inbox & Email Management
- **Goal**: Read/Write email capability compatible with standard IMAP.
- **Tech**: `imapclient`, `email` library.
- **Completion Criteria**:
  - [x] Async Fetch of last 20 emails.
  - [x] Parse MIME headers (Subject, From, Date).
  - [ ] Full Body rendering (HTML sanitization required).
  - [x] Local SQLite caching of headers.

### 3.3 Compose & Sending
- **Goal**: Reliable email delivery.
- **Tech**: `aiosmtplib`.
- **Completion Criteria**:
  - [x] SMTP connection over TLS/STARTTLS.
  - [x] UI Modal for composition.
  - [x] Send success/failure feedback.

### 3.4 LocalDrop (Peer-to-Peer)
- **Goal**: Instant LAN file transfer without cloud.
- **Tech**: Zeroconf (mDNS), WebSockets/HTTP.
- **Completion Criteria**:
  - [x] Auto-discovery of other Pegion clients on LAN.
  - [x] Visual Peer Grid in UI.
  - [x] Drag-and-drop interaction.
  - [ ] Implementation of full file stream piping.

### 3.5 MediaVault
- **Goal**: Offline, visual gallery of email attachments.
- **Tech**: Backend attachment extraction worker.
- **Completion Criteria**:
  - [x] Auto-extract image attachments on sync.
  - [x] Serve images via Static mount.
  - [x] Gallery Grid UI.

## 4. Constraints (Non-Negotiable)
1. **No Cloud Backend**: All logic must run on localhost.
2. **Vertical Integration**: Features must be slice-complete (UI + Backend).
3. **Design Standard**: "Superhuman" quality (Spacing, Typography, Animation).
