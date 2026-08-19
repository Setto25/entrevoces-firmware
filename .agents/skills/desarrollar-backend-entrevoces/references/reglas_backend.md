# Reglas del backend

## Capas

```text
Router FastAPI
→ esquema Pydantic
→ autorización
→ servicio de negocio
→ repositorio
→ PostgreSQL o almacenamiento
```

El router traduce HTTP. El servicio decide reglas. El repositorio persiste. El proveedor adapta servicios externos.

## Entidades principales

- `Usuario`
- `Dispositivo`
- `ActivoAudio`
- `Experiencia`
- `EmbeddingExperiencia`
- `Saludo`
- `SesionConversacion`
- `TurnoConversacion`
- `EventoModeracion`
- `EventoAuditoria`

## Invariantes

- Un saludo publicado tiene moderación aprobada.
- Una experiencia buscable está aprobada, publicada, visible y no eliminada.
- Una respuesta al saludo activo deriva el destinatario desde el saludo persistido.
- Un fallo de moderación deja el contenido sin publicar.
- Un dispositivo usa una credencial revocable distinta de credenciales humanas.
- Un audio binario no se almacena en la tabla principal.

## Proveedores

Definir interfaces en español:

```text
ProveedorModeloLenguaje
ProveedorVozATexto
ProveedorTextoAVoz
ProveedorEmbeddings
ProveedorModeracion
ProveedorAlmacenamiento
```

Cada integración externa define timeout, errores tipados, configuración por entorno y doble determinista de pruebas.

## Pruebas mínimas

- contrato y validación de endpoints;
- permisos por rol y dispositivo;
- derivación de destinatario;
- estados de moderación;
- filtros de visibilidad;
- idempotencia cuando corresponda;
- fallos y timeouts de proveedores;
- ausencia de secretos en respuestas y logs.

