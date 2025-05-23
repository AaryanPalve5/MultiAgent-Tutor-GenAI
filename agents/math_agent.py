from tools.calculator_tool import CalculatorTool
from agents.gemini_api import ask_gemini

class MathAgent:
    def __init__(self):
        self.calculator = CalculatorTool()

    def answer(self, question):
        # If it's likely a calculation, try calculator tool
        if any(op in question for op in ["+", "-", "*", "/", "sqrt", "log", "^"]):
            result = self.calculator.calculate(question)
            if "Invalid" not in result:
                return result
        # Else, use Gemini LLM
        return ask_gemini("math", question)