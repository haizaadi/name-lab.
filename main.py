from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import re

app = FastAPI(title="NAME LAB API", version="2.0.0",
              description="Username format validation API. Does not query platform availability.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your exact GitHub Pages origin.
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

PATTERNS = {
    "discord": re.compile(r"^[a-z0-9._]{2,32}$"),
    "tiktok": re.compile(r"^[A-Za-z0-9._]{2,24}$"),
    "generic": re.compile(r"^[A-Za-z0-9._-]{2,32}$"),
}

class ValidateRequest(BaseModel):
    platform: Literal["discord", "tiktok", "generic"] = "generic"
    usernames: list[str] = Field(min_length=1, max_length=500)

@app.get("/")
def root():
    return {"app": "NAME LAB API", "version": "2.0.0", "status": "online",
            "endpoints": ["/health", "/validate"]}

@app.get("/health")
def health():
    return {"status": "ok", "service": "name-lab-api"}

@app.post("/validate")
def validate(payload: ValidateRequest):
    pattern = PATTERNS[payload.platform]
    output = []
    for raw in payload.usernames:
        username = raw.strip()
        is_valid = bool(pattern.fullmatch(username))
        output.append({
            "username": username,
            "format": "VALID" if is_valid else "INVALID",
            "availability": "UNKNOWN"
        })
    return {"platform": payload.platform, "count": len(output), "results": output}
