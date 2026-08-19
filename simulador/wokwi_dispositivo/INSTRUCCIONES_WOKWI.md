# Primer simulador de EntreVoces en Wokwi

## Qué demuestra

Este simulador representa el primer comportamiento del dispositivo: al mantener pulsado el botón virtual entra en `ESCUCHANDO`; al soltarlo recorre `ENVIANDO`, `PROCESANDO`, `REPRODUCIENDO` y vuelve a `LISTO`.

No graba, no reproduce sonido, no usa Wi-Fi, no usa pantalla y no prueba el micrófono PDM. Es deliberadamente pequeño: valida primero el modelo de interacción y la máquina de estados.

## Archivos

- `main.py`: arranque que MicroPython ejecuta automáticamente.
- `nucleo_estados.py`: transiciones puras y reutilizables del dispositivo.
- `diagram.json`: XIAO ESP32-S3 y botón virtual conectado a D1/GPIO2.
- `wokwi.toml`: configuración requerida por Wokwi para cargar el firmware MicroPython compatible con ESP32-S3.

`main.py` y `diagram.json` conservan nombres técnicos obligatorios de Wokwi y MicroPython. No representan una excepción a la regla de español para nombres propios del proyecto.

## Ejecución en el navegador

1. Abrir [Wokwi](https://wokwi.com/) y crear un proyecto desde la plantilla **MicroPython ESP32**.
2. Reemplazar el contenido de `main.py` por este `main.py`.
3. Crear el archivo `nucleo_estados.py` y copiar su contenido.
4. Reemplazar `diagram.json` por el archivo de esta carpeta.
5. Copiar `wokwi.toml` desde esta carpeta a la raíz del proyecto de Wokwi.
6. Iniciar la simulación y abrir el monitor serie.
7. Mantener el botón azul **Hablar** y soltarlo. El monitor debe mostrar todos los estados y terminar en `LISTO`.

## Cableado virtual

| Elemento | XIAO virtual | GPIO de MicroPython |
|---|---:|---:|
| Pulsador, terminal 1 | D1 | 2 |
| Pulsador, terminal 2 | GND | — |

El pulsador virtual usa `PULL_UP`: sin pulsar lee `1` y pulsado lee `0`. D1/GPIO2 es una elección para la simulación inicial; el GPIO del pulsador físico se confirmará al montar el hardware real.

## Criterio de éxito

El monitor serie muestra esta secuencia después de una pulsación completa:

```text
LISTO → ESCUCHANDO → ENVIANDO → PROCESANDO → REPRODUCIENDO → LISTO
```

## Siguiente paso

Construir el backend mínimo y sustituir las demoras simuladas por una solicitud HTTP bajo el mismo contrato que usará el dispositivo real.
