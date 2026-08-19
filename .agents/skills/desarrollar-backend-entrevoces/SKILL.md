---
name: desarrollar-backend-entrevoces
description: Implementa, modifica o revisa el backend FastAPI de EntreVoces con Pydantic, SQLAlchemy, Alembic, PostgreSQL, pgvector, almacenamiento de audio y proveedores de IA. Usar para endpoints, modelos, esquemas, repositorios, servicios, autenticación, moderación, sesiones, saludos, experiencias y búsqueda. No usar para firmware, Flutter ni acceso directo del LLM a datos.
---

# Desarrollar backend EntreVoces

## Inicio

1. Leer `AGENTS.md`, `PROJECT_STATE.md` y el hito activo.
2. Leer [referencias/reglas_backend.md](referencias/reglas_backend.md).
3. Inspeccionar el código y pruebas existentes antes de diseñar archivos nuevos.
4. Seleccionar un corte vertical pequeño con un criterio de aceptación observable.

## Implementación

1. Definir primero el contrato Pydantic y los casos de éxito y error.
2. Escribir o ajustar pruebas que expresen la regla del dominio.
3. Implementar la secuencia router → servicio → repositorio.
4. Mantener identidad, autorización y destinatario fuera de las decisiones del LLM.
5. Encapsular SDK externos detrás de interfaces del dominio.
6. Aplicar moderación antes de cualquier publicación.
7. Guardar binarios de audio fuera de PostgreSQL.
8. Ejecutar pruebas focalizadas y luego la suite pertinente.

## Límites

- No introducir `execute_sql`, acceso genérico a base de datos ni ejecución arbitraria como herramienta del agente.
- No aceptar identificadores sensibles desde argumentos del LLM cuando puedan derivarse de la sesión.
- No devolver secretos ni URLs permanentes públicas.
- No distribuir consultas pgvector fuera del servicio o repositorio dedicado.
- No comenzar RAG antes de aprobar búsqueda semántica y filtros.

## Entrega

Informar archivos modificados, contrato, migraciones, pruebas ejecutadas, resultado, riesgos y siguiente paso. Invocar `$cerrar-modulo-entrevoces` cuando el módulo cumpla su criterio de aceptación.

