#!/bin/bash

echo "========================================"
echo " GitHub Copilot Credits - Aplicación"
echo "========================================"
echo

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Iniciando aplicación Streamlit..."
streamlit run src/app.py
