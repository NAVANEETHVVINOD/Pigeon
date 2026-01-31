from email.header import decode_header

def get_email_content(email_id: str, creds: dict):
    # Connect to IMAP
    with IMAPClient(creds["imap_server"]) as client:
        client.login(creds["email"], creds["password"])
        client.select_folder("INBOX")
        
        # Fetch body
        response = client.fetch([int(email_id)], ['BODY.PEEK[]'])
        raw_email = response[int(email_id)][b'BODY[]']
        msg = email.message_from_bytes(raw_email)
        
        subject, encoding = decode_header(msg["Subject"])[0]
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
