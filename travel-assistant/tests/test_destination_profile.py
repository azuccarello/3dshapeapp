from src.recommendations.destination_profile import load_destination_profile


def test_load_waikiki_profile():
    profile = load_destination_profile("waikiki")
    assert profile is not None
    assert profile.code == "waikiki"
    assert any("Knots" in c.name for c in profile.coffee)
    assert any("Da Cove" in f.name for f in profile.food)
    assert len(profile.bars) >= 1
    assert len(profile.activities) >= 1
    assert len(profile.free) >= 1


def test_load_unknown_destination_returns_none():
    assert load_destination_profile("nowhere") is None


def test_diamond_head_has_book_ahead_note():
    profile = load_destination_profile("waikiki")
    diamond_head = next(p for p in profile.activities if "Diamond Head" in p.name)
    assert diamond_head.book_ahead is not None
    assert "30 days" in diamond_head.book_ahead
