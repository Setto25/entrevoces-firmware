# Registro de cambios de EntreVoces

**Formato:** historial cronológico, acumulativo y sin eliminación de entradas  
**Zona horaria:** America/Santiago

## Convenciones

Cada entrada indica:

- fecha y versión;
- tipo de cambio;
- qué se cambió;
- tecnologías utilizadas;
- ubicación;
- verificación realizada;
- decisiones o riesgos;
- siguiente paso.

Estados de verificación:

- `VERIFICADO`: existe evidencia reproducible.
- `PARCIAL`: solo una parte cuenta con evidencia.
- `NO_VERIFICADO`: diseño o documentación todavía no implementada.

## 2026-08-17 — Versión documental 0.1

**Tipo:** planificación y arquitectura  
**Verificación:** VERIFICADO para existencia documental; NO_VERIFICADO para software y hardware

### Cambios

- Se revisó el informe maestro de arquitectura versión 3.0.
- Se confirmó la pantalla ST7789V de 2 pulgadas y 240 × 320.
- Se registró que los parlantes y la batería provendrán de una consola SUP/Game.
- Se adelantó el simulador al primer hito de implementación.
- Se priorizó el corte vertical voz–nube–voz.
- Se definió un plan acelerado de cinco jornadas ajustables.
- Se creó un prompt de sistema para continuidad entre IA.
- Se creó la documentación técnica viva.
- Se creó `AGENTS.md` para conservar las reglas permanentes dentro del proyecto real.
- Se creó `PROJECT_STATE.md` como memoria operativa.

### Tecnologías consideradas

- Markdown para documentación.
- Python y FastAPI para el backend y simulador previstos.
- PostgreSQL + pgvector para persistencia prevista.
- PlatformIO y Arduino Framework para firmware previsto.
- Flutter para cliente público previsto.

### Ubicación

- `AGENTS.md`
- `PROJECT_STATE.md`
- `documentacion/INDICE_DOCUMENTACION.md`
- `documentacion/PLAN_DESARROLLO_MVP.md`
- `documentacion/DOCUMENTACION_TECNICA.md`
- `documentacion/PROMPT_SISTEMA_IA.md`
- `documentacion/REGISTRO_CAMBIOS.md`

### Verificación realizada

- Se comprobó que el espacio de trabajo no contenía código previo.
- Se consultó documentación oficial de Seeed para micrófono y batería.
- No se ejecutaron pruebas de software ni hardware porque todavía no existen módulos implementados.

### Decisiones y riesgos

- La batería reciclada queda bloqueada hasta su identificación y medición.
- La asignación de GPIO queda pendiente de inspección física.
- RAG y streaming quedan fuera del MVP inmediato.
- Flutter y búsqueda semántica pueden reducirse antes de sacrificar el recorrido físico.

### Siguiente paso

Implementar H1: FastAPI mínimo, contrato tipado, respuesta de audio fija y simulador Python.

---

## 2026-08-18 — Versión documental 0.2

**Tipo:** implementación de herramientas de desarrollo  
**Verificación:** VERIFICADO

### Cambios

- Se crearon siete Skills locales de alcance repositorio.
- Se añadieron flujos para validar audio, diagnosticar hardware, ejecutar E2E y evaluar el agente.
- Se añadieron Skills de desarrollo para backend y firmware.
- Se añadió una Skill de cierre documental de módulos.
- Se documentaron `.agents/skills`, `SKILL.md` y `agents/openai.yaml` como nombres técnicos obligatorios.

### Tecnologías y versiones

- Python 3.13.7.
- Formato Agent Skills con manifiestos `SKILL.md`.
- Metadatos de interfaz `agents/openai.yaml`.
- Biblioteca estándar de Python para WAV, JSON y verificación de archivos.

### Ubicación

