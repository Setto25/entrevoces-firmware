# Reglas del firmware

## Responsabilidad

```text
capturar
mostrar
reproducir
transmitir
recibir
recuperar
```

El firmware no autoriza, modera, busca usuarios ni decide relaciones sociales.

La lógica de aplicación se escribe en MicroPython. Un componente nativo solo se admite como adaptador mínimo cuando una capacidad del ESP32-S3 no esté expuesta por el firmware MicroPython elegido.

## Máquina de estados

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

Errores:

```text
SIN_WIFI
ERROR_SERVIDOR
ERROR_AUDIO
TIEMPO_AGOTADO
```

Cada estado define evento de entrada, acciones, timeout, siguiente estado y recuperación.

## Pines conocidos

- GPIO 41: datos del micrófono PDM Sense.
- GPIO 42: reloj del micrófono PDM Sense.

El resto se decide después de inspeccionar y probar la pantalla, el DAC y el botón reales.

## Compatibilidad MicroPython

- Fijar la versión y variante del firmware antes de programar controladores.
- Verificar REPL, GPIO, Wi‑Fi, memoria disponible y PSRAM.
- Tratar `machine.I2S` como API en vista previa técnica.
- Verificar I2S TX con PCM5102A independientemente de PDM RX.
- No asumir PDM RX: la documentación oficial de `machine.I2S` describe I2S estándar, pero no modo PDM.
- Si PDM no está expuesto, evaluar un módulo nativo mínimo o una compilación personalizada sin mover la máquina de estados fuera de MicroPython.

## Contrato inicial

- WAV PCM de 16 kHz, mono y 16 bits.
- Solicitud HTTP completa.
- Respuesta con comandos tipados.
- Credencial de dispositivo revocable.
- Identificador de correlación por turno.

## Pruebas de salida

1. Verificar sintaxis y dependencias compatibles con MicroPython.
2. Cargar archivos y capturar salida REPL.
3. Ejecutar la prueba aislada cinco veces cuando sea repetible.
4. Forzar un error y verificar recuperación.
5. Confirmar que no existan secretos de servidor en archivos ni firmware personalizado.
