"""
Chart 1 — Cobertura de diseño (spider/radar chart).

Herramienta VIVA: se corre en cualquier momento del proceso de diseño,
antes de tener resultados de protocolos, para ver qué verticales tienen
buena cobertura de escenarios y cuáles tienen huecos.

Este es el "oráculo" declarado — el mapa de lo que se planificó probar,
contra el cual luego se compara el Chart 2 (desempeño de protocolos,
ver performance_chart.py, pendiente hasta tener resultados de protocolos).

Uso:
    python analysis/coverage_chart.py

Requiere: matplotlib (ver requirements.txt)
"""

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCENARIOS_DIR = Path(__file__).parent.parent / "scenarios"
OUTPUT_PATH = Path(__file__).parent / "results" / "coverage_chart.png"

# Nombres legibles para las verticales dentro de alcance del proyecto.
VERTICAL_LABELS = {
    "asi01_goal_hijack": "ASI01\nGoal Hijack",
    "asi02_tool_misuse": "ASI02\nTool Misuse",
    "asi03_identity_privilege": "ASI03\nIdentity/Privilege",
    "asi06_memory_poisoning": "ASI06\nMemory Poisoning",
    "asi09_human_trust": "ASI09\nHuman Trust",
    "asi10_rogue_agent": "ASI10\nRogue Agents",
}


def count_scenarios_per_vertical() -> dict:
    """Cuenta archivos .json (excluyendo schema.json) por subcarpeta de vertical."""
    counts = {}
    for vertical_dir, label in VERTICAL_LABELS.items():
        dir_path = SCENARIOS_DIR / vertical_dir
        if not dir_path.exists():
            counts[label] = 0
            continue
        json_files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
        counts[label] = len(json_files)
    return counts


def plot_radar(counts: dict, target_per_vertical: int = 3):
    """
    Dibuja el radar chart de cobertura. target_per_vertical define el eje
    máximo de referencia (cuántos escenarios por vertical se consideran
    "cobertura completa" para esta fase del proyecto) — ajustar a medida
    que el plan de escenarios se refine.
    """
    labels = list(counts.keys())
    values = list(counts.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle="solid", color="#2563eb")
    ax.fill(angles, values, alpha=0.25, color="#2563eb")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, max(target_per_vertical, max(values)))
    ax.set_title(
        "Chart 1 — Cobertura de diseño por vertical\n(oráculo: escenarios curados vs. objetivo)",
        fontsize=11,
        pad=20,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150)
    print(f"Chart guardado en: {OUTPUT_PATH}")
    print(f"Conteo actual por vertical: {counts}")


if __name__ == "__main__":
    counts = count_scenarios_per_vertical()
    plot_radar(counts)
