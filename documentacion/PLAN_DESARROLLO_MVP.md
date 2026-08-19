# Plan acelerado de desarrollo del MVP de EntreVoces

**Versión:** 0.1  
**Fecha base:** 2026-08-17  
**Horizonte propuesto:** cinco jornadas de desarrollo, ajustables al tiempo real disponible  
**Estrategia:** cortes verticales verificables y reemplazo transparente del simulador por el dispositivo

## 1. Resultado que debe demostrar el MVP

El MVP queda demostrado cuando se ejecuta, de forma repetible, este recorrido:

```text
Elena pulsa el botón
→ el dispositivo indica que escucha
→ Elena graba un mensaje
→ el dispositivo sube el WAV
→ el backend identifica la sesión y procesa el turno
→ el backend devuelve comandos y audio
→ el dispositivo reproduce la respuesta
→ siempre regresa al estado listo
```

El flujo social mínimo agrega:

```text
Tomás deja un saludo
→ el contenido se modera
→ Elena lo escucha
→ Elena responde al saludo activo
→ el backend determina que el destinatario es Tomás
→ Tomás puede reproducir la respuesta
```

## 2. Prioridades para un plazo corto

### P0 — Imprescindible

- Backend mínimo ejecutable.
- Contrato tipado y versionado entre cliente y servidor.
- Simulador funcional.
- Banco de pruebas del hardware por componentes.
- Recorrido voz–nube–voz en el ESP32.
- Flujo social determinista de un saludo y una respuesta.
- Manejo visible de fallos y retorno al estado listo.
- Documentación para instalar, ejecutar y probar.

### P1 — Muy deseable

- STT y TTS reales.
- Moderación real con resultados aprobado, bloqueado o revisión.
- Flutter mínimo para la bandeja y el reproductor de Tomás.
- Despliegue remoto demostrable.

### P2 — Si queda tiempo

- Embeddings y búsqueda semántica.
- Agente con herramientas restringidas.
- Avatar simple en pantalla.

### P3 — Después del MVP

- RAG.
- Streaming.
- Notificaciones push completas.
- Administración y cuidadores.
- Batería, carcasa y optimización energética definitivas.

## 3. Tablero maestro de hitos

| Hito | Entregable | Estado | Criterio de salida |
|---|---|---|---|
| H0 | Plan y memoria del proyecto | COMPLETADO | Los documentos iniciales existen y se relacionan entre sí. |
| H1 | Backend y simulador mínimos | COMPLETADO | Un WAV viaja al backend y el simulador reproduce un WAV de respuesta. |
| H2 | Hardware validado por piezas | PENDIENTE | Serie, Wi‑Fi, botón, micrófono y salida de audio funcionan por separado. |
| H3 | Voz–nube–voz en dispositivo | PENDIENTE | El ESP32 usa el contrato del simulador y completa un turno. |
| H4 | Núcleo social determinista | PENDIENTE | Elena escucha y responde un saludo de Tomás sin intervención del LLM. |
| H5 | STT, TTS y moderación | PENDIENTE | Se transcribe, modera y sintetiza una respuesta mediante interfaces. |
| H6 | Cliente público mínimo | PENDIENTE | Tomás reproduce la respuesta desde Flutter o, por contingencia, desde una interfaz mínima documentada. |
| H7 | Búsqueda semántica y agente limitado | PENDIENTE | Una consulta encuentra la historia de Carmen y solo usa herramientas autorizadas. |
| H8 | Demostración E2E y despliegue | PENDIENTE | El guion completo pasa dos veces seguidas y queda documentado. |

## 4. H0 — Preparación y documentación

### Tareas

- [x] Revisar el informe maestro.
- [x] Confirmar pantalla, parlantes y origen de la batería.
- [x] Priorizar el simulador al comienzo.
- [x] Crear `PROJECT_STATE.md`.
- [x] Crear el plan, el prompt de IA, la documentación y el registro.
- [x] Crear y validar las Skills locales de desarrollo, hardware y calidad.
- [ ] Confirmar cuántas jornadas reales quedan antes de la demostración.
- [ ] Elegir los proveedores de IA iniciales.

