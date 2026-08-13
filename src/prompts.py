import json


def build_prompt_v1(context: dict) -> str:
    """Build the first version of the campaign insight prompt."""

    context_json = json.dumps(context, indent=2)

    return f"""
You are analyzing synthetic aggregated performance-marketing campaign data
for a human performance marketer.

The numerical calculations and detected changes were produced
deterministically by Python. Treat them as the source of truth.
Do not recalculate the metrics.

Using only the supplied context:
- summarize the most important performance changes,
- explain what they may mean for the marketer,
- provide possible hypotheses,
- recommend practical next checks.

Keep the response concise and useful.

Campaign analysis context:

{context_json}
""".strip()

def build_prompt_v2(context: dict) -> str:
    """Build a stricter grounded campaign insight prompt."""

    context_json = json.dumps(context, indent=2)

    return f"""
You are analyzing synthetic aggregated performance-marketing campaign data
for a human performance marketer.

The supplied numerical values were calculated deterministically by Python
and must be treated as the source of truth.

Follow these rules strictly:

1. Use only information contained in the supplied context.
2. Do not recalculate or invent metrics.
3. Do not assume a currency unless one is explicitly supplied.
4. Every observation must be supported by numerical evidence from the context.
5. Separate observations from hypotheses:
   - An observation is directly supported by the supplied data.
   - A hypothesis is a possible explanation that requires additional evidence.
6. Never present a hypothesis as a confirmed cause.
7. Avoid causal language such as "caused by", "driven by", "due to",
   or "confirms" unless the supplied data directly proves that relationship.
8. If information such as CPM, CPC, creative performance, audience quality,
   targeting, placement mix, or frequency is not supplied, do not claim
   anything about it as fact. It may only appear as a hypothesis or
   recommended check.
9. If deterministic detection status is "stable":
   - clearly state that performance is stable,
   - return an empty observations list,
   - return an empty possible_hypotheses list,
   - do not recommend investigation into minor normal variations,
   - only mention continued monitoring if a recommended check is necessary.
10. Use concise language and explicitly acknowledge uncertainty where needed.
11. Recommended checks should help a human investigate the issue rather than
   instructing the system to make autonomous advertising decisions.

Campaign analysis context:

{context_json}
""".strip()