import math
import re

class CalculatorTool:
    def calculate(self, expression):
        try:
            allowed_names = {
                "sqrt": math.sqrt,
                "log": math.log,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "pi": math.pi,
                "e": math.e,
                "pow": math.pow,
            }
            clean_expr = re.sub(r'[^0-9\.\+\-\*\/\(\)\,\s\w]', '', expression)
            result = eval(clean_expr, {"__builtins__": None}, allowed_names)
            return f"Calculator result: {result}"
        except Exception as e:
            return "Invalid calculation."