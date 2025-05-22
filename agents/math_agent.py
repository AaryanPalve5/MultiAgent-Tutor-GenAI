# agents/math_agent.py
from tools.calculator_tool import calculate_expression
from agents.gemini_api import generate_content

def answer_math(query: str) -> str:
    """
    Handles math queries. Uses the calculator tool for expressions,
    and falls back to Gemini for explanations or complex problems.
    """
    # Attempt to compute the result directly
    try:
        result = calculate_expression(query)
        if result is not None:
            return f"The result is: {result}"
    except Exception:
        pass

    # If direct calculation fails, ask Gemini to explain or solve
    prompt = f"Solve this math problem: {query}"
    return generate_content(prompt)
