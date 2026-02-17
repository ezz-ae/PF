from __future__ import annotations

from .schemas import Listing, RankingScoreResult
from .integrity import calculate_quality_score


def integrity_gated_rank(listing: Listing, integrity_floor: float = 0.70) -> RankingScoreResult:
    q = calculate_quality_score(listing)
    base = float(listing.base_score)
    boost = float(listing.paid_boost)

    multiplier = 1.15 if (listing.dld_verified or listing.title_deed_verified) else 1.0
    effective_boost = boost if q.quality_score >= integrity_floor else (boost * 0.20)
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
        },
    )
