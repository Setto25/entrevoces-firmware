# Estado del proyecto EntreVoces

**Última actualización:** 2026-08-18  
**Zona horaria:** America/Santiago  
**Estado general:** H1 de backend, simulador y sesión temporal verificado; cliente HTTP de firmware preparado y validación física H2 pendiente  
**Fase activa:** H2 — validación de hardware por piezas

## 1. Objetivo vigente

Construir en pocos días un MVP demostrable de EntreVoces: una persona mayor pulsa un botón, graba voz, envía el audio al servidor, recibe una respuesta y la escucha en el dispositivo físico. Sobre ese corte vertical se incorpora el intercambio de saludos entre Elena y Tomás.

## 2. Alcance priorizado

### Obligatorio para declarar el MVP

- Simulador Python y dispositivo físico compatibles con el mismo contrato HTTP.
- Máquina de estados recuperable: listo, escuchando, enviando, procesando, reproduciendo y error.
- Captura WAV PCM de 16 kHz, mono y 16 bits.
- Envío del audio a FastAPI mediante HTTPS o HTTP local durante el banco de pruebas.
- Respuesta de audio descargable y reproducible.
- Autenticación básica del dispositivo sin secretos de infraestructura en el firmware.
- Flujo social mínimo Elena → Tomás → Elena con moderación previa a la publicación.
- Registro de las pruebas y de las decisiones técnicas.

### Importante si el plazo lo permite

- STT y TTS reales mediante proveedores desacoplados.
- Aplicación Flutter mínima para bandeja, reproducción y grabación de saludos.
- Embeddings y búsqueda semántica con PostgreSQL + pgvector.
- Agente con herramientas restringidas.

### Fuera del MVP inmediato

- RAG de síntesis comunitaria.
- Streaming WebSocket o audio full-duplex.
- Wake word permanente.
- Animaciones complejas del avatar.
- Batería integrada y carcasa definitiva antes de estabilizar el banco de pruebas.
- Sistemas multiagente, microservicios o Kubernetes.

## 3. Hardware confirmado

- Seeed Studio XIAO ESP32-S3 Sense.
- Micrófono PDM integrado en la placa Sense.
- Pantalla TFT LCD de 2 pulgadas, ST7789V, 240 × 320, SPI.
- DAC GY-PCM5102A por I2S.
- Amplificador PAM8403.
- Parlantes reciclados de una consola SUP/Game.
- Batería reciclada de la misma consola.
- Pulsador físico de dos pines.
- Protoboard GL-12 y jumpers.

## 4. Decisiones vigentes

1. El simulador se construye al inicio y no después del backend completo.
2. El simulador y el firmware consumen el mismo contrato de API.
3. El primer transporte usa audio completo por HTTP; no usa streaming.
4. El servidor toma las decisiones sociales, de identidad y autorización.
5. El LLM interpreta lenguaje, pero no selecciona identificadores sensibles ni accede a PostgreSQL.
6. Todo contenido social pasa por moderación antes de publicarse.
7. PostgreSQL + pgvector concentra datos relacionales y búsqueda vectorial.
8. Los audios se guardan fuera de PostgreSQL; la base conserva metadatos y referencias.
9. Los proveedores de STT, TTS, embeddings, moderación y LLM se abstraen mediante interfaces.
10. Todos los nombres creados para archivos, módulos, clases, modelos, esquemas y routers se escriben en español.
11. `AGENTS.md`, `PROJECT_STATE.md`, `.agents/skills`, `SKILL.md`, `agents/openai.yaml`, `main.py` y `diagram.json` constituyen excepciones nominales explícitas porque son nombres técnicos obligatorios para control, descubrimiento de Skills o ejecución de Wokwi y MicroPython.
12. Los comentarios y docstrings del código se escriben en español y en tercera persona del singular.
13. La batería reciclada no se conecta hasta verificar tipo, tensión, polaridad, estado físico y compatibilidad con carga.
14. El mapa definitivo de GPIO se decide después de inspeccionar las placas reales y comprobar conflictos.
15. El firmware de aplicación se implementa en MicroPython sobre ESP32-S3.
16. La captura del micrófono PDM se trata como prueba técnica temprana porque `machine.I2S` no documenta oficialmente modo PDM; si el firmware estándar no lo expone, se mantiene MicroPython y se utiliza un módulo nativo mínimo o una compilación personalizada como adaptador.

