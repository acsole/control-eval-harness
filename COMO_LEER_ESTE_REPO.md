# Cómo leer este repo, según quién sos

## Si tenés 30 segundos (reclutador/a)

Leé la sección "¿Qué es esto?" del [`README.md`](./README.md). Eso alcanza para entender el propósito del proyecto.

## Si tenés 5 minutos (hiring manager, no necesariamente técnico)

1. [`README.md`](./README.md) completo.
2. Un [`walkthroughs/*.md`](./walkthroughs/) — cada uno cuenta un caso de punta a punta (ataque, riesgo de negocio, cómo respondió cada protocolo, remediación propuesta) en lenguaje llano.

## Si sos técnico y querés correr el código

1. `requirements.txt` para dependencias.
2. `scenarios/schema.json` para el formato de datos.
3. `protocols/` para la lógica de cada protocolo evaluado.
4. `analysis/coverage_chart.py` para regenerar el gráfico de cobertura de diseño en cualquier momento.

## Si querés evaluar un protocolo "a ciegas" (sin ver la respuesta)

Usá únicamente los archivos de `scenarios/` — el veredicto correcto está deliberadamente separado en `ground_truth/`, referenciado por `id`, para que puedas correr tu propio criterio antes de comparar contra el mío.

## Si no sabés nada de AI Safety / Red Teaming

Empezá por [`GLOSARIO.md`](./GLOSARIO.md), después volvé a cualquiera de los puntos anteriores.