- `.agents/skills/validar-audio-dispositivo`
- `.agents/skills/diagnosticar-hardware-entrevoces`
- `.agents/skills/probar-e2e-entrevoces`
- `.agents/skills/evaluar-agente-entrevoces`
- `.agents/skills/desarrollar-backend-entrevoces`
- `.agents/skills/desarrollar-firmware-entrevoces`
- `.agents/skills/cerrar-modulo-entrevoces`

### Ejecución y verificación

- Las siete Skills pasaron `quick_validate.py` del creador oficial.
- El generador produjo un WAV PCM mono de 16 kHz y 16 bits de 0,25 segundos.
- El inspector reconoció 4.000 fotogramas, 16 bits, 16 kHz, un canal y PCM sin compresión.
- El verificador de memoria aprobó la estructura documental del proyecto.

### Decisiones, riesgos y deuda

- Solo las tareas que necesitan comportamiento determinista incorporan scripts.
- Las Skills E2E y de agente contienen referencias, pero los ejecutores específicos se añadirán cuando existan API y agente reales.
- La creación de Skills no cambia el hito activo H1.

### Siguiente paso

Implementar H1 usando `$desarrollar-backend-entrevoces` y validar el primer WAV con `$validar-audio-dispositivo`.

---

## 2026-08-18 — Versión documental 0.3

**Tipo:** decisión tecnológica y mitigación de riesgo  
**Verificación:** PARCIAL

### Cambios

- Se adoptó MicroPython como tecnología principal del dispositivo.
- Se eliminó Arduino Framework/PlatformIO como decisión arquitectónica vigente.
- Se actualizó la Skill de firmware para trabajar con MicroPython.
- Se agregó una prueba temprana obligatoria de REPL, memoria, Wi‑Fi, I2S TX y captura PDM.
- Se definió como contingencia un módulo nativo mínimo o firmware MicroPython personalizado únicamente para acceder al micrófono PDM.

### Tecnologías y versiones

- MicroPython para ESP32-S3; versión exacta pendiente de fijar al recibir y probar la placa.
- `machine.I2S`, actualmente documentado como vista previa técnica.
- Micrófono PDM del XIAO Sense en GPIO 41 y GPIO 42.

### Ubicación

- `PROJECT_STATE.md`
- `documentacion/PLAN_DESARROLLO_MVP.md`
- `documentacion/DOCUMENTACION_TECNICA.md`
- `documentacion/PROMPT_SISTEMA_IA.md`
- `.agents/skills/desarrollar-firmware-entrevoces`

### Ejecución y verificación

- Se verificó oficialmente que MicroPython soporta ESP32-S3 y proporciona `machine.I2S`.
- Se verificó que la documentación oficial de `machine.I2S` no describe modo PDM.
- Se verificó que la guía MicroPython de Seeed para XIAO ESP32-S3 Sense no incluye micrófono ni I2S.
- La captura PDM real permanece pendiente de prueba física.

### Decisiones, riesgos y deuda

- MicroPython se mantiene como lenguaje de aplicación.
- No se asume que `machine.I2S` estándar pueda capturar el micrófono integrado.
- No se autoriza construir todo el firmware sobre una hipótesis PDM no probada.

### Siguiente paso

Continuar H1 y, al disponer del hardware, ejecutar inmediatamente la prueba técnica de MicroPython/PDM.

---

## 2026-08-18 — Versión de implementación 0.4

**Tipo:** implementación de simulador de interacción  
**Verificación:** VERIFICADO para lógica local; PARCIAL para Wokwi porque falta ejecución manual en el navegador

### Cambios

- Se creó el simulador inicial de Wokwi para XIAO ESP32-S3 con un pulsador virtual.
- Se implementó la máquina de estados reutilizable `LISTO → ESCUCHANDO → ENVIANDO → PROCESANDO → REPRODUCIENDO → LISTO`.
- Se añadió antirrebote de entrada y recuperación explícita desde el estado `ERROR`.
- Se añadieron instrucciones de ejecución en navegador y pruebas automatizadas locales.

