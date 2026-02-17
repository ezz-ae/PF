from __future__ import annotations

from .schemas import Session, IntentResult

HIGH_INTENT_ACTIONS = {
    "view_price_map",
    "view_lifestyle_insights",
    "calculate_rent_vs_buy",
    "mortgage_prequal",
    "whatsapp_click",
    "call_click",
    "request_viewing",
}

RENT_SIGNALS = {"view_rent_estimate", "rent_filter", "short_term_filter"}


def classify_user_intent(session: Session) -> IntentResult:
    hits = 0
    rent_hits = 0
    for log in session.logs:
        action = (log.action or "").strip().lower()
        if action in HIGH_INTENT_ACTIONS:
            hits += 1
        if action in RENT_SIGNALS:
            rent_hits += 1

    score = min(1.0, hits / 3.0)
    if hits >= 2:
        intent = "HIGH_INTENT_RENTER" if rent_hits >= 1 else "HIGH_INTENT_BUYER"
    elif hits == 1:
        intent = "ACTIVE"
    else:
        intent = "BROWSER"

    return IntentResult(intent=intent, score=score)
