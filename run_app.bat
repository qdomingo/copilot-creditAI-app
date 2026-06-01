@echo off
echo ========================================
echo  GitHub Copilot Credits - Aplicacion
echo ========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Iniciando aplicacion Streamlit...
streamlit run src/app.py

pause