### Tecnologías y versiones

- MicroPython para la lógica del simulador.
- Wokwi con `board-xiao-esp32-s3` y `wokwi-pushbutton`.
- Python 3.13.7 y `unittest` para validar las transiciones.

### Ubicación

- `simulador/wokwi_dispositivo/`
- `pruebas/prueba_nucleo_estados.py`

### Ejecución y verificación

- Comando: `python -m unittest pruebas/prueba_nucleo_estados.py`
- Resultado esperado: tres pruebas aprobadas.
- Se validó estructuralmente el JSON del diagrama y se dejó pendiente su ejecución manual en Wokwi.

### Decisiones, riesgos y deuda

- D1/GPIO2 se usa solo como pin virtual temporal del pulsador.
- El módulo no representa captura PDM, pantalla, Wi-Fi, I2S ni audio.
- `main.py` y `diagram.json` se agregan como nombres técnicos obligatorios excepcionales a la convención de español.

### Siguiente paso

Implementar el backend FastAPI mínimo y el contrato HTTP compartido para reemplazar las demoras simuladas.

---

## 2026-08-18 — Versión correctiva 0.5

**Tipo:** corrección de configuración de simulación  
**Verificación:** VERIFICADO

### Cambios

- Se añadió el archivo `wokwi.toml` requerido por Wokwi para proyectos basados en ESP32-S3.
- Se descargó el firmware MicroPython oficial compatible con XIAO ESP32-S3 para que la simulación pueda arrancar sin errores de configuración.
- Se documentó el paso de copiar `wokwi.toml` y el firmware al proyecto de Wokwi.

### Tecnologías y versiones

- Wokwi CLI/VS Code y configuración TOML de proyecto.
- Firmware MicroPython `ESP32_GENERIC_S3-20251209-v1.27.0.bin`.
- Python 3.13.7 para verificar TOML y JSON.

### Ubicación

- `simulador/wokwi_dispositivo/wokwi.toml`
- `simulador/wokwi_dispositivo/ESP32_GENERIC_S3-20251209-v1.27.0.bin`
- `simulador/wokwi_dispositivo/INSTRUCCIONES_WOKWI.md`

### Ejecución y verificación

- Comando: `python -c "import json, tomllib; ..."`
- Resultado: `OK` y la configuración del proyecto se parsea correctamente.

### Decisiones, riesgos y deuda

- El archivo TOML se mantiene en la carpeta del simulador porque Wokwi requiere un proyecto con raíz explícita y `diagram.json` + `wokwi.toml`.
- El firmware se usa del repositorio oficial de Wokwi para mantener compatibilidad con la placa ESP32-S3 virtual.

### Siguiente paso

- Ejecutar el proyecto en el navegador Wokwi y confirmar que el monitor serie recorre la máquina de estados del simulador.

---

## 2026-08-18 — Versión de implementación 0.5

**Tipo:** implementación de backend y entorno  
**Verificación:** VERIFICADO

### Cambios

- Se creó un entorno reproducible administrado por `uv`.
- Se implementó FastAPI con salud, recepción de WAV, validación estricta, correlación y audio fijo de respuesta.
- Se definieron contratos Pydantic de salud, metadatos, comando y turno.
- Se añadió una guía de ejecución orientada a desarrollo local.

### Tecnologías y versiones

- uv 0.11.28.
- Python 3.13.7.
- FastAPI 0.141.1.
- Pydantic 2.13.4.
- Uvicorn 0.52.3.
- pytest 9.1.1.

### Ubicación

- `pyproject.toml`
- `uv.lock`
- `.venv`
- `servidor/`
- `pruebas/prueba_backend.py`
- `documentacion/GUIA_BACKEND.md`

### Ejecución y verificación

- Comando: `uv sync --group desarrollo`
- Comando: `uv run pytest`
- Resultado: seis pruebas aprobadas.
- Se verificó además la compilación sintáctica de `servidor/` y `pruebas/`.

