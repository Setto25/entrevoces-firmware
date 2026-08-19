"""Verifica el contrato HTTP mínimo del backend de EntreVoces."""

import wave
from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from aplicacion.aplicacion import aplicacion
from aplicacion.servicios.audios import LIMITE_AUDIO_BYTES
from aplicacion.servicios.sesiones_dispositivo import gestor_sesiones_dispositivo


cliente: TestClient = TestClient(aplicacion)
CREDENCIAL_PRUEBA: str = "credencial-prueba"


@pytest.fixture(autouse=True)
def preparar_sesiones(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configura una credencial temporal y aísla las sesiones de cada prueba."""
    monkeypatch.setenv("ENTREVOCES_CREDENCIAL_DISPOSITIVO", CREDENCIAL_PRUEBA)
    gestor_sesiones_dispositivo.reiniciar()


def iniciar_sesion() -> str:
    """Inicia una sesión válida para probar los endpoints protegidos."""
    respuesta = cliente.post(
        "/api/v1/sesiones/dispositivo/iniciar",
        headers={"X-Credencial-Dispositivo": CREDENCIAL_PRUEBA},
    )
    assert respuesta.status_code == 201
    return str(respuesta.json()["token_sesion"])


def encabezados_sesion() -> dict[str, str]:
    """Entrega los encabezados necesarios para una solicitud autenticada."""
    return {"X-Sesion-Dispositivo": iniciar_sesion()}


def crear_wav(frecuencia_hz: int = 16_000, bits: int = 16, canales: int = 1) -> bytes:
    """Genera un WAV pequeño con parámetros controlados para las pruebas."""
    contenido: BytesIO = BytesIO()
    with wave.open(contenido, "wb") as archivo:
        archivo.setnchannels(canales)
        archivo.setsampwidth(bits // 8)
        archivo.setframerate(frecuencia_hz)
        archivo.writeframes(b"\x00" * (frecuencia_hz // 10) * canales * (bits // 8))
    return contenido.getvalue()


def test_salud_responde_con_version_activa() -> None:
    """Comprueba que la API informa su estado y versión."""
    respuesta = cliente.get("/api/v1/salud")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "estado": "saludable",
        "servicio": "entrevoces",
        "version_api": "v1",
    }


def test_turno_acepta_wav_del_contrato() -> None:
    """Comprueba que un WAV válido produce un comando reproducible."""
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.wav", crear_wav(), "audio/wav")},
        headers={**encabezados_sesion(), "X-Id-Correlacion": "prueba-001"},
    )

    cuerpo = respuesta.json()
    assert respuesta.status_code == 201
    assert respuesta.headers["x-id-correlacion"] == "prueba-001"
    assert cuerpo["estado"] == "procesado"
    assert cuerpo["identificador_correlacion"] == "prueba-001"
    assert cuerpo["audio_entrada"]["frecuencia_hz"] == 16_000
    assert cuerpo["audio_entrada"]["canales"] == 1
    assert cuerpo["audio_entrada"]["bits_por_muestra"] == 16
    assert cuerpo["comandos"] == [
        {"tipo": "REPRODUCIR_AUDIO", "ruta_audio": "/api/v1/audios/respuesta-fija"}
    ]


def test_turno_rechaza_frecuencia_incorrecta() -> None:
    """Comprueba que un WAV de 8000 Hz no entra al flujo del dispositivo."""
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.wav", crear_wav(frecuencia_hz=8_000), "audio/wav")},
        headers=encabezados_sesion(),
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"]["codigo"] == "wav_invalido"


def test_turno_rechaza_tipo_incorrecto() -> None:
    """Comprueba que el endpoint no acepta un tipo distinto de WAV."""
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.txt", b"contenido", "text/plain")},
        headers=encabezados_sesion(),
    )

    assert respuesta.status_code == 415
    assert respuesta.json()["detail"]["codigo"] == "tipo_audio_no_permitido"


def test_turno_rechaza_audio_demasiado_grande() -> None:
    """Comprueba que el endpoint corta entradas por encima del límite."""
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.wav", b"0" * (LIMITE_AUDIO_BYTES + 1), "audio/wav")},
        headers=encabezados_sesion(),
    )

    assert respuesta.status_code == 413
    assert respuesta.json()["detail"]["codigo"] == "audio_demasiado_grande"


def test_audio_respuesta_cumple_el_contrato() -> None:
    """Comprueba que el WAV de respuesta puede ser reproducido por el cliente."""
    respuesta = cliente.get("/api/v1/audios/respuesta-fija")

    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"] == "audio/wav"
    with wave.open(BytesIO(respuesta.content), "rb") as archivo:
        assert archivo.getnchannels() == 1
        assert archivo.getframerate() == 16_000
        assert archivo.getsampwidth() == 2


def test_sesion_invalida_no_permite_enviar_audio() -> None:
    """Comprueba que un turno sin sesión válida no llega a validar el WAV."""
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.wav", crear_wav(), "audio/wav")},
    )

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"]["codigo"] == "sesion_dispositivo_invalida"


def test_credencial_invalida_no_crea_sesion() -> None:
    """Comprueba que una credencial distinta no crea una sesión temporal."""
    respuesta = cliente.post(
        "/api/v1/sesiones/dispositivo/iniciar",
        headers={"X-Credencial-Dispositivo": "credencial-invalida"},
    )

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"]["codigo"] == "credencial_dispositivo_invalida"


def test_cierre_revoca_la_sesion_del_dispositivo() -> None:
    """Comprueba que una sesión cerrada deja de autorizar turnos de audio."""
    token_sesion: str = iniciar_sesion()
    cierre = cliente.post(
        "/api/v1/sesiones/dispositivo/cerrar",
        headers={"X-Sesion-Dispositivo": token_sesion},
    )
    respuesta = cliente.post(
        "/api/v1/turnos/audio",
        files={"audio": ("entrada.wav", crear_wav(), "audio/wav")},
        headers={"X-Sesion-Dispositivo": token_sesion},
    )

    assert cierre.status_code == 204
    assert respuesta.status_code == 401
