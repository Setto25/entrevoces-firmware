# Documentación técnica viva de EntreVoces

**Versión:** 0.7  
**Fecha:** 2026-08-18  
**Estado:** simulador de estados y backend HTTP mínimo implementados; integración pendiente

## 0.1. Backend HTTP mínimo

### Propósito y ubicación

El paquete `servidor/` implementa el primer contrato ejecutable de H1. `servidor/aplicacion/aplicacion.py` crea FastAPI; `servidor/aplicacion/enrutadores/` traduce HTTP; `servidor/aplicacion/esquemas/` define respuestas Pydantic y `servidor/aplicacion/servicios/audios.py` concentra validación y generación de WAV. Las pruebas de contrato viven en `servidor/pruebas/`.

### Endpoints

- `GET /api/v1/salud`: devuelve estado, servicio y versión.
- `POST /api/v1/turnos/audio`: acepta un archivo completo y valida tipo, tamaño y formato.
- `GET /api/v1/audios/respuesta-fija`: entrega un WAV compatible para reproducción.

El contrato de entrada exige WAV PCM, mono, 16000 Hz y 16 bits, con límite temporal de 2 MiB. Una entrada válida produce un identificador de correlación, metadatos verificados y el comando cerrado `REPRODUCIR_AUDIO`.

### Entorno y verificación

`servidor/pyproject.toml` y `servidor/uv.lock` fijan las dependencias. Desde `servidor/`, `uv sync --group desarrollo` crea el único entorno Python del repositorio, `servidor/.venv`; `uv run uvicorn aplicacion.aplicacion:aplicacion --reload` inicia el servidor y `uv run pytest` ejecuta las seis pruebas de contrato.

La guía reproducible queda en `documentacion/GUIA_BACKEND.md`. Este corte todavía no persiste audios ni sesiones y no aplica autenticación o moderación.

## 0. Simulador inicial de interacción

### Propósito y ubicación

Valida el flujo de pulsar, escuchar, enviar, procesar, reproducir y volver a listo sin depender todavía de audio, Wi-Fi, backend ni hardware físico. Está en `simulador/wokwi_dispositivo/` y sus pruebas en `simulador/pruebas/prueba_nucleo_estados.py`.

### Funcionamiento y verificación

`diagram.json` conecta un pulsador virtual entre D1/GPIO2 y GND de una XIAO ESP32-S3 virtual. `main.py` configura `PULL_UP`, aplica antirrebote y delega transiciones en `nucleo_estados.py`. La red y la reproducción se representan por demoras de 350 ms.

Se verifica localmente con:

```powershell
python -m unittest simulador/pruebas/prueba_nucleo_estados.py
```

La guía de ejecución en Wokwi queda en `simulador/wokwi_dispositivo/INSTRUCCIONES_WOKWI.md`. Este módulo no simula el micrófono PDM, I2S, pantalla ni audio: esas comprobaciones se conservan para H2 y hardware físico.

## 0.2. Simulador HTTP local

`simulador/cliente_http.py` consume exclusivamente el contrato HTTP v1 del backend. Genera un WAV PCM mono de 16 kHz y 16 bits cuando se solicita, carga el archivo mediante `POST /api/v1/turnos/audio`, acepta solo el comando `REPRODUCIR_AUDIO`, descarga el WAV resultante y valida su formato antes de guardarlo. La opción `--reproducir` usa el reproductor WAV nativo de Windows; sin ella el recorrido es silencioso y automatizable.

Con Uvicorn iniciado desde `servidor/`, el recorrido se ejecuta desde la raíz con:

```powershell
python simulador/cliente_http.py --url-base http://127.0.0.1:8000 --generar-entrada --entrada C:\Temp\entrada.wav --salida C:\Temp\respuesta.wav --reproducir
```

