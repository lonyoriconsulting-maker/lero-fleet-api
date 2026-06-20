from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_TOKENS = {
    "LERO_MANAGER_SECRET_2026": "manager",
    "LERO_DRIVER_SECRET_2026": "driver"
}

def get_current_user_role(header_value: str = Security(api_key_header)):
    if header_value in VALID_TOKENS:
        return VALID_TOKENS[header_value]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized: Invalid or missing LERO Security API Key"
    )

