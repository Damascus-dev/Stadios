"""StadiumOS AI — Authentication Service

Mock OTP authentication with JWT-based session management.
Designed for modular replacement by Twilio/Firebase/Auth0.
"""

from __future__ import annotations

import os
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

# ── Configuration ────────────────────────────────────────────────────
JWT_SECRET = os.environ.get("JWT_SECRET", "stadiumos-dev-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

DEMO_OTP = "123456"
OTP_EXPIRY_SECONDS = 300  # 5 minutes

# ── User Database (in-memory mock) ───────────────────────────────────
USERS: dict[str, dict[str, Any]] = {
    "fan@example.com": {
        "user_id": "user-fan-001",
        "name": "Alex Fan",
        "role": "fan",
        "phone": "+1-555-0100",
    },
    "volunteer@example.com": {
        "user_id": "user-vol-001",
        "name": "Jordan Volunteer",
        "role": "volunteer",
        "phone": "+1-555-0101",
    },
    "ops@example.com": {
        "user_id": "user-ops-001",
        "name": "Taylor Operations",
        "role": "operations",
        "phone": "+1-555-0102",
    },
}

# ── OTP Store (in-memory) ────────────────────────────────────────────
_otp_store: dict[str, dict[str, Any]] = {}


def _generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"


def request_otp(identifier: str) -> dict[str, Any]:
    """Generate and store a 6-digit OTP for the given identifier (email/phone).

    In demo mode, returns the fixed OTP 123456 for any registered user.
    In production, this would send via SMS/email.
    """
    user = USERS.get(identifier)
    if user is None:
        # Allow OTP for unrecognized emails to not leak which users exist
        user = {"user_id": f"user-{identifier.split('@')[0]}", "name": identifier, "role": "fan", "phone": identifier}

    otp = DEMO_OTP if os.environ.get("DEMO_MODE", "true").lower() == "true" else _generate_otp()

    _otp_store[identifier] = {
        "otp": otp,
        "user_id": user["user_id"],
        "name": user["name"],
        "role": user["role"],
        "expires_at": time.time() + OTP_EXPIRY_SECONDS,
    }

    # Log the OTP (in production this would send SMS/email)
    print(f"[AUTH] OTP for {identifier}: {otp} (expires in {OTP_EXPIRY_SECONDS}s)")

    return {
        "message": "OTP sent successfully",
        "identifier": identifier,
        "expires_in_seconds": OTP_EXPIRY_SECONDS,
    }


def verify_otp(identifier: str, otp: str) -> dict[str, Any] | None:
    """Verify an OTP and return user session data + JWT on success."""
    stored = _otp_store.get(identifier)
    if stored is None:
        return None

    if time.time() > stored["expires_at"]:
        _otp_store.pop(identifier, None)
        return None

    if stored["otp"] != otp:
        return None

    # OTP valid — generate JWT
    _otp_store.pop(identifier, None)

    user_id = stored["user_id"]
    role = stored["role"]
    name = stored["name"]

    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": user_id,
        "role": role,
        "name": name,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRY_HOURS),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "token": token,
        "user_id": user_id,
        "name": name,
        "role": role,
        "expires_at": (now + timedelta(hours=JWT_EXPIRY_HOURS)).isoformat(),
    }


def verify_token(token: str) -> dict[str, Any] | None:
    """Validate a JWT and return the decoded payload."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_profile(user_id: str) -> dict[str, Any] | None:
    """Return user profile by user_id."""
    for u in USERS.values():
        if u["user_id"] == user_id:
            return u
    return None