El controlador transita por `LISTO → ESCUCHANDO → ENVIANDO → PROCESANDO → REPRODUCIENDO → LISTO`. Errores de transporte, timeout y respuestas inválidas pasan por `ERROR` y regresan a `LISTO`. Las pruebas unitarias viven en `simulador/pruebas/prueba_cliente_http.py`; la integración simulador–FastAPI está en `servidor/pruebas/prueba_integracion_simulador.py`.

## 0.3. Sesión temporal del dispositivo

El servidor exige que el proceso defina `ENTREVOCES_CREDENCIAL_DISPOSITIVO`; el valor no tiene un valor por defecto ni se guarda en archivos del proyecto. `POST /api/v1/sesiones/dispositivo/iniciar` recibe esa credencial en `X-Credencial-Dispositivo` y devuelve un token opaco de 15 minutos. `POST /api/v1/turnos/audio` exige ese token en `X-Sesion-Dispositivo`; `POST /api/v1/sesiones/dispositivo/cerrar` lo revoca.

Durante H1, `GestorSesionesDispositivo` conserva los tokens exclusivamente en memoria y bajo bloqueo local. Por lo tanto, un reinicio de Uvicorn invalida todas las sesiones, y un despliegue con más de un proceso todavía no es compatible. Al incorporar PostgreSQL se reemplaza por una persistencia de sesiones y registro revocable de dispositivos.

El simulador toma la credencial de la misma variable de entorno o del argumento efímero `--credencial-dispositivo`, inicia la sesión antes del audio y la cierra tanto al terminar como al recuperar un fallo. No escribe credenciales en archivos, respuestas impresas ni artefactos de prueba.

## 0.4. Cliente HTTP preparado para firmware

`dispositivo/micropython/cliente_http.py` usa la interfaz de `urequests` de MicroPython para iniciar una sesión temporal, enviar un WAV completo en multipart, aceptar solo el comando `REPRODUCIR_AUDIO`, descargar el binario RIFF y cerrar la sesión. La credencial se inyecta al constructor desde la configuración local de la placa y no forma parte del módulo ni del repositorio.

`dispositivo/micropython/controlador_turno.py` conecta el estado `ENVIANDO` con ese cliente. Una respuesta válida lleva a `PROCESANDO` y `REPRODUCIENDO`; red, servidor o contrato inválido pasan por `ERROR` y recuperan `LISTO`. La reproducción I2S se conserva como responsabilidad separada: el controlador entrega los bytes WAV, pero no asigna GPIO ni activa periféricos sin evidencia de H2.

La prueba `dispositivo/pruebas/prueba_cliente_http.py` usa respuestas compatibles con `urequests` y verifica sesión, revocación, comando permitido y recuperación. Se ejecuta en CPython como comprobación lógica; no sustituye cargar el módulo en la versión exacta de MicroPython ni la prueba física de Wi-Fi, PDM o I2S.

## 1. Propósito

Este documento explica cómo funciona EntreVoces, qué responsabilidad tiene cada parte y dónde debe ubicarse dentro del proyecto. Debe actualizarse cuando la implementación se aparte de lo descrito.

## 2. Arquitectura del MVP

```text
Persona mayor
  → botón, micrófono y pantalla
  → XIAO ESP32-S3 Sense
  → HTTP por Wi‑Fi
  → FastAPI
  → servicios del dominio
  → PostgreSQL + pgvector
  → almacenamiento de audios
  → proveedores de IA
  → audio de respuesta
  → ESP32 → PCM5102A → PAM8403 → parlante

Público general
  → Flutter
  → FastAPI
  → mismos servicios del dominio
```

## 3. Responsabilidades

### Dispositivo físico

Hace:

- detectar el botón;
- capturar audio;
- almacenar temporalmente buffers;
- mostrar estados;
- enviar y recibir datos;
- reproducir audio;
- recuperarse de errores locales y de red.

La lógica del dispositivo se implementa en MicroPython. Los controladores se separan de la máquina de estados para permitir pruebas con adaptadores simulados.

No hace:

