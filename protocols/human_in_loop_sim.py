"""
Protocolo: Human-in-the-loop simulado.

Cualquier acción que el monitor basado en reglas marcaría como sospechosa
queda "pausada" en vez de bloqueada automáticamente, a la espera de una
aprobación humana simulada. Este protocolo mide la tasa de ESCALAMIENTO,
no de bloqueo directo — la diferencia importa para el análisis de fricción
vs. seguridad en el README.

Estado: PENDIENTE — depende de la lógica de rule_based_monitor.evaluate()
para determinar qué se escala. Falta definir el criterio de "aprobación
simulada" (por ahora, se asume que todo lo escalado NO se aprueba, ver TODO).
"""

from protocols.rule_based_monitor import evaluate as rule_based_evaluate


def evaluate(scenario: dict) -> dict:
    """
    Evalúa un escenario bajo el protocolo human-in-the-loop simulado.

    Args:
        scenario: dict cargado desde scenarios/**/*.json (schema.json)

    Returns:
        dict con el veredicto del protocolo:
        {
            "scenario_id": str,
            "protocol": "human_in_loop_sim",
            "action_flagged": bool,     # si se marcó para revisión
            "action_escalated": bool,   # si se pausó a la espera de aprobación
            "action_blocked": bool,     # resultado final tras la "aprobación" simulada
        }
    """
    rule_result = rule_based_evaluate(scenario)
    escalated = rule_result["action_flagged"]

    # TODO: reemplazar este criterio binario simplista por una simulación real
    # de aprobación humana (ej. requerir justificación explícita en el escenario
    # para que la acción se apruebe). Por ahora, todo lo escalado se rechaza,
    # lo cual sobreestima la efectividad de este protocolo — documentar como
    # limitación conocida hasta implementar el criterio real.
    approved = False

    return {
        "scenario_id": scenario["id"],
        "protocol": "human_in_loop_sim",
        "action_flagged": escalated,
        "action_escalated": escalated,
        "action_blocked": escalated and not approved,
    }


if __name__ == "__main__":
    # TODO: cargar escenarios de scenarios/ y correr evaluate() sobre cada uno,
    # guardando resultados en analysis/results/human_in_loop_sim.json
    pass
