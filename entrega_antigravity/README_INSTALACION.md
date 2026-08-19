# Paquete portable de EntreVoces para Antigravity

## Contenido

Esta carpeta contiene una copia autocontenida de las instrucciones, el estado operativo, la documentación de arquitectura, el prompt de sistema y las siete Skills de EntreVoces. Se omiten los archivos `agents/openai.yaml` porque son metadatos exclusivos de Codex y Antigravity no los necesita.

La excepción nominal `entrega_antigravity` corresponde al nombre técnico de destino. Todos los nombres propios internos del proyecto permanecen en español.

```text
entrega_antigravity/
├── AGENTS.md
├── PROJECT_STATE.md
├── PROMPT_SISTEMA_ANTIGRAVITY.md
├── documentacion/
└── .agents/
    ├── rules/entrevoces_mvp.md
    └── skills/
```

## Instalación en Antigravity

1. Copiar el contenido de esta carpeta a la raíz del espacio de trabajo de EntreVoces que se abrirá en Antigravity. No se debe copiar dentro de `src`, `servidor` ni otra subcarpeta.
2. Abrir esa raíz como espacio de trabajo en Antigravity. El agente detecta `AGENTS.md` y las Skills ubicadas en `.agents/skills/`.
3. En **Customizations → Rules**, agregar `.agents/rules/entrevoces_mvp.md` como regla del espacio de trabajo y elegir **Always On**.
4. Si se usa Antigravity mediante API o un agente administrado, cargar además `PROMPT_SISTEMA_ANTIGRAVITY.md` como `system_instruction`. `AGENTS.md` y el prompt se complementan.
5. Iniciar una conversación nueva y pedir: “Lee `AGENTS.md` y `PROJECT_STATE.md`; indica el hito activo sin modificar archivos.” Debe identificar H2 como validación física por piezas.

## Skills incluidas

- `validar-audio-dispositivo`
- `diagnosticar-hardware-entrevoces`
- `probar-e2e-entrevoces`
- `evaluar-agente-entrevoces`
- `desarrollar-backend-entrevoces`
- `desarrollar-firmware-entrevoces`
- `cerrar-modulo-entrevoces`

Las rutas auxiliares se adaptaron de `references/` a `referencias/`, de modo que los enlaces internos de las Skills se resuelven correctamente y se mantiene la convención en español. Los scripts de verificación de audio y memoria se preservan sin cambios.

## Límites importantes

El paquete porta instrucciones y conocimiento; no concede acceso a infraestructura ni sustituye los controles de autorización del backend. El modelo no puede elegir identificadores sensibles, ejecutar SQL/código, extraer secretos ni publicar contenido sin moderación. Estas restricciones deben seguir respaldadas por esquemas, servicios y autorización reales del backend.
