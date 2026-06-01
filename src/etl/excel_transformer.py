"""
Módulo de transformación ETL para archivos Excel
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from loguru import logger
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.models import Usuario
from config import EXCEL_COLUMNS, OUTPUT_EXCEL_PATH


class ExcelTransformer:
    """Transformador ETL de Excel"""
    
    def __init__(self, df: pd.DataFrame, column_mapping: dict):
        self.df = df.copy()
        self.column_mapping = column_mapping
        self.df_transformed: Optional[pd.DataFrame] = None
        
    def normalize_columns(self):
        """Normalizar nombres de columnas"""
        logger.info("Normalizando columnas...")
        
        # Renombrar columnas según el mapeo
        rename_dict = {v: k for k, v in self.column_mapping.items()}
        self.df.rename(columns=rename_dict, inplace=True)
        
        logger.success(f"Columnas normalizadas: {list(self.df.columns)}")
        
    def clean_data(self):
        """Limpiar y validar datos"""
        logger.info("Limpiando datos...")
        
        # Eliminar filas completamente vacías
        self.df.dropna(how='all', inplace=True)
        
        # Limpiar espacios en blanco
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].str.strip() if self.df[col].dtype == 'object' else self.df[col]
        
        # Convertir email o cdalias a minúsculas
        if 'email' in self.df.columns:
            self.df['email'] = self.df['email'].str.lower()
        elif 'cdalias' in self.df.columns:
            self.df['cdalias'] = self.df['cdalias'].str.lower()
        
        # Eliminar duplicados basados en email o cdalias
        initial_rows = len(self.df)
        if 'email' in self.df.columns:
            self.df.drop_duplicates(subset=['email'], keep='first', inplace=True)
        elif 'cdalias' in self.df.columns:
            self.df.drop_duplicates(subset=['cdalias'], keep='first', inplace=True)
        
        duplicates_removed = initial_rows - len(self.df)
        
        if duplicates_removed > 0:
            logger.warning(f"Se eliminaron {duplicates_removed} duplicados")
        
        logger.success(f"Datos limpios: {len(self.df)} registros")
        
    def enrich_data(self):
        """Enriquecer datos con campos adicionales"""
        logger.info("Enriqueciendo datos...")
        
        # Agregar campos para métricas de GitHub
        self.df['creditos_usados'] = 0.0
        self.df['ultimo_uso'] = pd.NaT
        self.df['estado'] = 'pendiente'
        self.df['fecha_procesamiento'] = datetime.now()
        
        # Convertir fechas si existen
        if 'fecha' in self.df.columns:
            self.df['fecha'] = pd.to_datetime(self.df['fecha'], errors='coerce')
        
        logger.success("Datos enriquecidos con campos adicionales")
        
    def transform(self) -> pd.DataFrame:
        """Ejecutar pipeline de transformación completo"""
        logger.info("Iniciando transformación ETL...")
        
        self.normalize_columns()
        self.clean_data()
        self.enrich_data()
        
        self.df_transformed = self.df
        
        logger.success("Transformación completada exitosamente")
        return self.df_transformed
    
    def save(self, output_path: Optional[str] = None):
        """Guardar Excel transformado"""
        if self.df_transformed is None:
            raise ValueError("Primero debe ejecutar transform()")
        
        output_path = output_path or OUTPUT_EXCEL_PATH
        output_path = Path(output_path)
        
        # Asegurar que existe el directorio
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Guardando Excel transformado en: {output_path}")
        
        # Guardar con formato mejorado
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            self.df_transformed.to_excel(writer, sheet_name='Usuarios', index=False)
            
            # Obtener el workbook y worksheet para formato
            workbook = writer.book
            worksheet = writer.sheets['Usuarios']
            
            # Formato de encabezados
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            # Aplicar formato a encabezados
            for col_num, value in enumerate(self.df_transformed.columns.values):
                worksheet.write(0, col_num, value, header_format)
                # Ajustar ancho de columna
                worksheet.set_column(col_num, col_num, len(value) + 5)
        
        logger.success(f"Excel guardado exitosamente: {output_path}")
        return output_path
