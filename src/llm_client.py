import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError

from src.prompts import build_prompt_v1, build_prompt_v2


MODEL_NAME = "gemini-3.6-flash"


class Observation(BaseModel):
    metric: str = Field(
        description="The campaign metric or performance signal being discussed."
    )
    severity: Literal["low", "medium", "high"] = Field(
        description="How important the observation appears based on the supplied data."
    )
    evidence: str = Field(
        description="The numerical evidence supporting the observation."
    )
    interpretation: str = Field(
        description="A concise explanation of what the observation means."
    )


class CampaignInsight(BaseModel):
    executive_summary: str

    observations: list[Observation]

    possible_hypotheses: list[str]

    recommended_checks: list[str]

    confidence: Literal["low", "medium", "high"]

    limitations: list[str]


def create_gemini_client() -> genai.Client:
    """Create a Gemini client using the API key from the environment."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def generate_campaign_insight(
    context: dict,
    prompt_version: str = "v2",
) -> CampaignInsight:
    """Generate and validate a structured campaign insight."""

    client = create_gemini_client()

    if prompt_version == "v1":
        prompt = build_prompt_v1(context)
    elif prompt_version == "v2":
        prompt = build_prompt_v2(context)
    else:
        raise ValueError(
            "prompt_version must be either 'v1' or 'v2'."
        )

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": CampaignInsight.model_json_schema(),
        },
        store=False,
    )

    if not interaction.output_text:
        raise ValueError("Gemini returned an empty response.")

    try:
        return CampaignInsight.model_validate_json(
            interaction.output_text
        )
    except ValidationError as error:
        raise ValueError(
            "Gemini returned an invalid structured response."
        ) from error


if __name__ == "__main__":
    from src.change_detector import detect_changes
    from src.data_loader import load_campaign_data
    from src.period_analysis import analyze_campaign_periods

    campaign_data = load_campaign_data(
        "data/sample_campaign_data.csv"
    )

    analysis = analyze_campaign_periods(
        campaign_data,
        "Campaign Beta",
    )

    detection = detect_changes(analysis)

    context = {
        **analysis,
        "detection": detection,
    }

    insight = generate_campaign_insight(
        context,
        prompt_version="v2",
    )

    print(
        insight.model_dump_json(indent=2)
    )