## 5. Artefactos de documentación

- `AGENTS.md`: reglas permanentes reconocibles por los agentes de desarrollo.
- `.agents/skills/`: Skills reutilizables y locales del repositorio.
- `documentacion/INDICE_DOCUMENTACION.md`: puerta de entrada a la documentación.
- `documentacion/PLAN_DESARROLLO_MVP.md`: hitos, tareas, prioridades y criterios de aceptación.
- `documentacion/DOCUMENTACION_TECNICA.md`: arquitectura, flujos, ubicación y contratos.
- `documentacion/PROMPT_SISTEMA_IA.md`: reglas para una IA que continúe el proyecto.
- `documentacion/REGISTRO_CAMBIOS.md`: historial cronológico inmutable.

## 6. Implementado hasta ahora

- Se revisó el informe maestro de arquitectura versión 3.0.
- Se confirmó el hardware disponible o planificado.
- Se priorizó el corte vertical voz–nube–voz.
- Se definió el plan acelerado por hitos y criterios de salida.
- Se creó el conjunto inicial de documentación viva.
- Se crearon y validaron siete Skills locales para audio, hardware, E2E, agente, backend, firmware y cierre documental.
- Se probaron los scripts de generación e inspección WAV y el verificador de memoria del proyecto con Python 3.13.7.
- Se aprobó MicroPython como tecnología del dispositivo y se registró la captura PDM como riesgo técnico prioritario.
- Se implementó un simulador Wokwi inicial del XIAO ESP32-S3 con pulsador virtual, antirrebote y máquina de estados reutilizable.
- Se corrigió la configuración de Wokwi agregando `wokwi.toml` como archivo requerido por la plantilla MicroPython de ESP32-S3 y dejando el firmware compatible en la raíz del proyecto.
- Se verificó mediante pruebas automatizadas el recorrido `LISTO → ESCUCHANDO → ENVIANDO → PROCESANDO → REPRODUCIENDO → LISTO` y la recuperación desde `ERROR`.
- Se creó el proyecto Python administrado por `uv`, aislado completamente en `servidor/` con `servidor/.venv`, `servidor/pyproject.toml` y versiones resueltas en `servidor/uv.lock`.
- Se implementó FastAPI con salud, validación de WAV, procesamiento determinista de turno y descarga de un WAV fijo.
- Se verificaron seis pruebas de contrato y errores del backend.
- Se completó la reorganización del backend: los imports internos usan `aplicacion.*`, las pruebas de contrato están en `servidor/pruebas` y se recreó `servidor/.venv`.
- Se completó la separación física de componentes: las pruebas del simulador viven en `simulador/pruebas`, el código Wokwi en `simulador/wokwi_dispositivo`, el firmware queda en `dispositivo/` y el cliente futuro en `aplicacion_movil/`; se eliminó el entorno `.venv` duplicado de raíz.
- Se implementó el simulador HTTP local en `simulador/cliente_http.py`: genera o recibe un WAV PCM, lo envía al contrato v1, interpreta exclusivamente `REPRODUCIR_AUDIO`, descarga y valida la respuesta, permite reproducirla en Windows y recupera el estado `LISTO` ante red, timeout o respuesta inválida.
- Se verificó un turno con HTTP real contra Uvicorn local y la integración en memoria entre el simulador y FastAPI.
- Se implementó autenticación mínima del dispositivo mediante credencial de entorno, sesión temporal opaca de 15 minutos, validación obligatoria en carga de audio y revocación explícita al cerrar el turno.
- Se verificó el recorrido HTTP real de inicio de sesión, carga de audio, descarga y cierre de sesión sin persistir credenciales en el repositorio ni en el simulador.
- Se preparó el cliente HTTP compatible con MicroPython en `dispositivo/micropython/`: inicia y cierra sesión, sube WAV multipart, acepta solo `REPRODUCIR_AUDIO`, valida encabezado RIFF y libera respuestas HTTP.
- Se conectó `ENVIANDO` con el cliente HTTP mediante un controlador de turno que recupera `LISTO` ante red, servidor o contrato inválido. La evidencia actual es una prueba CPython con transporte controlado; ninguna capacidad física se considera validada todavía.

