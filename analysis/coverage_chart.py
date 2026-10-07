"""
Chart 1 - Cobertura de diseño (spider/radar chart).

Herramienta VIVA: se corre en cualquier momento del proceso de diseño,
antes de tener resultados de protocolos, para ver qué verticales tienen
buena cobertura de escenarios y cuáles tienen huecos.

Este es el "oráculo" declarado - el mapa de lo que se planificó probar,
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
GROUND_TRUTH_DIR = Path(__file__).parent.parent / "ground_truth"
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


def _is_legitimate_case(scenario_id: str) -> bool:
    """True si el ground truth del escenario dice que NO hay falta (ej. un gemelo inocente)."""
    gt_path = GROUND_TRUTH_DIR / f"{scenario_id}.json"
    if not gt_path.exists():
        return False
    with open(gt_path, encoding="utf-8") as f:
        return json.load(f).get("ground_truth_violation") is False


def count_scenarios_per_vertical() -> tuple[dict, dict]:
    """
    Cuenta, por subcarpeta de vertical, los escenarios CON FALTA (lo que el radar
    grafica como cobertura) y aparte los casos legítimos. Un gemelo inocente no
    cubre un ataque nuevo: es la contraparte de uno que ya existe, por eso no
    suma cobertura.
    """
    attack_counts, legit_counts = {}, {}
    for vertical_dir, label in VERTICAL_LABELS.items():
        dir_path = SCENARIOS_DIR / vertical_dir
        attack_counts[label] = legit_counts[label] = 0
        if not dir_path.exists():
            continue
        for f in os.listdir(dir_path):
            if not f.endswith(".json") or f == "schema.json":
                continue
            if _is_legitimate_case(Path(f).stem):
                legit_counts[label] += 1
            else:
                attack_counts[label] += 1
    return attack_counts, legit_counts


def plot_radar(counts: dict, target_per_vertical: int = 3):
    """
    Dibuja el radar chart de cobertura. target_per_vertical define el eje
    máximo de referencia (cuántos escenarios por vertical se consideran
    "cobertura completa" para esta fase del proyecto) - ajustar a medida
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
        "Chart 1 - Cobertura de diseño por vertical\n"
        "(escenarios con falta curados vs. objetivo; los casos legítimos no suman)",
        fontsize=11,
        pad=20,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150)
    print(f"Chart guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    attack_counts, legit_counts = count_scenarios_per_vertical()
    plot_radar(attack_counts)
    print()
    print(f"{'Vertical':<26}{'Con falta':<11}{'Legítimos':<10}")
    for label in attack_counts:
        print(f"{label.replace(chr(10), ' '):<26}{attack_counts[label]:<11}{legit_counts[label]:<10}")
