from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import engine
from models import Attachment
from typing import List

router = APIRouter(prefix="/media", tags=["media"])

@router.get("/images")
def get_images():
    with Session(engine) as session:
        statement = select(Attachment).where(Attachment.is_image == True).order_by(Attachment.id.desc())
        results = session.exec(statement).all()
        return results
