# Truchosafío 4 — Modpack oficial

**Repositorio de distribución para el launcher de Truchosafío 4**.

- Minecraft Java **1.21.1**
- **Fabric** exclusivamente.
- Mods/configuraciones desde assets de **GitHub Releases**.
- `manifest.json` en `main` es el índice público que consulta el launcher.
- El cliente valida SHA-256 y solo sustituye archivos administrados previamente.
- Los administradores publican desde Windows con `PUBLICAR_MODPACK.bat`.

## Estado inicial

El manifiesto contiene `"files": []` hasta que publiques la primera versión.
**Todavía NO hay un modpack publicado.** No distribuyas el launcher como listo para el evento antes de publicar los mods y hacer pruebas.

## Instalación para BenExter (administrador)

1. Instala Git, GitHub CLI y Python 3.11+ en Windows.
2. Extrae esta carpeta en tu PC y ejecuta `INICIALIZAR_GITHUB.bat`.
3. Autoriza el inicio de sesión de GitHub que abrirá el navegador; el programa crea un repositorio público `BenExter/Truchosafio4-Modpack` y sube los archivos de control.
4. Coloca los mods que **tienes derecho a redistribuir** dentro de `publish/mods/` y opcionalmente ajustes en `publish/config/`, `publish/defaultconfigs/`, paquetes de recursos o shaders.
5. Ejecuta `PUBLICAR_MODPACK.bat`, comprueba el resumen y confirma la publicación.
6. Prueba el launcher, el servidor y los mods antes de enviarlo a tus amigos.

## URL oficial del launcher

`https://raw.githubusercontent.com/BenExter/Truchosafio4-Modpack/main/manifest.json`

Cada ejecución consulta el mismo enlace. Al publicar una nueva versión, solo cambian los enlaces y hashes dentro del manifiesto.

## Seguridad y licencias

- No subas tokens, listas de jugadores, mapas privados, bases de datos, contraseñas o datos de cuentas.
- Publica únicamente mods y recursos con **permiso de redistribución**. Pedir permiso para modificar un logo no implica necesariamente permiso para subir el JAR de un tercero a una página pública.
- Los JAR de más de 100 MB se suben a **GitHub Releases**, no al historial Git.
- Una nueva publicación reemplaza el inventario **completo** del modpack, no solo un parche: antes de publicar asegúrate de tener todos los archivos necesarios en `publish/`.
- No borres la carpeta de mods antiguos durante una actualización si quieres conservarlos.

Lee `GUIA_WINDOWS.md` para instrucciones detalladas.
