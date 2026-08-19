"""Ejecuta el primer simulador MicroPython de EntreVoces en Wokwi."""

from machine import Pin
from time import sleep_ms

from nucleo_estados import ControladorEstados


PIN_BOTON: int = 2
DEMORA_ANTIRREBOTE_MS: int = 30
DEMORA_RED_SIMULADA_MS: int = 350


def mostrar_estado(estado: str) -> None:
    """Muestra el estado actual mediante el monitor serie."""
    print("[EntreVoces] Estado:", estado)


def ejecutar_turno_simulado(controlador: ControladorEstados) -> None:
    """Representa la comunicación y reproducción sin usar red ni periféricos reales."""
    if controlador.estado_actual != controlador.ENVIANDO:
        return

    sleep_ms(DEMORA_RED_SIMULADA_MS)
    mostrar_estado(controlador.transicionar("ENVIO_CONFIRMADO"))
    sleep_ms(DEMORA_RED_SIMULADA_MS)
    mostrar_estado(controlador.transicionar("RESPUESTA_LISTA"))
    sleep_ms(DEMORA_RED_SIMULADA_MS)
    mostrar_estado(controlador.transicionar("REPRODUCCION_FINALIZADA"))


def ejecutar() -> None:
    """Lee el botón virtual y coordina la simulación del turno de voz."""
    boton: Pin = Pin(PIN_BOTON, Pin.IN, Pin.PULL_UP)
    controlador: ControladorEstados = ControladorEstados()
    estado_boton_anterior: int = boton.value()

    print("[EntreVoces] Simulador iniciado. Mantiene el botón para escuchar y suéltalo para enviar.")
    mostrar_estado(controlador.iniciar())

    while True:
        estado_boton_actual: int = boton.value()
        if estado_boton_actual != estado_boton_anterior:
            sleep_ms(DEMORA_ANTIRREBOTE_MS)
            estado_estable: int = boton.value()
            if estado_estable != estado_boton_anterior:
                estado_boton_anterior = estado_estable
                if estado_estable == 0:
                    mostrar_estado(controlador.transicionar("BOTON_PRESIONADO"))
                else:
                    mostrar_estado(controlador.transicionar("BOTON_SOLTADO"))
                    ejecutar_turno_simulado(controlador)
        sleep_ms(10)


ejecutar()
