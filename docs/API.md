# API Reference

## Módulos Principales

### 1. ETL (Extract, Transform, Load)

#### ExcelLoader
Clase para cargar y validar archivos Excel.

```python
from src.etl.excel_loader import ExcelLoader

loader = ExcelLoader("path/to/file.xlsx")
df = loader.load()
columns = loader.get_column_names()
```

**Métodos:**
- `load()`: Cargar archivo Excel
- `validate_columns(required_columns)`: Validar columnas requeridas
- `get_column_names()`: Obtener nombres de columnas
- `detect_columns(column_variants)`: Detectar columnas por variantes

#### ExcelTransformer
Clase para transformar datos ETL.

```python
from src.etl.excel_transformer import ExcelTransformer

transformer = ExcelTransformer(df, column_mapping)
df_transformed = transformer.transform()
transformer.save()
```

**Métodos:**
- `normalize_columns()`: Normalizar nombres de columnas
- `clean_data()`: Limpiar y validar datos
- `enrich_data()`: Enriquecer con campos adicionales
- `transform()`: Pipeline completo
- `save(output_path)`: Guardar resultado

### 2. API de GitHub

#### GitHubCreditsCSVLoader
Cargador de CSV de créditos de GitHub.

```python
from src.etl.csv_credits_loader import GitHubCreditsCSVLoader

loader = GitHubCreditsCSVLoader()
df_credits = loader.load_csv("path/to/credits.csv")
summary = loader.get_user_credits_summary("username")
df_all = loader.get_all_users_summary()
```

**Métodos:**
- `load_csv(file_path)`: Cargar CSV de créditos
- `get_user_credits_summary(username)`: Obtener resumen de un usuario
- `get_all_users_summary()`: Obtener resumen de todos los usuarios
- `merge_with_licenses(df_licenses)`: Combinar con datos de licencias
- `get_credits_by_date_range(start, end)`: Filtrar por fechas
- `get_statistics()`: Obtener estadísticas generales

### 3. Modelos de Datos

#### Usuario
Modelo de datos de usuario.

```python
from src.models import Usuario

usuario = Usuario(
    email="user@example.com",
    nombre="Usuario Ejemplo",
    alias="uejemplo",
    tipo_licencia="Business",
    creditos_usados=100.0
)
```

**Atributos:**
- `email`: Email del usuario
- `nombre`: Nombre completo
- `alias`: Username de GitHub
- `tipo_licencia`: Tipo de licencia
- `fecha_asignacion`: Fecha de asignación
- `creditos_usados`: Créditos consumidos
- `ultimo_uso`: Última actividad
- `estado`: Estado actual

#### MetricasOrganizacion
Métricas a nivel organizacional.

```python
from src.models import MetricasOrganizacion

metricas = MetricasOrganizacion(
    total_usuarios=50,
    usuarios_activos=45,
    total_creditos_usados=5000.0
)
```

### 4. Dashboard Components

Componentes reutilizables para Streamlit.

```python
from src.dashboard.components import (
    show_metric_card,
    create_user_usage_chart,
    create_license_distribution_chart,
    show_user_table
)
```

**Funciones:**
- `show_metric_card(title, value, delta, icon)`: Tarjeta de métrica
- `create_user_usage_chart(df)`: Gráfico de uso por usuario
- `create_license_distribution_chart(df)`: Distribución de licencias
- `create_timeline_chart(df)`: Línea temporal de uso
- `show_user_table(df)`: Tabla formateada de usuarios
- `show_filters_sidebar(df)`: Filtros en sidebar
- `apply_filters(df, filters)`: Aplicar filtros

### 5. Configuración

```python
from config import (
    INPUT_DIR,
    PROCESSED_DIR,
    CSV_CREDITS_DIR,
    REPORTS_DIR,
    ensure_directories
)
```

**Variables:**
- `APP_TITLE`: Título de la aplicación
- `INPUT_DIR`: Directorio de Excel de licencias
- `PROCESSED_DIR`: Directorio de Excel procesado
- `CSV_CREDITS_DIR`: Directorio de CSVs de créditos
- `REPORTS_DIR`: Directorio de reportes

**Funciones:**
- `ensure_directories()`: Crear directorios necesarios

## Formato de CSV de Créditos

### Estructura del CSV de GitHub

El CSV debe contener las siguientes columnas:

```csv
date,username,product,sku,model,quantity,unit_type,applied_cost_per_quantity,gross_amount,discount_amount,net_amount,exceeds_quota,total_monthly_quota,organization,cost_center_name,aic_quantity,aic_gross_amount
```

**Descripción de columnas:**
- `date`: Fecha del uso (formato ISO)
- `username`: Usuario de GitHub
- `product`: Producto (ej: "copilot")
- `sku`: SKU del servicio
- `model`: Modelo usado (ej: "Auto: Claude Haiku 4.5")
- `quantity`: Cantidad de requests
- `unit_type`: Tipo de unidad (ej: "requests")
- `applied_cost_per_quantity`: Costo por unidad
- `gross_amount`: Monto bruto
- `discount_amount`: Descuento aplicado
- `net_amount`: Monto neto
- `exceeds_quota`: Si excede la cuota
- `total_monthly_quota`: Cuota mensual total
- `organization`: Organización
- `cost_center_name`: Centro de costos
- `aic_quantity`: Cantidad AIC
- `aic_gross_amount`: Monto bruto AIC

## Formato de Excel

### Entrada
Columnas esperadas (cualquier variante):
- Email / Correo / Usuario
- Nombre / Name / Nombre Completo
- Alias / Username / Usuario GitHub
- Licencia / License / Tipo Licencia
- Fecha / Date / Fecha Asignación

### Salida (después de combinar con CSV de créditos)
Columnas generadas:
- email
- nombre
- alias
- tipo_licencia
- fecha (si existe)
- proyecto
- empresa
- creditos_usados (del CSV - suma de aic_gross_amount)
- total_quantity (del CSV)
- total_aic_quantity (del CSV)
- first_date (del CSV)
- last_date (del CSV)
- records_count (del CSV)
- fecha_procesamiento

**Nota importante sobre el merge:**
- El sistema normaliza automáticamente los usernames del CSV eliminando sufijos
- Ejemplo: `mcubells_indra` en el CSV se matchea con `mcubells` en el Excel
- El match es case-insensitive (no importan mayúsculas/minúsculas)

## Ejemplos de Uso

### Ejecutar ETL completo
```bash
python -m src.etl.transform_excel
```

### Iniciar aplicación web
```bash
streamlit run src/app.py
```

### Probar API de GitHub
```bash
python examples/test_api.py
```

### Generar Excel de ejemplo
```bash
python examples/example_etl.py
```
