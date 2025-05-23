# File: agents/tutor_agent.py (modified)

from agents.math_agent import MathAgent
from agents.physics_agent import PhysicsAgent
from agents.biology_agent import BiologyAgent

class TutorAgent:
    def __init__(self):
        self.subject_agents = {
            "math": MathAgent(),
            "physics": PhysicsAgent(),
            "biology": BiologyAgent()      # Added biology agent
        }

    def route_question(self, subject, question):
        agent = self.subject_agents.get(subject.lower())
        if not agent:
            return "Sorry, I don't have an agent for that subject yet."
        return agent.answer(question)
