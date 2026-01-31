from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Account(SQLModel, table=True):
    email: str = Field(primary_key=True)
    encrypted_password: str
    imap_server: str
    smtp_server: str
    is_active: bool = True

class Email(SQLModel, table=True):
    id: str = Field(primary_key=True)  # Using Message-ID or IMAP UID as string
    subject: str = Field(index=True)
    from_addr: str = Field(index=True)
    to_addr: str
    date: datetime = Field(index=True)
    snippet: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    folder: str = "INBOX"
    is_read: bool = False

class Attachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email_id: str = Field(foreign_key="email.id")
    filename: str
    content_type: str
    file_path: str
    size: int
    is_image: bool = False

class LocalDropPeer(SQLModel, table=True):
    id: str = Field(primary_key=True) # Unique Device ID
    name: str 
    ip: str
    port: int
    last_seen: datetime

class TrustedDevice(SQLModel, table=True):
    id: str = Field(primary_key=True) # Device ID
    name: str
    fingerprint: Optional[str] = None # SHA256(public_key)
    public_key: Optional[str] = None # Base64 encoded X25519 public key
    paired_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_blocked: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
