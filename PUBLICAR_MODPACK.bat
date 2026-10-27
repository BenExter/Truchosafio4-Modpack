@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where gh >nul 2>nul || (echo ERROR: Instala GitHub CLI desde https://cli.github.com/ & pause & exit /b 1)
where git >nul 2>nul || (echo ERROR: Instala Git desde https://git-scm.com/download/win & pause & exit /b 1)
where py >nul 2>nul
if not errorlevel 1 (
    py -3 herramientas\publicar_modpack.py
) else (
    python herramientas\publicar_modpack.py
)
if errorlevel 1 (
    echo.
    echo La publicacion no se completo. Lee el mensaje anterior.
    pause
    exit /b 1
)
echo.
echo Actualizacion enviada correctamente. Tus amigos la recibiran al iniciar el launcher.
pause
