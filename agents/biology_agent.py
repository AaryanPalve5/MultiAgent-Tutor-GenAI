# agents/biology_agent.py
from agents.gemini_api import generate_content

def answer_biology(query: str) -> str:
    """
    Handles biology queries using Gemini.
    """
    prompt = f"Answer this biology question: {query}"
    return generate_content(prompt)
