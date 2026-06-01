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
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_csv:
            tmp_csv.write(csv_file.getbuffer())
            tmp_csv_path = tmp_csv.name
        
        # Cargar CSV original para guardarlo en session_state
        df_csv_raw = pd.read_csv(tmp_csv_path)
        
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
            st.success(f"📁 Archivo guardado: {Path(output_path).name}")
            
            return True
            
    except Exception as e:
        st.error(f"❌ Error al procesar archivos: {e}")
        logger.error(f"Error en process_files: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


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
            "Subir CSV de créditos",
            type=['csv'],
            help="CSV con columnas: username, aic_gross_amount, date, etc.",
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
    tabs = st.tabs(["📊 Dashboard", "👥 Usuarios", "📈 Reportes"])
    
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
    
    # Footer
    st.divider()
    st.caption(f"GitHub Copilot Credits Control v2.0.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
