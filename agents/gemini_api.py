# agents/gemini_api.py
import os
from google import genai
from google.genai import types

# Initialize the Gemini API client with the API key from .env
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_content(prompt: str, model: str = "gemini-2.0-pro") -> str:
    """
    Sends a prompt to the Gemini model and returns the generated text.
    """
    # Create content list as expected by the Gemini API
    response = client.models.generate_content(
        model=model,
        contents=[prompt]
    )
    return response.text
