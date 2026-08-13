# CampaignLens AI — Product Brief

## Problem

Performance-marketing teams work with many campaign metrics such as spend, clicks, installs, conversions, revenue, CPA, and ROAS. Identifying meaningful changes across campaigns can require manually reviewing multiple numbers and comparing performance across periods.

The product question behind CampaignLens AI is:

**Can a generative AI assistant help a human understand already-computed campaign performance signals faster without allowing the model to become the source of truth for numerical calculations?**

## Target User

The hypothetical users are professionals working with aggregated performance-marketing data, such as:

- Performance Marketers
- BI Analysts
- Product Managers
- Commercial team members

## User Story

> As a performance marketer, I want to receive a concise, evidence-grounded explanation of important campaign performance changes so that I can quickly decide what requires further investigation.

## Product Hypothesis

If deterministic Python logic first calculates campaign metrics and detects meaningful performance changes, an LLM can add value by translating those signals into a concise explanation, separating observations from possible hypotheses, and suggesting useful follow-up checks.

## Core Value Proposition

CampaignLens AI combines deterministic campaign analysis with an LLM interpretation layer.

Python is responsible for:

- validating input data,
- aggregating campaign periods,
- calculating performance metrics,
- calculating percentage changes,
- detecting significant changes using transparent rules.

The LLM is responsible for:

- synthesizing supplied evidence,
- producing concise explanations,
- separating observations from hypotheses,
- suggesting investigation steps,
- communicating limitations and uncertainty.

This separation keeps numerical calculations deterministic while using generative AI only where interpretation and communication add value.

## Why Use an LLM?

Rules are more reliable for deterministic calculations and threshold-based detection.

An LLM becomes useful when the task is interpretive rather than mathematical. It can:

- synthesize multiple performance signals,
- communicate findings in natural language,
- organize observations and hypotheses,
- suggest relevant follow-up questions,
- adapt explanations to the supplied context.

The LLM is deliberately **not** responsible for calculating metrics such as CPA, CPI, CTR, or ROAS.

## Why Not Just Use Rules?

A rule-based system can identify that, for example:

- CPA increased by 30%,
- ROAS decreased by 23%,
- spend increased while conversions remained flat.

However, rules alone are less flexible at turning several signals into a concise human-readable explanation or suggesting contextual investigation steps.

CampaignLens AI therefore uses rules for reliable detection and an LLM for interpretation and communication.

## MVP

The MVP includes:

- synthetic aggregated campaign data,
- CSV validation,
- 7-day period comparison,
- deterministic campaign metric calculation,
- rule-based performance change detection,
- hosted LLM API integration using Gemini,
- structured LLM output validated with Pydantic,
- Prompt V1 and Prompt V2,
- lightweight prompt evaluation,
- Streamlit interface,
- automated pytest tests.

## Metrics

The prototype calculates:

- **CTR** = Clicks / Impressions
- **Install Rate** = Installs / Clicks
- **CPI** = Spend / Installs
- **Post-Install Conversion Rate** = Conversions / Installs
- **CPA** = Spend / Conversions
- **ROAS** = Revenue / Spend

Division-by-zero cases return an undefined value rather than inventing a numerical result.

## Performance Change Detection

The MVP uses simple, transparent heuristic thresholds rather than machine-learning anomaly detection.

Examples include:

- significant CPA increase,
- significant ROAS decrease,
- significant Install Rate decrease,
- significant Post-Install Conversion Rate decrease,
- spend increasing significantly while conversions remain approximately flat.

The thresholds are prototype assumptions and are not presented as industry standards. In a production system, they would need to be calibrated using historical data and business context.

## Prompt Engineering Experiment

Two prompt versions were tested.

### Prompt V1

The first prompt instructed the model to use supplied campaign evidence and produce structured observations, hypotheses, and recommended checks.

Evaluation revealed two important weaknesses:

- the model sometimes assumed a currency that had not been supplied,
- it could still generate observations and hypotheses for a campaign classified as stable.

### Prompt V2

The second prompt introduced stronger grounding rules, including:

- never assume an unspecified currency,
- require numerical evidence for observations,
- separate observations from hypotheses,
- avoid unsupported causal claims,
- treat missing information as uncertainty,
- avoid manufacturing issues when deterministic detection reports a stable campaign.

The same model, data, output schema, and evaluation scenarios were used when comparing the prompt versions so that the prompt itself remained the primary variable being changed.

## Evaluation

The prototype currently evaluates three predefined scenarios:

- stable campaign,
- spend-efficiency deterioration,
- install-rate deterioration.

The lightweight automated evaluation checks:

- valid structured output,
- alignment with the expected issue,
- absence of invented currency,
- correct handling of stable campaigns.

Observed results:

| Scenario | Prompt V1 | Prompt V2 |
| --- | ---: | ---: |
| Stable campaign | 2/4 | 4/4 |
| Spend-efficiency issue | 3/4 | 4/4 |
| Install-rate issue | 3/4 | 4/4 |

These scores represent a small prototype evaluation, not a production benchmark.

Qualitative properties such as usefulness, unsupported causality, recommendation quality, and appropriate confidence still require human review.

## Success Criteria

For this prototype, success means:

- deterministic metrics are calculated correctly,
- known synthetic scenarios produce the expected signals,
- structured LLM responses are valid,
- numerical evidence is used in explanations,
- observations and hypotheses remain distinguishable,
- stable campaigns do not generate false alarms,
- the model avoids unsupported assumptions such as an unspecified currency,
- recommendations remain human-reviewed investigation suggestions.

## Responsible AI and Privacy

The prototype uses:

- synthetic data only,
- aggregated campaign-level data,
- no personal data,
- no user-level targeting data.

The LLM does not make autonomous advertising or spending decisions.

AI-generated hypotheses are presented as possible explanations rather than established facts, and a human is expected to review the output before acting on it.

The system is designed as a decision-support prototype rather than an autonomous optimization system.

## Constraints

CampaignLens AI is a small portfolio prototype designed to test a focused product hypothesis rather than reproduce a production analytics platform.

Current constraints include:

- synthetic rather than real campaign data,
- simple rule thresholds,
- two seven-day comparison periods,
- one hosted LLM provider,
- limited evaluation scenarios,
- no historical threshold calibration,
- no live advertising-platform integrations.

## Risks

Potential risks include:

- unsupported causal claims from the LLM,
- overconfidence in generated explanations,
- thresholds that do not generalize to real campaigns,
- missing business context,
- false positives or false negatives,
- users interpreting hypotheses as facts.

The architecture reduces some of these risks by keeping numerical calculations deterministic, validating structured outputs, and explicitly separating evidence from hypotheses.

## Non-Goals

CampaignLens AI does not attempt to:

- optimize real advertising campaigns,
- automatically change campaign budgets,
- predict user-level behavior,
- use proprietary advertising data,
- replicate proprietary advertising or optimization platforms,
- replace BI or analytics platforms,
- provide production-grade anomaly detection,
- make autonomous marketing decisions.

## Future Improvements

Possible future improvements include:

- configurable comparison periods,
- CSV upload,
- threshold calibration using historical data,
- additional evaluation scenarios,
- human evaluation rubrics,
- model latency and cost measurement,
- simple campaign comparison charts,
- improved handling of business-specific context,
- support for additional model providers.

These are intentionally outside the current MVP.

## Disclaimer

CampaignLens AI is an independent portfolio prototype built using synthetic aggregated campaign data.

It does not use proprietary advertising data, represent any real advertising platform, or replicate proprietary advertising technology. Its outputs are intended for experimentation and human-reviewed decision support rather than autonomous campaign optimization.