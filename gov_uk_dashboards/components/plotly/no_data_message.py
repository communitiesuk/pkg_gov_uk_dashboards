"""Message for when selection does not provide data."""


def no_data_message(metric: str, financial_year: str) -> list[str]:
    """Message for when selection does not provide data."""
    return [
        f"The selection you have made has no data for {metric.lower()}. ",
        f"This is probably because data has not been published for {financial_year}, ",
        "please select a different year.",
    ]
