from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class ListingDetails(BaseModel):
    permit_no: Optional[str] = Field(default=None, description="RERA permit or equivalent")
    community: Optional[str] = None
    building: Optional[str] = None
    sq_ft: Optional[float] = None

class Listing(BaseModel):
    listing_id: str
    details: ListingDetails
    images: List[str] = Field(default_factory=list)
    has_360_tour: bool = False
    dld_verified: bool = False
    title_deed_verified: bool = False
    form_a_attached: bool = False
    form_b_attached: bool = False
    last_response_minutes: Optional[int] = None
    last_update_days: Optional[int] = None
    paid_boost: float = 0.0
    base_score: float = 0.0

class SessionLog(BaseModel):
    ts: str
    action: str

class Session(BaseModel):
    session_id: str
    logs: List[SessionLog] = Field(default_factory=list)

IntentTier = Literal["BROWSER", "ACTIVE", "HIGH_INTENT_BUYER", "HIGH_INTENT_RENTER"]

class IntentResult(BaseModel):
    intent: IntentTier
    score: float

class FingerprintResult(BaseModel):
    fingerprint: str
    basis: str

class QualityScoreResult(BaseModel):
    quality_score: float
    components: dict

class RankingScoreResult(BaseModel):
    final_score: float
    components: dict
