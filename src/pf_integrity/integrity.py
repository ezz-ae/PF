from __future__ import annotations
import hashlib
from typing import Dict, Optional
from .schemas import Listing, FingerprintResult, QualityScoreResult


def _norm(s: Optional[str]) -> str:
    return (s or "").strip().lower()


def generate_listing_fingerprint(listing: Listing) -> FingerprintResult:
    """Detect duplicates across brokers using UAE-stable identifiers."""

    permit = _norm(listing.details.permit_no)
    community = _norm(listing.details.community)
    building = _norm(listing.details.building)
    sqft = listing.details.sq_ft or 0.0

    if permit:
        basis = f"permit_no:{permit}"
        raw = permit
    else:
        basis = "fallback:community_building_sqft"
        raw = f"{community}|{building}|{sqft:.0f}"

    fp = hashlib.md5(raw.encode("utf-8")).hexdigest()
    return FingerprintResult(fingerprint=fp, basis=basis)


def calculate_quality_score(listing: Listing) -> QualityScoreResult:
    """Evaluate listing truthfulness before ranking."""

    components: Dict[str, float] = {}

    verified = 0.0
    if listing.dld_verified:
        verified += 0.45
    if listing.title_deed_verified:
        verified += 0.2
    components["verification"] = min(verified, 0.6)

    compliance = 0.0
    if listing.form_a_attached:
        compliance += 0.08
    if listing.form_b_attached:
        compliance += 0.06
    components["compliance_docs"] = min(compliance, 0.14)

    media = 0.0
    if listing.has_360_tour:
        media += 0.1
    if len(listing.images) >= 10:
        media += 0.1
    elif len(listing.images) >= 5:
        media += 0.06
    components["media"] = min(media, 0.2)

    freshness = 0.0
    if listing.last_response_minutes is not None:
        freshness += 0.06 if listing.last_response_minutes <= 5 else (0.03 if listing.last_response_minutes <= 30 else 0.0)
    if listing.last_update_days is not None:
        freshness += 0.05 if listing.last_update_days <= 3 else (0.02 if listing.last_update_days <= 14 else 0.0)
    components["freshness_responsiveness"] = min(freshness, 0.12)

    score = sum(components.values())
    return QualityScoreResult(quality_score=min(score, 1.0), components=components)
