import os
import socket
import hashlib
import json
import base64
import uuid
from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser
from fastapi import WebSocket
from typing import List, Dict, Optional
from services.crypto_service import crypto_service
from sqlmodel import Session, select
from database import engine
from models import TrustedDevice

# State
PEERS: Dict[str, dict] = {}
MY_ID = socket.gethostname()
RECEIVED_DIR = "localdrop_received"

if not os.path.exists(RECEIVED_DIR):
    os.makedirs(RECEIVED_DIR)

class LocalDropListener:
    def update_service(self, zeroconf, type, name):
        pass

    def remove_service(self, zeroconf, type, name):
        if name in PEERS:
            del PEERS[name]

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
            PEERS[name] = {
                "id": name,
                "ip": addresses[0] if addresses else "unknown",
                "port": info.port,
                "server": info.server
            }

zeroconf = Zeroconf()
listener = LocalDropListener()
browser = ServiceBrowser(zeroconf, "_localdrop._tcp.local.", listener)

def announce_self(port: int):
    # Announce service
    try:
        ip = socket.gethostbyname(socket.gethostname())
        info = ServiceInfo(
            "_localdrop._tcp.local.",
            f"{MY_ID}._localdrop._tcp.local.",
            addresses=[socket.inet_aton(ip)],
            port=port,
            server=f"{MY_ID}.local.",
        )
        zeroconf.register_service(info)
        print(f"Announced LocalDrop service as {MY_ID} on {ip}:{port}")
    except Exception as e:
        print(f"Failed to announce service: {e}")

