"""
Script de ejemplo para ejecutar el ETL completo
"""
import pandas as pd
from pathlib import Path
import sys

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.etl.excel_loader import ExcelLoader
from src.etl.excel_transformer import ExcelTransformer
from src.utils.logger import setup_logger
from config import EXCEL_COLUMNS, ensure_directories

logger = setup_logger("logs/example_etl.log")


def create_sample_excel():
    """Crear un Excel de ejemplo para pruebas"""
    data = {
        'Email': [
            'juan.perez@empresa.com',
            'maria.garcia@empresa.com',
            'carlos.rodriguez@empresa.com',
            'ana.martinez@empresa.com',
            'luis.hernandez@empresa.com'
        ],
        'Nombre Completo': [
            'Juan Pérez',
            'María García',
            'Carlos Rodríguez',
            'Ana Martínez',
            'Luis Hernández'
        ],
        'Alias': [
            'jperez',
            'mgarcia',
            'crodriguez',
            'amartinez',
            'lhernandez'
        ],
        'Tipo Licencia': [
            'Business',
            'Business',
            'Enterprise',
            'Business',
            'Enterprise'
        ],
        'Fecha Asignacion': [
            '2024-01-15',
            '2024-01-20',
            '2024-02-01',
            '2024-02-10',
            '2024-03-05'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Guardar
    ensure_directories()
    sample_path = Path("data/input/ejemplo_usuarios.xlsx")
    df.to_excel(sample_path, index=False)
    
    logger.info(f"Excel de ejemplo creado: {sample_path}")
    return sample_path


def run_example_etl():
    """Ejecutar ejemplo completo de ETL"""
    try:
        logger.info("=== Ejemplo de ETL ===")
        
        # Crear Excel de ejemplo
        sample_path = create_sample_excel()
        
        # Cargar
        logger.info("1. Cargando Excel...")
        loader = ExcelLoader(str(sample_path))
        df = loader.load()
        
        logger.info(f"   Registros cargados: {len(df)}")
        logger.info(f"   Columnas: {loader.get_column_names()}")
        
        # Detectar columnas
        logger.info("2. Detectando columnas...")
        column_mapping = loader.detect_columns(EXCEL_COLUMNS)
        logger.info(f"   Mapeo detectado: {column_mapping}")
        
        # Transformar
        logger.info("3. Transformando datos...")
        transformer = ExcelTransformer(df, column_mapping)
        df_transformed = transformer.transform()
        
        logger.info(f"   Registros transformados: {len(df_transformed)}")
        logger.info(f"   Columnas finales: {list(df_transformed.columns)}")
        
        # Guardar
        logger.info("4. Guardando resultado...")
        output_path = transformer.save()
        
        logger.success(f"✅ ETL completado exitosamente")
        logger.success(f"   Archivo de salida: {output_path}")
        
        # Mostrar muestra de datos
        logger.info("\n=== Muestra de datos transformados ===")
        print(df_transformed.head().to_string())
        
    except Exception as e:
        logger.error(f"❌ Error en el ejemplo: {e}")
        raise


if __name__ == "__main__":
    run_example_etl()
