# Control Protocol Evaluation Harness

**Estado del proyecto: en construcción activa (work in progress). Este README se actualiza de forma incremental a medida que se agregan escenarios y resultados.**

## ¿Qué es esto, en 30 segundos?

Imaginá que contratás un asistente nuevo con acceso a las llaves de la oficina. Este proyecto no evalúa si el asistente es honesto — evalúa si tenés un buen sistema de cámaras y protocolos de aprobación que detecten cuando alguien usa esas llaves para algo que no debía.

Concretamente: este harness mide **qué tan bien distintos protocolos de supervisión detectan que un agente de IA se salió del scope autorizado** — no mide si el agente "puede ser engañado" (eso es red teaming clásico / jailbreaking), mide si el sistema que lo vigila funciona.

Si nunca escuchaste hablar de AI Control, Red Teaming o Safeguards, empezá por [`GLOSARIO.md`](./GLOSARIO.md).

## ¿Por qué esta distinción importa?

| | Red Teaming clásico | AI Control (este proyecto) |
|---|---|---|
| Pregunta que responde | ¿Puedo hacer que el modelo haga algo malo? | ¿El protocolo de supervisión atrapa al modelo cuando hace algo malo? |
| Qué se optimiza/varía | El ataque (el prompt, la inyección) | El protocolo (reglas, monitoreo, aprobación humana) |
| Analogía | Probar si un ladrón puede entrar | Probar si las cámaras lo detectan cuando entra |

## Estructura del repo

```
control-eval-harness/
├── README.md                          ← estás acá
├── GLOSARIO.md                        ← términos explicados en una frase
├── COMO_LEER_ESTE_REPO.md             ← guía de navegación según quién sos
├── LICENSE
├── requirements.txt
├── scenarios/                         ← escenarios de ataque, organizados por vertical OWASP ASI
│   ├── schema.json                    ← formato formal de un escenario
│   ├── asi01_goal_hijack/
│   ├── asi02_tool_misuse/
│   ├── asi03_identity_privilege/
│   ├── asi06_memory_poisoning/
│   ├── asi09_human_trust/
│   └── asi10_rogue_agent/
├── ground_truth/                      ← veredictos correctos, separados de los escenarios
├── walkthroughs/                      ← explicación narrada de cada escenario, en lenguaje llano
├── protocols/                         ← los protocolos de control evaluados
│   ├── no_supervision.py
│   ├── rule_based_monitor.py
│   └── human_in_loop_sim.py
├── external_validation/               ← validación cruzada contra R-Judge (dataset académico externo)
├── analysis/
│   ├── coverage_chart.py              ← Chart 1: cobertura de diseño (spider chart)
│   ├── performance_chart.py           ← Chart 2: desempeño de protocolos (spider chart)
│   └── results/
└── generate_scenario.py               ← script usado para generar escenarios vía API (uso puntual y acotado)
```

## Las seis verticales de riesgo evaluadas

Basadas en el [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/) (ASI01–ASI10), filtradas a las que son viables de simular con un solo agente sandboxeado, sin infraestructura multi-agente ni de producción:

- **ASI01** — Agent Goal Hijack
- **ASI02** — Tool Misuse & Exploitation
- **ASI03** — Identity & Privilege Abuse
- **ASI06** — Memory Poisoning
- **ASI09** — Human-Agent Trust Exploitation
- **ASI10** — Rogue Agents (versión simplificada)

Cuatro verticales del estándar completo (ASI04 Supply Chain, ASI05 Code Execution/RCE, ASI07 Inter-Agent Communication, ASI08 Cascading Failures) quedan **explícitamente fuera de alcance** por requerir infraestructura multi-agente o de producción real que este proyecto, deliberadamente acotado en presupuesto y cómputo, no cubre. Documentado como trabajo futuro, no ocultado.

## Metodología en una frase

Cada escenario se diseña respondiendo seis preguntas (tarea legítima → presión/vector → punto de decisión → acción observable → rastro disponible → protocolo que lo atraparía), y se evalúa contra tres protocolos de control (sin supervisión / monitor basado en reglas / aprobación humana simulada), midiendo si cada uno detecta la violación en el punto exacto donde ocurre.

## Restricciones de reproducibilidad (por diseño, no por accidente)

- **Costo:** el uso de API de pago está acotado a la generación puntual de escenarios (1-2 llamadas por escenario), nunca a la evaluación de protocolos, que corre 100% local sobre datos ya generados.
- **Cómputo:** los protocolos de control son basados en reglas (Python puro), no requieren GPU ni modelos locales pesados — corren en cualquier máquina, incluidas las de gama baja.
- **Validación externa:** se usa [R-Judge](https://github.com/Lordog/R-Judge) (Yuan et al., EMNLP Findings 2024) como set de contraste, bajo licencia CC BY-NC-SA — ver nota de licencia en `external_validation/`.

## Limitaciones honestas

- N chico de escenarios por vertical (diseño curado a mano, no generación masiva) — prioriza profundidad sobre volumen.
- Los "protocolos de control" son simulaciones simplificadas, no productos de producción.
- Ver cada `walkthroughs/*.md` para limitaciones específicas de cada escenario.

## Roadmap de este repo

Este proyecto es el ancla del Bloque 2 (meses 4-6) de un plan de transición de carrera hacia roles de AI Safety / Red Teaming / Safeguards. Se actualiza de forma incremental — ver estado actual de cobertura corriendo `analysis/coverage_chart.py`.
