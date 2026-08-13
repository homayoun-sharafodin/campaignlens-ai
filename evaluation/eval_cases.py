EVAL_CASES = [
    {
        "name": "stable_alpha",
        "campaign": "Campaign Alpha",
        "expected_status": "stable",
        "expected_codes": [],
    },
    {
        "name": "efficiency_beta",
        "campaign": "Campaign Beta",
        "expected_status": "attention_needed",
        "expected_codes": [
            "high_cpa",
            "low_roas",
            "spend_efficiency_problem",
        ],
    },
    {
        "name": "install_rate_gamma",
        "campaign": "Campaign Gamma",
        "expected_status": "attention_needed",
        "expected_codes": [
            "low_install_rate",
        ],
    },
]