@echo off
echo ========================================
echo  GitHub Copilot Credits - Instalador
echo ========================================
echo.

echo [1/4] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo [4/4] Creando archivo de configuracion...
if not exist .env (
    copy .env.example .env
    echo Se ha creado el archivo .env
    echo Por favor, edita .env con tus credenciales de GitHub
)

echo.
echo ========================================
echo  Instalacion completada exitosamente!
echo ========================================
echo.
echo Proximos pasos:
echo 1. Edita el archivo .env con tu token de GitHub
echo 2. Ejecuta: run_app.bat
echo.
pause
