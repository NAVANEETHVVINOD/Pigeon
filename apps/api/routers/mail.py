from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas import InboxPreview, EmailDetail, EmailSendRequest
from dependencies import get_current_user_creds
from services.mail_service import sync_inbox, get_inbox_from_db

router = APIRouter(prefix="/mail", tags=["mail"])

@router.get("/inbox", response_model=List[InboxPreview])
def get_inbox(creds: dict = Depends(get_current_user_creds)):
    """
    Fetches the last 20 emails from the IMAP server.
    Returns lightweight preview objects.
    """
    try:
        # Sync first (blocking for MVP, ideally background)
        # Sync is now handled by background worker
        # sync_inbox(creds)
        # Return from Cache
        # Return from Cache
        return get_inbox_from_db()
    except Exception as e:
        print(f"Sync Logic Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{email_id}", response_model=EmailDetail)
def get_email_body(email_id: str, creds: dict = Depends(get_current_user_creds)):
    # Placeholder for Step 3 (Reader)
    raise HTTPException(status_code=404, detail="Not implemented yet")

@router.get("/{email_id}")
def get_email_body(email_id: str, creds: dict = Depends(get_current_user_creds)):
    from services.mail_service import get_email_content
    try:
        return get_email_content(email_id, creds)
    except Exception as e:
        print(f"Fetch Content Error: {e}")
        raise HTTPException(status_code=404, detail="Email not found")

@router.post("/send")
async def send_email(email: EmailSendRequest, creds: dict = Depends(get_current_user_creds)):
    from services.mail_service import send_email_smtp
    result = await send_email_smtp(creds, email.to, email.subject, email.body)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"status": "sent"}
