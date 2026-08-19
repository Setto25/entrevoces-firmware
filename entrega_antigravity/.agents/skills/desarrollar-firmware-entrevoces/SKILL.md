---
name: desarrollar-firmware-entrevoces
description: Implementa, modifica o revisa firmware MicroPython del dispositivo EntreVoces para XIAO ESP32-S3 Sense con PDM, I2S, SPI, Wi‑Fi, botón, PCM5102A, PAM8403 y ST7789V. Usar para controladores, máquina de estados, buffers de audio, protocolo HTTP, compatibilidad de MicroPython, recuperación de errores y pruebas físicas. No usar para reglas sociales, moderación o consultas de datos.
---

# Desarrollar firmware EntreVoces

## Inicio

1. Leer `AGENTS.md`, `PROJECT_STATE.md` y [referencias/reglas_firmware.md](referencias/reglas_firmware.md).
2. Confirmar placa, versión del framework, pinout observado y mapa de GPIO vigente.
3. Confirmar la versión y variante exacta del firmware MicroPython.
4. Definir una prueba física aislada y su evidencia antes de editar.
5. Preservar el contrato compartido con el simulador.

## Implementación

1. Mantener controladores de periféricos separados de la máquina de estados.
2. Implementar transiciones explícitas y recuperación hacia `LISTO`.
3. Capturar WAV PCM mono de 16 kHz y 16 bits durante el primer MVP.
4. Demostrar captura PDM en la versión exacta de MicroPython antes de construir el flujo completo.
5. Usar PSRAM y límites explícitos para buffers.
6. Configurar timeouts y reintentos limitados de red.
7. Descargar o procesar audio por bloques cuando el tamaño lo requiera.
8. Mostrar y registrar el mismo estado operativo.
9. Probar un periférico por vez antes de combinarlo.

## Límites

- No guardar claves de base de datos, storage o IA.
- No implementar reglas sociales, RAG, moderación o elección de destinatarios.
- No asumir GPIO desde ejemplos de otra placa.
- No asumir soporte PDM porque exista `machine.I2S`; exigir evidencia real.
- No migrar toda la aplicación a C/C++ si PDM requiere código nativo; encapsular solo el adaptador necesario.
- No integrar batería durante el desarrollo inicial.
- No avanzar a streaming mientras el turno por archivo completo no sea estable.

## Entrega

Registrar hardware, GPIO, alimentación, versión de MicroPython, comando de instalación y carga, salida REPL, resultado observable y siguiente prueba. Invocar la Skill `diagnosticar-hardware-entrevoces` para fallos físicos y la Skill `cerrar-modulo-entrevoces` al completar el módulo.
