from __future__ import annotations

from fastapi import FastAPI

from .integrity import calculate_quality_score, generate_listing_fingerprint
from .intent import classify_user_intent
from .ranking import integrity_gated_rank
from .schemas import (
    FingerprintResult,
    IntentResult,
    Listing,
    QualityScoreResult,
    RankingScoreResult,
    Session,
)

app = FastAPI(title="PF Marketplace Integrity Engine", version="0.1.0")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/v1/integrity/fingerprint", response_model=FingerprintResult)
def fingerprint(listing: Listing):
    return generate_listing_fingerprint(listing)


@app.post("/v1/integrity/quality-score", response_model=QualityScoreResult)
def quality_score(listing: Listing):
    return calculate_quality_score(listing)


@app.post("/v1/intent/classify", response_model=IntentResult)
def classify_intent(session: Session):
    return classify_user_intent(session)


@app.post("/v1/ranking/score", response_model=RankingScoreResult)
def rank_score(listing: Listing):
    return integrity_gated_rank(listing)
