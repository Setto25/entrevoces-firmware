"""Consume el contrato HTTP v1 desde MicroPython sin secretos de infraestructura."""

try:
    import ujson as json
except ImportError:
    import json

try:
    import urequests
except ImportError:
    urequests = None


class ErrorRed(RuntimeError):
    """Representa un fallo de conectividad o timeout del dispositivo."""


class ErrorServidor(RuntimeError):
    """Representa una respuesta HTTP no aceptada por el contrato."""


class ErrorContrato(RuntimeError):
    """Representa un cuerpo o comando que no cumple el contrato v1."""


class ClienteHttpDispositivo:
    """Gestiona sesión, turno de audio y descarga de respuesta del dispositivo."""

    def __init__(
        self,
        url_base: str,
        credencial_dispositivo: str,
        modulo_http: object | None = None,
        tiempo_espera_segundos: int = 10,
    ) -> None:
        """Inicializa el cliente con su credencial local y transporte compatible."""
        if not url_base or not credencial_dispositivo:
            raise ValueError("La URL y la credencial del dispositivo son obligatorias.")
        self._url_base: str = url_base.rstrip("/")
        self._credencial_dispositivo: str = credencial_dispositivo
        self._modulo_http: object | None = modulo_http or urequests
        self._tiempo_espera_segundos: int = tiempo_espera_segundos

    def ejecutar_turno(self, audio_wav: bytes, identificador_correlacion: str) -> bytes:
        """Inicia sesión, envía el WAV, descarga la respuesta y revoca la sesión."""
        token_sesion: str | None = None
        try:
            token_sesion = self._iniciar_sesion()
            respuesta_turno: object = self._solicitar(
                "post",
                "/api/v1/turnos/audio",
                datos=self._crear_multipart(audio_wav),
                encabezados={
                    "Content-Type": "multipart/form-data; boundary=EntreVocesMicroPython",
                    "X-Id-Correlacion": identificador_correlacion,
                    "X-Sesion-Dispositivo": token_sesion,
                },
            )
            contenido_turno: bytes = self._leer_contenido(respuesta_turno)
            self._exigir_estado(respuesta_turno, 201)
            ruta_audio: str = self._extraer_ruta_audio(contenido_turno)
            respuesta_audio: object = self._solicitar("get", ruta_audio)
            contenido_audio: bytes = self._leer_contenido(respuesta_audio)
            self._exigir_estado(respuesta_audio, 200)
            self._exigir_wav(contenido_audio)
            return contenido_audio
        finally:
            if token_sesion is not None:
                self._cerrar_sesion_silenciosamente(token_sesion)

    def _iniciar_sesion(self) -> str:
        """Obtiene un token temporal sin exponer la credencial en resultados."""
        respuesta: object = self._solicitar(
            "post",
            "/api/v1/sesiones/dispositivo/iniciar",
            encabezados={"X-Credencial-Dispositivo": self._credencial_dispositivo},
        )
        contenido: bytes = self._leer_contenido(respuesta)
        self._exigir_estado(respuesta, 201)
        try:
            cuerpo: dict[str, object] = json.loads(contenido)
            token_sesion: object = cuerpo.get("token_sesion")
        except (TypeError, ValueError) as error:
            raise ErrorContrato("La sesión no devolvió JSON válido.") from error
        if not isinstance(token_sesion, str) or not token_sesion:
            raise ErrorContrato("La sesión no devolvió un token válido.")
        return token_sesion

    def _cerrar_sesion_silenciosamente(self, token_sesion: str) -> None:
        """Revoca la sesión sin ocultar el error principal del turno."""
        try:
            respuesta: object = self._solicitar(
                "post",
                "/api/v1/sesiones/dispositivo/cerrar",
                encabezados={"X-Sesion-Dispositivo": token_sesion},
            )
            self._leer_contenido(respuesta)
            self._exigir_estado(respuesta, 204)
        except (ErrorRed, ErrorServidor, ErrorContrato):
            return

    def _solicitar(
        self,
        metodo: str,
        ruta: str,
        datos: bytes | None = None,
        encabezados: dict[str, str] | None = None,
    ) -> object:
        """Ejecuta una solicitud con timeout y convierte fallos de transporte."""
        if self._modulo_http is None:
            raise ErrorRed("No existe un módulo HTTP disponible en este firmware.")
        funcion: object | None = getattr(self._modulo_http, metodo, None)
        if funcion is None:
            raise ErrorRed("El módulo HTTP no implementa el método solicitado.")
        try:
            return funcion(
                self._url_base + ruta,
                data=datos,
                headers=encabezados or {},
                timeout=self._tiempo_espera_segundos,
            )
        except OSError as error:
            raise ErrorRed("No se pudo comunicar con el servidor.") from error

    @staticmethod
    def _leer_contenido(respuesta: object) -> bytes:
        """Lee y cierra una respuesta HTTP para liberar recursos del dispositivo."""
        try:
            contenido: bytes = respuesta.content
            return contenido
        finally:
            respuesta.close()

    @staticmethod
    def _exigir_estado(respuesta: object, estado_esperado: int) -> None:
        """Comprueba el estado HTTP esperado sin exponer cuerpos sensibles."""
        if getattr(respuesta, "status_code", None) != estado_esperado:
            raise ErrorServidor("El servidor devolvió un estado no esperado.")

    @staticmethod
    def _crear_multipart(audio_wav: bytes) -> bytes:
        """Construye el formulario multipart con el único campo de audio permitido."""
        limite: bytes = b"EntreVocesMicroPython"
        cabecera: bytes = (
            b"--" + limite + b"\r\n"
            b'Content-Disposition: form-data; name="audio"; filename="turno.wav"\r\n'
            b"Content-Type: audio/wav\r\n\r\n"
        )
        return cabecera + audio_wav + b"\r\n--" + limite + b"--\r\n"

    @staticmethod
    def _extraer_ruta_audio(contenido: bytes) -> str:
        """Acepta únicamente el comando cerrado de reproducción del contrato v1."""
        try:
            cuerpo: dict[str, object] = json.loads(contenido)
            comandos: object = cuerpo.get("comandos")
            comando: object = comandos[0] if isinstance(comandos, list) and len(comandos) == 1 else None
            ruta_audio: object = comando.get("ruta_audio") if isinstance(comando, dict) else None
        except (TypeError, ValueError, IndexError) as error:
            raise ErrorContrato("La respuesta de turno no tiene comandos válidos.") from error
        if not isinstance(comando, dict) or comando.get("tipo") != "REPRODUCIR_AUDIO":
            raise ErrorContrato("El comando recibido no está permitido.")
        if not isinstance(ruta_audio, str) or not ruta_audio.startswith("/"):
            raise ErrorContrato("La ruta de audio recibida no es válida.")
        return ruta_audio

    @staticmethod
    def _exigir_wav(contenido: bytes) -> None:
        """Comprueba el encabezado RIFF antes de delegar la reproducción I2S futura."""
        if len(contenido) < 44 or contenido[:4] != b"RIFF" or contenido[8:12] != b"WAVE":
            raise ErrorContrato("La descarga no contiene un WAV RIFF válido.")
