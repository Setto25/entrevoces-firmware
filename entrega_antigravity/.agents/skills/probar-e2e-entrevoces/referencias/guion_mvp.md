# Guion E2E del MVP

## Datos controlados

- **Elena:** persona mayor propietaria del dispositivo.
- **Tomás:** usuario general que envía un saludo.
- **Carmen:** autora de una experiencia sobre costura en los años ochenta.

## Recorrido obligatorio

1. Tomás deja un saludo aprobado para Elena.
2. Elena inicia una sesión desde el simulador o dispositivo.
3. El backend consulta saludos no escuchados.
4. El avatar anuncia el mensaje mediante audio de sistema.
5. Se reproduce la voz original de Tomás.
6. La sesión registra el saludo activo.
7. Elena graba una respuesta.
8. El backend transcribe y modera la respuesta.
9. El backend deriva a Tomás como destinatario.
10. Tomás reproduce la voz original de Elena.

## Recorrido semántico opcional

1. Elena solicita historias de personas que trabajaron cosiendo.
2. El backend genera el embedding de consulta.
3. pgvector busca solo contenido aprobado, publicado y visible.
4. El resultado corresponde a la experiencia de Carmen.
5. Se reproduce la voz original de Carmen.

## Casos negativos mínimos

- Audio vacío o con formato incorrecto.
- Credencial de dispositivo inválida.
- Saludo bloqueado por moderación.
- Moderación indisponible.
- Respuesta sin saludo activo.
- Comando de dispositivo desconocido.
- Timeout del backend.
- Contenido privado o eliminado presente entre vectores cercanos.

## Evidencia mínima

- identificador de solicitud y sesión;
- estado HTTP y respuesta validada;
- filas o eventos persistidos pertinentes;
- objeto de audio esperado;
- estado de moderación;
- destinatario derivado;
- transición final del dispositivo.

