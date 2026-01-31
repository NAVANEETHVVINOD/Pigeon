# OpenMail Hub - Hackathon Submission

**Pegion (OpenMail Hub)** is a next-generation mail client that reimagines email as a real-time, multimedia-first hub. 

## 🚀 Unique Features (MVP)
1.  **LocalDrop**: Seamless, serverless file sharing between devices on the same network using Zeroconf/WebSockets. No more emailing files to yourself!
2.  **MediaVault**: Automatically aggregates all images from your inbox into a beautiful, Instagram-like gallery.
3.  **Superhuman-Inspired UI**: Minimalist, high-performance interface built with shadcn/ui and Tailwind CSS.
4.  **Full Email Client**: Reads IMAP (with sanitized HTML rendering) and sends SMTP emails.

## 🛠️ Tech Stack
-   **Frontend**: Next.js 14, Tailwind CSS, Shadcn UI, Sonner (Toasts)
-   **Backend**: Python FastAPI, SQLModel (SQLite), IMAPClient, Zeroconf
-   **Architecture**: Monorepo with completely decoupled Frontend/Backend.

## 📦 Setup & Demo Instructions

### Prerequisites
- Node.js 18+
- Python 3.10+

### Step 1: Backend
```bash
cd apps/api
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Step 2: Frontend
```bash
cd apps/web
npm install
npm run dev
# Open http://localhost:3000
```

### Step 3: Deployment
To build for production:
```bash
cd apps/web
npm run build
```

## 🔮 Future Roadmap (Post-Hackathon)
-   **AI Composer**: "Reply with AI" integration.
-   **Mobile App**: React Native port.
-   **Encryption**: End-to-end encrypted LocalDrop transfers.
