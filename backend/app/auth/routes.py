"""StadiumOS AI — Authentication Routes

POST /api/auth/request-otp  — Request a 6-digit OTP for the given identifier
POST /api/auth/verify-otp   — Verify OTP and receive a JWT
GET  /api/auth/me           — Return current user profile (requires auth)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from .middleware import get_current_user, require_auth
from .service import get_user_profile, request_otp, verify_otp

router = APIRouter()


# ── Request Schemas ──────────────────────────────────────────────────

class OTPRequest(BaseModel):
    identifier: str = Field(
        ..., description="Email or phone number to send OTP to",
        examples=["fan@example.com"],
    )


class OTPVerify(BaseModel):
    identifier: str = Field(..., examples=["fan@example.com"])
    otp: str = Field(..., min_length=6, max_length=6, examples=["123456"])


# ── Response Schemas ─────────────────────────────────────────────────

class OTPResponse(BaseModel):
    message: str
    identifier: str
    expires_in_seconds: int


class TokenResponse(BaseModel):
    token: str
    user_id: str
    name: str
    role: str
    expires_at: str


class UserProfile(BaseModel):
    user_id: str
    name: str
    role: str
    phone: str | None = None


# ── Routes ───────────────────────────────────────────────────────────

@router.post("/request-otp", response_model=OTPResponse)
async def request_otp_endpoint(body: OTPRequest):
    """Request a 6-digit OTP. In demo mode, always returns 123456."""
    return request_otp(body.identifier)


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp_endpoint(body: OTPVerify):
    """Verify OTP and receive a JWT token for authenticated requests."""
    result = verify_otp(body.identifier, body.otp)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP",
        )
    return TokenResponse(**result)


@router.get("/me", response_model=UserProfile)
async def get_me(payload: dict = Depends(require_auth)):
    """Return the current user's profile. Requires a valid JWT."""
    user = get_user_profile(payload.get("sub", ""))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)