### Criterio de aceptación

Una IA nueva puede leer los documentos y señalar sin adivinar cuál es el siguiente paso.

## 5. H1 — Backend y simulador mínimos

### Objetivo

Validar el protocolo antes de depender del hardware o de proveedores de IA.

### Backend

- [x] Crear la estructura de carpetas en español.
- [x] Configurar Python y dependencias con versiones fijadas.
- [x] Reorganizar el backend en `servidor/aplicacion` y las pruebas de contrato en `servidor/pruebas`.
- [x] Aislar el entorno `uv` en `servidor/.venv` y separar las pruebas del simulador en `simulador/pruebas`.
- [x] Crear FastAPI.
- [x] Implementar `GET /api/v1/salud`.
- [x] Implementar inicio y cierre de sesión temporal y revocable del dispositivo.
- [x] Implementar recepción de WAV con límites de tipo y tamaño.
- [x] Implementar respuesta fija mediante un audio local conocido.
- [ ] Definir esquemas Pydantic de comandos y errores; el comando está tipado y falta unificar el esquema de error.
- [x] Agregar identificador de correlación para cada solicitud.
- [x] Añadir pruebas de contrato y errores.

### Simulador

- [x] Simular una pulsación en Wokwi sobre XIAO ESP32-S3.
- [x] Crear la configuración mínima de Wokwi requerida por `wokwi.toml` y dejar el firmware MicroPython compatible en la raíz del proyecto.
- [x] Seleccionar o generar un WAV local PCM controlado.
- [x] Mostrar y probar la máquina de estados base.
- [x] Iniciar y cerrar una sesión temporal usando una credencial de entorno.
- [x] Subir el audio.
- [x] Interpretar los comandos devueltos.
- [x] Descargar y reproducir opcionalmente el audio en Windows.
- [x] Simular pérdida de red, timeout y respuesta inválida.

### Criterio de aceptación

Un comando documentado inicia el servidor y otro ejecuta el simulador. El simulador envía un WAV válido, reproduce la respuesta y vuelve al estado listo. Las pruebas automatizadas pasan.

## 6. H2 — Validación del hardware por piezas

### Puerta de seguridad de la batería

- [ ] Inspeccionar hinchazón, perforaciones, corrosión, olor y daño térmico.
- [ ] Leer etiqueta y confirmar química y tensión nominal.
- [ ] Medir polaridad y tensión con multímetro.
- [ ] Confirmar que sea una celda recargable de litio de 3,7 V compatible.
- [ ] No usarla si está hinchada, dañada, invertida, sin identificar o fuera de tensión razonable.
- [ ] Desarrollar inicialmente con USB-C; integrar batería al final.

### Parlantes reciclados

- [ ] Inspeccionar etiqueta o medir resistencia en reposo.
- [ ] Confirmar compatibilidad aproximada con 4 u 8 Ω.
- [ ] Probar primero a volumen mínimo en un solo canal del PAM8403.
- [ ] No unir salidas amplificadas ni conectar un terminal del parlante a GND.

### Pruebas eléctricas y funcionales

- [ ] H2.0: instalar una versión fijada de MicroPython para ESP32-S3 y verificar REPL.
- [ ] H2.0a: comprobar memoria disponible, PSRAM, GPIO y Wi‑Fi.
- [ ] H2.1: cargar firmware mínimo y observar serie.
- [ ] H2.2: conectar Wi‑Fi y consultar `/api/v1/salud`.
- [ ] H2.3: leer el botón con antirrebote.
- [ ] H2.4: capturar micrófono PDM a 16 kHz y 16 bits. (Pendiente de H2.4b)
- [x] H2.4a: determinar si `machine.I2S` del firmware elegido soporta PDM en esta placa. (Resultado: No expone filtro PDM a PCM).
- [ ] H2.4b: si PDM no está expuesto, validar un módulo nativo mínimo o firmware MicroPython personalizado antes de continuar.
- [ ] H2.5: reproducir tono o WAV por I2S hacia PCM5102A.
- [ ] H2.6: validar salida analógica antes del PAM8403.
- [ ] H2.7: conectar un canal del PAM8403 y un parlante.
- [ ] H2.8: mostrar estados básicos en ST7789V.

