# agents/tutor_agent.py
from agents.math_agent import answer_math
from agents.physics_agent import answer_physics
from agents.biology_agent import answer_biology

def classify_and_respond(query: str) -> str:
    """
    Classifies the query into math, physics, or biology, and delegates accordingly.
    """
    q_lower = query.lower()

    # Simple keyword-based classification
    math_keywords = ["solve", "calculate", "compute", "+", "-", "*", "/", "integral", "derivative", "limit"]
    physics_keywords = ["force", "energy", "velocity", "acceleration", "mass", "gravity", "quantum", "electron", "motion"]
    biology_keywords = ["cell", "dna", "gene", "biology", "life", "organism", "evolution", "ecosystem"]

    if any(word in q_lower for word in math_keywords):
        return answer_math(query)
    elif any(word in q_lower for word in physics_keywords):
        return answer_physics(query)
    elif any(word in q_lower for word in biology_keywords):
        return answer_biology(query)
    else:
        # Default: use Gemini for general questions
        return generate_content(f"Answer this question: {query}")
