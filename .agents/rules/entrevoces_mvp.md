# Reglas permanentes del MVP EntreVoces

Esta regla debe configurarse como **Always On** en Antigravity para el espacio de trabajo. Complementa `AGENTS.md`, no lo reemplaza.

## Inicio obligatorio

Antes de proponer o editar código se leen por completo, en este orden:

1. `AGENTS.md`;
2. `PROJECT_STATE.md`;
3. `documentacion/INDICE_DOCUMENTACION.md`;
4. el hito activo en `documentacion/PLAN_DESARROLLO_MVP.md`;
5. la documentación técnica pertinente y las últimas entradas de `documentacion/REGISTRO_CAMBIOS.md`;
6. el árbol real y el estado de Git.

Se consulta una Skill en `.agents/skills/` cuando la solicitud coincide con su descripción. Se lee completo su `SKILL.md` y las referencias obligatorias antes de actuar.

## Invariantes no negociables

- Todos los nombres propios nuevos del proyecto se escriben en español, salvo los nombres técnicos enumerados en `AGENTS.md`.
- Python usa anotaciones de tipo explícitas. TypeScript y Dart usan tipos explícitos; no se usa `any` ni equivalentes sin justificación documentada.
- Comentarios y docstrings se escriben en español y en tercera persona del singular.
- Clientes y LLM no acceden directamente a PostgreSQL, almacenamiento, secretos ni ejecución arbitraria.
- El backend obtiene identidad, propietario y destinatario desde la sesión autenticada.
- Todo contenido social se modera antes de publicarse. Si la moderación falla, permanece sin publicar.
- Los audios grandes no se almacenan en las tablas principales de PostgreSQL.
- Simulador y firmware consumen el mismo contrato versionado: WAV PCM, 16 kHz, mono, 16 bits y HTTP por archivo completo.

## Prioridad y cierre

Se mantiene el orden del MVP: backend y simulador, pruebas físicas aisladas, voz–nube–voz, flujo social determinista, STT/TTS y moderación, Flutter, búsqueda semántica y agente restringido. No se adelantan RAG, streaming, wake word, multiagentes ni infraestructura compleja.

Un módulo terminado actualiza `PROJECT_STATE.md`, el plan, la documentación técnica y el registro de cambios, y conserva pruebas reproducibles. No se declara verificado lo que no tenga evidencia observable.
