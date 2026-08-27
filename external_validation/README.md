# Validación externa — R-Judge

**Estado: PENDIENTE de incorporación.** Esta carpeta va a contener un subset
de R-Judge usado como set de contraste independiente: ¿el protocolo de
reglas diseñado sobre escenarios propios también coincide con el consenso
humano de qué es inseguro en un benchmark académico ajeno?

## Qué es R-Judge

Dataset de 569 registros de interacción de agentes multi-turno, etiquetados
por consenso humano como seguros/inseguros, con foco en conciencia de riesgo
de agentes LLM ante múltiples tipos de ataque, incluida inyección de
instrucciones.

- Paper: Yuan et al., "R-Judge: Benchmarking Safety Risk Awareness for LLM
  Agents", EMNLP Findings 2024.
- Repositorio: https://github.com/Lordog/R-Judge

## Aviso de licencia — IMPORTANTE

R-Judge está publicado bajo licencia **CC BY-NC-SA** (Atribución -
NoComercial - CompartirIgual). Esto significa:

- Se puede usar y compartir con fines no comerciales (como este proyecto de
  portafolio), citando la fuente.
- **No** puede usarse en ningún contexto comercial ni remunerado sin permiso
  adicional de los autores originales.
- Cualquier trabajo derivado debe distribuirse bajo la misma licencia.

Este proyecto usa R-Judge exclusivamente como material de validación
cruzada para fines educativos/de portafolio, con atribución explícita, en
cumplimiento de estos términos.

## Pendiente

- [ ] Descargar el subset relevante de R-Judge (casos que involucren
      inyección de instrucciones, para comparabilidad con las verticales
      ASI01/ASI06 de este proyecto).
- [ ] Documentar cuántos registros se usaron y con qué criterio de selección.
- [ ] Correr `protocols/rule_based_monitor.py` sobre el subset y comparar
      contra el label de consenso humano de R-Judge.
- [ ] Documentar resultados y discrepancias en un walkthrough dedicado.
