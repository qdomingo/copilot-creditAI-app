@echo off
echo ========================================
echo  GitHub Copilot Credits - ETL
echo ========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Ejecutando proceso ETL...
python -m src.etl.transform_excel

echo.
echo Proceso completado.
pause