- autorización social;
- moderación;
- búsqueda vectorial;
- elección de destinatarios;
- acceso a base de datos;
- ejecución del LLM.

### Backend

Hace:

- autenticar usuarios y dispositivos;
- validar entradas;
- mantener sesiones y contexto activo;
- aplicar reglas sociales y permisos;
- almacenar metadatos;
- coordinar audio e IA;
- moderar antes de publicar;
- auditar decisiones relevantes;
- devolver comandos limitados a los clientes.

### LLM

Hace:

- interpretar intención;
- seleccionar una herramienta autorizada;
- formular frases breves del avatar.

No hace:

- consultar SQL;
- decidir identidades o destinatarios;
- publicar sin moderación;
- ejecutar código arbitrario;
- obedecer instrucciones encontradas dentro de historias recuperadas.

## 4. Estructura prevista del repositorio

Los nombres se mantienen en español, salvo los archivos de control obligatorios `AGENTS.md`, `PROJECT_STATE.md`, la ruta estándar `.agents/skills`, los manifiestos `SKILL.md`, `agents/openai.yaml` y otros nombres técnicos que una herramienta no permita configurar. Toda excepción se documenta.

```text
entrevoces/
├── AGENTS.md
├── PROJECT_STATE.md
├── .agents/
│   └── skills/
│       ├── validar-audio-dispositivo/
│       ├── diagnosticar-hardware-entrevoces/
│       ├── probar-e2e-entrevoces/
│       ├── evaluar-agente-entrevoces/
│       ├── desarrollar-backend-entrevoces/
│       ├── desarrollar-firmware-entrevoces/
│       └── cerrar-modulo-entrevoces/
├── servidor/
│   ├── .venv/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── aplicacion/
│   │   ├── esquemas/
│   │   ├── enrutadores/
│   │   ├── servicios/
│   └── pruebas/
├── aplicacion_movil/
├── dispositivo/
│   ├── micropython/
│   └── pruebas/
├── simulador/
│   ├── pruebas/
│   └── wokwi_dispositivo/
└── documentacion/
```

La estructura puede crecer solo cuando exista una necesidad implementada. No se crean capas vacías por anticipado.

## 5. Contrato inicial dispositivo-servidor

### Transporte

- Desarrollo local: HTTP dentro de una red controlada.
- Despliegue: HTTPS obligatorio.
- Audio: archivo WAV completo por solicitud.
- Streaming: excluido del MVP.

### Formato de captura

```text
contenedor: WAV
codificación: PCM lineal
frecuencia: 16 000 Hz
canales: 1
profundidad: 16 bits
```

### Respuesta conceptual

```json
{
  "id_solicitud": "01H...",
  "id_sesion": "01H...",
  "comandos": [
    {
      "tipo": "MOSTRAR_HABLANDO"
    },
    {
      "tipo": "REPRODUCIR_AUDIO",
      "url_audio": "https://servidor/temporal/audio"
    },
    {
      "tipo": "INICIAR_ESCUCHA"
    }
  ]
}
```

### Comandos permitidos inicialmente

```text
MOSTRAR_LISTO
MOSTRAR_ESCUCHANDO
MOSTRAR_PROCESANDO
MOSTRAR_HABLANDO
REPRODUCIR_AUDIO
INICIAR_ESCUCHA
DETENER_ESCUCHA
FINALIZAR_SESION
MOSTRAR_ERROR
```

El cliente ignora de forma segura comandos desconocidos, registra el incidente y vuelve a listo cuando sea posible.

## 6. Máquina de estados

```text
ARRANQUE
  → CONECTANDO_WIFI
  → LISTO
  → ESCUCHANDO
  → ENVIANDO
  → PROCESANDO
  → REPRODUCIENDO
  → LISTO
```

Estados de error:

```text
SIN_WIFI
ERROR_SERVIDOR
ERROR_AUDIO
TIEMPO_AGOTADO
```