### Criterio de aceptación

Cada componente cuenta con una prueba independiente y un resultado registrado. Todavía no se exige que todos funcionen al mismo tiempo.

## 7. H3 — Corte vertical voz–nube–voz

### Tareas

- [x] Implementar y probar en CPython la máquina de estados y el cliente HTTP de firmware, sin afirmar validación física.
- [ ] Capturar un WAV completo en PSRAM.
- [ ] Validar duración y encabezado WAV.
- [x] Preparar la subida del mismo formato utilizado por el simulador, con sesión temporal, mediante transporte MicroPython simulado.
- [x] Preparar el procesamiento seguro de `REPRODUCIR_AUDIO` y el rechazo de comandos desconocidos.
- [ ] Descargar audio por bloques para no agotar memoria.
- [ ] Reproducirlo mediante PCM5102A y PAM8403.
- [ ] Indicar estados en pantalla y por serie.
- [ ] Recuperarse de Wi‑Fi caído, timeout, audio inválido y error 5xx.
- [ ] Ejecutar cinco ciclos consecutivos.

### Criterio de aceptación

Cinco pulsaciones completan cinco turnos sin reinicio manual y el equipo vuelve a listo después de cada turno o error.

## 8. H4 — Núcleo social determinista

### Datos y seguridad

- [ ] Levantar PostgreSQL y pgvector.
- [ ] Configurar SQLAlchemy y Alembic.
- [ ] Modelar usuarios, dispositivos, audios, experiencias, saludos, sesiones, turnos, moderación y auditoría.
- [ ] Sembrar Elena, Tomás y Carmen.
- [ ] Emitir credencial revocable para el dispositivo.
- [ ] Mantener secretos únicamente en el servidor.

### Reglas sociales

- [ ] Crear una experiencia.
- [ ] Crear un saludo.
- [ ] Consultar saludos no escuchados.
- [ ] Marcar un saludo como escuchado.
- [ ] Guardar `saludo_activo_id` en la sesión.
- [ ] Responder al saludo activo sin aceptar un destinatario propuesto por el cliente o LLM.
- [ ] Aplicar moderación antes de publicar.

### Criterio de aceptación

Elena escucha el saludo sembrado de Tomás, responde y el backend relaciona automáticamente la respuesta con Tomás.

## 9. H5 — STT, TTS y moderación

### Tareas

- [ ] Definir `ProveedorVozATexto`.
- [ ] Definir `ProveedorTextoAVoz`.
- [ ] Definir `ProveedorModeracion`.
- [ ] Crear implementaciones simuladas deterministas.
- [ ] Integrar un proveedor real detrás de cada interfaz necesaria.
- [ ] Guardar nombre y versión del proveedor en eventos relevantes.
- [ ] Manejar aprobado, bloqueado y revisión requerida.
- [ ] Bloquear datos de contacto, solicitudes de dinero y contenido dañino definido por el producto.
- [ ] Evitar publicar si falla la moderación.

### Criterio de aceptación

Una frase grabada se transcribe, se modera y produce una respuesta audible. Un caso de prueba riesgoso no se publica.

## 10. H6 — Cliente público mínimo

### Flutter preferido

- [ ] Crear proyecto Flutter con estructura en español cuando sea configurable.
- [ ] Implementar acceso mínimo.
- [ ] Mostrar bandeja de saludos.
- [ ] Reproducir audio original.
- [ ] Grabar y enviar saludo.
- [ ] Mostrar estado de moderación.

### Contingencia si el plazo se agota

Una colección de API o interfaz web temporal puede demostrar el lado de Tomás, pero debe registrarse como deuda y no presentarse como aplicación móvil terminada.

### Criterio de aceptación

Tomás puede escuchar desde un cliente distinto del dispositivo la respuesta de Elena.

## 11. H7 — Búsqueda semántica y agente limitado

### Búsqueda

