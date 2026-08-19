---
name: probar-e2e-entrevoces
description: Ejecuta y documenta pruebas de extremo a extremo del MVP EntreVoces con Elena, Tomás y Carmen. Usar al verificar saludos, respuestas, moderación, reproducción de audio, contexto activo, búsqueda semántica o una demostración completa entre simulador, dispositivo, backend y cliente público. No usar para marcar un flujo como aprobado sin evidencia observable de cada etapa.
---

# Probar E2E EntreVoces

## Preparación

1. Leer [referencias/guion_mvp.md](referencias/guion_mvp.md).
2. Leer `PROJECT_STATE.md` y detectar qué hitos están realmente implementados.
3. Identificar ambiente, versión, servicios, proveedor simulado o real y datos de prueba.
4. Evitar datos reales de usuarios y evitar cambios en producción sin autorización explícita.
5. Definir identificadores de correlación para seguir cada turno.

## Ejecución

1. Preparar Elena, Tomás y Carmen mediante el mecanismo de datos de prueba del proyecto.
2. Ejecutar primero el recorrido obligatorio de saludo y respuesta.
3. Ejecutar la búsqueda de Carmen solo cuando H7 esté implementado.
4. Incluir fallos de moderación, red y contexto activo.
5. Capturar solicitudes, estados, registros y resultados sin exponer secretos.
6. Repetir dos veces el guion destinado a demostración.

## Criterios

- Verificar resultados persistidos y no solo respuestas HTTP.
- Verificar que el audio correcto llegue al destinatario correcto.
- Verificar que la respuesta derive su destinatario desde `saludo_activo_id`.
- Verificar que contenido bloqueado no aparezca en bandejas o búsquedas.
- Verificar que un error permita regresar a `LISTO`.
- Marcar como no ejecutada cualquier etapa ausente; no simular evidencia.

## Informe

Entregar una tabla con caso, precondición, acción, evidencia, resultado esperado, resultado observado y estado. Terminar con bloqueos, regresiones y decisión `APROBADO` o `NO_APROBADO` para el alcance evaluado.

