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
