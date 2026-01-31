from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# --- Auth ---
class LoginRequest(BaseModel):
    email: str = "user@example.com"
    password: str
    imap_server: str = "imap.gmail.com"
    smtp_server: str = "smtp.gmail.com"

class LoginResponse(BaseModel):
    token: str
    email: str

# --- Mail ---
class InboxPreview(BaseModel):
    id: str  # UID
    from_addr: str
    subject: str
    snippet: str
    date: datetime
    is_read: bool

class EmailDetail(BaseModel):
    id: str
    from_addr: str
    to_addr: str
    subject: str
    date: datetime
    body_html: Optional[str] = None
    body_text: Optional[str] = None
    attachments: List[str] = [] # List of filenames

class EmailSendRequest(BaseModel):
    to: str
    subject: str
    body: str

# --- LocalDrop ---
class PeerInfo(BaseModel):
    id: str
    name: str
    ip: str
    status: str = "active"
