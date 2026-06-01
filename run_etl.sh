#!/bin/bash

echo "========================================"
echo " GitHub Copilot Credits - ETL"
echo "========================================"
echo

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Ejecutando proceso ETL..."
python -m src.etl.transform_excel

echo
echo "Proceso completado."
