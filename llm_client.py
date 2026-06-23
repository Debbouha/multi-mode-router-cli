from google import genai
from google.genai.errors import APIError

from config import MODEL_NAME


client = genai.Client()

def generate_schema_response(prompt: str, json_schema: dict) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": json_schema,
            },
        )
    except APIError as err:
        raise RuntimeError(f"Gemini API error: {err}") from err

    return response.text