Cada error define una transición de recuperación. Ningún error deja indefinidamente la interfaz en procesando.

## 7. API prevista

Los nombres finales se congelan al implementar el contrato.

```text
GET  /api/v1/salud

POST /api/v1/autenticacion/iniciar
POST /api/v1/autenticacion/renovar
POST /api/v1/autenticacion/cerrar

POST /api/v1/dispositivos/provisionar
POST /api/v1/dispositivos/sesiones/iniciar
POST /api/v1/dispositivos/sesiones/finalizar
POST /api/v1/dispositivos/turnos

POST /api/v1/audios
GET  /api/v1/audios/{id_audio}/reproduccion

GET  /api/v1/experiencias
GET  /api/v1/experiencias/{id_experiencia}
POST /api/v1/experiencias
POST /api/v1/experiencias/buscar

GET  /api/v1/saludos/bandeja
POST /api/v1/saludos
POST /api/v1/saludos/{id_saludo}/escuchado
```

## 8. Datos principales

### Entidades

- `Usuario`
- `Dispositivo`
- `ActivoAudio`
- `Experiencia`
- `EmbeddingExperiencia`
- `Saludo`
- `SesionConversacion`
- `TurnoConversacion`
- `EventoModeracion`
- `EventoAuditoria`

### Regla de audio

PostgreSQL almacena propietario, clave del objeto, tipo, duración, tamaño, checksum y fechas. El archivo binario se mantiene en almacenamiento de objetos o, durante H1, en un directorio local aislado.

### Regla de sesión

La sesión conserva `saludo_activo_id` y `experiencia_activa_id`. La respuesta “quiero contestarle” no contiene destinatario. El backend lo deriva de la entidad activa.

## 9. Proveedores de IA

Se definen interfaces equivalentes a:

```text
ProveedorModeloLenguaje
ProveedorVozATexto
ProveedorTextoAVoz
ProveedorEmbeddings
ProveedorModeracion
```

Cada proveedor tiene:

- implementación simulada determinista para pruebas;
- implementación real configurable;
- timeouts explícitos;
- errores tipados;
- nombre y versión registrables;
- ausencia de secretos en clientes.

## 10. Moderación y publicación

```text
GRABADO
  → TRANSCRITO
  → MODERADO
  → APROBADO | BLOQUEADO | REVISION_REQUERIDA
  → EMBEDDING, solo si corresponde
  → PUBLICADO
```

Si la moderación falla o queda indisponible, el contenido no se publica automáticamente.

La detección mínima considera:

- teléfonos, correos, direcciones y redes sociales;
- datos financieros;
- solicitudes o promesas de dinero;
- amenazas, acoso y contenido ofensivo;
- intentos de mover la conversación fuera de la plataforma.

## 11. Búsqueda semántica

La búsqueda pasa por un único servicio. La consulta vectorial filtra al mismo tiempo:

- moderación aprobada;
- publicación vigente;
- visibilidad permitida;
- ausencia de eliminación;
- autor o comunidad según el caso.

La primera versión devuelve experiencias y reproduce su audio original. Eso constituye búsqueda semántica, no RAG.

## 12. Hardware conocido

### Micrófono

La documentación oficial de Seeed asigna al micrófono PDM del XIAO ESP32-S3 Sense:

```text
GPIO 41: datos
GPIO 42: reloj
```

Seeed recomienda para su ejemplo 16 kHz, 16 bits y PDM mono. Estos pines quedan reservados al micrófono mientras se utilice la placa Sense.

MicroPython estándar soporta ESP32-S3 y ofrece `machine.I2S`, pero la documentación oficial mantiene esa API como vista previa técnica y no documenta un modo PDM. Por ello, la captura PDM constituye una puerta temprana de H2. Si el firmware elegido no la expone, la aplicación continúa en MicroPython y el acceso PDM se encapsula mediante un módulo nativo mínimo o una compilación personalizada.

### Salida de audio

