from pf_integrity.ranking import integrity_gated_rank
from pf_integrity.schemas import Listing, ListingDetails


def test_boost_is_throttled_when_integrity_low():
    listing = Listing(
        listing_id="RL1",
        details=ListingDetails(community="x", building="y", sq_ft=1200),
        base_score=0.5,
        paid_boost=1.0,
    )
    result = integrity_gated_rank(listing, integrity_floor=0.9)
    assert result.components["paid_boost_effective"] == 0.2


def test_env_config_controls_thresholds(monkeypatch):
    monkeypatch.setenv("PF_INTEGRITY_FLOOR", "0.9")
    monkeypatch.setenv("PF_BOOST_SUPPRESSION", "0.1")
    listing = Listing(
        listing_id="RL2",
        details=ListingDetails(community="x", building="y", sq_ft=1200),
        base_score=0.5,
        paid_boost=1.0,
    )
    result = integrity_gated_rank(listing)
    assert result.components["integrity_floor"] == 0.9
    assert result.components["boost_suppression"] == 0.1
    assert result.components["paid_boost_effective"] == 0.1
