# Glosario

Cada término explicado en una frase, pensado para alguien que nunca leyó sobre AI Safety o Red Teaming.

**Agente (agent)**: Un asistente de IA que no solo responde texto, sino que puede usar herramientas (buscar en la web, enviar correos, ejecutar comandos) para cumplir una tarea por su cuenta.

**AI Control**: Disciplina que evalúa si los sistemas que supervisan a un agente de IA funcionan, asumiendo que el agente en sí puede fallar o ser manipulado. Distinto de "romper" al modelo: acá se evalúa lo que lo rodea.

**Allow-list (lista blanca)**: Una regla que solo permite explícitamente las acciones/destinos autorizados, en vez de tratar de bloquear los prohibidos uno por uno.

**ASR (Attack Success Rate)**: Porcentaje de intentos de ataque que lograron su objetivo. Métrica típica del red teaming clásico, el que ataca al modelo.

**Checkpoint**: El turno exacto de una conversación/trayectoria donde el agente toma la decisión que nos interesa evaluar (por ejemplo, el momento en que decide a quién enviar un correo).

**Control evaluation (evaluación de control)**: Medir si un protocolo de supervisión detecta comportamiento no autorizado de un agente, sin importar por qué el agente llegó a ese comportamiento.

**Ground truth**: La respuesta "correcta" verificada por una persona, contra la cual se compara el veredicto de un protocolo automatizado.

**Human-in-the-loop**: Protocolo de control donde una acción sensible queda pausada hasta que un humano la aprueba explícitamente.

**Injection (inyección de prompt)**: Instrucción maliciosa escondida dentro de contenido que el agente consulta (una página web, un documento), que intenta redirigir su comportamiento sin que el usuario lo haya pedido.

**OWASP ASI (Agentic Application Security Initiative)**: Estándar público (OWASP Top 10 for Agentic Applications) que cataloga las categorías de riesgo más comunes en sistemas de agentes de IA.

**Protocolo de control**: El sistema de reglas o supervisión (automatizado o humano) que revisa lo que el agente está por hacer o ya hizo, y decide si intervenir.

**Red teaming (clásico)**: Disciplina que evalúa si un modelo de IA puede ser manipulado para hacer algo no deseado. Ataca al modelo, no al sistema que lo supervisa.

**Sandbox**: Entorno aislado y controlado donde el agente puede "actuar" (usar herramientas simuladas) sin riesgo real, porque nada de lo que hace tiene efecto fuera de ese entorno.

**Spider chart / radar chart**: Gráfico con varios ejes (uno por categoría) que permite ver de un vistazo qué tan cubierta o bien evaluada está cada categoría. Este proyecto usa dos: uno de cobertura de diseño (¿cuántos escenarios buenos tengo por categoría?) y uno de desempeño (¿qué tan bien detectó cada protocolo las violaciones por categoría?).

**Trayectoria (trajectory)**: La secuencia completa de turnos (usuario, agente, ambiente) que compone un escenario, de principio a fin.
