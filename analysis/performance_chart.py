"""
Chart 2 — Desempeño de protocolos por vertical (spider/radar chart).

Se construye DESPUÉS de correr los tres protocolos (protocols/*.py) sobre
el set completo de escenarios. Usa los mismos seis ejes que coverage_chart.py
(Chart 1) para que ambos gráficos sean directamente comparables lado a lado:
Chart 1 = qué se planificó probar, Chart 2 = qué tan bien se detectó.

Métrica graficada: Safeguard Catch Rate (SCR) por vertical y por protocolo —
porcentaje de violaciones (ground_truth_violation=true) que cada protocolo
efectivamente marcó/bloqueó en el checkpoint correcto.

Estado: PENDIENTE. Requiere:
1. Más de un escenario por vertical corrido (hoy solo existe asi01_001).
2. Resultados guardados en analysis/results/{protocol_name}.json por
   protocols/*.py (ver TODO en cada uno).

Uso esperado una vez implementado:
    python analysis/performance_chart.py
"""

import json
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
OUTPUT_PATH = RESULTS_DIR / "performance_chart.png"


def compute_scr_per_vertical(results: list[dict], ground_truth: dict) -> dict:
    """
    Calcula el Safeguard Catch Rate por vertical dado:
    - results: lista de veredictos de un protocolo (uno por escenario evaluado)
    - ground_truth: dict {scenario_id: ground_truth_violation (bool)}

    TODO: implementar una vez que haya más de un escenario por vertical —
    con n=1 por vertical el SCR es simplemente 0% o 100%, no aporta señal
    estadística real todavía.
    """
    raise NotImplementedError(
        "Pendiente hasta tener múltiples escenarios por vertical evaluados."
    )


def plot_performance_radar(scr_by_protocol_and_vertical: dict):
    """
    TODO: implementar con la misma librería y estilo que coverage_chart.py
    (matplotlib, radar chart), pero con una serie por protocolo (3 líneas
    superpuestas en el mismo gráfico) en vez de una sola serie de conteos.
    """
    raise NotImplementedError("Pendiente — ver docstring del módulo.")


if __name__ == "__main__":
    print(
        "Chart 2 pendiente: requiere resultados de protocols/*.py sobre "
        "más de un escenario por vertical. Ver TODOs en este archivo."
    )
