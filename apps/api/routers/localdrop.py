from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from services.localdrop_service import PEERS, file_manager
from services.crypto_service import crypto_service
from typing import List, Optional
from sqlmodel import Session, select
from database import get_session
from models import TrustedDevice
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/localdrop", tags=["localdrop"])

class PairingRequest(BaseModel):
    id: str
    name: str
    fingerprint: str
    public_key: str # Base64

@router.get("/peers")
def get_peers():
    return list(PEERS.values())

@router.get("/identity")
def get_identity():
    from services.localdrop_service import MY_ID
    # Ensure key is loaded
    if not crypto_service.identity_private_key:
        crypto_service.ensure_identity_key()
        
    return {
        "id": MY_ID,
        "name": MY_ID, # For now same as ID, or we can add a friendly name config
        "fingerprint": crypto_service.get_fingerprint(),
        "public_key": crypto_service.get_public_key_b64()
    }

@router.post("/pair/request")
async def request_pair(req: PairingRequest):
    # Determine if we should auto-approve or queue for manual approval
    # For MVP, we just broadcast this to the UI via WebSocket or just returning status
    # But ideally, we trigger a UI modal.
    # We will use the WebSocket broadcast in file_manager to alert the frontend.
    await file_manager.broadcast_pairing_request(req.id, req.name, req.fingerprint)
    return {"status": "REQUEST_SENT"}

@router.post("/pair/approve")
def approve_pair(req: PairingRequest, session: Session = Depends(get_session)):
    # Check if exists
    device = session.get(TrustedDevice, req.id)
    if not device:
        device = TrustedDevice(
            id=req.id,
            name=req.name,
            fingerprint=req.fingerprint,
            public_key=req.public_key,
            paired_at=datetime.utcnow()
        )
        session.add(device)
    else:
        # Update existing
        device.name = req.name
        device.fingerprint = req.fingerprint
        device.public_key = req.public_key
        device.paired_at = datetime.utcnow()
        device.is_blocked = False
        session.add(device)
        
    session.commit()
    return {"status": "APPROVED"}

class TransferAction(BaseModel):
    transfer_id: str

@router.post("/transfer/approve")
async def approve_transfer_endpoint(req: TransferAction):
    success = await file_manager.approve_transfer(req.transfer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return {"status": "APPROVED"}

@router.post("/transfer/reject")
async def reject_transfer_endpoint(req: TransferAction):
    success = await file_manager.reject_transfer(req.transfer_id)
    return {"status": "REJECTED"}

@router.get("/trusted")
def get_trusted(session: Session = Depends(get_session)):
    return session.exec(select(TrustedDevice)).all()

@router.websocket("/ui-ws")
async def ui_websocket_endpoint(websocket: WebSocket):
    await file_manager.connect_ui(websocket)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await file_manager.handle_transfer(websocket)
