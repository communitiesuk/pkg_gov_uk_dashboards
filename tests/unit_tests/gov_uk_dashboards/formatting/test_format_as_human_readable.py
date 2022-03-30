from gov_uk_dashboards.formatting.human_readable import format_as_human_readable


def test_format_as_human_readable_returns_formatted_billions():
    assert format_as_human_readable(1_000_000_000) == "1bn"
    assert format_as_human_readable(2_100_000_000) == "2.1bn"
    assert format_as_human_readable(45_678_987_654, prefix = "£") == "£45.679bn"


def test_format_as_human_readable_returns_formatted_millions():
    assert format_as_human_readable(1_000_000) == "1m"
    assert format_as_human_readable(999_100_000) == "999.1m"
    assert format_as_human_readable(45_678_987, prefix = "$") == "$45.679m"


def test_format_as_human_readable_returns_formatted_thousands():
    assert format_as_human_readable(1_000) == "1k"
    assert format_as_human_readable(425_000) == "425k"
    assert format_as_human_readable(45_678, prefix = "ABC") == "ABC45.678k"


def test_format_as_human_readable_returns_formatted_units():
    assert format_as_human_readable(1) == "1"
    assert format_as_human_readable(999) == "999"
    assert format_as_human_readable(45.678, prefix = "ABC") == "ABC45.678"
