# agents/physics_agent.py
from tools.physics_constants_tool import get_constant
from agents.gemini_api import generate_content

def answer_physics(query: str) -> str:
    """
    Handles physics queries. Checks for known constants first, else uses Gemini.
    """
    # Check if the query asks for a constant or its value
    constant_value = get_constant(query)
    if constant_value:
        return constant_value

    # Otherwise, ask Gemini for a physics explanation
    prompt = f"Explain this physics problem: {query}"
    return generate_content(prompt)
