# tools/physics_constants_tool.py

PHYSICS_CONSTANTS = {
    "speed of light": "299792458 m/s",
    "gravitational constant": "6.67430e-11 m^3/(kg·s^2)",
    "planck constant": "6.62607015e-34 J·s",
    "elementary charge": "1.602176634e-19 C",
    "boltzmann constant": "1.380649e-23 J/K",
    "avogadro number": "6.02214076e23 1/mol",
    "vacuum permeability": "4π×10^-7 N/A^2",
    "vacuum permittivity": "8.8541878128e-12 F/m"
}

def get_constant(query: str) -> str:
    """
    Checks if the query mentions a known constant and returns its value.
    """
    q = query.lower()
    for name, value in PHYSICS_CONSTANTS.items():
        if name in q or name.split()[0] in q:
            return f"{name.title()}: {value}"
    return ""
