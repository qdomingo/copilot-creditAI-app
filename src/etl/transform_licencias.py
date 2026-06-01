"""
Módulo de transformación de Excel de licencias
"""
import pandas as pd
from pathlib import Path
from loguru import logger


def extraer_alias_de_email(email):
    """
    Extrae el alias del email (parte antes de la @)
    
    Args:
        email: Email completo (ej: usuario@empresa.com)
        
    Returns:
        Alias sin dominio (ej: usuario)
    """
    if pd.isna(email) or email == "":
        return ""
    
    email_str = str(email).strip()
    if "@" in email_str:
        return email_str.split("@")[0]
    return email_str


def transformar_excel_licencias(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Transforma el Excel de licencias al formato requerido
    
    Mapeo de columnas:
    - cod_empleado = columna J (índice 9)
    - nombre_empleado = columna K (índice 10)
    - cdalias = columna L (índice 11) - email sin @dominio
    - proyecto = columna F (índice 5)
    - empresa = columna H (índice 7)
    - tipo_licencia = columna C (índice 2)
    - estado_licencia = columna B (índice 1)
    
    Filtra solo registros con estado "Asignada"
    
    Args:
        input_path: Ruta del archivo Excel de entrada
        output_path: Ruta del archivo Excel de salida
        
    Returns:
        DataFrame transformado
    """
    try:
        logger.info(f"Leyendo archivo: {input_path}")
        
        # Leer Excel con encabezados
        df = pd.read_excel(input_path, header=0)
        
        logger.info(f"Total de registros leídos: {len(df)}")
        logger.info(f"Columnas: {df.columns.tolist()}")
        
        # Obtener columnas por índice
        columnas = df.columns.tolist()
        
        logger.info("Creando DataFrame de salida...")
        
        df_output = pd.DataFrame()
        
        # cod_empleado = columna J (índice 9)
        df_output['cod_empleado'] = df.iloc[:, 9] if len(columnas) > 9 else ""
        
        # nombre_empleado = columna K (índice 10)
        df_output['nombre_empleado'] = df.iloc[:, 10] if len(columnas) > 10 else ""
        
        # cdalias = columna L (índice 11) - email sin @dominio
        if len(columnas) > 11:
            df_output['cdalias'] = df.iloc[:, 11].apply(extraer_alias_de_email)
        else:
            df_output['cdalias'] = ""
        
        # proyecto = columna F (índice 5)
        df_output['proyecto'] = df.iloc[:, 5] if len(columnas) > 5 else ""
        
        # empresa = columna H (índice 7)
        df_output['empresa'] = df.iloc[:, 7] if len(columnas) > 7 else ""
        
        # tipo_licencia = columna C (índice 2)
        df_output['tipo_licencia'] = df.iloc[:, 2] if len(columnas) > 2 else ""
        
        # estado_licencia = columna B (índice 1) - preservar estado original
        df_output['estado_licencia'] = df.iloc[:, 1] if len(columnas) > 1 else ""
        
        # Calcular créditos_base según el tipo de licencia
        def calcular_creditos_base(tipo_licencia):
            """
            Calcula los créditos base según el tipo de licencia:
            - Copilot Business (CB) o CB + DebtDoctor (todos los grupos) → 30 créditos
            - Copilot Enterprise (CE) o CE + DebtDoctor (todos los grupos) → 30 créditos
            - Otros → 0
            
            Ejemplos:
            - "Github + CB + DebtDoctor Grupo10" → 30
            - "Github + CE + DebtDoctor Grupo5" → 30
            - "Copilot Business" → 30
            - "Copilot Enterprise" → 70 (solo si NO tiene DebtDoctor)
            """
            if pd.isna(tipo_licencia) or tipo_licencia == "":
                return 0
            
            tipo_str = str(tipo_licencia).strip().upper()
            
            # Verificar si tiene DebtDoctor (siempre 30 créditos, sea CB o CE)
            if 'DEBTDOCTOR' in tipo_str or 'DEBT DOCTOR' in tipo_str:
                return 30
            
            # Sin DebtDoctor: verificar tipo base
            # Copilot Enterprise sin DebtDoctor → 70 créditos
            if 'COPILOT ENTERPRISE' in tipo_str or tipo_str.startswith('CE ') or tipo_str == 'CE':
                return 70
            
            # Copilot Business sin DebtDoctor → 30 créditos
            if 'COPILOT BUSINESS' in tipo_str or tipo_str.startswith('CB ') or tipo_str == 'CB':
                return 30
            
            return 0
        
        # Aplicar el cálculo de créditos base
        df_output['creditos_base'] = df_output['tipo_licencia'].apply(calcular_creditos_base)
        df_output['creditos_usados'] = 0.0
        df_output['grupo'] = ""
        
        # Campos adicionales para la aplicación
        df_output['ultimo_uso'] = pd.NaT
        df_output['fecha_procesamiento'] = pd.Timestamp.now()
        
        # Crear email y licencia para compatibilidad con la aplicación
        df_output['email'] = df_output['cdalias'].apply(lambda x: f"{x}@empresa.com" if x and x != "" else "")
        df_output['licencia'] = df_output['tipo_licencia']
        
        logger.info(f"Registros antes de filtrar: {len(df_output)}")
        
        # Filtrar solo registros con estado "Asignada" (columna B, índice 1)
        mask_asignada = df_output['estado_licencia'].str.strip().str.lower() == "asignada"
        df_output = df_output[mask_asignada].copy()
        
        logger.info(f"Registros después de filtrar por 'Asignada': {len(df_output)}")
        
        # Eliminar filas completamente vacías
        df_output = df_output.dropna(how='all')
        
        # Ordenar por cdalias descendente
        df_output = df_output.sort_values('cdalias', ascending=False, na_position='last')
        
        # Reset index
        df_output = df_output.reset_index(drop=True)
        
        logger.info(f"Registros finales: {len(df_output)}")
        
        # Guardar resultado
        logger.info(f"Guardando resultado en: {output_path}")
        
        # Crear directorio si no existe
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar con formato
        with pd.ExcelWriter(output_path, engine='xlsxwriter', 
                          engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
            df_output.to_excel(writer, sheet_name='Licencias', index=False)
            
            # Obtener workbook y worksheet para formato
            workbook = writer.book
            worksheet = writer.sheets['Licencias']
            
            # Formato de encabezados
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            # Aplicar formato a encabezados
            for col_num, value in enumerate(df_output.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
                # Ajustar ancho de columna basado en el contenido
                max_length = max(
                    df_output[value].astype(str).str.len().max(),
                    len(value)
                )
                worksheet.set_column(col_num, col_num, min(max_length + 2, 50))
        
        logger.success(f"✅ Transformación completada exitosamente!")
        logger.success(f"📊 Archivo de salida: {output_path}")
        logger.info(f"📈 Estadísticas:")
        logger.info(f"   - Registros procesados: {len(df_output)}")
        logger.info(f"   - Columnas generadas: {len(df_output.columns)}")
        
        return df_output
        
    except Exception as e:
        logger.error(f"❌ Error en la transformación: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise
