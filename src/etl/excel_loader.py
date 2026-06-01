"""
Módulo para cargar y validar archivos Excel de entrada
"""
import pandas as pd
from pathlib import Path
from typing import Optional, List
from loguru import logger


class ExcelLoader:
    """Cargador y validador de archivos Excel"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        
    def load(self) -> pd.DataFrame:
        """Cargar archivo Excel"""
        try:
            logger.info(f"Cargando archivo Excel: {self.file_path}")
            
            if not self.file_path.exists():
                raise FileNotFoundError(f"El archivo no existe: {self.file_path}")
            
            # Intentar leer Excel
            self.df = pd.read_excel(self.file_path)
            logger.success(f"Archivo cargado correctamente: {len(self.df)} registros")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Error al cargar Excel: {e}")
            raise
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """Validar que existan las columnas requeridas"""
        if self.df is None:
            raise ValueError("Primero debe cargar el archivo con load()")
        
        missing_columns = set(required_columns) - set(self.df.columns)
        
        if missing_columns:
            logger.warning(f"Columnas faltantes: {missing_columns}")
            return False
        
        logger.success("Todas las columnas requeridas están presentes")
        return True
    
    def get_column_names(self) -> List[str]:
        """Obtener nombres de todas las columnas"""
        if self.df is None:
            raise ValueError("Primero debe cargar el archivo con load()")
        
        return self.df.columns.tolist()
    
    def detect_columns(self, column_variants: dict) -> dict:
        """
        Detectar columnas basándose en variantes de nombres
        
        Args:
            column_variants: Dict con key=nombre_estandar, value=lista de variantes
            
        Returns:
            Dict con mapeo nombre_estandar -> nombre_columna_real
        """
        if self.df is None:
            raise ValueError("Primero debe cargar el archivo con load()")
        
        columns_lower = {col.lower(): col for col in self.df.columns}
        detected = {}
        
        for standard_name, variants in column_variants.items():
            for variant in variants:
                if variant.lower() in columns_lower:
                    detected[standard_name] = columns_lower[variant.lower()]
                    logger.debug(f"Columna '{standard_name}' detectada como '{columns_lower[variant.lower()]}'")
                    break
        
        return detected
