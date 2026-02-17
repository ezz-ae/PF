from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="PF Marketplace Integrity Engine", version="0.1.0")


@app.get("/health")
def health():
    return {"ok": True}
