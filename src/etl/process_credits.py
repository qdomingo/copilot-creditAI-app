"""
Procesamiento unificado de licencias y créditos de GitHub
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional
from loguru import logger


def extract_alias_from_email(email: str) -> str:
    """
    Extraer alias del email (parte antes del @)
    
    Args:
        email: Email completo (ej: mcubells@minsait.com)
        
    Returns:
        Alias (ej: mcubells)
    """
    if pd.isna(email) or not isinstance(email, str):
        return ""
    
    # Tomar la parte antes del @
    alias = email.split('@')[0].strip().lower()
    return alias


def extract_alias_from_username(username: str) -> str:
    """
    Extraer alias del username de GitHub (parte antes del _)
    
    Args:
        username: Username de GitHub (ej: mcubells_indra)
        
    Returns:
        Alias (ej: mcubells)
    """
    if pd.isna(username) or not isinstance(username, str):
        return ""
    
    # Tomar la parte antes del primer _
    alias = username.split('_')[0].strip().lower()
    return alias


def calculate_creditos_base(tipo_licencia: str) -> int:
    """
    Calcular créditos base según el tipo de licencia
    
    Args:
        tipo_licencia: Tipo de licencia (ej: "Github + Copilot Business", "Github + CB + ...")
        
    Returns:
        Créditos base: 30 para Business/CB, 70 para Enterprise/CE, 0 para otros
    """
    if pd.isna(tipo_licencia) or not isinstance(tipo_licencia, str):
        return 0
    
    tipo_lower = tipo_licencia.lower()
    
    # Buscar Business o CB
    if 'business' in tipo_lower or 'cb' in tipo_lower.split():
        return 30
    
    # Buscar Enterprise o CE
    if 'enterprise' in tipo_lower or 'ce' in tipo_lower.split():
        return 70
    
    # Resto
    return 0


def calculate_effective_creditos_usados(df_credits: pd.DataFrame) -> pd.Series:
    """
    Calcular créditos usados por fila según unit_type.

    Reglas:
    - unit_type=ai-credits: usar quantity * 0.01 (convertir de créditos a dólares)
    - resto (incl. requests): mantener aic_gross_amount
    """
    unit_type = df_credits.get('unit_type', pd.Series('', index=df_credits.index)).astype(str).str.strip().str.lower()
    is_ai_credits = unit_type == 'ai-credits'

    quantity = pd.to_numeric(df_credits.get('quantity', pd.Series(0, index=df_credits.index)), errors='coerce').fillna(0)
    aic_gross_amount = pd.to_numeric(df_credits.get('aic_gross_amount', pd.Series(0, index=df_credits.index)), errors='coerce').fillna(0)

    return aic_gross_amount.where(~is_ai_credits, quantity * 0.01)


def process_licenses_and_credits(
    excel_file_path: str,
    csv_file_path: str,
    output_path: Optional[str] = None
) -> Tuple[pd.DataFrame, str]:
    """
    Procesar Excel de licencias y CSV de créditos de GitHub
    
    Args:
        excel_file_path: Ruta al archivo Excel de licencias
        csv_file_path: Ruta al archivo CSV de créditos de GitHub
        output_path: Ruta de salida (opcional)
        
    Returns:
        Tuple con (DataFrame procesado, ruta del archivo guardado)
    """
    try:
        logger.info("=== Iniciando procesamiento de licencias y créditos ===")
        
        # 1. Cargar Excel de licencias
        logger.info(f"Cargando Excel de licencias: {excel_file_path}")
        df_licenses = pd.read_excel(excel_file_path)
        logger.info(f"Excel cargado: {len(df_licenses)} registros")
        logger.info(f"Columnas encontradas: {list(df_licenses.columns)}")
        
        # 1.1. Filtrar solo licencias con estado "Asignada"
        # Intentar buscar columna de estado por nombre o posición
        estado_col = None
        possible_estado_cols = ['Estado', 'estado', 'ESTADO', 'Estado Licencia', 'estado_licencia']
        
        # Si las columnas son índices numéricos, usar posición B = índice 1
        if isinstance(df_licenses.columns[0], int) or all(isinstance(c, int) for c in df_licenses.columns):
            logger.info("Usando columnas por índice numérico")
            # Columna B = índice 1 (0-based)
            estado_col = df_licenses.columns[1]
        else:
            # Buscar por nombre
            for col in possible_estado_cols:
                if col in df_licenses.columns:
                    estado_col = col
                    break
        
        if estado_col is None:
            # Si no se encuentra, usar la columna en posición B (índice 1)
            estado_col = df_licenses.columns[1] if len(df_licenses.columns) > 1 else None
        
        if estado_col is not None:
            logger.info(f"Columna de estado: '{estado_col}'")
            logger.info(f"Valores únicos en estado: {df_licenses[estado_col].unique()}")
            # Filtrar solo "Asignada"
            df_licenses = df_licenses[df_licenses[estado_col].str.strip().str.lower() == 'asignada'].copy()
            logger.info(f"Después de filtrar 'Asignada': {len(df_licenses)} registros")
        else:
            logger.warning("No se pudo identificar columna de estado, procesando todos los registros")
        
        # 1.2. Mapear columnas específicas del Excel por índice
        # Columnas requeridas (0-based index):
        # B (índice 1) - Estado (ya usado para filtrar)
        # C (índice 2) - Licencia → tipo_licencia
        # F (índice 5) - Proyecto → proyecto
        # H (índice 7) - Empresa → empresa
        # J (índice 9) - Código Empleado → cod_empleado
        # K (índice 10) - Nombre Completo → nombre_empleado
        # L (índice 11) - Mail → Mail
        
        logger.info("Mapeando columnas del Excel por índice...")
        
        # Verificar que hay suficientes columnas
        if len(df_licenses.columns) < 12:
            logger.error(f"El Excel debe tener al menos 12 columnas (A-L), pero solo tiene {len(df_licenses.columns)}")
            raise ValueError(f"Excel inválido: se esperan 12 columnas, encontradas {len(df_licenses.columns)}")
        
        # Crear DataFrame con solo las columnas que necesitamos
        df_mapped = pd.DataFrame()
        df_mapped['cod_empleado'] = df_licenses.iloc[:, 9]       # Columna J
        df_mapped['tipo_licencia'] = df_licenses.iloc[:, 2]      # Columna C
        df_mapped['proyecto'] = df_licenses.iloc[:, 5]           # Columna F
        df_mapped['empresa'] = df_licenses.iloc[:, 7]            # Columna H
        df_mapped['nombre_empleado'] = df_licenses.iloc[:, 10]   # Columna K
        df_mapped['Mail'] = df_licenses.iloc[:, 11]              # Columna L
        
        # Reemplazar df_licenses con el mapeado
        df_licenses = df_mapped
        
        logger.info(f"Columnas mapeadas: {list(df_licenses.columns)}")
        
        # 2. Extraer alias del email (columna Mail)
        logger.info("Extrayendo alias de emails...")
        
        if 'Mail' in df_licenses.columns:
            df_licenses['cdalias'] = df_licenses['Mail'].apply(extract_alias_from_email)
            logger.info("Alias extraídos de columna 'Mail'")
        else:
            logger.error(f"No se encontró columna 'Mail' después del mapeo")
            logger.error(f"Columnas disponibles: {list(df_licenses.columns)}")
            raise ValueError(
                f"No se pudo mapear la columna 'Mail' (columna L). "
                f"Columnas encontradas: {list(df_licenses.columns)}"
            )
        
        # 3. Cargar CSV de créditos de GitHub
        logger.info(f"Cargando CSV de créditos: {csv_file_path}")
        df_credits = pd.read_csv(csv_file_path)
        logger.info(f"CSV cargado: {len(df_credits)} registros")
        
        # 4. Extraer alias del username del CSV
        logger.info("Extrayendo alias de usernames del CSV...")
        if 'username' in df_credits.columns:
            df_credits['alias_csv'] = df_credits['username'].apply(extract_alias_from_username)
        else:
            logger.error("No se encontró columna 'username' en el CSV")
            raise ValueError("El CSV debe contener una columna 'username'")
        
        # 5. Agrupar CSV por alias con lógica por unit_type
        logger.info("Agrupando créditos por usuario...")
        if 'quantity' not in df_credits.columns:
            logger.error("No se encontró columna 'quantity' en el CSV")
            raise ValueError("El CSV debe contener una columna 'quantity'")

        if 'aic_gross_amount' not in df_credits.columns:
            logger.warning("No se encontró columna 'aic_gross_amount' en el CSV; se asumirá 0 para unit_type distinto de ai-credits")

        df_credits['creditos_usados_calculados'] = calculate_effective_creditos_usados(df_credits)
        
        df_credits_agg = df_credits.groupby('alias_csv').agg({
            'creditos_usados_calculados': 'sum',
            'date': ['min', 'max', 'count']
        }).reset_index()
        
        # Renombrar columnas
        df_credits_agg.columns = ['cdalias', 'creditos_usados', 'first_date', 'last_date', 'records_count']
        
        logger.info(f"Créditos agrupados: {len(df_credits_agg)} usuarios únicos")
        
        # 6. Hacer merge por alias (cdalias)
        logger.info("Combinando datos de licencias con créditos...")
        df_final = df_licenses.merge(
            df_credits_agg[['cdalias', 'creditos_usados', 'first_date', 'last_date', 'records_count']],
            on='cdalias',
            how='left'
        )
        
        # Rellenar créditos usados con 0 para usuarios sin datos en CSV
        df_final['creditos_usados'] = df_final['creditos_usados'].fillna(0)
        
        # 7. Preparar columnas finales
        logger.info("Preparando columnas finales...")
        
        # cod_empleado ya viene del Excel (columna J), no hay que generarlo
        
        # Calcular créditos_base según tipo_licencia
        logger.info("Calculando créditos base según tipo de licencia...")
        df_final['creditos_base'] = df_final['tipo_licencia'].apply(calculate_creditos_base)
        
        if 'estado_licencia' not in df_final.columns:
            # Como ya filtramos por "Asignada", todos tienen ese estado
            df_final['estado_licencia'] = 'Asignada'
        
        if 'grupo' not in df_final.columns:
            df_final['grupo'] = ''
        
        # Asegurar que las columnas necesarias existen
        required_columns = ['nombre_empleado', 'tipo_licencia', 'proyecto', 'empresa', 'cod_empleado']
        for col in required_columns:
            if col not in df_final.columns:
                logger.warning(f"Columna '{col}' no encontrada, agregando vacía")
                df_final[col] = ''
        
        # 8. Seleccionar y ordenar columnas finales
        final_columns = [
            'cod_empleado',
            'nombre_empleado',
            'cdalias',
            'proyecto',
            'empresa',
            'tipo_licencia',
            'estado_licencia',
            'creditos_base',
            'creditos_usados',
            'grupo'
        ]
        
        # Seleccionar solo las columnas finales
        df_final = df_final[final_columns]
        
        logger.info(f"DataFrame final: {len(df_final)} registros con {len(final_columns)} columnas")
        
        # 9. Guardar archivo Excel final
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = Path(__file__).parent.parent.parent / "Excel-CreditsIA"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"licencias_creditos_{timestamp}.xlsx"
        
        logger.info(f"Guardando archivo final en: {output_path}")
        df_final.to_excel(output_path, index=False)
        
        logger.success(f"✅ Procesamiento completado exitosamente")
        logger.info(f"   - Total registros: {len(df_final)}")
        logger.info(f"   - Usuarios con créditos: {(df_final['creditos_usados'] > 0).sum()}")
        logger.info(f"   - Total créditos usados: {df_final['creditos_usados'].sum():.2f}")
        
        return df_final, str(output_path)
        
    except Exception as e:
        logger.error(f"Error en procesamiento: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


def validate_excel_structure(df: pd.DataFrame) -> bool:
    """
    Validar que el Excel tenga las columnas mínimas requeridas
    
    Args:
        df: DataFrame del Excel
        
    Returns:
        True si es válido, False en caso contrario
    """
    required_columns = ['email']
    optional_columns = [
        'cod_empleado', 'nombre_empleado', 'proyecto', 
        'empresa', 'tipo_licencia', 'estado_licencia', 
        'creditos_base', 'grupo'
    ]
    
    missing_required = [col for col in required_columns if col not in df.columns]
    
    if missing_required:
        logger.error(f"Columnas requeridas faltantes: {missing_required}")
        return False
    
    return True


def validate_csv_structure(df: pd.DataFrame) -> bool:
    """
    Validar que el CSV tenga las columnas mínimas requeridas
    
    Args:
        df: DataFrame del CSV
        
    Returns:
        True si es válido, False en caso contrario
    """
    required_columns = ['username', 'quantity', 'date']
    
    missing_required = [col for col in required_columns if col not in df.columns]
    
    if missing_required:
        logger.error(f"Columnas requeridas faltantes en CSV: {missing_required}")
        return False
    
    return True