### Decisiones, riesgos y deuda

- Los binarios recibidos no se persisten todavía.
- El audio de respuesta es un tono determinista y no TTS.
- La autenticación, las sesiones persistentes y el esquema unificado de error quedan para los siguientes cortes de H1.
- La prueba usa `TestClient`; la versión resuelta de Starlette avisa que esta integración migrará de `httpx` a `httpx2`.

### Siguiente paso

Crear el simulador HTTP local que envía un WAV, interpreta el comando y descarga la respuesta.

---

## 2026-08-18 — Reorganización del backend

**Tipo:** corrección estructural
**Verificación:** VERIFICADO

### Cambios

- Se corrigieron los imports internos y de pruebas para usar el paquete `aplicacion.*`.
- Se reubicaron las seis pruebas de contrato en `servidor/pruebas/prueba_backend.py`.
- Se recreó el entorno aislado `servidor/.venv` desde `uv.lock`.

### Tecnologías y versiones

- Python 3.13.7.
- uv 0.11.28.
- FastAPI 0.141.1 y pytest 9.1.1.

### Ubicación

- `servidor/aplicacion/`
- `servidor/pruebas/prueba_backend.py`
- `servidor/.venv`
- `documentacion/GUIA_BACKEND.md`

### Ejecución y verificación

- Directorio: `servidor/`.
- Comando: `uv sync --group desarrollo`.
- Comando: `uv run pytest`.
- Resultado: seis pruebas aprobadas.
- Comando: `uv run python -m compileall -q aplicacion pruebas`.
- Resultado: compilación e importación de `aplicacion.aplicacion` correctas.

### Decisiones, riesgos y deuda

- La ejecución de `uv` requiere acceso a su caché local; el entorno se genera correctamente una vez disponible ese acceso.
- Permanece la advertencia de deprecación de `starlette.testclient` respecto de `httpx`.

### Siguiente paso

Crear el simulador HTTP local que consume este contrato desde la nueva ubicación del backend.

---

## 2026-08-18 — Reorganización estructural consolidada

**Tipo:** corrección estructural y documentación  
**Verificación:** VERIFICADO

### Cambios

- Se confirmó que todo el backend queda bajo `servidor/`: código en `servidor/aplicacion/`, pruebas en `servidor/pruebas/`, manifiesto y bloqueo de dependencias en `servidor/` y entorno aislado en `servidor/.venv`.
- Se corrigió la ubicación de la prueba de máquina de estados a `simulador/pruebas/prueba_nucleo_estados.py` y su ruta de importación hacia `simulador/wokwi_dispositivo/`.
- Se eliminó el entorno `.venv` duplicado de la raíz.
- Se preservaron los límites de componentes: Wokwi y pruebas locales en `simulador/`, firmware en `dispositivo/` y cliente futuro en `aplicacion_movil/`.
- Se actualizaron la guía del backend, el plan, la documentación técnica y la memoria del proyecto con rutas y comandos comprobados.

### Tecnologías y versiones

- Python 3.13.7.
- uv 0.11.28.
- FastAPI 0.141.1, Pydantic 2.13.4, Uvicorn 0.52.3 y pytest 9.1.1.
- MicroPython y `unittest` para la lógica local del simulador.

### Ubicación

- `servidor/aplicacion/`
- `servidor/pruebas/`
- `servidor/.venv/`
- `simulador/pruebas/prueba_nucleo_estados.py`
- `simulador/wokwi_dispositivo/`
- `dispositivo/`
- `aplicacion_movil/`

### Ejecución y verificación

- Directorio `servidor/`: `uv run pytest` — seis pruebas aprobadas.
- Directorio `servidor/`: `uv run python -m compileall -q aplicacion pruebas` — sin errores.
- Directorio raíz: `python -m unittest simulador/pruebas/prueba_nucleo_estados.py` — tres pruebas aprobadas.
- Se verificó la importación de `aplicacion.aplicacion` desde el entorno aislado del servidor.

