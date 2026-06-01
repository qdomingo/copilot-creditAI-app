"""
Componentes reutilizables para el dashboard
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict


def show_metric_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """Mostrar una tarjeta de métrica"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<h1 style='text-align: center; margin: 0;'>{icon}</h1>", unsafe_allow_html=True)
    with col2:
        st.metric(label=title, value=value, delta=delta)


def create_user_usage_chart(df: pd.DataFrame) -> go.Figure:
    """Crear gráfico de uso por usuario"""
    # Determinar columna de nombre a usar
    nombre_col = 'nombre' if 'nombre' in df.columns else 'nombre_empleado' if 'nombre_empleado' in df.columns else 'cdalias'
    
    fig = px.bar(
        df.sort_values('creditos_usados', ascending=True).tail(20),
        x='creditos_usados',
        y=nombre_col,
        orientation='h',
        title='Top 20 Usuarios por Consumo de Créditos ($)',
        labels={'creditos_usados': 'Créditos Usados ($)', nombre_col: 'Usuario'},
        color='creditos_usados',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_credit_consumption_histogram(df: pd.DataFrame) -> go.Figure:
    """Crear histograma de consumo de créditos por intervalos"""
    if 'creditos_usados' not in df.columns:
        return None
    
    # Definir intervalos y etiquetas (de mayor a menor consumo)
    intervals = [
        (300.01, float('inf'), '> 300'),
        (200.01, 300, '200 - 300'),
        (100.01, 200, '100 - 200'),
        (80.01, 100, '80 - 100'),
        (60.01, 80, '60 - 80'),
        (40.01, 60, '40 - 60'),
        (20.01, 40, '20 - 40'),
        (10.01, 20, '10 - 20'),
        (5.01, 10, '5 - 10'),
        (0.01, 5, '0 - 5'),
        (0, 0, 'Sin uso (0)')
    ]
    
    # Contar usuarios en cada intervalo
    counts = []
    labels = []
    total_users = len(df)
    
    for min_val, max_val, label in intervals:
        if min_val == 0 and max_val == 0:
            # Caso especial: exactamente 0
            count = len(df[df['creditos_usados'] == 0])
        else:
            count = len(df[(df['creditos_usados'] > min_val) & (df['creditos_usados'] <= max_val)])
        
        if count > 0:  # Solo incluir intervalos con usuarios
            counts.append(count)
            labels.append(label)
    
    # Calcular porcentajes
    percentages = [(count / total_users * 100) if total_users > 0 else 0 for count in counts]
    
    # Crear gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=labels,
        y=counts,
        text=[f'{count}<br>({pct:.1f}%)' for count, pct in zip(counts, percentages)],
        textposition='outside',
        marker=dict(
            color=counts,
            colorscale='Blues',
            showscale=False
        ),
        hovertemplate='<b>%{x}</b><br>Usuarios: %{y}<br>Porcentaje: %{customdata:.1f}%<extra></extra>',
        customdata=percentages
    ))
    
    fig.update_layout(
        title='Distribución de Consumo de Créditos ($)',
        xaxis_title='Rango de Créditos ($)',
        yaxis_title='Número de Usuarios',
        height=500,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=-45)
    )
    
    return fig


