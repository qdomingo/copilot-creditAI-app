"""
Script principal para ejecutar la transformación ETL
"""
from loguru import logger
from pathlib import Path
import sys

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.etl.excel_loader import ExcelLoader
from src.etl.excel_transformer import ExcelTransformer
from src.utils.logger import setup_logger
from config import INPUT_EXCEL_PATH, EXCEL_COLUMNS, ensure_directories


def main():
    """Función principal de transformación"""
    try:
        # Asegurar que existen los directorios
        ensure_directories()
        
        logger.info("=== Iniciando proceso ETL ===")
        
        # 1. Cargar Excel
        loader = ExcelLoader(INPUT_EXCEL_PATH)
        df = loader.load()
        
        logger.info(f"Columnas encontradas: {loader.get_column_names()}")
        
        # 2. Detectar columnas automáticamente
        column_mapping = loader.detect_columns(EXCEL_COLUMNS)
        
        if not column_mapping:
            logger.error("No se pudieron detectar las columnas necesarias")
            logger.info("Por favor verifica que el Excel contenga columnas como: email, nombre, alias, licencia")
            return False
        
        logger.info(f"Mapeo de columnas: {column_mapping}")
        
        # 3. Transformar datos
        transformer = ExcelTransformer(df, column_mapping)
        df_transformed = transformer.transform()
        
        logger.info(f"Registros transformados: {len(df_transformed)}")
        
        # 4. Guardar resultado
        output_path = transformer.save()
        
        logger.success(f"=== Proceso ETL completado exitosamente ===")
        logger.success(f"Archivo de salida: {output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error en el proceso ETL: {e}")
        return False


if __name__ == "__main__":
    # Configurar logger
    logger.add("logs/etl_{time}.log", rotation="1 day")
    main()
