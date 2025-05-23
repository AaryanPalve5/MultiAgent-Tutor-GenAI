# File: agents/biology_agent.py

from agents.gemini_api import ask_gemini

class BiologyAgent:
    def answer(self, question):
        # Delegate the question to Gemini, specifying "biology" as the subject
        return ask_gemini("biology", question)