def create_timeline_chart(df: pd.DataFrame) -> go.Figure:
    """Crear gráfico de línea temporal de uso"""
    if 'ultimo_uso' not in df.columns or df['ultimo_uso'].isna().all():
        return None
    
    # Agrupar por fecha
    df_timeline = df.groupby(df['ultimo_uso'].dt.date)['creditos_usados'].sum().reset_index()
    
    fig = px.line(
        df_timeline,
        x='ultimo_uso',
        y='creditos_usados',
        title='Evolución del Consumo de Créditos ($)',
        labels={'ultimo_uso': 'Fecha', 'creditos_usados': 'Créditos Usados ($)'}
    )
    
    fig.update_layout(
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_model_usage_pie_chart(df_csv: pd.DataFrame) -> go.Figure:
    """Crear gráfico de tarta con los modelos más usados del CSV de GitHub"""
    if 'model' not in df_csv.columns:
        return None
    
    # Contar uso por modelo
    model_counts = df_csv['model'].value_counts().head(10)  # Top 10 modelos
    
    if len(model_counts) == 0:
        return None
    
    # Crear gráfico de tarta
    fig = px.pie(
        values=model_counts.values,
        names=model_counts.index,
        title='Top 10 Modelos Más Utilizados (por Requests)',
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Requests: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_model_credits_pie_chart(df_csv: pd.DataFrame) -> go.Figure:
    """Crear gráfico de tarta con los modelos que más créditos consumen"""
    if 'model' not in df_csv.columns or 'aic_quantity' not in df_csv.columns:
        return None
    
    # Agrupar por modelo y sumar aic_quantity
    model_credits = df_csv.groupby('model')['aic_quantity'].sum().sort_values(ascending=False).head(10)
    
    if len(model_credits) == 0:
        return None
    
    # Crear gráfico de tarta
    fig = px.pie(
        values=model_credits.values,
        names=model_credits.index,
        title='Top 10 Modelos que Más Créditos Consumen ($)',
        hole=0.4,  # Donut chart
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Créditos: %{value:.2f}<br>Porcentaje: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def show_user_table(df: pd.DataFrame):
    """Mostrar tabla de usuarios con formato"""
    
    # Determinar columna de licencia
    col_licencia = 'tipo_licencia' if 'tipo_licencia' in df.columns else 'licencia'
    
    # Determinar columnas a mostrar basándose en las disponibles
    display_columns = []
    
    # Nombre
    if 'nombre' in df.columns:
        display_columns.append('nombre')
    elif 'nombre_empleado' in df.columns:
        display_columns.append('nombre_empleado')
    
    # Email
    if 'email' in df.columns:
        display_columns.append('email')
    
    # Alias
    if 'alias' in df.columns:
        display_columns.append('alias')
    elif 'cdalias' in df.columns:
        display_columns.append('cdalias')
    
    # Código de empleado
    if 'cod_empleado' in df.columns:
        display_columns.append('cod_empleado')
    
    # Proyecto
    if 'proyecto' in df.columns:
        display_columns.append('proyecto')
    
    # Empresa
    if 'empresa' in df.columns:
        display_columns.append('empresa')
    
    # Licencia
    if col_licencia in df.columns:
        display_columns.append(col_licencia)
    
    # Créditos base
    if 'creditos_base' in df.columns:
        display_columns.append('creditos_base')
    
    # Créditos usados
    if 'creditos_usados' in df.columns:
        display_columns.append('creditos_usados')
    
    # Filtrar solo las columnas que existen
    display_columns = [col for col in display_columns if col in df.columns]
    
    display_df = df[display_columns].copy()
    
    # NO formatear a string para mantener ordenación numérica correcta
    # El formato se aplicará en column_config de st.dataframe
    
    # Renombrar columnas
    column_names = []
    for col in display_df.columns:
        if col in ['nombre', 'nombre_empleado']:
            column_names.append('Nombre')
        elif col == 'email':
            column_names.append('Email')
        elif col in ['alias', 'cdalias']:
            column_names.append('Alias')
        elif col == 'cod_empleado':
            column_names.append('Código Empleado')
        elif col == 'proyecto':
            column_names.append('Proyecto')
        elif col == 'empresa':
            column_names.append('Empresa')
        elif col in ['tipo_licencia', 'licencia']:
            column_names.append('Licencia')
        elif col == 'creditos_base':
            column_names.append('Créditos Base ($)')
        elif col == 'creditos_usados':
            column_names.append('Créditos Usados ($)')
        else:
            column_names.append(col)
    
    display_df.columns = column_names
    
    # Configurar formato de columnas para mantener ordenación numérica
    column_config = {}
    
    if 'Créditos Base ($)' in display_df.columns:
        column_config['Créditos Base ($)'] = st.column_config.NumberColumn(
            'Créditos Base ($)',
            format="%.2f"
        )
    
    if 'Créditos Usados ($)' in display_df.columns:
        column_config['Créditos Usados ($)'] = st.column_config.NumberColumn(
            'Créditos Usados ($)',
            format="%.2f"
        )
    
    # Mostrar tabla con formato numérico pero visualización con 2 decimales
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config
    )


def show_filters_sidebar(df: pd.DataFrame) -> Dict:
    """Mostrar barra lateral con filtros"""
    st.sidebar.header("🔍 Filtros")
    st.sidebar.info("💡 Selecciona valores para filtrar. Puedes elegir múltiples opciones en cada categoría.")
    
    filters = {}
    
    # Filtro por Proyecto
    if 'proyecto' in df.columns:
        proyectos_unicos = sorted([str(p) for p in df['proyecto'].dropna().unique() if str(p).strip() != ''])
        if proyectos_unicos:
            filters['proyecto'] = st.sidebar.multiselect(
                "📁 Proyecto",
                options=proyectos_unicos,
                default=None,
                help="Selecciona uno o varios proyectos"
            )
    
    # Filtro por Empresa
    if 'empresa' in df.columns:
        empresas_unicas = sorted([str(e) for e in df['empresa'].dropna().unique() if str(e).strip() != ''])
        if empresas_unicas:
            filters['empresa'] = st.sidebar.multiselect(
                "🏢 Empresa",
                options=empresas_unicas,
                default=None,
                help="Selecciona una o varias empresas"
            )
    
    # Filtro por tipo de licencia
    col_licencia = 'tipo_licencia' if 'tipo_licencia' in df.columns else 'licencia'
    if col_licencia in df.columns:
        licenses_unicas = sorted([str(l) for l in df[col_licencia].dropna().unique() if str(l).strip() != ''])
        if licenses_unicas:
            filters['licencia'] = st.sidebar.multiselect(
                "💳 Tipo de Licencia",
                options=licenses_unicas,
                default=None,
                help="Selecciona uno o varios tipos de licencia"
            )
            filters['col_licencia'] = col_licencia
    
    # Filtro por estado de licencia
    if 'estado_licencia' in df.columns:
        estados_licencia = sorted([str(e) for e in df['estado_licencia'].dropna().unique() if str(e).strip() != ''])
        if estados_licencia:
            filters['estado_licencia'] = st.sidebar.multiselect(
                "✅ Estado de Licencia",
                options=estados_licencia,
                default=None,
                help="Selecciona uno o varios estados"
            )
    
    # Filtro por Código de Empleado
    if 'cod_empleado' in df.columns:
        codigos_unicos = sorted([str(c) for c in df['cod_empleado'].dropna().unique() if str(c).strip() != ''])
        if codigos_unicos and len(codigos_unicos) <= 500:  # Solo mostrar si no hay demasiados
            filters['cod_empleado'] = st.sidebar.multiselect(
                "🆔 Código Empleado",
                options=codigos_unicos,
                default=None,
                help="Selecciona uno o varios códigos"
            )
    
    st.sidebar.divider()
    
    # Filtro por rango de créditos usados
    st.sidebar.markdown("**📊 Rango de Créditos**")
    
    if 'creditos_usados' in df.columns:
        min_creditos = float(df['creditos_usados'].min())
        max_creditos = float(df['creditos_usados'].max())
        
        # Solo mostrar slider si hay rango de valores
        if min_creditos < max_creditos:
            filters['creditos_range'] = st.sidebar.slider(
                "Créditos Usados ($)",
                min_creditos,
                max_creditos,
                (min_creditos, max_creditos),
                help="Filtra por rango de créditos usados ($)"
            )
        else:
            st.sidebar.info(f"Créditos Usados ($): {min_creditos:.2f}")
            filters['creditos_range'] = (min_creditos, max_creditos)
    
    # Filtro por rango de créditos base
    if 'creditos_base' in df.columns:
        min_base = float(df['creditos_base'].min())
        max_base = float(df['creditos_base'].max())
        
        if min_base < max_base:
            filters['creditos_base_range'] = st.sidebar.slider(
                "Créditos Base ($)",
                min_base,
                max_base,
                (min_base, max_base),
                help="Filtra por rango de créditos base ($)"
            )
        else:
            st.sidebar.info(f"Créditos Base ($): {min_base:.2f}")
            filters['creditos_base_range'] = (min_base, max_base)
    
    return filters


def apply_filters(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """Aplicar filtros al dataframe"""
    filtered_df = df.copy()
    
    # Filtro de proyecto
    if filters.get('proyecto') and len(filters['proyecto']) > 0:
        if 'proyecto' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['proyecto'].astype(str).isin(filters['proyecto'])]
    
    # Filtro de empresa
    if filters.get('empresa') and len(filters['empresa']) > 0:
        if 'empresa' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['empresa'].astype(str).isin(filters['empresa'])]
    
    # Filtro de licencia
    if filters.get('licencia') and len(filters['licencia']) > 0:
        col_licencia = filters.get('col_licencia', 'tipo_licencia' if 'tipo_licencia' in filtered_df.columns else 'licencia')
        if col_licencia in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col_licencia].astype(str).isin(filters['licencia'])]
    
    # Filtro de estado de licencia
    if filters.get('estado_licencia') and len(filters['estado_licencia']) > 0:
        if 'estado_licencia' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['estado_licencia'].astype(str).isin(filters['estado_licencia'])]
    
    # Filtro de código de empleado
    if filters.get('cod_empleado') and len(filters['cod_empleado']) > 0:
        if 'cod_empleado' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['cod_empleado'].astype(str).isin(filters['cod_empleado'])]
    
    # Filtro de rango de créditos usados
    if filters.get('creditos_range'):
        if 'creditos_usados' in filtered_df.columns:
            min_c, max_c = filters['creditos_range']
            filtered_df = filtered_df[
                (filtered_df['creditos_usados'] >= min_c) & 
                (filtered_df['creditos_usados'] <= max_c)
            ]
    
    # Filtro de rango de créditos base
    if filters.get('creditos_base_range'):
        if 'creditos_base' in filtered_df.columns:
            min_b, max_b = filters['creditos_base_range']
            filtered_df = filtered_df[
                (filtered_df['creditos_base'] >= min_b) & 
                (filtered_df['creditos_base'] <= max_b)
            ]
    
    return filtered_df
