---
name: cerrar-modulo-entrevoces
description: Cierra y documenta un módulo terminado de EntreVoces después de implementar backend, simulador, firmware, Flutter, IA o infraestructura. Usar cuando las pruebas ya pasaron o el usuario aprobó un módulo, para verificar evidencia, actualizar PROJECT_STATE.md, plan, documentación técnica y registro de cambios, y fijar el siguiente paso. No usar para marcar trabajo incompleto como terminado.
---

# Cerrar módulo EntreVoces

## Puerta de cierre

1. Confirmar que exista un criterio de aceptación explícito.
2. Ejecutar las pruebas pertinentes y conservar sus comandos y resultados.
3. Revisar el diff o la lista exacta de archivos modificados.
4. No cerrar si falta evidencia o si una prueba necesaria falla.

## Actualización obligatoria

1. Actualizar `PROJECT_STATE.md` con fecha, estado, implementación, tecnologías y versiones, rutas, ejecución, pruebas, riesgos y siguiente paso.
2. Actualizar `documentacion/PLAN_DESARROLLO_MVP.md` marcando únicamente tareas comprobadas.
3. Actualizar `documentacion/DOCUMENTACION_TECNICA.md` si cambió el funcionamiento o la ubicación.
4. Agregar una entrada nueva y acumulativa a `documentacion/REGISTRO_CAMBIOS.md`.
5. Ejecutar `scripts/verificar_memoria_proyecto.py` desde esta Skill.

## Comando

```powershell
python scripts/verificar_memoria_proyecto.py D:\ruta\del\proyecto --json
```

## Salida

Entregar resultado funcional, pruebas ejecutadas, documentación actualizada, deuda conocida y siguiente acción concreta. Diferenciar claramente implementación verificada de diseño pendiente.

