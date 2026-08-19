"""Verifica las transiciones deterministas del simulador del dispositivo."""

import sys
import unittest
from pathlib import Path


RUTA_SIMULADOR: Path = Path(__file__).resolve().parents[1] / "wokwi_dispositivo"
sys.path.insert(0, str(RUTA_SIMULADOR))

from nucleo_estados import ControladorEstados


class PruebaControladorEstados(unittest.TestCase):
    """Comprueba el recorrido principal y la recuperación ante fallo."""

    def test_recorrido_completo_vuelve_a_listo(self) -> None:
        """Comprueba que un turno simulado termina en listo."""
        controlador: ControladorEstados = ControladorEstados()

        self.assertEqual(controlador.iniciar(), controlador.LISTO)
        self.assertEqual(controlador.transicionar("BOTON_PRESIONADO"), controlador.ESCUCHANDO)
        self.assertEqual(controlador.transicionar("BOTON_SOLTADO"), controlador.ENVIANDO)
        self.assertEqual(controlador.transicionar("ENVIO_CONFIRMADO"), controlador.PROCESANDO)
        self.assertEqual(controlador.transicionar("RESPUESTA_LISTA"), controlador.REPRODUCIENDO)
        self.assertEqual(controlador.transicionar("REPRODUCCION_FINALIZADA"), controlador.LISTO)

    def test_fallo_recupera_el_estado_listo(self) -> None:
        """Comprueba que un fallo permite volver al estado listo."""
        controlador: ControladorEstados = ControladorEstados()
        controlador.iniciar()

        self.assertEqual(controlador.transicionar("FALLO"), controlador.ERROR)
        self.assertEqual(controlador.transicionar("REINTENTAR"), controlador.LISTO)

    def test_evento_invalido_conserva_el_estado(self) -> None:
        """Comprueba que un evento no permitido no altera el estado."""
        controlador: ControladorEstados = ControladorEstados()
        controlador.iniciar()

        self.assertEqual(controlador.transicionar("RESPUESTA_LISTA"), controlador.LISTO)


if __name__ == "__main__":
    unittest.main()
