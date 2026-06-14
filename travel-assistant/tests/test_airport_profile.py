from src.recommendations.airport_profile import load_airport_profile


def test_load_lax_profile():
    profile = load_airport_profile("LAX")
    assert profile is not None
    assert profile.code == "LAX"
    assert profile.transfer_minutes == 15
    assert any("Klatch" in c.name for c in profile.coffee)
    assert any("Ashland Hill" in f.name for f in profile.food)
    assert len(profile.activities) >= 1


def test_load_unknown_airport_returns_none():
    assert load_airport_profile("ZZZ") is None
