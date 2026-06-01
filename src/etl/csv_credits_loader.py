"""
Módulo para cargar y procesar CSV de créditos de GitHub
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from loguru import logger


class GitHubCreditsCSVLoader:
    """Cargador y procesador de CSV de créditos de GitHub"""
    
    # Columnas esperadas en el CSV
    EXPECTED_COLUMNS = [
        'date', 'username', 'product', 'sku', 'model', 'quantity', 
        'unit_type', 'applied_cost_per_quantity', 'gross_amount', 
        'discount_amount', 'net_amount', 'exceeds_quota', 
        'total_monthly_quota', 'organization', 'cost_center_name',
        'aic_quantity', 'aic_gross_amount'
    ]
    
    def __init__(self):
        self.df_credits = None
        self.file_path = None
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Cargar CSV de créditos de GitHub
        
        Args:
            file_path: Ruta al archivo CSV
            
        Returns:
            DataFrame con los datos de créditos
        """
        try:
            logger.info(f"Cargando CSV de créditos desde: {file_path}")
            
            # Leer CSV
            df = pd.read_csv(file_path)
            
            # Validar columnas
            missing_cols = set(self.EXPECTED_COLUMNS) - set(df.columns)
            if missing_cols:
                logger.warning(f"Columnas faltantes en el CSV: {missing_cols}")
            
            # Convertir columnas numéricas
            numeric_columns = [
                'quantity', 'applied_cost_per_quantity', 'gross_amount',
                'discount_amount', 'net_amount', 'total_monthly_quota',
                'aic_quantity', 'aic_gross_amount'
            ]
            
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convertir columna de fecha
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Limpiar espacios en username y normalizar (eliminar sufijos como _indra, _empresa, etc.)
            if 'username' in df.columns:
                df['username'] = df['username'].str.strip()
                # Crear columna normalizada sin sufijos (toma la parte antes del primer _)
                df['username_normalized'] = df['username'].str.split('_').str[0]
            
            self.df_credits = df
            self.file_path = file_path
            
            logger.success(f"CSV cargado exitosamente: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error al cargar CSV: {e}")
            raise
    
    def get_user_credits_summary(self, username: str) -> Optional[Dict]:
        """
        Obtener resumen de créditos para un usuario específico
        
        Args:
            username: Nombre de usuario de GitHub
            
        Returns:
            Diccionario con resumen de créditos del usuario
        """
        if self.df_credits is None:
            logger.warning("No hay datos de créditos cargados")
            return None
        
        try:
            # Filtrar por usuario (case insensitive) usando username normalizado
            df_user = self.df_credits[
                self.df_credits['username_normalized'].str.lower() == username.lower()
            ].copy()
            
            if len(df_user) == 0:
                return {
                    'username': username,
                    'creditos_usados': 0,
                    'total_quantity': 0,
                    'total_aic_quantity': 0,
                    'records_count': 0,
                    'models_used': [],
                    'first_date': None,
                    'last_date': None
                }
            
            # Calcular agregados - USAR aic_gross_amount como créditos usados
            summary = {
                'username': username,
                'creditos_usados': df_user['aic_gross_amount'].sum() if 'aic_gross_amount' in df_user.columns else 0,
                'total_quantity': df_user['quantity'].sum() if 'quantity' in df_user.columns else 0,
                'total_aic_quantity': df_user['aic_quantity'].sum() if 'aic_quantity' in df_user.columns else 0,
                'records_count': len(df_user),
                'models_used': df_user['model'].unique().tolist() if 'model' in df_user.columns else [],
                'first_date': df_user['date'].min() if 'date' in df_user.columns else None,
                'last_date': df_user['date'].max() if 'date' in df_user.columns else None
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error al obtener resumen de créditos para {username}: {e}")
            return None
    
    def get_all_users_summary(self) -> pd.DataFrame:
        """
        Obtener resumen de créditos para todos los usuarios
        
        Returns:
            DataFrame con resumen por usuario
        """
        if self.df_credits is None:
            logger.warning("No hay datos de créditos cargados")
            return pd.DataFrame()
        
        try:
            # Agrupar por usuario NORMALIZADO
            summary = self.df_credits.groupby('username_normalized').agg({
                'quantity': 'sum',
                'aic_quantity': 'sum',
                'aic_gross_amount': 'sum',
                'date': ['min', 'max', 'count']
            }).reset_index()
            
            # Aplanar columnas multi-nivel
            summary.columns = [
                'username', 'total_quantity', 'total_aic_quantity', 
                'creditos_usados', 'first_date', 'last_date', 'records_count'
            ]
            
            logger.info(f"Resumen generado para {len(summary)} usuarios")
            return summary
            
        except Exception as e:
            logger.error(f"Error al generar resumen: {e}")
            return pd.DataFrame()
    
    def merge_with_licenses(self, df_licenses: pd.DataFrame, 
                           license_alias_col: str = 'cdalias',
                           username_col: str = 'username') -> pd.DataFrame:
        """
        Combinar datos de créditos con datos de licencias
        
        Args:
            df_licenses: DataFrame con datos de licencias
            license_alias_col: Nombre de la columna de alias en df_licenses
            username_col: Nombre de la columna de username en df_credits
            
        Returns:
            DataFrame combinado
        """
        try:
            if self.df_credits is None:
                logger.warning("No hay datos de créditos cargados")
                return df_licenses
            
            # Obtener resumen por usuario
            df_summary = self.get_all_users_summary()
            
            if df_summary.empty:
                logger.warning("No se pudo generar resumen de créditos")
                return df_licenses
            
            # Normalizar alias para merge (lowercase)
            df_licenses_copy = df_licenses.copy()
            df_summary_copy = df_summary.copy()
            
            df_licenses_copy['_alias_lower'] = df_licenses_copy[license_alias_col].str.lower()
            df_summary_copy['_username_lower'] = df_summary_copy[username_col].str.lower()
            
            # Merge
            df_merged = df_licenses_copy.merge(
                df_summary_copy,
                left_on='_alias_lower',
                right_on='_username_lower',
                how='left'
            )
            
            # Limpiar columnas temporales
            df_merged = df_merged.drop(columns=['_alias_lower', '_username_lower'], errors='ignore')
            
            # Rellenar NaN en columnas numéricas con 0
            numeric_cols = [
                'total_quantity', 'total_aic_quantity', 'creditos_usados', 'records_count'
            ]
            for col in numeric_cols:
                if col in df_merged.columns:
                    df_merged[col] = df_merged[col].fillna(0)
            
            logger.success(f"Datos combinados exitosamente: {len(df_merged)} registros")
            return df_merged
            
        except Exception as e:
            logger.error(f"Error al combinar datos: {e}")
            return df_licenses
    
    def get_credits_by_date_range(self, start_date: Optional[str] = None, 
                                  end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Filtrar créditos por rango de fechas
        
        Args:
            start_date: Fecha inicial (formato YYYY-MM-DD)
            end_date: Fecha final (formato YYYY-MM-DD)
            
        Returns:
            DataFrame filtrado
        """
        if self.df_credits is None:
            logger.warning("No hay datos de créditos cargados")
            return pd.DataFrame()
        
        try:
            df_filtered = self.df_credits.copy()
            
            if start_date:
                start = pd.to_datetime(start_date)
                df_filtered = df_filtered[df_filtered['date'] >= start]
            
            if end_date:
                end = pd.to_datetime(end_date)
                df_filtered = df_filtered[df_filtered['date'] <= end]
            
            logger.info(f"Filtrado por fechas: {len(df_filtered)} registros")
            return df_filtered
            
        except Exception as e:
            logger.error(f"Error al filtrar por fechas: {e}")
            return self.df_credits
    
    def get_statistics(self) -> Dict:
        """
        Obtener estadísticas generales de los datos de créditos
        
        Returns:
            Diccionario con estadísticas
        """
        if self.df_credits is None:
            return {}
        
        try:
            stats = {
                'total_records': len(self.df_credits),
                'unique_users': self.df_credits['username_normalized'].nunique() if 'username_normalized' in self.df_credits.columns else 0,
                'total_quantity': self.df_credits['quantity'].sum() if 'quantity' in self.df_credits.columns else 0,
                'total_creditos_usados': self.df_credits['aic_gross_amount'].sum() if 'aic_gross_amount' in self.df_credits.columns else 0,
                'total_aic_quantity': self.df_credits['aic_quantity'].sum() if 'aic_quantity' in self.df_credits.columns else 0,
                'date_range': {
                    'start': self.df_credits['date'].min() if 'date' in self.df_credits.columns else None,
                    'end': self.df_credits['date'].max() if 'date' in self.df_credits.columns else None
                },
                'unique_models': self.df_credits['model'].nunique() if 'model' in self.df_credits.columns else 0,
                'organizations': self.df_credits['organization'].unique().tolist() if 'organization' in self.df_credits.columns else []
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error al calcular estadísticas: {e}")
            return {}
