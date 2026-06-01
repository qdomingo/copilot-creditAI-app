#!/bin/bash

echo "========================================"
echo " GitHub Copilot Credits - Instalador"
echo "========================================"
echo

echo "[1/4] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

echo "[2/4] Activando entorno virtual..."
source venv/bin/activate

echo "[3/4] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo "[4/4] Creando archivo de configuración..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Se ha creado el archivo .env"
    echo "Por favor, edita .env con tus credenciales de GitHub"
fi

echo
echo "========================================"
echo " Instalación completada exitosamente!"
echo "========================================"
echo
echo "Próximos pasos:"
echo "1. Edita el archivo .env con tu token de GitHub"
echo "2. Ejecuta: ./run_app.sh"
echo
