# LocalDrop Security Specification

## Overview
Phase 7.2 upgrades LocalDrop from an open P2P transfer system to a secure, trusted network inspired by AirDrop's security model.

## 1. Threat Model & Requirements
- **Unknown Peers**: Cannot transfer files without explicit approval.
- **Data Privacy**: All transfers must be encrypted in transit (AES-GCM).
- **Control**: Receiver must confirm every file transfer request.
- **Persistence**: Trusted devices are remembered to avoid re-pairing.

## 2. Architecture

### Backend (SQLModel + Crypto)
**TrustedDevice Model**
```python
class TrustedDevice(SQLModel, table=True):
    id: str = Field(primary_key=True) # Hardware UUID or generated ID
    name: str # Friendly name
    public_key: str # For future asymmetric handshake (RSA/ECC)
    fingerprint: str # Short hash for visual verification
    is_blocked: bool = False
    created_at: datetime
```

**CryptoService**
- `generate_key()`: Creates ephemeral AES-256 key for session.
- `encrypt_chunk(chunk, key)`: Encrypts file parts.
- `decrypt_chunk(chunk, key)`: Decrypts on receipt.

### API Flow (Pairing)
1. **Sender** -> `POST /localdrop/pair/request` (payload: `{ my_id, my_name, fingerprint }`)
2. **Receiver API** -> Triggers WebSocket event `PAIRING_REQUEST` -> Frontend shows Modal.
3. **Receiver User** -> Clicks [Approve].
4. **Receiver API** -> `POST /localdrop/pair/approve` -> Stores `TrustedDevice`.
5. **Receiver API** -> Sends WS `PAIRING_ACCEPTED` to both parties.

### API Flow (Transfer)
1. **Sender** -> WebSocket `FILE_OFFER` (payload: `{ filename, size, sender_id }`)
2. **Receiver** -> If sender trusted -> Show Accept Dialog. Else -> Block/Ignore.
3. **Receiver User** -> Clicks [Accept].
4. **Sender** -> Generates Key -> Sends `FILE_START` (with Key encrypted if we had RSA, for now share via secure channel or pre-shared trust - *Optimization: We will simulate key exchange or send key in pairing response for this phase*).
5. **Transfer** -> Encrypted Chunks -> Decrypt -> Write to Disk.

## 3. UI Components
- **PairingModal**: "Device X wants to connect. Fingerprint: ABCD."
- **IncomingFileDialog**: "Receive 'report.pdf' from 'Device X'?"
- **TrustedDevicesList**: Settings page to view/revoke trust.
