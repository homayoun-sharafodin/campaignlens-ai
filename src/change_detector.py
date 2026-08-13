from src.metrics import percentage_change


CHANGE_THRESHOLD = 20.0
CONVERSION_GROWTH_LIMIT = 5.0


def detect_changes(analysis: dict) -> dict:
    """Detect meaningful campaign performance changes using transparent rules."""

    previous_period = analysis["previous_period"]
    current_period = analysis["current_period"]
    metric_changes = analysis["metric_changes"]

    previous_totals = previous_period["totals"]
    current_totals = current_period["totals"]

    spend_change = percentage_change(
        previous_totals["spend"],
        current_totals["spend"],
    )

    conversion_change = percentage_change(
        previous_totals["conversions"],
        current_totals["conversions"],
    )

    changes = []

    cpa_change = metric_changes["cpa"]
    if cpa_change is not None and cpa_change >= CHANGE_THRESHOLD:
        changes.append(
            {
                "code": "high_cpa",
                "metric": "cpa",
                "previous": previous_period["metrics"]["cpa"],
                "current": current_period["metrics"]["cpa"],
                "change_pct": round(cpa_change, 2),
            }
        )

    roas_change = metric_changes["roas"]
    if roas_change is not None and roas_change <= -CHANGE_THRESHOLD:
        changes.append(
            {
                "code": "low_roas",
                "metric": "roas",
                "previous": previous_period["metrics"]["roas"],
                "current": current_period["metrics"]["roas"],
                "change_pct": round(roas_change, 2),
            }
        )

    install_rate_change = metric_changes["install_rate"]
    if (
        install_rate_change is not None
        and install_rate_change <= -CHANGE_THRESHOLD
    ):
        changes.append(
            {
                "code": "low_install_rate",
                "metric": "install_rate",
                "previous": previous_period["metrics"]["install_rate"],
                "current": current_period["metrics"]["install_rate"],
                "change_pct": round(install_rate_change, 2),
            }
        )

    post_install_change = metric_changes["post_install_conversion_rate"]
    if (
        post_install_change is not None
        and post_install_change <= -CHANGE_THRESHOLD
    ):
        changes.append(
            {
                "code": "low_post_install_conversion",
                "metric": "post_install_conversion_rate",
                "previous": previous_period["metrics"][
                    "post_install_conversion_rate"
                ],
                "current": current_period["metrics"][
                    "post_install_conversion_rate"
                ],
                "change_pct": round(post_install_change, 2),
            }
        )

    if (
        spend_change is not None
        and conversion_change is not None
        and spend_change >= CHANGE_THRESHOLD
        and conversion_change <= CONVERSION_GROWTH_LIMIT
    ):
        changes.append(
            {
                "code": "spend_efficiency_problem",
                "spend_change_pct": round(spend_change, 2),
                "conversion_change_pct": round(conversion_change, 2),
            }
        )

    return {
        "status": "attention_needed" if changes else "stable",
        "changes": changes,
    }


if __name__ == "__main__":
    from src.data_loader import load_campaign_data
    from src.period_analysis import analyze_campaign_periods

    campaign_data = load_campaign_data("data/sample_campaign_data.csv")

    for campaign_name in ["Campaign Alpha", "Campaign Beta"]:
        analysis = analyze_campaign_periods(
            campaign_data,
            campaign_name,
        )

        result = detect_changes(analysis)

        print()
        print(f"{campaign_name}:")
        print(result)