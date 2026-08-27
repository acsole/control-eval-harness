"""
Protocolo: Sin supervisión (baseline).

No aplica ninguna verificación al escenario. Sirve como línea base para medir
cuánto agregan los otros dos protocolos (rule_based_monitor, human_in_loop_sim).

Estado: PENDIENTE de implementación completa hasta tener el set de escenarios
de al menos una vertical adicional a ASI01. Estructura definida para que el
resto de protocolos comparta la misma interfaz.
"""

from typing import Any


def evaluate(scenario: dict) -> dict:
    """
    Evalúa un escenario bajo el protocolo "sin supervisión".

    Args:
        scenario: dict cargado desde scenarios/**/*.json (schema.json)

    Returns:
        dict con el veredicto del protocolo:
        {
            "scenario_id": str,
            "protocol": "no_supervision",
            "action_flagged": bool,   # nunca marca nada, por definición
            "action_blocked": bool,   # nunca bloquea nada, por definición
        }
    """
    return {
        "scenario_id": scenario["id"],
        "protocol": "no_supervision",
        "action_flagged": False,
        "action_blocked": False,
    }


if __name__ == "__main__":
    # TODO: cargar escenarios de scenarios/ y correr evaluate() sobre cada uno,
    # guardando resultados en analysis/results/no_supervision.json
    pass
