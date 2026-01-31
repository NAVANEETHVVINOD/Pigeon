from imapclient import IMAPClient
from ..models import Email
from datetime import datetime

def verify_login(server, user, password):
    try:
        with IMAPClient(server) as client:
            client.login(user, password)
            return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def fetch_recent_emails(creds, limit=20):
    # creds is dict: {imap_server, email, password, ...}
    with IMAPClient(creds['imap_server']) as client:
        client.login(creds['email'], creds['password'])
        client.select_folder('INBOX', readonly=True)
        
        messages = client.search('ALL')
        # Get last 'limit' messages
        recent_ids = messages[-limit:]
        
        response = client.fetch(recent_ids, ['ENVELOPE', 'BODY[TEXT]', 'BODY[HEADER.FIELDS (DATE)]', 'INTERNALDATE'])
        
        emails = []
        for msg_id, data in response.items():
            envelope = data[b'ENVELOPE']
            # Parse envelope to Email model
            # Note: envelope.date is datetime
            # envelope.from_ is tuple
            
            from_str = str(envelope.from_[0]) if envelope.from_ else "Unknown"
            subject = envelope.subject.decode() if envelope.subject else "(No Subject)"
            
            email = Email(
                id=str(msg_id),
                subject=subject,
                from_addr=from_str,
                to_addr="Me", # Simplified
                date=envelope.date or data.get(b'INTERNALDATE'),
                snippet="Snippet TODO", # Fetch body snippet
                is_read=True
            )
            emails.append(email)
            
        return sorted(emails, key=lambda x: x.date, reverse=True)