### Decisiones, riesgos y deuda

- La suite FastAPI emite una advertencia deprecada de `starlette.testclient` respecto a la futura migración de `httpx`; no afecta las seis pruebas aprobadas.
- El simulador HTTP de audio, las sesiones y la autenticación del dispositivo permanecen pendientes dentro de H1.

### Siguiente paso

Crear el simulador HTTP local para cargar un WAV válido, interpretar `REPRODUCIR_AUDIO`, descargar la respuesta y comprobar la recuperación ante fallos de red y timeout.

---

## 2026-08-18 — Simulador HTTP local H1

**Tipo:** implementación de simulador y prueba de integración  
**Verificación:** VERIFICADO

### Cambios

- Se añadió `simulador/cliente_http.py` como consumidor local del contrato HTTP v1.
- El simulador genera opcionalmente un WAV PCM mono de 16 kHz y 16 bits, carga un WAV válido, acepta únicamente `REPRODUCIR_AUDIO`, descarga el WAV de respuesta y lo valida antes de guardarlo.
- Se añadió reproducción opcional en Windows mediante `--reproducir`.
- Se añadieron recuperaciones verificadas desde pérdida de red, timeout y respuesta de comando inválida al estado `LISTO`.
- Se agregó una prueba de integración que ejecuta el cliente del simulador contra la aplicación FastAPI en memoria.

### Tecnologías y versiones

- Python 3.13.7 y biblioteca estándar (`urllib`, `wave`, `unittest`).
- FastAPI 0.141.1, pytest 9.1.1 y Uvicorn 0.52.3.
- WAV PCM mono de 16 kHz y 16 bits mediante HTTP multipart por archivo completo.

### Ubicación

- `simulador/cliente_http.py`
- `simulador/pruebas/prueba_cliente_http.py`
- `servidor/pruebas/prueba_integracion_simulador.py`

### Ejecución y verificación

- Directorio raíz: `python -m unittest simulador/pruebas/prueba_nucleo_estados.py simulador/pruebas/prueba_cliente_http.py` — siete pruebas aprobadas.
- Directorio `servidor/`: `uv run pytest -p no:cacheprovider` — siete pruebas aprobadas, incluida la integración simulador–FastAPI.
- Se ejecutó Uvicorn en `127.0.0.1:8010` y `python simulador/cliente_http.py --url-base http://127.0.0.1:8010 --generar-entrada ...`; el servidor respondió `201 Created` y luego `200 OK`, y el simulador terminó en `LISTO`.
- Directorio `servidor/`: `uv run python -m compileall -q aplicacion pruebas ../simulador` — sin errores.

### Decisiones, riesgos y deuda

- La reproducción audible se deja explícita y opcional para que las pruebas automáticas no dependan del dispositivo de audio del equipo.
- El simulador no almacena credenciales, no accede a base de datos ni persiste el audio de entrada fuera de la ruta que indique quien ejecuta la prueba.
- Sigue pendiente autenticación y ciclo de sesión revocable para el dispositivo.

### Siguiente paso

Implementar inicio y cierre de sesión del dispositivo en el backend y consumir esa sesión desde el simulador antes de enviar un turno de audio.

---

## 2026-08-18 — Sesión temporal y revocable de dispositivo H1

**Tipo:** implementación de autenticación mínima e integración  
**Verificación:** VERIFICADO

### Cambios

- Se añadieron los endpoints `POST /api/v1/sesiones/dispositivo/iniciar` y `POST /api/v1/sesiones/dispositivo/cerrar`.
- Se implementó un gestor local de sesiones opacas de 15 minutos, validado antes de aceptar `POST /api/v1/turnos/audio` y revocado de forma explícita al cerrar.
- La credencial permanente se toma únicamente de `ENTREVOCES_CREDENCIAL_DISPOSITIVO`; el código no provee un valor por defecto ni la imprime.
- El simulador inicia sesión antes de subir audio, incorpora el token temporal en `X-Sesion-Dispositivo` y revoca la sesión al terminar o abortar el turno.
- Se añadieron pruebas de credencial inválida, ausencia de sesión, revocación y flujo integrado simulador–backend.

