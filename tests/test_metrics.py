import pytest

from src.metrics import calculate_metrics, percentage_change


def test_calculate_metrics_normal_case():
    metrics = calculate_metrics(
        spend=700,
        impressions=70000,
        clicks=1400,
        installs=280,
        conversions=70,
        revenue=1750,
    )

    assert metrics["ctr"] == pytest.approx(0.02)
    assert metrics["install_rate"] == pytest.approx(0.20)
    assert metrics["cpi"] == pytest.approx(2.5)
    assert metrics["post_install_conversion_rate"] == pytest.approx(0.25)
    assert metrics["cpa"] == pytest.approx(10.0)
    assert metrics["roas"] == pytest.approx(2.5)


def test_zero_denominators_return_none():
    metrics = calculate_metrics(
        spend=100,
        impressions=0,
        clicks=0,
        installs=0,
        conversions=0,
        revenue=0,
    )

    assert metrics["ctr"] is None
    assert metrics["install_rate"] is None
    assert metrics["cpi"] is None
    assert metrics["post_install_conversion_rate"] is None
    assert metrics["cpa"] is None
    assert metrics["roas"] == pytest.approx(0.0)


def test_percentage_change_from_zero_returns_none():
    assert percentage_change(
        previous=0,
        current=10,
    ) is None