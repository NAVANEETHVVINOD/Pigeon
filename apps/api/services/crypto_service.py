import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

IDENTITY_KEY_PATH = "localdrop_identity.pem"

class CryptoService:
    def __init__(self):
        self.identity_private_key = None
        self.ensure_identity_key()

    def ensure_identity_key(self):
        """Load or generate the static X25519 identity key for this device."""
        if os.path.exists(IDENTITY_KEY_PATH):
            try:
                with open(IDENTITY_KEY_PATH, "rb") as f:
                    self.identity_private_key = serialization.load_pem_private_key(
                        f.read(), password=None
                    )
            except Exception as e:
                print(f"Failed to load identity key: {e}. Regenerating.")
        
        if not self.identity_private_key:
            self.identity_private_key = x25519.X25519PrivateKey.generate()
            with open(IDENTITY_KEY_PATH, "wb") as f:
                f.write(self.identity_private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
    
    def get_public_key_b64(self) -> str:
        """Return base64 encoded public key."""
        public_key = self.identity_private_key.public_key()
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.b64encode(pub_bytes).decode('utf-8')

    def get_fingerprint(self) -> str:
        """Return SHA256 fingerprint of the public key."""
        public_key = self.identity_private_key.public_key()
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        digest = hashes.Hash(hashes.SHA256())
        digest.update(pub_bytes)
        return digest.finalize().hex()

    def derive_session_key(self, peer_public_key_b64: str) -> bytes:
        """
        Derive a shared AES-GCM session key using HKDF.
        Input: My Private Key + Peer Public Key (Ephemeral or Static).
        """
        peer_pub_bytes = base64.b64decode(peer_public_key_b64)
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_pub_bytes)
        
        shared_secret = self.identity_private_key.exchange(peer_public_key)
        
        # Derive AES key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'localdrop-v1',
        ).derive(shared_secret)
        
        return derived_key

    @staticmethod
    def decrypt_chunk(encrypted_packet: bytes, key: bytes) -> bytes:
        """
        Decrypt a chunk.
        Packet Format: [Nonce (12 bytes)] [Ciphertext + Tag]
        """
        if len(encrypted_packet) < 28: # 12 (nonce) + 16 (tag)
            raise ValueError("Packet too short")
            
        nonce = encrypted_packet[:12]
        ciphertext_and_tag = encrypted_packet[12:]
        
        aesgcm = AESGCM(key)
        # AESGCM.decrypt takes (nonce, data, associated_data) where data is ciphertext + tag
        return aesgcm.decrypt(nonce, ciphertext_and_tag, None)

crypto_service = CryptoService()
