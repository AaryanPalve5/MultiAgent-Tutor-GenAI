# tools/calculator_tool.py
from sympy import sympify

def calculate_expression(expr: str):
    """
    Safely evaluate a mathematical expression given as a string.
    Returns the numerical result or None if invalid.
    """
    try:
        # Convert string to SymPy expression
        sym_expr = sympify(expr)
        # Evaluate numerically (float)
        result = sym_expr.evalf()
        return result
    except Exception:
        # If sympify fails (invalid expression), return None
        return None
