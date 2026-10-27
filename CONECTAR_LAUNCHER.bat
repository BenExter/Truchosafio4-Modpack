@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 herramientas\configurar_launcher.py
) else (
    python herramientas\configurar_launcher.py
)
if errorlevel 1 echo No se pudo configurar el launcher.
pause
