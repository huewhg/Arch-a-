from fastapi import Form, FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import json
import os
import subprocess

app = FastAPI()

# Load the public key
with open("public_key.pem", "rb") as file:
    public_key = serialization.load_pem_public_key(file.read())

# Security scheme for HTTP bearer tokens
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify custom token."""
    try:
        token_parts = credentials.credentials.split('.')
        if len(token_parts) != 2:
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        encoded_payload, encoded_signature = token_parts
        
        payload_json = base64.urlsafe_b64decode(encoded_payload.encode('utf-8'))
        signature = base64.urlsafe_b64decode(encoded_signature.encode('utf-8'))

        # Verify signature
        public_key.verify(
            signature,
            payload_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        payload = json.loads(payload_json.decode('utf-8'))
        return payload

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.get("/")
async def read_root():
    return "{data:'online'}"

@app.get("/regen-keys/")
def regen_keys(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    """Regenerate keys."""
    try:
        # Replace 'script.py' with the path to your actual script
        result = subprocess.run(["python", "make-key.py"], capture_output=True, text=True, check=True)
        return {"output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Script failed with error: {e.stderr}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
