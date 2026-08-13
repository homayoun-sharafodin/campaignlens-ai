import json

from evaluation.eval_cases import EVAL_CASES
from src.change_detector import detect_changes
from src.data_loader import load_campaign_data
from src.period_analysis import analyze_campaign_periods
from src.llm_client import generate_campaign_insight


def contains_expected_code_text(
    insight_text: str,
    expected_codes: list[str],
) -> bool:
    """Check whether the output references the expected issue areas."""

    code_keywords = {
        "high_cpa": ["cpa", "acquisition cost"],
        "low_roas": ["roas", "return on ad spend"],
        "spend_efficiency_problem": [
            "spend",
            "conversions",
            "revenue",
            "efficiency",
        ],
        "low_install_rate": ["install rate", "installs"],
    }

    for code in expected_codes:
        keywords = code_keywords.get(code, [])
        if not any(keyword in insight_text for keyword in keywords):
            return False

    return True


def mentions_currency_symbol(insight_text: str) -> bool:
    """Detect whether the output invents a currency symbol."""
    return "$" in insight_text or "€" in insight_text


def evaluate_case(
    data,
    case: dict,
    prompt_version: str,
) -> dict:
    """Run one evaluation case for one prompt version."""

    analysis = analyze_campaign_periods(
        data,
        case["campaign"],
    )

    detection = detect_changes(analysis)

    context = {
        **analysis,
        "detection": detection,
    }

    insight = generate_campaign_insight(
        context,
        prompt_version=prompt_version,
    )

    insight_dict = insight.model_dump()
    insight_text = json.dumps(insight_dict).lower()

    structure_ok = True
    stable_case_ok = True
    no_fake_currency = not mentions_currency_symbol(insight_text)
    issue_alignment_ok = contains_expected_code_text(
        insight_text,
        case["expected_codes"],
    )

    if case["expected_status"] == "stable":
        stable_case_ok = len(insight.observations) == 0 or (
            "stable" in insight.executive_summary.lower()
            or "no significant" in insight.executive_summary.lower()
        )

    score = sum(
        [
            structure_ok,
            issue_alignment_ok,
            no_fake_currency,
            stable_case_ok,
        ]
    )

    return {
        "case": case["name"],
        "campaign": case["campaign"],
        "prompt_version": prompt_version,
        "score": score,
        "max_score": 4,
        "structure_ok": structure_ok,
        "issue_alignment_ok": issue_alignment_ok,
        "no_fake_currency": no_fake_currency,
        "stable_case_ok": stable_case_ok,
        "confidence": insight.confidence,
        "executive_summary": insight.executive_summary,
    }


def run_evaluation():
    """Run all evaluation cases for both V1 and V2."""

    data = load_campaign_data("data/sample_campaign_data.csv")

    results = []

    for case in EVAL_CASES:
        for prompt_version in ["v1", "v2"]:
            result = evaluate_case(
                data=data,
                case=case,
                prompt_version=prompt_version,
            )
            results.append(result)

    return results


if __name__ == "__main__":
    results = run_evaluation()

    for result in results:
        print("-" * 60)
        print(
            f"{result['case']} | {result['prompt_version']} "
            f"| score: {result['score']}/{result['max_score']}"
        )
        print(
            f"structure_ok={result['structure_ok']}, "
            f"issue_alignment_ok={result['issue_alignment_ok']}, "
            f"no_fake_currency={result['no_fake_currency']}, "
            f"stable_case_ok={result['stable_case_ok']}"
        )
        print(f"confidence={result['confidence']}")
        print(f"summary={result['executive_summary']}")