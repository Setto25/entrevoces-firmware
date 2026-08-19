# Secuencia de pruebas físicas

## Orden

1. **Placa:** cargar firmware mínimo y verificar puerto serie.
2. **Wi‑Fi:** conectar y consultar `/api/v1/salud`.
3. **Botón:** validar entrada, resistencia y antirrebote.
4. **Micrófono:** capturar PDM con GPIO 41 para datos y GPIO 42 para reloj.
5. **DAC:** reproducir un tono conocido por I2S hacia PCM5102A.
6. **Amplificador:** conectar un canal analógico del DAC a un canal del PAM8403.
7. **Parlante:** probar con volumen mínimo y confirmar impedancia compatible.
8. **Pantalla:** mostrar estados básicos por SPI.
9. **Integración:** combinar periféricos de uno en uno y repetir pruebas anteriores.
10. **Batería:** integrar únicamente después de identificarla, medirla y calcular alimentación y consumo.

## Puertas de avance

- No probar amplificación si la salida analógica del DAC no está validada.
- No probar el recorrido remoto si captura y reproducción local no funcionan por separado.
- No cerrar el mapa de GPIO sin validar la coexistencia de PDM, I2S, SPI y botón.
- No integrar batería antes de estabilizar el recorrido mediante USB-C.

## Estados de prueba

- `APROBADO`: la evidencia coincide con el criterio.
- `FALLIDO`: la prueba se ejecutó y no alcanzó el criterio.
- `BLOQUEADO`: falta un dato o condición de seguridad.
- `NO_EJECUTADO`: todavía no se realizó.

## Fuentes oficiales

- [Micrófono XIAO ESP32-S3 Sense](https://wiki.seeedstudio.com/es/xiao_esp32s3_sense_mic/)
- [Alimentación y batería XIAO ESP32-S3](https://wiki.seeedstudio.com/es/xiao_esp32s3_getting_started/)

