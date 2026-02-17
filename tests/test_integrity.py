from pf_integrity.integrity import calculate_quality_score, generate_listing_fingerprint
from pf_integrity.schemas import Listing, ListingDetails


def test_fingerprint_prefers_permit():
    listing = Listing(
        listing_id="L1",
        details=ListingDetails(permit_no="12345", community="marina", building="tower", sq_ft=2000),
    )
    result = generate_listing_fingerprint(listing)
    assert result.basis.startswith("permit_no:")
    assert len(result.fingerprint) == 32


def test_fingerprint_falls_back_to_community():
    listing = Listing(
        listing_id="L2",
        details=ListingDetails(community="marina", building="tower", sq_ft=2000),
    )
    result = generate_listing_fingerprint(listing)
    assert result.basis == "fallback:community_building_sqft"


def test_quality_score_accumulates_components():
    listing = Listing(
        listing_id="L3",
        details=ListingDetails(permit_no="abc", community="core", building="alpha", sq_ft=1500),
        images=[str(i) for i in range(12)],
        has_360_tour=True,
        dld_verified=True,
        title_deed_verified=True,
        form_a_attached=True,
        form_b_attached=True,
        last_response_minutes=2,
        last_update_days=1,
    )
    score = calculate_quality_score(listing)
    assert score.quality_score >= 0.75
    assert "media" in score.components