# File Manager
class FileManager:
    def __init__(self):
        # active_uploads: {ws: {filepath, filename, size, received, session_key, file_hash, current_hasher, status, transfer_id, file_handle?}}
        self.active_uploads = {} 
        self.ui_connections: List[WebSocket] = []

    async def connect_ui(self, websocket: WebSocket):
        await websocket.accept()
        self.ui_connections.append(websocket)
        try:
            while True:
                await websocket.receive_text() # Keep alive / commands from UI
        except:
            if websocket in self.ui_connections:
                self.ui_connections.remove(websocket)

    async def broadcast_pairing_request(self, id: str, name: str, fingerprint: str):
        payload = {
            "type": "PAIRING_REQUEST",
            "peer": {"id": id, "name": name, "fingerprint": fingerprint}
        }
        await self.broadcast_to_ui(payload)

    async def broadcast_file_offer(self, transfer_id: str, sender_id: str, filename: str, size: int, file_hash: str, sender_fingerprint: str = None):
        payload = {
            "type": "FILE_OFFER",
            "offer": {
                "transfer_id": transfer_id,
                "sender_id": sender_id,
                "filename": filename,
                "size": size,
                "file_hash": file_hash,
                "sender_fingerprint": sender_fingerprint
            }
        }
        await self.broadcast_to_ui(payload)

    async def broadcast_to_ui(self, payload: dict):
        to_remove = []
        for ws in self.ui_connections:
            try:
                await ws.send_json(payload)
            except:
                to_remove.append(ws)
        for ws in to_remove:
            if ws in self.ui_connections:
                self.ui_connections.remove(ws)

    async def approve_transfer(self, transfer_id: str):
        target_ws = None
        for ws, upload in self.active_uploads.items():
            if upload.get("transfer_id") == transfer_id and upload.get("status") == "PENDING_APPROVAL":
                target_ws = ws
                break
        
        if target_ws:
            upload = self.active_uploads[target_ws]
            try:
                # Open File Handle Now
                upload["file_handle"] = open(upload["filepath"], "wb")
                upload["status"] = "APPROVED"
                # Init Hasher
                upload["current_hasher"] = hashlib.sha256()
                
                await target_ws.send_json({"status": "READY", "file": upload["filename"]})
                return True
            except Exception as e:
                print(f"Failed to open file: {e}")
                return False
        return False
        
    async def reject_transfer(self, transfer_id: str):
        target_ws = None
        for ws, upload in self.active_uploads.items():
            if upload.get("transfer_id") == transfer_id:
                target_ws = ws
                break
        
        if target_ws:
            await target_ws.send_json({"status": "ERROR", "message": "Transfer declined by user."})
            await target_ws.close()
            if target_ws in self.active_uploads:
                del self.active_uploads[target_ws]
            return True
        return False

    async def handle_transfer(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                message = await websocket.receive()
                if "text" in message:
                    await self.process_command(websocket, message["text"])
                elif "bytes" in message:
                    await self.process_chunk(websocket, message["bytes"])
        except Exception as e:
            print(f"WS Error: {e}")
        finally:
            self.cleanup(websocket)

    async def process_command(self, websocket: WebSocket, data: str):
        try:
            cmd = json.loads(data)
            type = cmd.get("type")
            
            if type == "FILE_META":
                sender_id = cmd.get("sender_id")
                ephemeral_pub = cmd.get("sender_ephemeral_pub") # B64
                file_hash = cmd.get("file_hash")
                
                # Trust Check
                is_trusted = False
                if sender_id:
                    with Session(engine) as session:
                        device = session.exec(select(TrustedDevice).where(TrustedDevice.id == sender_id)).first()
                        if device and not device.is_blocked:
                            is_trusted = True
                
                if not is_trusted:
                    print(f"Rejected transfer from unknown/blocked device: {sender_id}")
                    await websocket.send_json({"status": "ERROR", "message": "Device not paired or blocked."})
                    return

                if not ephemeral_pub:
                    await websocket.send_json({"status": "ERROR", "message": "Missing key material."})
                    return

                # Derive Session Key
                try:
                    session_key = crypto_service.derive_session_key(ephemeral_pub)
                except Exception as e:
                    print(f"Key Derivation Failed: {e}")
                    await websocket.send_json({"status": "ERROR", "message": "Key exchange failed."})
                    return

                filename = cmd["filename"]
                safe_filename = os.path.basename(filename) 
                filepath = os.path.join(RECEIVED_DIR, safe_filename)
                transfer_id = str(uuid.uuid4())
                
                # Store Metadata ONLY (Deferred Open)
                self.active_uploads[websocket] = {
                    "filepath": filepath,
                    "filename": safe_filename,
                    "size": cmd["size"],
                    "received": 0,
                    "session_key": session_key,
                    "file_hash": file_hash,
                    "sender_id": sender_id,
                    "status": "PENDING_APPROVAL",
                    "transfer_id": transfer_id,
                    "file_handle": None,
                    "current_hasher": None
                }
                
                sender_fingerprint = device.fingerprint if device else "UNKNOWN"

                # Notify UI to Ask for Approval
                await self.broadcast_file_offer(transfer_id, sender_id, safe_filename, cmd["size"], file_hash, sender_fingerprint)
                print(f"Waiting for approval for {safe_filename} from {sender_id}...")

            elif type == "FILE_DONE":
                upload = self.active_uploads.get(websocket)
                if upload and upload.get("status") == "APPROVED":
                    if upload["file_handle"]:
                        upload["file_handle"].close()
                    
                    # Verify Hash
                    calculated_hash = upload["current_hasher"].hexdigest()
                    expected_hash = upload["file_hash"]
                    
                    if calculated_hash != expected_hash:
                        print(f"Hash Mismatch! Expected {expected_hash}, got {calculated_hash}")
                        # Security: Delete corrupt file
                        if os.path.exists(upload["filepath"]):
                            os.remove(upload["filepath"])
                        await websocket.send_json({"status": "ERROR", "message": "Integrity check failed."})
                    else:
                        print(f"Finished receiving {upload['filename']} (Hash Verified)")
                        await websocket.send_json({"status": "SUCCESS", "file": upload["filename"]})
                    
                    del self.active_uploads[websocket]

        except Exception as e:
            print(f"Cmd processing error: {e}")
            await websocket.send_json({"status": "ERROR", "message": str(e)})

    async def process_chunk(self, websocket: WebSocket, chunk: bytes):
        upload = self.active_uploads.get(websocket)
        if upload and upload.get("status") == "APPROVED":
            try:
                # Decrypt (split IV handles inside decrypt_chunk)
                decrypted_data = crypto_service.decrypt_chunk(chunk, upload["session_key"])
                
                # Write
                upload["file_handle"].write(decrypted_data)
                upload["received"] += len(decrypted_data) # Note: this is encrypted size approx + overhead? Or we want plaintext size? Usually progress tracks bytes over wire.
                
                # Update Hash
                upload["current_hasher"].update(decrypted_data)
                
            except Exception as e:
                print(f"Decryption failed: {e}")
                # Potentially abort transfer here
                await websocket.send_json({"status": "ERROR", "message": "Decryption error."})
                await websocket.close()
        else:
            # Drop chunk if not approved
            pass

    def cleanup(self, websocket: WebSocket):
        upload = self.active_uploads.get(websocket)
        if upload:
            if upload.get("file_handle"):
                upload["file_handle"].close()
            # If incomplete, maybe delete file? For now keep partial or standard temp behavior.
            del self.active_uploads[websocket]

file_manager = FileManager()
