import streamlit as st

from src.change_detector import detect_changes
from src.data_loader import load_campaign_data
from src.llm_client import generate_campaign_insight
from src.period_analysis import analyze_campaign_periods


METRIC_LABELS = {
    "ctr": "CTR",
    "install_rate": "Install Rate",
    "cpi": "CPI",
    "post_install_conversion_rate": "Post-Install Conversion Rate",
    "cpa": "CPA",
    "roas": "ROAS",
}

RATE_METRICS = {
    "ctr",
    "install_rate",
    "post_install_conversion_rate",
}

INVERSE_DELTA_METRICS = {
    "cpi",
    "cpa",
}

CHANGE_LABELS = {
    "high_cpa": "CPA increased significantly",
    "low_roas": "ROAS decreased significantly",
    "low_install_rate": "Install Rate decreased significantly",
    "low_post_install_conversion": (
        "Post-Install Conversion Rate decreased significantly"
    ),
    "spend_efficiency_problem": (
        "Spend increased without proportional conversion growth"
    ),
}


def format_metric(metric_name: str, value: float | None) -> str:
    """Format a metric for display in the UI."""

    if value is None:
        return "N/A"

    if metric_name in RATE_METRICS:
        return f"{value * 100:.1f}%"

    if metric_name == "roas":
        return f"{value:.2f}x"

    return f"{value:.2f}"


def format_change(change: float | None) -> str:
    """Format a percentage change for display."""

    if change is None:
        return "N/A"

    return f"{change:+.1f}%"


def render_metrics(analysis: dict) -> None:
    """Render current metrics with previous-period comparisons."""

    previous_metrics = analysis["previous_period"]["metrics"]
    current_metrics = analysis["current_period"]["metrics"]
    metric_changes = analysis["metric_changes"]

    metric_names = list(METRIC_LABELS.keys())

    for start_index in range(0, len(metric_names), 3):
        columns = st.columns(3)

        for column, metric_name in zip(
            columns,
            metric_names[start_index:start_index + 3],
        ):
            with column:
                st.metric(
                    label=METRIC_LABELS[metric_name],
                    value=format_metric(
                        metric_name,
                        current_metrics[metric_name],
                    ),
                    delta=format_change(
                        metric_changes[metric_name]
                    ),
                    delta_color=(
                        "inverse"
                        if metric_name in INVERSE_DELTA_METRICS
                        else "normal"
                    ),
                )

                st.caption(
                    "Previous: "
                    + format_metric(
                        metric_name,
                        previous_metrics[metric_name],
                    )
                )


def render_detected_changes(detection: dict) -> None:
    """Render deterministic performance-change detection results."""

    if detection["status"] == "stable":
        st.success(
            "No significant changes were detected by the current rule set."
        )
        return

    st.warning(
        "The deterministic rules found performance changes "
        "that may require attention."
    )

    for change in detection["changes"]:
        label = CHANGE_LABELS.get(
            change["code"],
            change["code"],
        )

        st.markdown(f"- **{label}**")


def render_ai_insight(insight) -> None:
    """Render the structured Gemini response."""

    st.subheader("AI Insight")

    st.write(insight.executive_summary)

    st.markdown("### Observations")

    for observation in insight.observations:
        st.markdown(
            f"**{observation.metric} — "
            f"{observation.severity.title()} severity**"
        )
        st.write(observation.evidence)
        st.caption(observation.interpretation)

    st.markdown("### Possible Hypotheses")

    st.caption(
        "Hypotheses are possible explanations, not established causes."
    )

    for hypothesis in insight.possible_hypotheses:
        st.markdown(f"- {hypothesis}")

    st.markdown("### Recommended Checks")

    for check in insight.recommended_checks:
        st.markdown(f"- {check}")

    st.markdown("### Confidence")

    st.write(insight.confidence.title())

    st.markdown("### Limitations")

    for limitation in insight.limitations:
        st.markdown(f"- {limitation}")


st.set_page_config(
    page_title="CampaignLens AI",
    page_icon="📊",
    layout="wide",
)

st.title("CampaignLens AI")

st.caption("Grounded AI Campaign Insight Assistant")

st.write(
    "Analyze synthetic performance-marketing campaign data, "
    "detect meaningful changes using deterministic Python logic, "
    "and generate evidence-grounded AI insights."
)

campaign_data = load_campaign_data(
    "data/sample_campaign_data.csv"
)

campaign_names = sorted(
    campaign_data["campaign"].unique()
)

selected_campaign = st.selectbox(
    "Select a campaign",
    campaign_names,
)

analysis = analyze_campaign_periods(
    campaign_data,
    selected_campaign,
)

detection = detect_changes(analysis)

context = {
    **analysis,
    "detection": detection,
}

st.subheader("Period Comparison")

st.caption(
    f"Previous: "
    f"{analysis['previous_period']['start_date']} "
    f"to {analysis['previous_period']['end_date']} "
    f" | Current: "
    f"{analysis['current_period']['start_date']} "
    f"to {analysis['current_period']['end_date']}"
)

render_metrics(analysis)

st.subheader("Detected Changes")

render_detected_changes(detection)

with st.expander("View structured analysis evidence"):
    st.json(context)

st.divider()

if st.button(
    "Generate AI Insight",
    type="primary",
):
    try:
        with st.spinner(
            "Generating grounded campaign insight..."
        ):
            insight = generate_campaign_insight(
                context,
                prompt_version="v2",
            )

        render_ai_insight(insight)

    except Exception as error:
        st.error(
            f"AI insight generation failed: {error}"
        )

st.divider()

st.caption(
    "Independent portfolio prototype using synthetic aggregated data. "
    "It does not use proprietary advertising data or replicate "
    "proprietary advertising technology. "
    "AI outputs are intended for human review and do not make "
    "autonomous advertising decisions."
)