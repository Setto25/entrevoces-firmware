"""Conecta el estado de envío con el cliente HTTP del dispositivo."""

from cliente_http import ErrorContrato, ErrorRed, ErrorServidor
from nucleo_estados import ControladorEstados


class ControladorTurno:
    """Coordina el envío de un WAV sin conocer captura, pantalla ni reproducción."""

    def __init__(self, controlador: ControladorEstados, cliente_http: object) -> None:
        """Inicializa el coordinador con estado y transporte ya configurados."""
        self._controlador: ControladorEstados = controlador
        self._cliente_http: object = cliente_http

    def enviar_audio(self, audio_wav: bytes, identificador_correlacion: str) -> bytes:
        """Envía el audio solo desde ENVIANDO y prepara su reproducción posterior."""
        if self._controlador.estado_actual != self._controlador.ENVIANDO:
            raise ErrorContrato("El audio solo se puede enviar desde el estado ENVIANDO.")
        try:
            audio_respuesta: bytes = self._cliente_http.ejecutar_turno(
                audio_wav, identificador_correlacion
            )
        except (ErrorRed, ErrorServidor, ErrorContrato):
            self._controlador.transicionar("FALLO")
            self._controlador.transicionar("REINTENTAR")
            raise
        self._controlador.transicionar("ENVIO_CONFIRMADO")
        self._controlador.transicionar("RESPUESTA_LISTA")
        return audio_respuesta

    def finalizar_reproduccion(self) -> str:
        """Devuelve el dispositivo a listo cuando termina la capa de audio."""
        return self._controlador.transicionar("REPRODUCCION_FINALIZADA")