### Tecnologías y versiones

- Python 3.13.7 con `secrets`, `datetime`, `threading` y variables de entorno.
- FastAPI 0.141.1, pytest 9.1.1 y Uvicorn 0.52.3.

### Ubicación

- `servidor/aplicacion/enrutadores/sesiones.py`
- `servidor/aplicacion/servicios/sesiones_dispositivo.py`
- `servidor/aplicacion/esquemas/respuestas.py`
- `servidor/aplicacion/enrutadores/audios.py`
- `simulador/cliente_http.py`
- `servidor/pruebas/prueba_backend.py`
- `servidor/pruebas/prueba_integracion_simulador.py`

### Ejecución y verificación

- Directorio raíz: `python -m unittest simulador/pruebas/prueba_nucleo_estados.py simulador/pruebas/prueba_cliente_http.py` — siete pruebas aprobadas.
- Directorio `servidor/`: `uv run pytest -p no:cacheprovider` — diez pruebas aprobadas.
- Se ejecutó Uvicorn en `127.0.0.1:8011` con una credencial solo de proceso. El simulador completó `iniciar sesión (201) → turno (201) → descarga (200) → cierre (204)` y finalizó en `LISTO`.
- Directorio `servidor/`: `uv run python -m compileall -q aplicacion pruebas ../simulador` — sin errores.

### Decisiones, riesgos y deuda

- La sesión es temporal y revocable, pero aún reside en memoria: no sobrevive a reinicios ni soporta múltiples procesos.
- La credencial de entorno es adecuada únicamente para banco local H1; el registro persistente y rotación por dispositivo entran junto con PostgreSQL.
- Continúa la advertencia deprecada de `starlette.testclient`; no afecta las pruebas aprobadas.

### Siguiente paso

Conectar el firmware MicroPython a la sesión y contrato HTTP, después de ejecutar las pruebas físicas prioritarias de Wi-Fi, I2S TX y captura PDM.

---

## 2026-08-18 — Cliente HTTP de firmware preparado H2/H3

**Tipo:** implementación de firmware lógico y preparación de integración  
**Verificación:** PARCIAL

### Cambios

- Se creó la máquina de estados reutilizable del dispositivo físico en `dispositivo/micropython/nucleo_estados.py`.
- Se creó `dispositivo/micropython/cliente_http.py`, compatible con la interfaz de `urequests`: inicia y revoca sesiones, transmite WAV multipart, procesa solo `REPRODUCIR_AUDIO` y valida el encabezado RIFF de la descarga.
- Se creó `dispositivo/micropython/controlador_turno.py`, que conecta `ENVIANDO` con el cliente y recupera `LISTO` ante error de red, servidor o contrato.
- Se añadieron pruebas de recorrido, liberación de respuestas, recuperación de red y rechazo de comandos no permitidos.

### Tecnologías y versiones

- MicroPython previsto sobre XIAO ESP32-S3 Sense; versión exacta aún pendiente de fijar físicamente.
- Interfaz HTTP `urequests`, JSON compatible con `ujson` y WAV RIFF por archivo completo.
- Python 3.13.7 y `unittest` para la verificación lógica aislada.

### Ubicación

- `dispositivo/micropython/nucleo_estados.py`
- `dispositivo/micropython/cliente_http.py`
- `dispositivo/micropython/controlador_turno.py`
- `dispositivo/pruebas/prueba_cliente_http.py`

### Ejecución y verificación