- [ ] Definir `ProveedorEmbeddings`.
- [ ] Generar embeddings solo para experiencias aprobadas y publicadas.
- [ ] Implementar un único servicio de búsqueda semántica.
- [ ] Filtrar visibilidad, autor, publicación, moderación y eliminación dentro de la consulta.
- [ ] Verificar que “personas que cosían” encuentra la historia de Carmen.

### Agente

- [ ] Definir herramientas con esquemas Pydantic cerrados.
- [ ] Permitir solo operaciones del dominio.
- [ ] Resolver usuario, dispositivo y destinatario en el backend.
- [ ] Tratar transcripciones recuperadas como contenido y no como instrucciones.
- [ ] Rechazar herramientas desconocidas o argumentos no autorizados.

### Criterio de aceptación

La frase de búsqueda encuentra a Carmen y una instrucción maliciosa dentro de una historia no puede ampliar las capacidades del agente.

## 12. H8 — Demostración E2E y despliegue

### Guion obligatorio

1. Elena pulsa el botón.
2. El dispositivo anuncia y reproduce el saludo de Tomás.
3. Elena responde.
4. La moderación aprueba.
5. Tomás reproduce la respuesta.
6. Elena solicita historias relacionadas con costura.
7. El sistema encuentra y reproduce la historia original de Carmen.

### Verificaciones

- [ ] Ejecutar el guion dos veces sin intervención técnica.
- [ ] Registrar tiempos de cada etapa.
- [ ] Verificar retorno a listo tras errores.
- [ ] Confirmar que ninguna clave secreta está en firmware o Flutter.
- [ ] Confirmar que contenido no aprobado no aparece en búsquedas.
- [ ] Documentar instalación, ejecución, pruebas y restauración.
- [ ] Etiquetar una versión demostrable.

## 13. Calendario acelerado sugerido

| Jornada | Foco principal | Resultado al cierre |
|---|---|---|
| 1 | H1 | Backend mínimo y simulador completan un turno con audio fijo. |
| 2 | H2 + H3 parcial | MicroPython validado, riesgo PDM resuelto y captura/reproducción local disponibles. |
| 3 | H3 + H4 | Voz–nube–voz físico y saludo determinista almacenado. |
| 4 | H5 + H6 parcial | STT/TTS/moderación y cliente público mínimo. |
| 5 | H7 opcional + H8 | Demostración estabilizada, documentación y despliegue. |

Si el plazo es menor, se elimina H7 antes de sacrificar H3, H4 o la estabilidad. RAG no entra en estas cinco jornadas.

## 14. Reglas de seguimiento diario

Al comenzar:

1. leer `PROJECT_STATE.md`;
2. seleccionar un solo hito activo;
3. ejecutar primero la prueba que demostrará el resultado;
4. limitar el trabajo paralelo que pueda bloquear el corte vertical.

Al terminar:

1. marcar tareas realmente verificadas;
2. registrar comandos y resultados;
3. actualizar arquitectura si cambió;
4. agregar entrada al registro de cambios;
5. indicar el siguiente paso exacto.

## 15. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Batería reciclada desconocida | Daño o incendio | Desarrollar por USB y aplicar la puerta de seguridad antes de integrarla. |
| Parlante de impedancia desconocida | Audio deficiente o daño | Medir, probar a volumen mínimo y usar un solo canal. |
| Conflictos de GPIO/I2S/SPI | Retraso de hardware | Probar periféricos aislados y cerrar el mapa solo con módulos presentes. |
| MicroPython sin PDM expuesto | Bloquea micrófono integrado | Ejecutar la prueba PDM al inicio de H2 y preparar un módulo nativo mínimo sin migrar la lógica de aplicación. |
| Latencia de IA | Mala demostración | Conservar respuestas simuladas y audios de contingencia. |
| Flutter consume el plazo | No completar dispositivo | Mantener Flutter en P1 y proteger H3/H4. |
| Integración de muchos proveedores | Fallos difíciles de aislar | Usar interfaces y dobles deterministas desde el inicio. |
| Moderación indisponible | Publicación insegura | Aplicar cierre seguro: el contenido queda en revisión. |
| Wi‑Fi inestable | Turno incompleto | Timeouts, reintentos limitados y retorno visible a listo. |
