# Índice de documentación de EntreVoces

**Versión:** 0.2  
**Fecha:** 2026-08-18

Este conjunto permite desarrollar el MVP sin perder el contexto entre sesiones o entre distintas IA.

## Archivos

1. [Plan de desarrollo del MVP](PLAN_DESARROLLO_MVP.md)  
   Define prioridades, hitos, tareas, criterios de aceptación y calendario acelerado.

2. [Documentación técnica](DOCUMENTACION_TECNICA.md)  
   Explica qué hace cada componente, cómo se comunica y dónde debe ubicarse.

3. [Prompt de sistema para IA](PROMPT_SISTEMA_IA.md)  
   Contiene las condiciones que debe respetar cualquier IA que continúe el proyecto.

4. [Registro de cambios](REGISTRO_CAMBIOS.md)  
   Conserva el historial cronológico de implementaciones y decisiones.

5. `../PROJECT_STATE.md`  
   Mantiene el estado operativo actual, el último trabajo terminado y el próximo paso.

6. [Guía de ejecución del backend](GUIA_BACKEND.md)  
   Explica cómo crear el entorno con `uv`, iniciar FastAPI y ejecutar las pruebas.

## Skills locales

Las Skills del proyecto se encuentran en `../.agents/skills/`:

- `validar-audio-dispositivo`;
- `diagnosticar-hardware-entrevoces`;
- `probar-e2e-entrevoces`;
- `evaluar-agente-entrevoces`;
- `desarrollar-backend-entrevoces`;
- `desarrollar-firmware-entrevoces`;
- `cerrar-modulo-entrevoces`.

## Regla de uso al comenzar una sesión

La persona o IA que retome EntreVoces debe leer, en este orden:

1. las instrucciones `AGENTS.md` disponibles;
2. `PROJECT_STATE.md`;
3. este índice;
4. el plan del MVP;
5. la documentación técnica relevante;
6. las últimas entradas del registro de cambios.

## Regla de cierre de una sesión

Antes de cerrar una sesión con cambios materiales se debe:

1. ejecutar las verificaciones correspondientes;
2. actualizar `PROJECT_STATE.md`;
3. agregar una entrada al registro de cambios;
4. actualizar el estado de las tareas del plan;
5. documentar qué funciona, dónde está y cómo se reproduce.