- Directorio raíz: `python -m unittest dispositivo/pruebas/prueba_cliente_http.py simulador/pruebas/prueba_nucleo_estados.py simulador/pruebas/prueba_cliente_http.py` — diez pruebas aprobadas.
- Directorio `servidor/`: `uv run pytest -p no:cacheprovider` — diez pruebas aprobadas.
- Directorio `servidor/`: `uv run python -m compileall -q aplicacion pruebas ../simulador ../dispositivo` — sin errores.

### Decisiones, riesgos y deuda

- Esta evidencia comprueba la lógica en CPython con un transporte controlado; no certifica compatibilidad de la variante real de MicroPython ni comportamiento eléctrico.
- El código no contiene claves de base de datos, almacenamiento, IA ni una credencial de dispositivo predeterminada.
- PDM, Wi-Fi, PSRAM, I2S TX, pantalla, DAC y amplificador continúan pendientes de H2 y deben probarse por separado.

### Siguiente paso

Fijar y cargar MicroPython en la XIAO ESP32-S3 Sense, capturar REPL y validar Wi-Fi contra salud antes de probar I2S TX y PDM de forma aislada.

---

## 2026-08-18 — Guía operativa para sesiones de Antigravity

**Tipo:** documentación  
**Verificación:** VERIFICADO

### Cambios

- Se agregó una guía para decidir cuándo conservar o reiniciar un chat de Antigravity.
- Se incluyeron mensajes reproducibles de inicio, auditoría en modo solo lectura, prueba de comportamiento de reglas y prueba de activación de la Skill de evaluación del agente.
- Se añadió la guía al índice documental y a los artefactos de memoria del proyecto.

### Tecnologías y versiones

- Markdown y estructura de instrucciones compatible con `AGENTS.md` y `.agents/skills/`.

### Ubicación

- `documentacion/GUIA_SESIONES_ANTIGRAVITY.md`
- `documentacion/INDICE_DOCUMENTACION.md`
- `PROJECT_STATE.md`

### Ejecución y verificación

- Se revisó que la guía apunte a las rutas existentes de estado, documentación y Skills del proyecto.

### Decisiones, riesgos y deuda

- La presencia de un archivo de prompt no prueba por sí sola la activación de una instrucción interna; la guía exige validar el comportamiento ante solicitudes contradictorias.

### Siguiente paso

- Ejecutar la auditoría inicial al abrir EntreVoces en Antigravity antes de iniciar H2 en hardware físico.

---

## 2026-08-18 — Diagnóstico inicial de Hardware H2

**Tipo:** implementación | hardware
**Verificación:** VERIFICADO

### Cambios
- Se conectó físicamente por primera vez la placa XIAO ESP32-S3 Sense vía USB-C.
- Se instaló la versión genérica estable de MicroPython (ESP32-S3).
- Se ejecutaron pruebas a través del REPL en Thonny IDE.
- Se verificó la disponibilidad de PSRAM (~8MB libres).
- Se verificó la conexión exitosa a red Wi-Fi local.
- Se verificó la inicialización lógica exitosa del micrófono PDM integrado en la placa de expansión Sense usando `machine.I2S`.

### Tecnologías y versiones
- Thonny IDE.
- MicroPython v1.22.1 (o superior) genérico para ESP32-S3.
- Hardware: XIAO ESP32-S3 Sense.

### Ubicación
- Placa física (sin modificaciones de código fuente en el repositorio).

### Ejecución y verificación
- Comando: Código de inicialización de `network.WLAN` y `machine.I2S` por REPL.
- Resultado: El REPL reportó IP asignada por DHCP y no lanzó excepciones al usar `I2S.RX` con los pines del micrófono PDM (GPIO 41 y 42).

### Decisiones, riesgos y deuda
- Se superó el riesgo de que el firmware estándar no soportara el hardware PDM. No será necesario crear un módulo en C personalizado.
- La lectura de bytes (1024) funcionó, pero aún está pendiente la comprobación acústica de esos bytes (guardar un WAV y escucharlo) para confirmar que no haya ruido o silencio (tarea para H2.4).
- Se respetó la restricción de seguridad de no usar la batería reciclada ni ensamblar los periféricos externos.

