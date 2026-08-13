import pytest

from src.change_detector import detect_changes
from src.data_loader import load_campaign_data
from src.period_analysis import analyze_campaign_periods


SAMPLE_DATA_PATH = "data/sample_campaign_data.csv"


def test_beta_detects_expected_changes():
    data = load_campaign_data(SAMPLE_DATA_PATH)

    analysis = analyze_campaign_periods(
        data,
        "Campaign Beta",
    )

    detection = detect_changes(analysis)

    detected_codes = {
        change["code"]
        for change in detection["changes"]
    }

    assert detection["status"] == "attention_needed"

    assert detected_codes == {
        "high_cpa",
        "low_roas",
        "spend_efficiency_problem",
    }


def test_alpha_is_stable():
    data = load_campaign_data(SAMPLE_DATA_PATH)

    analysis = analyze_campaign_periods(
        data,
        "Campaign Alpha",
    )

    detection = detect_changes(analysis)

    assert detection["status"] == "stable"
    assert detection["changes"] == []


def test_missing_required_column_is_rejected():
    with pytest.raises(
        ValueError,
        match="Missing required columns: revenue",
    ):
        load_campaign_data(
            "tests/fixtures/invalid_missing_revenue.csv"
        )


def test_empty_csv_is_rejected():
    with pytest.raises(
        ValueError,
        match="The CSV file is empty.",
    ):
        load_campaign_data(
            "tests/fixtures/empty.csv"
        )