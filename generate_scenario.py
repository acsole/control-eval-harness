"""
Genera el/los turno(s) críticos de un escenario vía API, dado un template
escrito a mano con el resto de la trayectoria fija.

Diseño deliberado para controlar costo: NO genera la trayectoria completa.
El humano escribe task_context, los turnos de usuario y de ambiente
(incluida cualquier inyección). La API se llama únicamente para generar
la respuesta del agente en el/los turno(s) marcados como "a completar",
típicamente 1-2 llamadas por escenario.

Uso esperado: correr este script una vez por escenario nuevo, revisar el
resultado a mano, y commitear el JSON final a scenarios/. No se re-corre
en cada evaluación de protocolo — eso es responsabilidad de protocols/*.py,
que operan 100% sobre los JSON ya generados y versionados.

Estado: PENDIENTE de primera ejecución real. asi01_001 fue diseñado
manualmente sin pasar por este script como prueba de concepto del formato;
este script formaliza el proceso para los escenarios siguientes.
"""

import json
import os

# TODO: instalar el SDK oficial (pip install anthropic) y setear
# ANTHROPIC_API_KEY como variable de entorno antes de usar este script.
# import anthropic

MODEL = "claude-sonnet-4-6"  # TODO: confirmar el modelo más económico que
                              # cumpla el propósito antes de correr el batch completo.


def generate_agent_turn(task_context: str, prior_turns: list[dict]) -> str:
    """
    Genera un único turno de 'assistant' dado el contexto de la tarea y los
    turnos previos de la trayectoria (incluida cualquier inyección ya presente
    en un turno de 'environment' anterior).

    Args:
        task_context: descripción del rol/herramientas del agente en este escenario.
        prior_turns: lista de turnos previos en formato {"role": ..., "content": ...}

    Returns:
        El texto del turno generado por el modelo.
    """
    # TODO: implementar la llamada real. Ejemplo de estructura:
    #
    # client = anthropic.Anthropic()
    # response = client.messages.create(
    #     model=MODEL,
    #     max_tokens=500,
    #     system=task_context,
    #     messages=[{"role": t["role"] if t["role"] != "environment" else "user",
    #                 "content": t["content"]} for t in prior_turns],
    # )
    # return response.content[0].text
    raise NotImplementedError("Pendiente de primera implementación real.")


if __name__ == "__main__":
    # TODO: loop sobre templates/ (carpeta pendiente de crear) con la parte
    # fija de cada escenario nuevo, llamar a generate_agent_turn() para el/los
    # turno(s) crítico(s), y guardar el resultado en scenarios/{vertical}/.
    pass
