from fastapi import Header, HTTPException
from services.auth_service import verify_token, decrypt_password
from models import Account
from database import engine
from sqlmodel import Session

async def get_current_user_creds(authorization: str = Header(...)):
    # 1. Validate Header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid header")
    token = authorization.split(" ")[1]
    
    # 2. Decode Token
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    # 3. Get Credentials from DB
    with Session(engine) as session:
        account = session.get(Account, token_data.email)
        if not account:
            raise HTTPException(status_code=401, detail="User not found")
            
        # 4. Decrypt and Return
        # We assume the user wants to perform an action, so we return the decrypted creds
        try:
            password = decrypt_password(account.encrypted_password)
        except Exception:
             raise HTTPException(status_code=500, detail="Could not decrypt credentials")
             
        return {
            "email": account.email,
            "password": password,
            "imap_server": account.imap_server,
            "smtp_server": account.smtp_server
        }
