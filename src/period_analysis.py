import pandas as pd

from src.metrics import calculate_metrics, percentage_change


AGGREGATION_COLUMNS = [
    "spend",
    "impressions",
    "clicks",
    "installs",
    "conversions",
    "revenue",
]


def aggregate_period(period_data: pd.DataFrame) -> dict:
    """Aggregate raw campaign values and calculate metrics for one period."""

    totals = {
    column: float(period_data[column].sum())
    for column in AGGREGATION_COLUMNS
    }

    metrics = calculate_metrics(
        spend=totals["spend"],
        impressions=totals["impressions"],
        clicks=totals["clicks"],
        installs=totals["installs"],
        conversions=totals["conversions"],
        revenue=totals["revenue"],
    )

    return {
        "start_date": period_data["date"].min().date().isoformat(),
        "end_date": period_data["date"].max().date().isoformat(),
        "totals": totals,
        "metrics": metrics,
    }


def compare_metrics(
    previous_metrics: dict[str, float | None],
    current_metrics: dict[str, float | None],
) -> dict[str, float | None]:
    """Calculate percentage changes between two metric dictionaries."""

    return {
        metric: percentage_change(
            previous=previous_metrics[metric],
            current=current_metrics[metric],
        )
        for metric in previous_metrics
    }


def analyze_campaign_periods(
    data: pd.DataFrame,
    campaign_name: str,
) -> dict:
    """Compare the latest two seven-day periods for one campaign."""

    campaign_data = data[data["campaign"] == campaign_name].copy()

    if campaign_data.empty:
        raise ValueError(f"Campaign '{campaign_name}' was not found.")

    campaign_data = campaign_data.sort_values("date")

    if len(campaign_data) < 14:
        raise ValueError(
            f"Campaign '{campaign_name}' needs at least 14 days of data."
        )

    latest_14_days = campaign_data.tail(14)

    previous_data = latest_14_days.iloc[:7]
    current_data = latest_14_days.iloc[7:]

    previous_period = aggregate_period(previous_data)
    current_period = aggregate_period(current_data)

    metric_changes = compare_metrics(
        previous_period["metrics"],
        current_period["metrics"],
    )

    return {
        "campaign": campaign_name,
        "previous_period": previous_period,
        "current_period": current_period,
        "metric_changes": metric_changes,
    }


if __name__ == "__main__":
    from src.data_loader import load_campaign_data

    campaign_data = load_campaign_data("data/sample_campaign_data.csv")

    analysis = analyze_campaign_periods(
        campaign_data,
        "Campaign Beta",
    )

    print("Campaign:", analysis["campaign"])

    print()
    print("Previous period metrics:")
    print(analysis["previous_period"]["metrics"])

    print()
    print("Current period metrics:")
    print(analysis["current_period"]["metrics"])

    print()
    print("Metric changes (%):")
    print(analysis["metric_changes"])