```text
ESP32-S3
  → I2S
  → PCM5102A
  → salida analógica de un canal
  → entrada de un canal del PAM8403
  → salida diferencial del mismo canal
  → un parlante
```

No se unen las dos salidas del PAM8403. Ningún terminal de la salida diferencial del parlante se conecta a GND.

### Pantalla

La pantalla ST7789V usa SPI y muestra inicialmente solo:

- LISTO;
- ESCUCHANDO;
- PROCESANDO;
- HABLANDO;
- SIN INTERNET;
- ERROR.

Las animaciones del avatar se posponen hasta estabilizar audio y red.

### Alimentación

La documentación oficial de Seeed especifica una entrada de batería de 3,7 V y recomienda una batería de litio recargable calificada. También indica que, cuando se alimenta por batería, el pin de 5 V no entrega tensión. Por ello, la batería reciclada no se conecta hasta identificarla y medirla, y se debe diseñar conscientemente la alimentación del PAM8403 y de los periféricos.

Durante el desarrollo inicial se usa USB-C. La integración portátil queda detrás de una prueba separada de consumo, ruido y carga.

### Mapa de GPIO pendiente

El mapa se completa al inspeccionar mañana:

- etiquetas exactas de la pantalla;
- etiquetas y puentes del PCM5102A;
- disponibilidad real de GPIO;
- coexistencia de entrada PDM, salida I2S y SPI;
- necesidades de selección de chip, datos/comando y reinicio de la pantalla.

No se fija un cableado basándose únicamente en el nombre comercial.

## 13. Seguridad mínima del MVP

- La credencial del dispositivo es revocable y distinta de las credenciales de usuario.
- El firmware no contiene claves de base de datos, storage o IA.
- Flutter no contiene secretos de servidor.
- Las entradas tienen límites de tipo, tamaño y duración.
- Las descargas de audio usan autorización o URL temporal.
- El backend nunca acepta un destinatario sensible decidido por el LLM.
- Los logs evitan tokens y contenido sensible innecesario.
- Los eventos de moderación y acciones sociales relevantes quedan auditados.

## 14. Estrategia de pruebas

### Unitarias

- transiciones de estado;
- validación WAV;
- moderación y estados de publicación;
- derivación segura del destinatario;
- filtros de búsqueda.

### Integración

- API y PostgreSQL;
- almacenamiento y reproducción;
- proveedores simulados y reales;
- simulador contra backend.

### Hardware

- cada periférico por separado;
- cinco turnos consecutivos;
- pérdida y recuperación de Wi‑Fi;
- timeout del backend;
- reinicio durante un turno;
- volumen mínimo y máximo seguro.

### E2E

- Elena, Tomás y Carmen;
- saludo, respuesta y reproducción;
- búsqueda de costura si H7 entra en el plazo;
- contenido bloqueado ausente de bandejas y búsquedas.

## 15. Cómo se documenta cada módulo

Cada módulo terminado agrega una sección o documento con:

```text
Propósito
Ubicación
Entradas y salidas
Dependencias y versiones
Configuración necesaria
Cómo se ejecuta
Cómo se prueba
Errores conocidos
Decisiones y motivos
Siguiente paso
```

Además, se actualizan `PROJECT_STATE.md`, el plan y el registro de cambios.

## 16. Fuentes técnicas verificadas

- [Primeros pasos con XIAO ESP32-S3 — Seeed Studio](https://wiki.seeedstudio.com/es/xiao_esp32s3_getting_started/)
- [Uso del micrófono del XIAO ESP32-S3 Sense — Seeed Studio](https://wiki.seeedstudio.com/es/xiao_esp32s3_sense_mic/)
- [MicroPython para XIAO ESP32-S3 Sense — Seeed Studio](https://wiki.seeedstudio.com/es/XIAO_ESP32S3_Micropython/)
- [I2S en MicroPython — documentación oficial](https://docs.micropython.org/en/latest/library/machine.I2S.html)
