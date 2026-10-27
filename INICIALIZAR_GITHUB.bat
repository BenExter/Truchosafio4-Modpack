@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set REPO=BenExter/Truchosafio4-Modpack
where gh >nul 2>nul || (echo ERROR: Instala GitHub CLI desde https://cli.github.com/ & pause & exit /b 1)
where git >nul 2>nul || (echo ERROR: Instala Git desde https://git-scm.com/download/win & pause & exit /b 1)
echo =====================================================
echo  TRUCHOSAFIO 4 - CREAR REPOSITORIO DE ACTUALIZACIONES
echo =====================================================
echo Repositorio: %REPO%
echo Sera PUBLICO para que el launcher de tus amigos funcione.
echo Se subiran SOLO los archivos de configuracion del repositorio.
echo No se subiran los JAR de publish/ en el historial de Git.
echo.
gh auth status >nul 2>nul
if errorlevel 1 (
    echo Autorizacion necesaria en GitHub. Sigue el navegador.
    gh auth login -h github.com -p https -w
    if errorlevel 1 goto :fail
)
if not exist .git\HEAD (
    git init -b main
    if errorlevel 1 goto :fail
)
git branch -M main
if errorlevel 1 goto :fail
git add README.md GUIA_WINDOWS.md manifest.json .gitignore .github herramientas *.bat
if errorlevel 1 goto :fail
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Preparar actualizador oficial de Truchosafio 4"
    if errorlevel 1 (
        echo Configura tu nombre y correo para Git una vez y reintenta.
        echo git config --global user.name "BenExter"
        echo git config --global user.email "tu-correo-de-GitHub"
        goto :fail
    )
)
gh repo view %REPO% >nul 2>nul
if errorlevel 1 (
    gh repo create %REPO% --public --source=. --remote=origin --push
    if errorlevel 1 goto :fail
) else (
    git remote get-url origin >nul 2>nul
    if errorlevel 1 git remote add origin https://github.com/%REPO%.git
    git push -u origin main
    if errorlevel 1 goto :fail
)
echo.
echo LISTO: https://github.com/%REPO%
echo Manifiesto: https://raw.githubusercontent.com/%REPO%/main/manifest.json
echo Ahora coloca tus mods en publish\mods y ejecuta PUBLICAR_MODPACK.bat.
pause
exit /b 0
:fail
echo No se completo la inicializacion. Revisa el error de arriba.
pause
exit /b 1
