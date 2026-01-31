# OpenMail Hub - Task Checklist

## 1. Project Infrastructure
- [x] **1.1 Setup Monorepo Structure** <!-- id: 1.1 -->
- [x] **1.2 Initialize Tech Stack** <!-- id: 1.2 -->
- [x] **1.3 Define API Contracts** <!-- id: 1.3 -->

## 2. Authentication Slice
- [x] **2.1 Backend Auth Logic** <!-- id: 2.1 -->
- [x] **2.2 Frontend Login UI** <!-- id: 2.2 -->

## 3. Inbox Vertical Slice
- [x] **3.1 Mail Service (IMAP)** <!-- id: 3.1 -->
- [x] **3.2 Inbox API Endpoint** <!-- id: 3.2 -->
- [x] **3.3 Inbox UI Components** <!-- id: 3.3 -->

## 4. Compose Vertical Slice
- [x] **4.1 SMTP Service** <!-- id: 4.1 -->
- [x] **4.2 Send API Endpoint** <!-- id: 4.2 -->
- [x] **4.3 Compose Modal UI** <!-- id: 4.3 -->

## 5. LocalDrop (P2P) Slice
- [x] **5.1 Zeroconf Discovery** <!-- id: 5.1 -->
- [x] **5.2 LocalDrop UI** <!-- id: 5.2 -->
- [x] **5.3 File Transfer Logic** <!-- id: 5.3 -->

## 6. MediaVault Slice
- [x] **6.1 Attachment Extraction** <!-- id: 6.1 -->
- [x] **6.2 Media API** <!-- id: 6.2 -->
- [x] **6.3 Media Gallery UI** <!-- id: 6.3 -->

## 7. QA & Polish
- [x] **7.1 End-to-End Verification** <!-- id: 7.1 -->
- [x] **7.2 Documentation Refinement** <!-- id: 7.2 -->

## 8. Production Readiness (Phase 5)
- [x] **8.1 Credential Security** <!-- id: 8.1 -->
    - [x] Install crypto libs (python-jose, cryptography)
    - [x] Create AuthService with Fernet encryption
    - [x] Implement JWT Session Tokens
- [x] **8.2 Background Sync** <!-- id: 8.2 -->
    - [x] Implement SyncWorker
    - [x] Remove blocking sync from Inbox API
- [x] **8.3 Database Migrations** <!-- id: 8.3 -->
    - [x] Init Alembic and apply initial migration
- [x] **8.4 Desktop Packaging** <!-- id: 8.4 -->
    - [x] Init Tauri in apps/web
    - [x] Add BackendGate / Health Check
    - [x] Configure CI Workflow
- [x] **8.5 UI/UX Polish (Phase 5.6)** <!-- id: 8.5 -->
    - [x] App Shell (Sidebar, Topbar)
    - [x] Split-View Inbox
    - [x] Compose Modal & Shortcuts
    - [x] LocalDrop UI
    - [x] MediaVault UI
    - [x] Settings Page

- [x] **Phase 6: Mobile Compatibility** <!-- id: 6.0 -->
    - [x] **6.1 Responsive Layout** <!-- id: 6.1 -->
        - [x] Bottom Tab Navigation
        - [x] Collapse Sidebar on Mobile
        - [x] Floating Compose Button
    - [x] **6.2 Mobile Reader** <!-- id: 6.2 -->
        - [x] Dynamic Route `/dashboard/inbox/[id]`
        - [x] Back Navigation
    - [x] **6.3 PWA Integration** <!-- id: 6.3 -->
        - [x] Manifest & Icons
        - [x] Service Worker
    - [x] **6.4 Mobile LocalDrop** <!-- id: 6.4 -->
        - [x] Mobile-friendly Peer List
        - [x] Tap-to-Send

- [ ] **Phase 7: Real Open Source Startup Launch** <!-- id: 7.0 -->
    - [x] **7.1 Cleanup + Refactor** <!-- id: 7.1 -->
        - [x] Consolidate `ReaderPane` (Use `inbox` version)
        - [x] Fix `mail_service.py` null bytes (Done)
        - [x] Fix `main.py` duplicate DB init
        - [x] Component Folder Re-org (`mail`, `layout`, etc.)
        - [x] Add `doc/pwa.md`
        - [x] **Refinement**
            - [x] Dashboard Layout Responsive Fixes
            - [x] ReaderPane Sanitization & Skeleton
            - [x] PWA Docs Update
            - [x] API Client Usage
    - [ ] **7.2 LocalDrop Security** <!-- id: 7.2 -->
        - [ ] Pairing / Encryption
    - [ ] **7.3 Sidecar Bundling** <!-- id: 7.3 -->

