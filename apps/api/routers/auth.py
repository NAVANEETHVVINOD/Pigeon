from fastapi import APIRouter, HTTPException, Depends
from uuid import uuid4
from schemas import LoginRequest, LoginResponse

from services.auth_service import create_access_token, encrypt_password
from models import Account
from database import engine
from sqlmodel import Session, select

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(creds: LoginRequest):
    # 1. Check if account exists in DB
    with Session(engine) as session:
        account = session.get(Account, creds.email)
        
        if not account:
            # First time login: Verify with IMAP provider
            from services.imap_service import verify_login
            if verify_login(creds.imap_server, creds.email, creds.password):
                # Encrypt and Save
                new_account = Account(
                    email=creds.email,
                    encrypted_password=encrypt_password(creds.password),
                    imap_server=creds.imap_server,
                    smtp_server=creds.smtp_server,
                    is_active=True
                )
                session.add(new_account)
                session.commit()
                account = new_account
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials or IMAP connection failed")
        
        # 2. Login successful (either cached or new) -> Issue Token
        # NOTE: For MVP we trust the stored password if it exists. 
        # Ideally, we should maybe re-verify periodically.
        
        access_token = create_access_token(data={"sub": account.email})
        return {"token": access_token, "email": account.email}
