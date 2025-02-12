from gov_uk_dashboards.formatting.human_readable import format_as_human_readable


def test_format_as_human_readable_returns_formatted_billions():
    assert format_as_human_readable(1_000_000_000) == "1bn"
    assert format_as_human_readable(2_100_000_000) == "2.1bn"
    assert format_as_human_readable(45_678_987_654, prefix="£") == "£45.679bn"


def test_format_as_human_readable_returns_formatted_millions():
    assert format_as_human_readable(1_000_000) == "1m"
    assert format_as_human_readable(999_100_000) == "999.1m"
    assert format_as_human_readable(45_678_987, prefix="$") == "$45.679m"


def test_format_as_human_readable_returns_formatted_thousands():
    assert format_as_human_readable(1_000) == "1k"
    assert format_as_human_readable(425_000) == "425k"
    assert format_as_human_readable(45_678, prefix="ABC") == "ABC45.678k"


def test_format_as_human_readable_returns_formatted_units():
    assert format_as_human_readable(1) == "1"
    assert format_as_human_readable(999) == "999"
    assert format_as_human_readable(45.678, prefix="ABC") == "ABC45.678"


def test_format_as_human_readable_returns_adds_suffix():
    assert format_as_human_readable(1, suffix="%") == "1%"
    assert (
        format_as_human_readable(156_000, prefix="£", suffix=" per annum")
        == "£156k per annum"
    )


def test_format_as_human_readable_applies_rounding():
    assert format_as_human_readable(1.234, decimal_places=1) == "1.2"
    assert format_as_human_readable(1_234_567, decimal_places=2) == "1.23m"
    assert format_as_human_readable(12_345, prefix="£", decimal_places=0) == "£12k"


def test_format_as_human_readable_applies_negative_round():
    assert format_as_human_readable(123, decimal_places=-1) == "120"
    assert format_as_human_readable(567_890, decimal_places=-1) == "570k"
    assert format_as_human_readable(567_890, decimal_places=-2) == "600k"


def test_format_as_human_readable_returns_dash_for_nan():
    assert format_as_human_readable(None, decimal_places=-1) == "-"
    assert (
        format_as_human_readable(float("NaN"), decimal_places=-1, separator="ABC")
        == "ABC"
    )


def test_format_as_human_readable_returns_formatted_negative_values():
    assert format_as_human_readable(-1_234, prefix="£") == "-£1.234k"
    assert format_as_human_readable(-2_100_000, prefix="£") == "-£2.1m"
    assert format_as_human_readable(-45_678_987_654, prefix="£") == "-£45.679bn"
