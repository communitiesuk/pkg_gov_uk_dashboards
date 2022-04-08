from gov_uk_dashboards.formatting.rounding import round_thousands_to_1dp


def test_round_thousands_to_1dp_returns_rounded_billions():
    assert round_thousands_to_1dp(1_234_567_890) == 1_200_000_000
    assert round_thousands_to_1dp(45_678_987_654) == 45_700_000_000


def test_round_thousands_to_1dp_returns_rounded_millions():
    assert round_thousands_to_1dp(1_234_567) == 1_200_000
    assert round_thousands_to_1dp(45_678_987) == 45_700_000


def test_round_thousands_to_1dp_returns_rounded_thousands():
    assert round_thousands_to_1dp(1_234) == 1_200
    assert round_thousands_to_1dp(45_678) == 45_700


def test_round_thousands_to_1dp_returns_rounded_units():
    assert round_thousands_to_1dp(1.234) == 1.2
    assert round_thousands_to_1dp(45.678) == 45.7
