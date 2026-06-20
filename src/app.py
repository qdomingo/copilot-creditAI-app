"""
Aplicación principal de Streamlit para control de créditos de GitHub Copilot
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys
import tempfile

# Agregar el directorio raíz al path para importaciones
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils.logger import setup_logger
from src.etl.process_credits import process_licenses_and_credits
from src.dashboard.components import (
    show_metric_card,
    create_user_usage_chart,
    create_credit_consumption_histogram,
    show_user_table,
    show_filters_sidebar,
    apply_filters
)
from config import (
    APP_TITLE, 
    APP_ICON, 
    PROCESSED_DIR,
    ensure_directories
)

# Configurar página
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup logger
logger = setup_logger()

# CSS personalizado para estética moderna
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Inicializar estado de la sesión"""
    if 'df_usuarios' not in st.session_state:
        st.session_state.df_usuarios = None
    if 'df_csv_raw' not in st.session_state:
        st.session_state.df_csv_raw = None
    if 'archivo_procesado' not in st.session_state:
        st.session_state.archivo_procesado = None
    if 'excel_file' not in st.session_state:
        st.session_state.excel_file = None
    if 'csv_file' not in st.session_state:
        st.session_state.csv_file = None


def get_latest_file_in_dir(directory: Path, pattern: str = "*.xlsx"):
    """Obtener el archivo más reciente en un directorio"""
    try:
        files = list(directory.glob(pattern))
        if not files:
            return None
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        return latest_file
    except Exception as e:
        logger.error(f"Error al buscar archivos: {e}")
        return None


def load_processed_data():
    """Cargar datos ya procesados si existen en Excel-CreditsIA"""
    processed_dir = Path(PROCESSED_DIR)
    latest_file = get_latest_file_in_dir(processed_dir, "*.xlsx")
    
    if latest_file and latest_file.exists():
        try:
            df = pd.read_excel(latest_file)
            logger.info(f"Datos cargados desde: {latest_file}")
            st.session_state.archivo_procesado = latest_file
            return df
        except Exception as e:
            logger.error(f"Error al cargar datos procesados: {e}")
    return None


def clean_processed_data():
    """Limpiar datos procesados y archivos de la carpeta Excel-CreditsIA"""
    try:
        # Limpiar carpeta Excel-CreditsIA
        excel_credits_dir = Path(__file__).parent.parent / "Excel-CreditsIA"
        if excel_credits_dir.exists():
            for file in excel_credits_dir.glob("*.xlsx"):
                try:
                    file.unlink()
                    logger.info(f"Archivo eliminado: {file.name}")
                except Exception as e:
                    logger.error(f"Error al eliminar {file.name}: {e}")
        
        # Limpiar session_state
        st.session_state.df_usuarios = None
        st.session_state.df_csv_raw = None
        st.session_state.archivo_procesado = None
        
        logger.info("Datos procesados limpiados")
        return True
        
    except Exception as e:
        logger.error(f"Error al limpiar datos: {e}")
        return False


