from imapclient import IMAPClient
from sqlmodel import Session, select
from datetime import datetime
from database import engine
from models import Email, Attachment
from schemas import InboxPreview
from models import Account
from services.auth_service import decrypt_password
import email
from email.header import decode_header
import os
import email.utils
from email.message import EmailMessage
import aiosmtplib

def decode_mime_header(header_value):
    if not header_value:
        return ""
    decoded_list = decode_header(header_value)
    text = ""
    for decoded, charset in decoded_list:
        if isinstance(decoded, bytes):
            if charset:
                try:
                    text += decoded.decode(charset)
                except LookupError:
                    text += decoded.decode('utf-8', errors='ignore')
            else:
                text += decoded.decode('utf-8', errors='ignore')
        else:
            text += str(decoded)
    return text

def sync_inbox(account: Account):
    """
    Syncs the last 20 emails from IMAP to SQLite.
    Returns the list of emails from DB.
    """
    pass # Managed by background worker

def get_inbox_from_db():
    with Session(engine) as session:
        statement = select(Email).order_by(Email.date.desc()).limit(50)
        results = session.exec(statement).all()
        return [
            InboxPreview(
                id=str(email.id),
                subject=email.subject or "(No Subject)",
                sender=email.sender,
                preview=email.preview,
                date=email.date.strftime("%Y-%m-%d %H:%M") if email.date else "",
                is_read=email.is_read
            )
            for email in results
        ]

def get_email_content(email_id: str, creds: dict):
    # Connect to IMAP
    with IMAPClient(creds["imap_server"]) as client:
        client.login(creds["email"], creds["password"])
        client.select_folder("INBOX")
        
        # Fetch body
        response = client.fetch([int(email_id)], ['BODY.PEEK[]'])
        raw_email = response[int(email_id)][b'BODY[]']
        msg = email.message_from_bytes(raw_email)
        
        subject_data = decode_header(msg["Subject"])[0]
        subject, encoding = subject_data
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
            
        from_ = msg.get("From")
        date_ = msg.get("Date")
        
        body_text = ""
        body_html = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" not in content_disposition:
                    try:
                        payload = part.get_payload(decode=True).decode()
                    except:
                        payload = part.get_payload()
                        
                    if content_type == "text/plain":
                        body_text += payload
                    elif content_type == "text/html":
                        body_html += payload
        else:
            try:
                payload = msg.get_payload(decode=True).decode()
            except:
                payload = msg.get_payload()
                
            if msg.get_content_type() == "text/html":
                body_html = payload
            else:
                body_text = payload
                
        return {
            "id": str(email_id),
            "subject": subject,
            "from": from_,
            "date": date_,
            "body_text": body_text,
            "body_html": body_html
        }

async def send_email_smtp(creds: dict, to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = creds["email"]
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=creds["smtp_server"],
        port=587,
        username=creds["email"],
        password=creds["password"],
        start_tls=True,
    )