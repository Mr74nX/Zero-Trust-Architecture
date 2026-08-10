import datetime
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Zero Trust Access Control Gate")

USERS_DB = {
    "tan_dev": {
        "role": "admin",
        "allowed_devices": ["SECURE_LAPTOP_01"],
        "token": "secret-token-tan-123"
    },
    "user_guest": {
        "role": "guest",
        "allowed_devices": ["GUEST_MOBILE_02"],
        "token": "secret-token-guest-456"
    }
}

class AccessRequest(BaseModel):
    username: str
    device_id: str
    is_device_encrypted: bool
    requested_resource: str

def verify_zero_trust_policy(req: AccessRequest, auth_token: str):
    user = USERS_DB.get(req.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Zero Trust Decision: Unknown Identity")

    if auth_token != user["token"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Zero Trust Decision: Invalid Credentials")

    if req.device_id not in user["allowed_devices"] or not req.is_device_encrypted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Zero Trust Decision: Device untrusted or health check failed"
        )

    if req.requested_resource == "production_db" and user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Zero Trust Decision: Access denied. Insufficient privileges"
        )

    return True

@app.post("/api/v1/secure-access")
def access_resource(request_data: AccessRequest, authorization: str = Header(...)):
    
    verify_zero_trust_policy(request_data, authorization)
    
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] [AUDIT LOG] Access GRANTED to '{request_data.username}' for '{request_data.requested_resource}'")

    return {
        "status": "ACCESS_GRANTED",
        "timestamp": timestamp,
        "message": f"Welcome {request_data.username}. Temporary JIT access granted to {request_data.requested_resource}."
    }
