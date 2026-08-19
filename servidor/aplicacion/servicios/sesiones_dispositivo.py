"""Gestiona sesiones temporales y revocables de dispositivos."""

import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from secrets import compare_digest, token_urlsafe
from threading import RLock


DURACION_SESION_SEGUNDOS: int = 900
NOMBRE_VARIABLE_CREDENCIAL: str = "ENTREVOCES_CREDENCIAL_DISPOSITIVO"


class ErrorConfiguracionSesion(RuntimeError):
    """Representa la ausencia de una credencial configurada en el entorno."""


class ErrorCredencialDispositivo(PermissionError):
    """Representa una credencial de dispositivo inválida."""


class ErrorSesionDispositivo(PermissionError):
    """Representa una sesión inexistente, vencida o revocada."""


@dataclass(frozen=True)
class SesionDispositivo:
    """Describe una sesión temporal asociada a una credencial de dispositivo."""

    token: str
    expira_en: datetime


class GestorSesionesDispositivo:
    """Conserva sesiones temporales en memoria para el corte local H1."""

    def __init__(self, duracion_segundos: int = DURACION_SESION_SEGUNDOS) -> None:
        """Inicializa el almacén temporal y la duración de las sesiones."""
        self._duracion: timedelta = timedelta(seconds=duracion_segundos)
        self._sesiones: dict[str, SesionDispositivo] = {}
        self._bloqueo: RLock = RLock()

    def iniciar(self, credencial: str) -> SesionDispositivo:
        """Verifica la credencial configurada y emite una sesión temporal."""
        credencial_configurada: str | None = os.getenv(NOMBRE_VARIABLE_CREDENCIAL)
        if not credencial_configurada:
            raise ErrorConfiguracionSesion("No existe credencial de dispositivo configurada.")
        if not compare_digest(credencial, credencial_configurada):
            raise ErrorCredencialDispositivo("La credencial del dispositivo no es válida.")
        sesion: SesionDispositivo = SesionDispositivo(
            token=token_urlsafe(32),
            expira_en=datetime.now(UTC) + self._duracion,
        )
        with self._bloqueo:
            self._sesiones[sesion.token] = sesion
        return sesion

    def validar(self, token_sesion: str) -> SesionDispositivo:
        """Comprueba que la sesión exista y no haya vencido."""
        with self._bloqueo:
            sesion: SesionDispositivo | None = self._sesiones.get(token_sesion)
            if sesion is None:
                raise ErrorSesionDispositivo("La sesión del dispositivo no es válida.")
            if sesion.expira_en <= datetime.now(UTC):
                del self._sesiones[token_sesion]
                raise ErrorSesionDispositivo("La sesión del dispositivo venció.")
            return sesion

    def cerrar(self, token_sesion: str) -> None:
        """Revoca una sesión existente para impedir usos posteriores."""
        with self._bloqueo:
            if token_sesion not in self._sesiones:
                raise ErrorSesionDispositivo("La sesión del dispositivo no es válida.")
            del self._sesiones[token_sesion]

    def reiniciar(self) -> None:
        """Elimina las sesiones temporales para aislar las pruebas."""
        with self._bloqueo:
            self._sesiones.clear()


gestor_sesiones_dispositivo: GestorSesionesDispositivo = GestorSesionesDispositivo()
