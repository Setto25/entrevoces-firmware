"""Contiene la máquina de estados mínima del dispositivo EntreVoces."""


class ControladorEstados:
    """Representa las transiciones permitidas durante un turno de voz."""

    ARRANQUE: str = "ARRANQUE"
    LISTO: str = "LISTO"
    ESCUCHANDO: str = "ESCUCHANDO"
    ENVIANDO: str = "ENVIANDO"
    PROCESANDO: str = "PROCESANDO"
    REPRODUCIENDO: str = "REPRODUCIENDO"
    ERROR: str = "ERROR"

    def __init__(self) -> None:
        """Inicializa el controlador en el estado de arranque."""
        self.estado_actual: str = self.ARRANQUE

    def iniciar(self) -> str:
        """Pasa el dispositivo al estado listo después del arranque."""
        self.estado_actual = self.LISTO
        return self.estado_actual

    def transicionar(self, evento: str) -> str:
        """Aplica una transición conocida o conserva el estado ante un evento inválido."""
        transiciones = {
            (self.LISTO, "BOTON_PRESIONADO"): self.ESCUCHANDO,
            (self.ESCUCHANDO, "BOTON_SOLTADO"): self.ENVIANDO,
            (self.ENVIANDO, "ENVIO_CONFIRMADO"): self.PROCESANDO,
            (self.PROCESANDO, "RESPUESTA_LISTA"): self.REPRODUCIENDO,
            (self.REPRODUCIENDO, "REPRODUCCION_FINALIZADA"): self.LISTO,
            (self.ERROR, "REINTENTAR"): self.LISTO,
        }
        if evento == "FALLO":
            self.estado_actual = self.ERROR
            return self.estado_actual

        clave: tuple[str, str] = (self.estado_actual, evento)
        if clave in transiciones:
            self.estado_actual = transiciones[clave]
        return self.estado_actual
