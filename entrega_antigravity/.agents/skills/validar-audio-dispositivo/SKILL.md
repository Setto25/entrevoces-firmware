---
name: validar-audio-dispositivo
description: Valida, genera y diagnostica audio WAV del dispositivo EntreVoces y su contrato con el backend. Usar al inspeccionar grabaciones del XIAO ESP32-S3 Sense o del simulador, comprobar PCM mono de 16 kHz y 16 bits, investigar audio corrupto o silencioso, preparar muestras reproducibles y verificar flujos de subida o reproducción. No usar para diseñar conversaciones, moderación o búsqueda semántica.
---

# Validar audio del dispositivo

## Flujo

1. Preservar el archivo original y trabajar sobre una copia si se requiere conversión.
2. Leer [referencias/contrato_audio.md](referencias/contrato_audio.md) antes de evaluar compatibilidad.
3. Ejecutar `scripts/inspeccionar_wav.py` sobre cada WAV recibido.
4. Separar fallos de captura, contenedor, transporte y reproducción.
5. Generar una muestra controlada con `scripts/generar_audio_prueba.py` cuando se necesite aislar hardware o red.
6. Comparar la muestra controlada y la grabación real usando el mismo recorrido.
7. Informar propiedades observadas, veredicto, evidencia, bloqueo y siguiente prueba mínima.

## Comandos

Resolver las rutas de scripts desde el directorio de esta Skill.

```powershell
python scripts/inspeccionar_wav.py ruta\audio.wav --json
python scripts/generar_audio_prueba.py ruta\tono.wav --duracion 2
```

Interpretar los códigos de salida del inspector:

- `0`: cumple el contrato.
- `1`: se pudo leer, pero incumple el contrato.
- `2`: no se pudo abrir o interpretar como WAV.

## Diagnóstico

- Si el archivo no abre, revisar encabezado, truncamiento y transporte.
- Si abre pero no cumple formato, informar los campos exactos antes de convertir.
- Si cumple y no se oye, revisar amplitud, salida I2S, DAC, amplificador y parlante por separado.
- Si la muestra controlada funciona y la grabación no, concentrar el diagnóstico en captura PDM y buffers.
- No declarar un audio válido solo porque tenga extensión `.wav`.

## Salida requerida

Entregar siempre:

```text
Archivo evaluado
Propiedades detectadas
Cumplimiento del contrato
Errores y advertencias
Prueba ejecutada
Resultado observable
Siguiente prueba mínima
```

