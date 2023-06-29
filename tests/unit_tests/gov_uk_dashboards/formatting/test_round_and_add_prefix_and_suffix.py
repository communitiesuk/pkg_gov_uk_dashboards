from gov_uk_dashboards.formatting.round_and_add_prefix_and_suffix import (
    round_and_add_prefix_and_suffix,
)


def test_round_and_add_prefix_and_suffix_returns_formatted_value():
    assert round_and_add_prefix_and_suffix(1000000000) == "1000000000"
    assert round_and_add_prefix_and_suffix(2100000000) == "2100000000"
    assert round_and_add_prefix_and_suffix(45678987654, prefix="£") == "£45678987654"
    assert round_and_add_prefix_and_suffix(569, suffix="%") == "569%"
    assert (
        round_and_add_prefix_and_suffix(342.2, prefix="£", suffix=" per person")
        == "£342.2 per person"
    )
    assert (
        round_and_add_prefix_and_suffix(
            569, decimal_places=3, prefix="£", suffix=" per person"
        )
        == "£569.000 per person"
    )
    assert (
        round_and_add_prefix_and_suffix(
            342.2, decimal_places=4, prefix="£", suffix=" per person"
        )
        == "£342.2000 per person"
    )
    assert (
        round_and_add_prefix_and_suffix(
            float("NaN"), decimal_places=-1, separator="ABC"
        )
        == "ABC"
    )
    # assert (
    #     round_and_add_prefix_and_suffix(
    #         342.2, decimal_places=0, prefix="£", suffix=" per person"
    #     )
    #     == "£342 per person"
    # )
    assert round_and_add_prefix_and_suffix(None, decimal_places=-1) == "-"
    assert round_and_add_prefix_and_suffix(123, decimal_places=-1) == "120"
