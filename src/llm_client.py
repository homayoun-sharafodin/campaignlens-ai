import os

from dotenv import load_dotenv
from google import genai


MODEL_NAME = "gemini-3.6-flash"


def create_gemini_client() -> genai.Client:
    """Create a Gemini client using the API key from the environment."""

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def test_connection() -> str:
    """Send a minimal request to verify Gemini API connectivity."""

    client = create_gemini_client()

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input="Reply with exactly: CampaignLens API connection successful",
        store=False,
    )

    return interaction.output_text


if __name__ == "__main__":
    print(test_connection())