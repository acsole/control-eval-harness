# Cómo leer este repo, según quién sos

## Si tenés 30 segundos (reclutador/a)

Leé la sección "¿Qué es esto?" del [`README.md`](../README.md). Eso alcanza para entender el propósito del proyecto.

## Si tenés 5 minutos (hiring manager, no necesariamente técnico)

1. [`README.md`](../README.md) completo.
2. Un [`walkthroughs/*.md`](./walkthroughs/) - cada uno cuenta un caso de punta a punta (ataque, riesgo de negocio, cómo respondió cada protocolo, remediación propuesta) en lenguaje llano.

## Si sos técnico y querés correr el código

1. [`PASO_A_PASO_REPRODUCIR.md`](./PASO_A_PASO_REPRODUCIR.md) para instalar y correr todo, con la salida esperada.
2. `requirements.txt` para dependencias.
3. `scenarios/schema.json` y `ground_truth/schema.json` para el formato de los datos.
4. `protocols/` para la lógica de cada protocolo evaluado.
5. `tests/test_harness.py` para ver qué comportamiento está garantizado (y qué huecos están documentados a propósito).
6. `analysis/coverage_chart.py` para regenerar el gráfico de cobertura de diseño en cualquier momento.

## Si querés aprender a construir un escenario nuevo

1. [`COMO_SE_CONSTRUYE_UN_ESCENARIO.md`](./COMO_SE_CONSTRUYE_UN_ESCENARIO.md): el razonamiento completo, paso a paso, con ASI03 como ejemplo resuelto.
2. [`GEMELO_INOCENTE.md`](./GEMELO_INOCENTE.md): por qué cada caso con falta tiene un par legítimo.

## Si querés evaluar un protocolo "a ciegas" (sin ver la respuesta)

Usá únicamente los archivos de `scenarios/` - el veredicto correcto está deliberadamente separado en `ground_truth/`, referenciado por `id`, para que puedas correr tu propio criterio antes de comparar contra el mío. Ojo: algunos escenarios son legítimos a propósito (gemelos inocentes); no todos contienen una falta.

## Si no sabés nada de AI Safety / Red Teaming

Empezá por [`GLOSARIO.md`](./GLOSARIO.md), después volvé a cualquiera de los puntos anteriores.
