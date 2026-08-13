def safe_divide(numerator: float, denominator: float) -> float | None:
    """Return a division result, or None when division is undefined."""

    if denominator == 0:
        return None

    return float(numerator / denominator)


def calculate_metrics(
    spend: float,
    impressions: float,
    clicks: float,
    installs: float,
    conversions: float,
    revenue: float,
) -> dict[str, float | None]:
    """Calculate deterministic campaign performance metrics."""

    return {
        "ctr": safe_divide(clicks, impressions),
        "install_rate": safe_divide(installs, clicks),
        "cpi": safe_divide(spend, installs),
        "post_install_conversion_rate": safe_divide(conversions, installs),
        "cpa": safe_divide(spend, conversions),
        "roas": safe_divide(revenue, spend),
    }


def percentage_change(
    previous: float | None,
    current: float | None,
) -> float | None:
    """Calculate percentage change from a previous value to a current value."""

    if previous is None or current is None or previous == 0:
        return None

    return float(((current - previous) / previous) * 100)


if __name__ == "__main__":
    example_metrics = calculate_metrics(
        spend=700,
        impressions=70000,
        clicks=1400,
        installs=280,
        conversions=70,
        revenue=1750,
    )

    print("Example campaign metrics:")
    print(example_metrics)

    print()
    print("CPA change example:")
    print(percentage_change(previous=10, current=13))

    print()
    print("Division-by-zero example:")
    print(calculate_metrics(
        spend=100,
        impressions=0,
        clicks=0,
        installs=0,
        conversions=0,
        revenue=0,
    ))