# Contrato de audio del MVP

## Entrada inicial

| Propiedad | Valor requerido |
|---|---|
| Contenedor | WAV RIFF |
| Codificación | PCM lineal sin compresión |
| Frecuencia | 16 000 Hz |
| Canales | 1 |
| Profundidad | 16 bits |
| Orden de bytes | Little-endian propio de WAV PCM |
| Duración inicial | Mayor que 0 y dentro del límite configurado |

## Recorrido inicial

```text
PDM del micrófono
→ PCM mono
→ encabezado WAV
→ solicitud HTTP completa
→ validación del backend
→ almacenamiento temporal
```

El backend puede transcodificar a Ogg Opus para almacenamiento definitivo. El firmware mantiene WAV durante el primer corte vertical para facilitar el diagnóstico.

## Capas de diagnóstico

1. **Captura:** comprobar que existan muestras y amplitud útil.
2. **Contenedor:** comprobar encabezado, frames y duración.
3. **Transporte:** comprobar tamaño, checksum y respuesta HTTP.
4. **Procesamiento:** comprobar aceptación del backend y proveedor STT.
5. **Reproducción:** comprobar descarga, decodificación, I2S, DAC y amplificación.

No se deben modificar varias capas al mismo tiempo durante una prueba.

