"""
PRISM Backend — Waitlist Service
Handles waitlist email capture for the PRISM landing page.
This service is built to grow into the full PRISM backend later.
"""

import os
import re
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client

# ===== Config =====
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY environment variables."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ===== App =====
app = FastAPI(title="PRISM Backend", version="0.1.0")

# CORS — allow the landing page (and later the full app) to call this API.
# Update allow_origins with your real Vercel domain(s) once known.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app",
        "https://prism-waitlist.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ===== Models =====
class WaitlistRequest(BaseModel):
    email: EmailStr
    source: str = "landing_page"


class WaitlistResponse(BaseModel):
    success: bool
    message: str


# ===== Routes =====
@app.get("/")
def root():
    return {"service": "PRISM Backend", "status": "online"}


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/waitlist", response_model=WaitlistResponse)
def join_waitlist(payload: WaitlistRequest):
    email = payload.email.lower().strip()

    # Check if email already exists
    existing = (
        supabase.table("waitlist")
        .select("id")
        .eq("email", email)
        .execute()
    )

    if existing.data and len(existing.data) > 0:
        # Already on the list — don't error, just confirm gracefully
        return WaitlistResponse(
            success=True,
            message="You're already on the waitlist!"
        )

    # Insert new entry
    try:
        supabase.table("waitlist").insert(
            {"email": email, "source": payload.source}
        ).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to join waitlist: {str(e)}")

    return WaitlistResponse(
        success=True,
        message="You're on the list. We'll be in touch soon."
    )


@app.get("/waitlist/count")
def waitlist_count():
    """Public endpoint to show live waitlist count on the landing page."""
    result = supabase.table("waitlist").select("id", count="exact").execute()
    return {"count": result.count if result.count is not None else 0}
