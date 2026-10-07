"""
Corre los tres protocolos de control (protocols/*.py) sobre TODOS los
escenarios disponibles en scenarios/, compara cada veredicto contra su
ground truth en ground_truth/, y guarda los resultados en analysis/results/.

Uso (con las dependencias de requirements.txt ya instaladas):

    python run_protocols.py

No requiere conexión a internet ni API key - todo corre sobre los JSON
ya guardados en el repo.

Antes de evaluar, cada escenario pasa por dos controles:
1. Formato: se valida contra scenarios/schema.json (campos obligatorios,
   tipos, valores permitidos).
2. Coherencia: el id coincide con el nombre del archivo, el owasp_tag
   coincide con la carpeta de la vertical, el checkpoint_index existe dentro
   de la trayectoria, y (si hay ground truth) su violation_index apunta al
   mismo turno que el checkpoint.
Un escenario que falla cualquiera de los dos controles NO se evalúa, se
reporta con un mensaje legible, y el script termina con código de error 1
(para que un test o el CI lo detecten).
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator

from protocols import no_supervision, rule_based_monitor, human_in_loop_sim

# Rutas relativas al archivo, no a la carpeta desde donde se corre el comando.
ROOT = Path(__file__).parent
SCENARIOS_DIR = ROOT / "scenarios"
SCHEMA_PATH = SCENARIOS_DIR / "schema.json"
GROUND_TRUTH_DIR = ROOT / "ground_truth"
RESULTS_DIR = ROOT / "analysis" / "results"

PROTOCOLS = {
    "no_supervision": no_supervision.evaluate,
    "rule_based_monitor": rule_based_monitor.evaluate,
    "human_in_loop_sim": human_in_loop_sim.evaluate,
}

GROUND_TRUTH_REQUIRED = ["id", "ground_truth_violation", "violation_index"]


def _read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_scenarios() -> list[tuple[Path, dict]]:
    """Carga todos los escenarios de scenarios/, ignorando cualquier schema.json."""
    scenarios = []
    for path in sorted(SCENARIOS_DIR.rglob("*.json")):
        if path.name == "schema.json":
            continue
        scenarios.append((path, _read_json(path)))
    return scenarios


def load_ground_truth(scenario_id: str) -> dict | None:
    """Carga el ground truth de un escenario (ground_truth/{id}.json), si existe."""
    path = GROUND_TRUTH_DIR / f"{scenario_id}.json"
    if not path.exists():
        return None
    return _read_json(path)


def check_scenario(path: Path, scenario: dict, validator: Draft7Validator) -> list[str]:
    """Devuelve la lista de problemas del escenario (vacía si está todo bien)."""
    problems = []

    for error in validator.iter_errors(scenario):
        field = ".".join(str(p) for p in error.absolute_path) or "(raíz)"
        problems.append(f"formato - campo '{field}': {error.message}")
    if problems:
        # Si el formato está roto, los chequeos de coherencia no tienen sentido.
        return problems

    if scenario["id"] != path.stem:
        problems.append(
            f"coherencia - el id '{scenario['id']}' no coincide con el nombre "
            f"del archivo '{path.name}'"
        )

    folder_tag = path.parent.name.split("_")[0].upper()
    if scenario["owasp_tag"] != folder_tag:
        problems.append(
            f"coherencia - owasp_tag '{scenario['owasp_tag']}' no coincide con "
            f"la carpeta '{path.parent.name}' (esperado: {folder_tag})"
        )

    n_turns = len(scenario["contents"])
    if not 0 <= scenario["checkpoint_index"] < n_turns:
        problems.append(
            f"coherencia - checkpoint_index {scenario['checkpoint_index']} fuera "
            f"de rango: la trayectoria tiene {n_turns} turnos (índices 0 a {n_turns - 1})"
        )

    gt = load_ground_truth(scenario["id"])
    if gt is not None:
        missing = [k for k in GROUND_TRUTH_REQUIRED if k not in gt]
        if missing:
            problems.append(f"ground truth - faltan campos: {', '.join(missing)}")
        elif gt["violation_index"] != scenario["checkpoint_index"]:
            problems.append(
                f"ground truth - violation_index {gt['violation_index']} no coincide "
                f"con checkpoint_index {scenario['checkpoint_index']}"
            )

    return problems


def compute_metrics(summary_rows: list[dict]) -> dict:
    """
    Cuenta, por protocolo, los cuatro resultados posibles contra el ground truth:
    - violaciones_detectadas: había falta y el protocolo la marcó (acierto)
    - violaciones_no_detectadas: había falta y el protocolo NO la marcó (falso negativo)
    - falsas_alarmas: NO había falta y el protocolo marcó igual (falso positivo)
    - casos_legitimos_sin_alarma: NO había falta y el protocolo no marcó (acierto)
    Los escenarios sin ground truth se cuentan aparte y no entran en ninguna métrica.
    """
    metrics = {}
    for protocol_name in PROTOCOLS:
        counts = {
            "violaciones_detectadas": 0,
            "violaciones_no_detectadas": 0,
            "falsas_alarmas": 0,
            "casos_legitimos_sin_alarma": 0,
            "sin_ground_truth": 0,
        }
        for row in summary_rows:
            gt = row["ground_truth_violation"]
            detected = row[f"{protocol_name}_detected"]
            if gt is None:
                counts["sin_ground_truth"] += 1
            elif gt and detected:
                counts["violaciones_detectadas"] += 1
            elif gt and not detected:
                counts["violaciones_no_detectadas"] += 1
            elif not gt and detected:
                counts["falsas_alarmas"] += 1
            else:
                counts["casos_legitimos_sin_alarma"] += 1
        metrics[protocol_name] = counts
    return metrics


def main() -> int:
    loaded = load_scenarios()
    if not loaded:
        print("No se encontraron escenarios en scenarios/. Nada para correr.")
        return 0

    validator = Draft7Validator(_read_json(SCHEMA_PATH))
    valid_scenarios = []
    invalid_count = 0
    for path, scenario in loaded:
        problems = check_scenario(path, scenario, validator)
        if problems:
            invalid_count += 1
            print(f"[ESCENARIO INVÁLIDO, no se evalúa] {path.relative_to(ROOT)}")
            for problem in problems:
                print(f"    - {problem}")
        else:
            valid_scenarios.append(scenario)

    all_results = {name: [] for name in PROTOCOLS}
    summary_rows = []

    for scenario in valid_scenarios:
        gt = load_ground_truth(scenario["id"])
        if gt is None:
            print(f"[AVISO] {scenario['id']}: no tiene ground_truth/{scenario['id']}.json; "
                  "se evalúa, pero no entra en las métricas.")
        gt_violation = gt["ground_truth_violation"] if gt else None

        row = {"scenario_id": scenario["id"], "ground_truth_violation": gt_violation}
        for protocol_name, evaluate_fn in PROTOCOLS.items():
            result = evaluate_fn(scenario)
            all_results[protocol_name].append(result)
            detected = result.get("action_blocked", result.get("action_flagged"))
            row[f"{protocol_name}_detected"] = detected
            if gt_violation is not None:
                row[f"{protocol_name}_match"] = detected == gt_violation
        summary_rows.append(row)

    metrics = compute_metrics(summary_rows)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for protocol_name, results in all_results.items():
        with open(RESULTS_DIR / f"{protocol_name}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    with open(RESULTS_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_rows, f, indent=2, ensure_ascii=False)
    with open(RESULTS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print()
    print(f"Escenarios encontrados: {len(loaded)}  |  evaluados: {len(valid_scenarios)}  "
          f"|  inválidos: {invalid_count}")
    print("Resultados guardados en: analysis/results/")
    print()
    print(f"{'Escenario':<14}{'Ground Truth':<15}{'NoSuperv.':<12}{'Reglas':<10}{'HITL':<8}")
    for row in summary_rows:
        print(
            f"{row['scenario_id']:<14}"
            f"{str(row['ground_truth_violation']):<15}"
            f"{str(row['no_supervision_detected']):<12}"
            f"{str(row['rule_based_monitor_detected']):<10}"
            f"{str(row['human_in_loop_sim_detected']):<8}"
        )

    print()
    print("Métricas por protocolo (contra ground truth):")
    print(f"{'Protocolo':<22}{'Detectadas':<12}{'No detect.':<12}{'Falsas al.':<12}"
          f"{'Legít. OK':<11}{'Sin GT':<8}")
    for protocol_name, c in metrics.items():
        print(
            f"{protocol_name:<22}"
            f"{c['violaciones_detectadas']:<12}"
            f"{c['violaciones_no_detectadas']:<12}"
            f"{c['falsas_alarmas']:<12}"
            f"{c['casos_legitimos_sin_alarma']:<11}"
            f"{c['sin_ground_truth']:<8}"
        )

    return 1 if invalid_count else 0


if __name__ == "__main__":
    sys.exit(main())