### Siguiente paso
- Soldar los pines a la placa para poder integrarla en la protoboard.
- Capturar una muestra PDM más larga, guardarla como WAV en la PSRAM y descargarla al computador para validar la calidad del audio (completar H2.4).

---

## 2026-08-18 — Diagnóstico acústico PDM (H2.4a)

**Tipo:** diagnóstico de hardware y firmware  
**Verificación:** VERIFICADO

### Cambios
- Se comprobó acústicamente la muestra PDM grabada mediante `machine.I2S` estándar.
- Se verificó usando `validar-audio-dispositivo` que el archivo de salida cumple estructuralmente con WAV PCM 16kHz, mono, 16 bits.
- Se detectó que el contenido del archivo corresponde a ruido estático (bitstream PDM crudo) y no a sonido PCM decodificado.
- Se concluyó la tarea H2.4a de comprobación de `machine.I2S` con resultado negativo.

### Tecnologías y versiones
- Script de MicroPython `prueba_pdm.py`.
- Inspector de audio WAV.

### Ubicación
- `dispositivo/pruebas/prueba_pdm.py`

### Ejecución y verificación
- Comando: `python .agents\skills\validar-audio-dispositivo\scripts\inspeccionar_wav.py captura_pdm.wav --json`
- Resultado: Estructura válida, pero evaluación acústica indica que es un flujo PDM no decodificado.

### Decisiones, riesgos y deuda
- Se materializa el riesgo documentado "MicroPython sin PDM expuesto". `machine.I2S` genérico no decodifica PDM a PCM para esta placa de manera automática.
- Se revierte la suposición previa de que el riesgo había sido superado por el éxito lógico del REPL.
- Se aprueba pasar a H2.4b: Preparar compilación personalizada de MicroPython o módulo C nativo para configurar el filtro PDM de la interfaz I2S.

### Siguiente paso
- Desarrollar un plan de implementación (H2.4b) para compilar un módulo C o un firmware customizado para el ESP32-S3 que permita configurar la captura PDM.

---

## 2026-08-18 — Implementación Módulo C Nativo PDM (H2.4b Parcial)

**Tipo:** implementación de firmware  
**Verificación:** NO_VERIFICADO (Pendiente de compilación)

### Cambios
- Se creó el código fuente del módulo en C `modulo_pdm.c` que usa la API `i2s_channel_init_pdm_rx_mode` de ESP-IDF v5.x.
- Se configuró el archivo `micropython.cmake` para enlazar el módulo como un `USER_C_MODULE` en la cadena de compilación de MicroPython.
- El módulo expone los métodos `pdm.init(clk, dat, frec)`, `pdm.read(handle, buffer)` y `pdm.deinit(handle)` a Python, aislando la complejidad.

### Tecnologías y versiones
- Lenguaje C compatible con ESP-IDF y API de módulos de usuario de MicroPython.

### Ubicación
- `dispositivo/firmware_personalizado/modulo_pdm/modulo_pdm.c`
- `dispositivo/firmware_personalizado/modulo_pdm/micropython.cmake`

### Ejecución y verificación
- No verificado. El código fue escrito pero requiere ser compilado (usando ESP-IDF) para generar el archivo `firmware.bin` e instalarlo en la placa.

### Decisiones, riesgos y deuda
- Se eligió la vía de crear un módulo nativo en C según el plan de mitigación en lugar de abandonar MicroPython por Arduino.
- **Deuda**: El entorno de compilación de ESP-IDF no está disponible localmente en la máquina Windows. Será necesario utilizar un contenedor Docker o GitHub Actions para compilar el firmware sin ensuciar el entorno local.

### Siguiente paso
- Compilar el firmware modificado (ya sea usando Docker localmente o mediante la nube) y flashearlo a la placa para retomar H2.4 (capturar el WAV inteligible).
