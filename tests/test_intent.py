from pf_integrity.intent import classify_user_intent
from pf_integrity.schemas import Session, SessionLog


def test_high_intent_buyer():
    session = Session(
        session_id="S1",
        logs=[
            SessionLog(ts="1", action="view_price_map"),
            SessionLog(ts="2", action="whatsapp_click"),
        ],
    )
    result = classify_user_intent(session)
    assert result.intent == "HIGH_INTENT_BUYER"


def test_browser_detected():
    session = Session(
        session_id="S2",
        logs=[SessionLog(ts="1", action="scroll")],
    )
    result = classify_user_intent(session)
    assert result.intent == "BROWSER"
