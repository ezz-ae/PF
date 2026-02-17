from __future__ import annotations

import os

from .schemas import Listing, RankingScoreResult
from .integrity import calculate_quality_score


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def integrity_gated_rank(
    listing: Listing,
    integrity_floor: float | None = None,
    boost_suppression: float | None = None,
) -> RankingScoreResult:
    q = calculate_quality_score(listing)
    base = float(listing.base_score)
    boost = float(listing.paid_boost)

    integrity_floor = integrity_floor if integrity_floor is not None else _env_float("PF_INTEGRITY_FLOOR", 0.70)
    boost_suppression = boost_suppression if boost_suppression is not None else _env_float("PF_BOOST_SUPPRESSION", 0.20)

    multiplier = 1.15 if (listing.dld_verified or listing.title_deed_verified) else 1.0
    effective_boost = boost if q.quality_score >= integrity_floor else (boost * boost_suppression)
    final = (base * multiplier) + effective_boost

    return RankingScoreResult(
        final_score=final,
        components={
            "base_score": base,
            "multiplier": multiplier,
            "paid_boost_raw": boost,
            "paid_boost_effective": effective_boost,
            "integrity_score": q.quality_score,
            "integrity_floor": integrity_floor,
            "boost_suppression": boost_suppression,
        },
    )
