# Guía de GitHub — Truchosafío 4

## Requisitos (Windows 10/11)

Instala Git (https://git-scm.com/download/win), GitHub CLI (https://cli.github.com/) y Python (https://www.python.org/downloads/). En una consola nueva ejecuta:

```powershell
git --version
gh --version
py -3 --version
```

Si `gh` no está instalado, puedes ejecutar en PowerShell:

```powershell
winget install --id GitHub.cli -e
```

## Primera vez

1. Extrae `Truchosafio4_GitHub_CONFIGURADO.zip` en una carpeta propia.
2. Ejecuta `INICIALIZAR_GITHUB.bat` y sigue los pasos de inicio de sesión de GitHub.
3. El script creará el repositorio público `BenExter/Truchosafio4-Modpack` si no existe.
4. La cuenta conectada deberá tener permisos de publicación en ese repositorio.
5. Abre GitHub y comprueba `https://github.com/BenExter/Truchosafio4-Modpack`.

No uses un repositorio privado con esta beta: el launcher descarga el manifiesto y los assets públicamente, sin tokens de autenticación.

## Publicar la versión 1

1. Copia **todos** los JAR compatibles con Fabric 1.21.1 que quieras distribuir a `publish/mods/`.
2. Los archivos de configuración van a `publish/config/` o `publish/defaultconfigs/`. Resource packs: `publish/resourcepacks/`.
3. Ejecuta `PUBLICAR_MODPACK.bat`.
4. El programa calcula SHA-256 de cada archivo, crea un GitHub Release en borrador, sube los assets, los verifica y publica el Release. Al final actualiza `manifest.json` en `main`.
5. Si algo falla antes del último paso, el manifiesto antiguo se mantiene; puedes corregir el problema y volver a ejecutar el script.

**Importante:** el contenido de `publish/` es el estado COMPLETO de la próxima versión. Si omites un mod que tenías antes, el launcher eliminará el archivo que gestionaba cuando lea el nuevo manifiesto.

## Conectar el launcher beta 0.1

En **Ajustes** pega esta URL:

`https://raw.githubusercontent.com/BenExter/Truchosafio4-Modpack/main/manifest.json`

También puedes ejecutar `CONECTAR_LAUNCHER.bat` en tu PC para escribir esa URL en la configuración local, sin borrar tus otros ajustes.

## Actualizaciones posteriores

Modifica o reemplaza archivos en `publish/`, ejecuta `PUBLICAR_MODPACK.bat` nuevamente y el launcher descargará los archivos con SHA-256 distintos al abrirse.

No es una vigilancia en tiempo real de tu carpeta: la publicación se realiza cuando das clic en `PUBLICAR_MODPACK.bat`. Después de publicar, la actualización de los clientes **sí es automática**.

## Diagnóstico

- Error `gh: command not found`: instala GitHub CLI y abre una consola nueva.
- Error al crear el repo: confirma inicio de sesión en la cuenta **BenExter** y permisos necesarios.
- Error 404 al cargar el manifiesto: primero crea el repositorio y comprueba que `main/manifest.json` existe.
- Error de descarga de un mod: comprueba que el Release está publicado y contiene el asset. El script no actualiza el manifiesto hasta verificar los assets.
- Error por tamaño del archivo: GitHub Releases admite archivos individuales grandes, pero comprueba los límites vigentes de la plataforma.
- Error por derecho de autor: no distribuyas un archivo de terceros sin tener el permiso correspondiente.
