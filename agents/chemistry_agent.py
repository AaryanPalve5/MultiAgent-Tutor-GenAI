from agents.gemini_api import ask_gemini

class ChemistryAgent:
    def answer(self, question):
        return ask_gemini("chemistry", question)