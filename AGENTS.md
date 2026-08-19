# Instrucciones permanentes de EntreVoces

## 1. Estilo de código y documentación

- Todos los nombres creados para archivos, carpetas, módulos, clases, esquemas, modelos y routers deben escribirse obligatoriamente en español.
- No se deben mezclar idiomas en nombres propios del proyecto.
- `AGENTS.md`, `PROJECT_STATE.md`, `.agents/skills`, `SKILL.md`, `agents/openai.yaml`, `main.py`, `diagram.json`, `pyproject.toml`, `uv.lock`, `.python-version` y `.venv` se conservan como excepciones porque constituyen nombres técnicos exigidos para el control, descubrimiento de Skills, ejecución de Wokwi/MicroPython o gestión del entorno con `uv`.
- Si una herramienta impone otro nombre técnico no configurable, se debe documentar la excepción antes de crearlo.
- Todo código Python debe usar type hints explícitos.
- Todo código TypeScript y Dart debe usar tipos explícitos; no se debe usar `any` o equivalentes sin una justificación documentada.
- Todos los comentarios y docstrings deben escribirse en español y siempre en tercera persona del singular.

Ejemplo correcto:

```python
def cumple_limite(duracion_ms: int, maximo_ms: int) -> bool:
    """Determina si el audio respeta el límite configurado."""
    return 0 < duracion_ms <= maximo_ms
```

## 2. Memoria y continuidad

- Se debe leer `PROJECT_STATE.md` antes de sugerir o modificar código.
- Después de terminar un módulo o recibir aprobación del usuario, se debe actualizar `PROJECT_STATE.md` con lo implementado, las tecnologías y versiones utilizadas, la ubicación, la forma de verificarlo y el siguiente paso lógico.
- Se debe agregar una entrada cronológica en `documentacion/REGISTRO_CAMBIOS.md` sin borrar entradas anteriores.
- Se debe actualizar el estado real de las tareas en `documentacion/PLAN_DESARROLLO_MVP.md`.
- Se debe mantener `documentacion/DOCUMENTACION_TECNICA.md` sincronizado con la implementación comprobada.

## 3. Arquitectura y seguridad

- Los clientes no deben acceder directamente a PostgreSQL.
- El LLM no debe acceder directamente a PostgreSQL, storage, secretos o código arbitrario.
- El backend debe resolver identidad, permisos y destinatarios mediante la sesión autenticada.
- Todo contenido social debe pasar por moderación antes de publicarse.
- Si la moderación falla, el contenido debe quedar sin publicar.
- Los audios grandes deben almacenarse fuera de PostgreSQL.
- El simulador y el firmware deben consumir el mismo contrato versionado.
- El primer MVP debe usar WAV PCM de 16 kHz, mono y 16 bits mediante HTTP por archivo completo.

## 4. Prioridad del MVP

Se protege este orden:

1. backend y simulador;
2. pruebas físicas aisladas;
3. voz–nube–voz en el ESP32;
4. flujo social determinista;
5. STT, TTS y moderación;
6. Flutter mínimo;
7. búsqueda semántica y agente limitado.

RAG, streaming, wake word, multiagentes, microservicios, batería definitiva y carcasa quedan fuera mientras el corte vertical no esté estable.

## 5. Definición de terminado

Un módulo solo se considera terminado cuando el código está implementado, las pruebas pertinentes pasan, existe una forma reproducible de ejecutarlo y la documentación de estado, funcionamiento y cambios se encuentra actualizada.

## 6. Skills del proyecto

- Se deben consultar las Skills locales en `.agents/skills` cuando la tarea coincida con su descripción o el usuario las invoque explícitamente.
- Se debe leer completamente el `SKILL.md` seleccionado antes de actuar.
- Se deben resolver scripts y referencias desde el directorio de la Skill correspondiente.
- Se debe usar `$cerrar-modulo-entrevoces` después de completar y verificar un módulo.
