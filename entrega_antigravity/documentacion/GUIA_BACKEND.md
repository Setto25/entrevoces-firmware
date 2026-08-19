# Guía de ejecución del backend de EntreVoces

## 1. Preparar el entorno

Se abre una terminal de PowerShell en el directorio del backend:

```powershell
cd D:\PROYECTOS\Habitat\Codigo_Proyecto\servidor
uv sync --group desarrollo
```

`uv` crea automáticamente `servidor/.venv` e instala las versiones fijadas en `servidor/uv.lock`. No se necesita activar manualmente el entorno cuando se usa `uv run`.

## 2. Iniciar el servidor

```powershell
$env:ENTREVOCES_CREDENCIAL_DISPOSITIVO = "una-credencial-secreta-local"
uv run uvicorn aplicacion.aplicacion:aplicacion --reload
```

Mientras el comando esté ejecutándose, se pueden abrir:

- comprobación de salud: <http://127.0.0.1:8000/api/v1/salud>;
- documentación interactiva: <http://127.0.0.1:8000/docs>.

El servidor se detiene en la terminal mediante `Ctrl+C`.

## 3. Ejecutar las pruebas

```powershell
uv run pytest
```

El corte inicial contiene seis pruebas: salud, WAV válido, frecuencia incorrecta, tipo incorrecto, límite de tamaño y WAV de respuesta.

La suite actual incluye además autenticación de dispositivo, rechazo de sesión ausente, revocación de sesión e integración con el simulador HTTP.

## 4. Contrato inicial

### `GET /api/v1/salud`

Confirma que la API está disponible y declara la versión `v1`.

### `POST /api/v1/turnos/audio`

Recibe un formulario `multipart/form-data` cuyo campo `audio` contiene un WAV PCM mono de 16000 Hz y 16 bits. El límite temporal es 2 MiB.

Exige el encabezado `X-Sesion-Dispositivo`, obtenido previamente al iniciar sesión. No acepta audio sin una sesión vigente.

### `POST /api/v1/sesiones/dispositivo/iniciar`

Recibe `X-Credencial-Dispositivo` y compara su valor con `ENTREVOCES_CREDENCIAL_DISPOSITIVO`, configurada solo en el entorno del proceso. Si es válida, devuelve un token opaco de sesión temporal de 15 minutos. La credencial permanente nunca aparece en respuestas ni se almacena en el repositorio.

### `POST /api/v1/sesiones/dispositivo/cerrar`

Recibe `X-Sesion-Dispositivo` y revoca el token de forma inmediata. El simulador lo llama al terminar o al abortar un turno.

Si el audio es válido, devuelve:

- identificador del turno;
- identificador de correlación;
- propiedades verificadas del WAV;
- comando cerrado `REPRODUCIR_AUDIO`;
- ruta del audio fijo de respuesta.

### `GET /api/v1/audios/respuesta-fija`

Devuelve un tono WAV mono de 16000 Hz y 16 bits para comprobar la descarga y reproducción sin depender todavía de TTS.

## 5. Límites de este corte

Todavía no implementa persistencia de sesiones, registro de dispositivos, PostgreSQL, almacenamiento de audios, STT, TTS ni moderación. El siguiente corte conecta la sesión temporal al firmware y prepara persistencia cuando se incorpore PostgreSQL.