def process_files(excel_file, csv_file):
    """Procesar archivos Excel y CSV"""
    try:
        # Crear archivos temporales
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_excel:
            tmp_excel.write(excel_file.getbuffer())
            tmp_excel_path = tmp_excel.name

        # Cargar CSV agregado (incluye todos los días)
        df_csv_raw = pd.read_csv(csv_file)

        # Crear CSV temporal para el proceso ETL existente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_csv:
            df_csv_raw.to_csv(tmp_csv.name, index=False)
            tmp_csv_path = tmp_csv.name
        
        # Procesar
        with st.spinner("Procesando archivos..."):
            df_result, output_path = process_licenses_and_credits(
                tmp_excel_path,
                tmp_csv_path
            )
            
            st.session_state.df_usuarios = df_result
            st.session_state.df_csv_raw = df_csv_raw  # Guardar CSV original
            st.session_state.archivo_procesado = output_path
            
            # Limpiar archivos temporales
            Path(tmp_excel_path).unlink()
            Path(tmp_csv_path).unlink()
            
            st.success(f"✅ Procesamiento completado: {len(df_result)} registros")
            st.success(f"📄 CSV cargado: {len(df_csv_raw)} fila(s)")
            st.success(f"📁 Archivo guardado: {Path(output_path).name}")
            
            return True
            
    except Exception as e:
        st.error(f"❌ Error al procesar archivos: {e}")
        logger.error(f"Error en process_files: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def _find_first_existing_column(df: pd.DataFrame, candidates):
    """Encontrar la primera columna existente por nombre (insensible a mayúsculas)."""
    col_map = {str(col).strip().lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in col_map:
            return col_map[candidate]
    return None


def apply_excel_user_filter(df: pd.DataFrame, uploaded_excel):
    """Aplicar filtro de usuarios a partir de un Excel con cod_empleado o alias."""
    try:
        df_filter = pd.read_excel(uploaded_excel)
    except Exception as e:
        return df, {
            'ok': False,
            'message': f"No se pudo leer el Excel: {e}",
            'type': 'error'
        }

    if df_filter.empty:
        return df, {
            'ok': False,
            'message': "El Excel de filtro está vacío.",
            'type': 'warning'
        }

    code_candidates = [
        'cod_empleado',
        'codigo_empleado',
        'código_empleado',
        'codigo empleado',
        'código empleado'
    ]
    alias_candidates = ['cdalias', 'alias', 'usuario', 'username']

    code_col_file = _find_first_existing_column(df_filter, code_candidates)
    alias_col_file = _find_first_existing_column(df_filter, alias_candidates)

    if not code_col_file and not alias_col_file:
        return df, {
            'ok': False,
            'message': (
                "El Excel de filtro debe contener obligatoriamente una columna de "
                "'cod_empleado' o 'alias/cdalias'."
            ),
            'type': 'error'
        }

    mask = pd.Series([False] * len(df), index=df.index)
    applied_with = []
    skipped_with = []

    if code_col_file:
        code_values = {
            str(value).strip()
            for value in df_filter[code_col_file].dropna().tolist()
            if str(value).strip() != ''
        }
        if code_values:
            if 'cod_empleado' in df.columns:
                mask = mask | df['cod_empleado'].astype(str).str.strip().isin(code_values)
                applied_with.append(f"código empleado ({len(code_values)} valor(es))")
            else:
                skipped_with.append("código empleado (no existe en datos cargados)")

    if alias_col_file:
        alias_values = {
            str(value).strip().lower()
            for value in df_filter[alias_col_file].dropna().tolist()
            if str(value).strip() != ''
        }
        if alias_values:
            if 'cdalias' in df.columns:
                mask = mask | df['cdalias'].astype(str).str.strip().str.lower().isin(alias_values)
                applied_with.append(f"alias ({len(alias_values)} valor(es))")
            elif 'alias' in df.columns:
                mask = mask | df['alias'].astype(str).str.strip().str.lower().isin(alias_values)
                applied_with.append(f"alias ({len(alias_values)} valor(es))")
            else:
                skipped_with.append("alias (no existe en datos cargados)")

    if not applied_with:
        details = ", ".join(skipped_with) if skipped_with else "no hay valores válidos"
        return df, {
            'ok': False,
            'message': f"No se pudo aplicar el filtro por Excel: {details}.",
            'type': 'warning'
        }

    filtered_df = df[mask]

    return filtered_df, {
        'ok': True,
        'type': 'success',
        'message': (
            f"Filtro por Excel aplicado con {', '.join(applied_with)}. "
            f"Coincidencias: {len(filtered_df)} usuario(s)."
        ),
        'matched_rows': len(filtered_df),
        'original_rows': len(df)
    }


def main():
    """Función principal de la aplicación"""
    
    # Inicializar
    init_session_state()
    ensure_directories()
    
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{APP_ICON}</h1>", unsafe_allow_html=True)
    with col2:
        st.title(APP_TITLE)
        st.caption("Monitoreo y control de créditos de GitHub Copilot")
    
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("📤 Cargar Archivos")
        
        st.markdown("### 📊 Excel de Licencias")
        excel_file = st.file_uploader(
            "Subir Excel de licencias",
            type=['xlsx', 'xls'],
            help="Excel con columnas: email, cod_empleado, nombre_empleado, proyecto, empresa, tipo_licencia, estado_licencia, creditos_base, grupo",
            key="excel_uploader"
        )
        
        st.markdown("### 📄 CSV de Créditos GitHub")
        csv_file = st.file_uploader(
            "Subir CSV agregado de créditos",
            type=['csv'],
            help="CSV agregado con el histórico diario (username, aic_gross_amount, date, etc.)",
            key="csv_uploader"
        )
        
        st.divider()
        
        # Botón de procesar
        if excel_file is not None and csv_file is not None:
            if st.button("🔄 Procesar Archivos", use_container_width=True, type="primary"):
                if process_files(excel_file, csv_file):
                    st.rerun()
        else:
            st.info("ℹ️ Carga ambos archivos para procesar")
        
        # Botón de limpiar datos (siempre visible)
        st.markdown("")
        if st.button("🗑️ Eliminar Archivos Procesados", use_container_width=True, type="secondary"):
            if clean_processed_data():
                st.success("✅ Datos eliminados correctamente")
                st.rerun()
            else:
                st.error("❌ Error al eliminar datos")
        
        st.divider()
        
        # Botón de descarga del Excel procesado
        if st.session_state.archivo_procesado and Path(st.session_state.archivo_procesado).exists():
            st.header("📥 Descargar")
            with open(st.session_state.archivo_procesado, 'rb') as f:
                st.download_button(
                    label="📄 Descargar Excel Procesado",
                    data=f,
                    file_name=Path(st.session_state.archivo_procesado).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    # Main content
    tabs = st.tabs(["📊 Dashboard", "👥 Usuarios", "📈 Reportes", "🧩 Detalle de usuario"])
    
    # Tab 1: Dashboard
    with tabs[0]:
        if st.session_state.df_usuarios is None:
            st.session_state.df_usuarios = load_processed_data()
        
        if st.session_state.df_usuarios is not None:
            df = st.session_state.df_usuarios
            
            # Filtrar solo licencias asignadas si existe la columna
            if 'estado_licencia' in df.columns:
                df_display = df[df['estado_licencia'].str.strip().str.lower() == 'asignada'].copy()
            else:
                df_display = df.copy()
            
            # Métricas principales (4 columnas)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                show_metric_card(
                    "Total Usuarios",
                    str(len(df_display)),
                    icon="👥"
                )
            
            with col2:
                total_creditos_base = df_display['creditos_base'].sum() if 'creditos_base' in df_display.columns else 0
                show_metric_card(
                    "Créditos Base ($)",
                    f"{total_creditos_base:.0f}",
                    icon="💳"
                )
            
            with col3:
                total_creditos_usados = df_display['creditos_usados'].sum() if 'creditos_usados' in df_display.columns else 0
                show_metric_card(
                    "Créditos Usados ($)",
                    f"{total_creditos_usados:.2f}",
                    icon="📊"
                )
            
            with col4:
                usuarios_activos = (df_display['creditos_usados'] > 0).sum() if 'creditos_usados' in df_display.columns else 0
                show_metric_card(
                    "Usuarios Activos",
                    str(usuarios_activos),
                    icon="✅"
                )
            
            st.divider()
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                if 'creditos_usados' in df_display.columns:
                    fig_users = create_user_usage_chart(df_display)
                    st.plotly_chart(fig_users, use_container_width=True)
            
            with col2:
                if 'creditos_usados' in df_display.columns:
                    fig_consumption = create_credit_consumption_histogram(df_display)
                    if fig_consumption:
                        st.plotly_chart(fig_consumption, use_container_width=True)
            
        else:
            st.info("📁 No hay datos cargados. Por favor, carga los archivos Excel y CSV desde la barra lateral.")
    
    # Tab 2: Usuarios
    with tabs[1]:
        if st.session_state.df_usuarios is not None:
            df = st.session_state.df_usuarios
            
            # Filtrar solo licencias asignadas si existe la columna
            if 'estado_licencia' in df.columns:
                df_display = df[df['estado_licencia'].str.strip().str.lower() == 'asignada'].copy()
            else:
                df_display = df.copy()
            
            # Filtros
            filters = show_filters_sidebar(df_display)
            df_filtered = apply_filters(df_display, filters)

            st.markdown("### 🎯 Filtro por Excel de usuarios")
            st.caption(
                "Sube un Excel con lista de usuarios para filtrar grupos específicos. "
                "Debe incluir 'cod_empleado' o 'alias/cdalias'."
            )

            excel_filter_file = st.file_uploader(
                "Adjuntar Excel de filtro (usuarios)",
                type=['xlsx', 'xls'],
                key='users_excel_filter_uploader',
                help="Columnas válidas: cod_empleado, codigo_empleado, alias o cdalias"
            )

            if excel_filter_file is not None:
                df_filtered, excel_filter_result = apply_excel_user_filter(df_filtered, excel_filter_file)

                if excel_filter_result['type'] == 'success':
                    st.success(excel_filter_result['message'])
                elif excel_filter_result['type'] == 'warning':
                    st.warning(excel_filter_result['message'])
                else:
                    st.error(excel_filter_result['message'])

            st.subheader(f"👥 Lista de Usuarios ({len(df_filtered)} registros)")
            
            # Buscador y botón de estimación
            col1, col2 = st.columns([1, 1])
            
            with col1:
                search = st.text_input("🔍 Buscar usuario", placeholder="Nombre, email, alias, proyecto...")
            
            with col2:
                if st.button("📊 Estimar Proyectos", use_container_width=True, type="primary"):
                    st.session_state.show_project_estimation = True
            
            if search:
                mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
                
                for col in ['nombre_empleado', 'email', 'cdalias', 'cod_empleado', 'proyecto', 'empresa']:
                    if col in df_filtered.columns:
                        mask = mask | df_filtered[col].astype(str).str.contains(search, case=False, na=False)
                
                df_filtered = df_filtered[mask]
            
            # Mostrar estimación de proyectos si se solicitó
            if st.session_state.get('show_project_estimation', False):
                st.divider()
                st.markdown("### 📊 Estimación por Proyecto-Empresa")
                
                if 'proyecto' in df_filtered.columns and 'empresa' in df_filtered.columns:
                    # Preparar datos para agrupación
                    df_temp = df_filtered.copy()
                    
                    # Convertir a string y limpiar valores nulos
                    df_temp['proyecto'] = df_temp['proyecto'].astype(str).fillna('Sin Proyecto')
                    df_temp['empresa'] = df_temp['empresa'].astype(str).fillna('Sin Empresa')
                    
                    # Asegurar que las columnas numéricas son numéricas
                    df_temp['creditos_base'] = pd.to_numeric(df_temp['creditos_base'], errors='coerce').fillna(0)
                    df_temp['creditos_usados'] = pd.to_numeric(df_temp['creditos_usados'], errors='coerce').fillna(0)
                    
                    # Agrupar por proyecto y empresa
                    project_summary = df_temp.groupby(['proyecto', 'empresa'], as_index=False).agg({
                        'creditos_base': 'sum',
                        'creditos_usados': 'sum',
                        'cdalias': 'count'
                    })
                    
                    project_summary.columns = ['Proyecto', 'Empresa', 'Créditos Base ($)', 'Créditos Usados ($)', 'Usuarios']
                    
                    # Calcular diferencia y porcentaje
                    project_summary['Diferencia'] = project_summary['Créditos Base ($)'] - project_summary['Créditos Usados ($)']
                    project_summary['% Uso'] = (project_summary['Créditos Usados ($)'] / project_summary['Créditos Base ($)'] * 100).round(2)
                    
                    # Manejar divisiones por cero
                    project_summary['% Uso'] = project_summary['% Uso'].replace([float('inf'), -float('inf')], 0)
                    
                    # Ordenar por créditos usados (mayor a menor)
                    project_summary = project_summary.sort_values('Créditos Usados ($)', ascending=False)
                    
                    # Función para aplicar colores
                    def color_rows(row):
                        if row['Créditos Usados ($)'] > row['Créditos Base ($)']:
                            return ['background-color: #ffcccc'] * len(row)  # Rojo claro
                        else:
                            return ['background-color: #ccffcc'] * len(row)  # Verde claro
                    
                    # Aplicar estilos
                    styled_df = project_summary.style.apply(color_rows, axis=1).format({
                        'Créditos Base ($)': '{:.2f}',
                        'Créditos Usados ($)': '{:.2f}',
                        'Diferencia': '{:.2f}',
                        '% Uso': '{:.2f}%'
                    })
                    
                    st.markdown(f"""
                    **Resumen:** {len(project_summary)} combinaciones Proyecto-Empresa encontradas
                    
                    **Leyenda:**
                    - 🟢 **Verde claro**: Créditos disponibles (uso dentro del límite)
                    - 🔴 **Rojo claro**: Sobrepasando créditos base ($) (requiere atención)
                    """)
                    
                    st.dataframe(styled_df, use_container_width=True, height=400)
                    
                    # Botón para cerrar
                    if st.button("✖️ Cerrar Estimación", use_container_width=False):
                        st.session_state.show_project_estimation = False
                        st.rerun()
                else:
                    st.warning("⚠️ No se encontraron columnas 'proyecto' y 'empresa' para realizar la estimación.")
                
                st.divider()
            
            # Tabla
            show_user_table(df_filtered)
            
            # Totales calculados con los filtros aplicados
            st.divider()
            st.markdown("### 📊 Totales del Grupo Filtrado")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric(
                    label="👥 Total Usuarios",
                    value=f"{len(df_filtered):,}",
                    help="Número de usuarios en el grupo filtrado"
                )
            
            with col2:
                if 'creditos_base' in df_filtered.columns:
                    total_base = df_filtered['creditos_base'].sum()
                    st.metric(
                        label="💳 Total Créditos Base ($)",
                        value=f"{total_base:,.2f}",
                        help="Suma de créditos base ($) del grupo filtrado"
                    )
            
            with col3:
                if 'creditos_usados' in df_filtered.columns:
                    total_usados = df_filtered['creditos_usados'].sum()
                    st.metric(
                        label="📈 Total Créditos Usados ($)",
                        value=f"{total_usados:,.2f}",
                        help="Suma de créditos usados ($) del grupo filtrado"
                    )
            
            # Mostrar porcentaje de uso si ambas columnas existen
            if 'creditos_base' in df_filtered.columns and 'creditos_usados' in df_filtered.columns:
                if total_base > 0:
                    porcentaje_uso = (total_usados / total_base) * 100
                    st.info(f"📊 **Porcentaje de Uso:** {porcentaje_uso:.2f}% del total de créditos base ($)")
            
            st.divider()
            
            # Descargar
            st.download_button(
                label="📥 Descargar datos filtrados",
                data=df_filtered.to_csv(index=False).encode('utf-8'),
                file_name=f"usuarios_filtrados_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("📁 No hay datos cargados.")
    
    # Tab 3: Reportes
    with tabs[2]:
        st.subheader("📈 Reportes y Análisis")
        
        if st.session_state.df_usuarios is not None:
            df = st.session_state.df_usuarios
            
            # Filtrar solo licencias asignadas si existe la columna
            if 'estado_licencia' in df.columns:
                df_display = df[df['estado_licencia'].str.strip().str.lower() == 'asignada'].copy()
            else:
                df_display = df.copy()
            
            # Resumen ejecutivo
            st.markdown("### 📋 Resumen Ejecutivo")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Por Tipo de Licencia:**")
                if 'tipo_licencia' in df_display.columns and 'creditos_usados' in df_display.columns:
                    license_summary = df_display.groupby('tipo_licencia').agg({
                        'cdalias': 'count',
                        'creditos_usados': 'sum'
                    }).rename(columns={'cdalias': 'Usuarios', 'creditos_usados': 'Créditos Usados'})
                    st.dataframe(license_summary, use_container_width=True)
            
            with col2:
                st.markdown("**Por Empresa:**")
                if 'empresa' in df_display.columns and 'creditos_usados' in df_display.columns:
                    empresa_summary = df_display.groupby('empresa').agg({
                        'cdalias': 'count',
                        'creditos_usados': 'sum'
                    }).rename(columns={'cdalias': 'Usuarios', 'creditos_usados': 'Créditos Usados'})
                    st.dataframe(empresa_summary, use_container_width=True)
            
            # Gráfico de modelos más usados
            st.divider()
            st.markdown("### 🤖 Análisis de Modelos de IA")
            
            if st.session_state.df_csv_raw is not None and 'model' in st.session_state.df_csv_raw.columns:
                from src.dashboard.components import create_model_usage_pie_chart, create_model_credits_pie_chart
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_models_usage = create_model_usage_pie_chart(st.session_state.df_csv_raw)
                    if fig_models_usage:
                        st.plotly_chart(fig_models_usage, use_container_width=True)
                
                with col2:
                    fig_models_credits = create_model_credits_pie_chart(st.session_state.df_csv_raw)
                    if fig_models_credits:
                        st.plotly_chart(fig_models_credits, use_container_width=True)
                    else:
                        st.info("📊 Columna 'aic_quantity' no disponible en el CSV")
            else:
                st.info("📊 No hay datos de modelos disponibles. Procesa los archivos para ver esta información.")

            # Exportar reporte
            st.divider()
            
            if st.button("📥 Generar Reporte Completo", use_container_width=True):
                report_path = Path(f"data/reports/reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                report_path.parent.mkdir(parents=True, exist_ok=True)
                
                with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
                    # Hoja principal con datos
                    df_display.to_excel(writer, sheet_name='Datos', index=False)
                    
                    # Resumen por licencia
                    if 'license_summary' in locals():
                        license_summary.to_excel(writer, sheet_name='Por Licencia')
                    
                    # Resumen por empresa
                    if 'empresa_summary' in locals():
                        empresa_summary.to_excel(writer, sheet_name='Por Empresa')
                
                st.success(f"✅ Reporte generado: {report_path}")
                
                with open(report_path, 'rb') as f:
                    st.download_button(
                        label="📥 Descargar Reporte",
                        data=f,
                        file_name=report_path.name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        else:
            st.info("📁 No hay datos para generar reportes.")

    # Tab 4: Detalle de usuario
    with tabs[3]:
        st.subheader("🧩 Detalle de usuario")

        if st.session_state.df_csv_raw is None:
            st.info("📁 No hay CSV cargado. Procesa los archivos para habilitar el detalle por usuario.")
        else:
            df_csv = st.session_state.df_csv_raw.copy()

            if 'username' not in df_csv.columns:
                st.warning("⚠️ El CSV no contiene la columna 'username'.")
            else:
                # Preparar identificadores de usuario a partir del CSV
                df_csv['username'] = df_csv['username'].astype(str)
                df_csv['alias'] = df_csv['username'].str.split('_').str[0].str.strip().str.lower()

                # Enriquecer con nombre (si está disponible en el Excel procesado)
                df_csv['nombre_empleado'] = ''
                if st.session_state.df_usuarios is not None:
                    df_users = st.session_state.df_usuarios.copy()
                    if 'cdalias' in df_users.columns and 'nombre_empleado' in df_users.columns:
                        alias_to_name = (
                            df_users[['cdalias', 'nombre_empleado']]
                            .dropna(subset=['cdalias'])
                            .drop_duplicates(subset=['cdalias'])
                        )
                        alias_to_name['cdalias'] = alias_to_name['cdalias'].astype(str).str.strip().str.lower()
                        map_name = dict(zip(alias_to_name['cdalias'], alias_to_name['nombre_empleado']))
                        df_csv['nombre_empleado'] = df_csv['alias'].map(map_name).fillna('')

                unique_users = (
                    df_csv[['alias', 'username', 'nombre_empleado']]
                    .drop_duplicates()
                    .sort_values(['alias', 'username'])
                )

                # Filtro libre que revisa alias y username (y nombre si existe)
                user_query = st.text_input(
                    "🔍 Buscar usuario (alias o username)",
                    placeholder="Ejemplo: jlfdiaz o jlfdiaz_indra"
                ).strip().lower()

                if user_query:
                    mask_query = (
                        unique_users['alias'].astype(str).str.lower().str.contains(user_query, na=False)
                        | unique_users['username'].astype(str).str.lower().str.contains(user_query, na=False)
                        | unique_users['nombre_empleado'].astype(str).str.lower().str.contains(user_query, na=False)
                    )
                    unique_users = unique_users[mask_query]

                if unique_users.empty:
                    st.info("No se encontraron usuarios con ese criterio de búsqueda.")
                else:
                    # Selector de usuario mostrando alias + username + nombre
                    options = []
                    for _, row in unique_users.iterrows():
                        nombre_txt = row['nombre_empleado'] if str(row['nombre_empleado']).strip() else 'Sin nombre'
                        options.append(f"{row['alias']} | {row['username']} | {nombre_txt}")

                    selected_option = st.selectbox(
                        "👤 Selecciona usuario",
                        options=options,
                        help="El filtro combina alias y username para mostrar el detalle completo"
                    )

                    selected_alias = selected_option.split(' | ')[0].strip().lower()

                    # Traer todas las interacciones del alias seleccionado a través de los días
                    df_user = df_csv[df_csv['alias'].astype(str).str.lower() == selected_alias].copy()

                    # Normalizar fechas y numéricos
                    if 'date' in df_user.columns:
                        df_user['date'] = pd.to_datetime(df_user['date'], errors='coerce')

                    numeric_cols = [
                        'quantity', 'aic_quantity', 'aic_gross_amount', 'gross_amount',
                        'discount_amount', 'net_amount', 'total_monthly_quota'
                    ]
                    for c in numeric_cols:
                        if c in df_user.columns:
                            df_user[c] = pd.to_numeric(df_user[c], errors='coerce').fillna(0)

                    # Cálculo efectivo para visualización:
                    # - unit_type=ai-credits: tokens=quantity, consumo=quantity*0.01
                    # - resto: tokens=aic_quantity, consumo=aic_gross_amount
                    unit_type = df_user.get('unit_type', pd.Series('', index=df_user.index)).astype(str).str.strip().str.lower()
                    is_ai_credits = unit_type == 'ai-credits'

                    quantity = pd.to_numeric(df_user.get('quantity', pd.Series(0, index=df_user.index)), errors='coerce').fillna(0)
                    aic_quantity = pd.to_numeric(df_user.get('aic_quantity', pd.Series(0, index=df_user.index)), errors='coerce').fillna(0)
                    aic_gross_amount = pd.to_numeric(df_user.get('aic_gross_amount', pd.Series(0, index=df_user.index)), errors='coerce').fillna(0)

                    df_user['tokens_usados_visual'] = aic_quantity.where(~is_ai_credits, quantity)
                    df_user['consumo_usd_visual'] = aic_gross_amount.where(~is_ai_credits, quantity * 0.01)

                    # Métricas principales
                    total_interacciones = len(df_user)
                    total_dias = df_user['date'].dt.date.nunique() if 'date' in df_user.columns else 0
                    total_tokens = float(df_user['tokens_usados_visual'].sum())
                    total_consumo = float(df_user['consumo_usd_visual'].sum())
                    agentes_usados = df_user['model'].dropna().nunique() if 'model' in df_user.columns else 0

                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Interacciones", f"{total_interacciones:,}")
                    with col2:
                        st.metric("Días con uso", f"{total_dias:,}")
                    with col3:
                        st.metric("Tokens usados", f"{total_tokens:,.2f}")
                    with col4:
                        st.metric("Consumo ($)", f"{total_consumo:,.4f}")
                    with col5:
                        st.metric("Agentes/Modelos", f"{agentes_usados:,}" if 'model' in df_user.columns else "N/D")

                    st.markdown("#### 📊 Consumo diario")
                    if 'date' in df_user.columns and not df_user['date'].dropna().empty:
                        daily_agg = {'quantity': 'sum'} if 'quantity' in df_user.columns else {}
                        daily_agg['tokens_usados_visual'] = 'sum'
                        daily_agg['consumo_usd_visual'] = 'sum'

                        if daily_agg:
                            df_daily_base = df_user.dropna(subset=['date']).copy()
                            df_daily_base['date_only'] = df_daily_base['date'].dt.date
                            df_daily = (
                                df_daily_base
                                .groupby('date_only')
                                .agg(daily_agg)
                                .reset_index()
                                .rename(columns={'date_only': 'date'})
                                .sort_values('date')
                            )
                            st.line_chart(df_daily.set_index('date'), use_container_width=True)
                    else:
                        st.info("No hay fechas válidas para construir la evolución diaria.")

                    st.markdown("#### 📋 Detalle completo de interacciones")
                    detail_cols = [
                        col for col in [
                            'date', 'username', 'alias', 'nombre_empleado', 'product', 'sku', 'model',
                            'quantity', 'unit_type', 'tokens_usados_visual', 'consumo_usd_visual', 'aic_quantity', 'aic_gross_amount',
                            'gross_amount', 'discount_amount', 'net_amount',
                            'organization', 'cost_center_name', 'exceeds_quota', 'total_monthly_quota'
                        ] if col in df_user.columns
                    ]

                    if 'date' in df_user.columns:
                        df_user = df_user.sort_values('date', ascending=False)

                    st.dataframe(df_user[detail_cols], use_container_width=True, height=450)

                    st.download_button(
                        label="📥 Descargar detalle del usuario",
                        data=df_user[detail_cols].to_csv(index=False).encode('utf-8'),
                        file_name=f"detalle_usuario_{selected_alias}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
    
    # Footer
    st.divider()
    st.caption(f"GitHub Copilot Credits Control v2.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
