import machine
import struct
import time

# Configuración de pines para el micrófono PDM en XIAO ESP32-S3 Sense
PIN_CLK = 42
PIN_DAT = 41

FRECUENCIA_MUESTREO = 16000
BITS_POR_MUESTRA = 16
CANALES = 1
DURACION_SEGUNDOS = 3

def crear_encabezado_wav(tamanio_datos: int) -> bytearray:
    """Genera un encabezado WAV RIFF PCM básico."""
    encabezado = bytearray()
    encabezado.extend(b'RIFF')
    encabezado.extend(struct.pack('<I', tamanio_datos + 36))
    encabezado.extend(b'WAVE')
    encabezado.extend(b'fmt ')
    encabezado.extend(struct.pack('<I', 16))
    encabezado.extend(struct.pack('<H', 1)) # PCM
    encabezado.extend(struct.pack('<H', CANALES))
    encabezado.extend(struct.pack('<I', FRECUENCIA_MUESTREO))
    encabezado.extend(struct.pack('<I', FRECUENCIA_MUESTREO * CANALES * (BITS_POR_MUESTRA // 8)))
    encabezado.extend(struct.pack('<H', CANALES * (BITS_POR_MUESTRA // 8)))
    encabezado.extend(struct.pack('<H', BITS_POR_MUESTRA))
    encabezado.extend(b'data')
    encabezado.extend(struct.pack('<I', tamanio_datos))
    return encabezado

def capturar_audio():
    """Captura datos del micrófono y los guarda en un archivo WAV."""
    print("Configurando I2S...")
    
    # En MicroPython estándar, la inicialización puede variar.
    # Asignaremos sck y ws al pin de reloj, y sd al pin de datos.
    pin_clk = machine.Pin(PIN_CLK)
    pin_dat = machine.Pin(PIN_DAT)
    
    try:
        i2s = machine.I2S(
            1,
            sck=pin_clk,
            ws=pin_clk, # ws actúa como el reloj en algunas configuraciones PDM
            sd=pin_dat,
            mode=machine.I2S.RX,
            bits=BITS_POR_MUESTRA,
            format=machine.I2S.MONO,
            rate=FRECUENCIA_MUESTREO,
            ibuf=16384 # Buffer intermedio de 16 KB
        )
    except Exception as e:
        print("Error al inicializar I2S:", e)
        return

    tamanio_total_bytes = FRECUENCIA_MUESTREO * (BITS_POR_MUESTRA // 8) * CANALES * DURACION_SEGUNDOS
    archivo_salida = "/captura_pdm.wav"
    
    print(f"Grabando {DURACION_SEGUNDOS} segundos en {archivo_salida}...")
    
    try:
        with open(archivo_salida, "wb") as f:
            # Escribir el encabezado WAV
            f.write(crear_encabezado_wav(tamanio_total_bytes))
            
            bytes_leidos_total = 0
            buffer_lectura = bytearray(4096)
            
            while bytes_leidos_total < tamanio_total_bytes:
                # Leer datos desde el periférico
                bytes_leidos = i2s.readinto(buffer_lectura)
                
                if bytes_leidos > 0:
                    f.write(buffer_lectura[:bytes_leidos])
                    bytes_leidos_total += bytes_leidos
                    
        print(f"Grabación terminada. Se guardaron {bytes_leidos_total} bytes de audio.")
        
        # Inspeccionar las primeras muestras para ver si no es puro silencio (0) o máximo (-1)
        with open(archivo_salida, "rb") as f:
            f.seek(44) # Saltar el encabezado
            primeros_bytes = f.read(20)
            muestras = struct.unpack(f'<{len(primeros_bytes)//2}h', primeros_bytes)
            print("Primeras 10 muestras PCM:", muestras)
            
    except Exception as e:
        print("Error durante la captura o guardado:", e)
    finally:
        i2s.deinit()
        print("Periférico I2S desinicializado.")

if __name__ == "__main__":
    capturar_audio()
