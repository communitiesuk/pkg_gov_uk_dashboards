"""Tests for key_value_pair component"""


from gov_uk_dashboards.components.dash.key_value_pair import key_value_pair


def test_key_value_pair_works_for_float():
    """Test component returns an array with a <Dt> and <Dd> for a float value input"""
    actual = key_value_pair("a", 1.0)

    assert actual[1].children == 1.0


def test_key_value_pair_works_for_string():
    """Test component returns an array with a <Dt> and <Dd> for a string value input"""
    actual = key_value_pair("a", "hat")

    assert actual[1].children == "hat"


def test_key_value_pair_works_for_none():
    """Test component returns an array with a <Dt> and <Dd> for a none value input"""
    actual = key_value_pair("a", None)

    assert actual[1].children == "-"


def test_key_value_pair_works_for_nan():
    """Test component returns an array with a <Dt> and <Dd> for a nan value input"""
    actual = key_value_pair("a", float("Nan"))

    assert actual[1].children == "-"