No existe todavía persistencia de sesiones, registro de dispositivos, firmware para periféricos reales ni Flutter.

## 7. Tecnologías decididas

- Python, FastAPI, Pydantic, SQLAlchemy y Alembic.
- Entorno `uv` 0.11.28 con Python 3.13.7.
- FastAPI 0.141.1, Pydantic 2.13.4, Uvicorn 0.52.3 y pytest 9.1.1 para el corte H1 inicial.
- `uv sync --group desarrollo` y `uv run pytest` se ejecutan desde `servidor/`; el arranque local usa `uv run uvicorn aplicacion.aplicacion:aplicacion --reload`. La variable de proceso `ENTREVOCES_CREDENCIAL_DISPOSITIVO` debe configurarse antes de arrancar. Las pruebas de lógica se ejecutan desde la raíz con `python -m unittest dispositivo/pruebas/prueba_cliente_http.py simulador/pruebas/prueba_nucleo_estados.py simulador/pruebas/prueba_cliente_http.py`. El turno local usa `python simulador/cliente_http.py --url-base http://127.0.0.1:8000 --generar-entrada --entrada ruta/entrada.wav --salida ruta/respuesta.wav --reproducir`; el simulador toma la credencial de la misma variable de entorno o del argumento efímero `--credencial-dispositivo`.
- PostgreSQL con pgvector.
- Object Storage; se admite almacenamiento local durante el primer corte.
- Flutter para la aplicación móvil.
- MicroPython para la lógica y los controladores del dispositivo.
- Módulo nativo mínimo o compilación personalizada de MicroPython solo si la prueba PDM demuestra que el firmware estándar no puede capturar el micrófono integrado.
- WAV PCM de 16 kHz, mono y 16 bits.
- HTTP por lotes para el primer MVP.
- Skills locales según el estándar de Codex, con `SKILL.md`, metadatos de interfaz, referencias y scripts deterministas donde corresponda.

## 8. Siguiente paso lógico

Continuar H1:

1. Ejecutar H2.0 a H2.2 con la placa: fijar MicroPython, capturar REPL y comprobar Wi-Fi contra `/api/v1/salud`.
2. Probar I2S TX y PDM por separado; PDM no se asume hasta capturar un WAV comprobable.
3. Copiar y ejecutar el cliente HTTP solo después de confirmar red y memoria suficientes.
4. Reemplazar el almacén de sesiones en memoria por persistencia cuando se incorpore PostgreSQL.

En paralelo con H1, ejecutar al disponer del hardware una prueba corta de MicroPython: REPL, GPIO, Wi‑Fi, PSRAM, I2S TX y captura PDM. La prueba PDM debe resolverse antes de construir el firmware conversacional completo.

## 9. Protocolo obligatorio de actualización

Después de completar cada módulo se actualiza este archivo con:

1. qué se implementó;
2. qué tecnologías y versiones se utilizaron;
3. dónde quedó cada componente;
4. cómo se ejecuta y cómo se verifica;
5. qué pruebas pasaron o fallaron;
6. qué decisión cambió y por qué;
7. cuál es el siguiente paso lógico.

El detalle histórico se agrega, sin reescribir entradas anteriores, en `documentacion/REGISTRO_CAMBIOS.md`.

## 10. Bloqueos y datos pendientes

- Falta inspeccionar las etiquetas, impedancia y potencia de los parlantes reciclados.
- Falta medir la batería y confirmar que sea una celda recargable de litio de 3,7 V en buen estado.
- Falta inspeccionar el pinout impreso de la pantalla ST7789V y del PCM5102A.
- Falta elegir proveedores iniciales de STT, TTS, LLM, embeddings y moderación.
- Falta decidir si el primer despliegue remoto usa Railway desde H1 o después del corte local estable.
- Falta verificar en la placa si el firmware MicroPython elegido expone captura PDM; la API oficial `machine.I2S` documenta I2S estándar como vista previa técnica, pero no documenta PDM.
