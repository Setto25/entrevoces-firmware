---
name: diagnosticar-hardware-entrevoces
description: Guía y documenta pruebas seguras del hardware EntreVoces con XIAO ESP32-S3 Sense, botón, micrófono PDM, PCM5102A, PAM8403, parlante, pantalla ST7789V y batería. Usar al planificar cableado, asignar GPIO, probar periféricos, interpretar fallos eléctricos o registrar evidencia del banco de pruebas. No usar para adivinar pinouts ni energizar baterías o módulos sin identificar.
---

# Diagnosticar hardware EntreVoces

## Flujo obligatorio

1. Leer completamente [referencias/secuencia_pruebas.md](referencias/secuencia_pruebas.md).
2. Consultar `PROJECT_STATE.md` y el mapa de GPIO vigente si existe.
3. Identificar el modelo y las etiquetas reales de cada placa mediante fotografías o inspección directa.
4. Registrar tensión de alimentación, lógica, tierra común y conexiones antes de energizar.
5. Probar un solo componente o cambio por vez.
6. Capturar evidencia serial, visual, auditiva o de medición.
7. Clasificar el resultado como aprobado, fallido, bloqueado o no ejecutado.
8. Indicar la siguiente prueba mínima y reversible.

## Reglas de seguridad

- Detener la prueba si la batería está hinchada, perforada, caliente, corroída, sin identificar o presenta polaridad dudosa.
- Desarrollar inicialmente mediante USB-C.
- No fijar un pinout desde el nombre comercial; confirmar las etiquetas de la placa real.
- Probar el PCM5102A antes de conectar el PAM8403.
- Usar un solo canal del PAM8403 y no conectar sus salidas diferenciales a GND.
- Comenzar el audio con volumen mínimo.
- No modificar simultáneamente alimentación, cableado y firmware durante un diagnóstico.

## Registro requerido

Documentar:

```text
Fecha y responsable
Objetivo de la prueba
Componentes y versión
Alimentación utilizada
Conexiones y GPIO
Firmware y comando de carga
Resultado esperado
Resultado observado
Mediciones o salida serial
Estado final
Siguiente prueba
```

Actualizar la documentación técnica solo después de obtener evidencia verificable.

