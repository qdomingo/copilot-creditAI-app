# GitHub Copilot Credits IA - Control de Uso

Aplicación para controlar y monitorear el uso de créditos de GitHub Copilot en organizaciones.

## 🚀 Características

- **ETL de Excel**: Transformación automática de datos de usuarios y licencias
- **Carga de CSV de Créditos**: Importación de datos de uso desde CSV de GitHub Enterprise
- **Dashboard Moderno**: Interfaz web interactiva con Streamlit
- **Reportes Automáticos**: Generación de informes de consumo
- **Visualizaciones**: Gráficos y métricas en tiempo real
- **Combinación de Datos**: Merge automático entre licencias y créditos usados

## 📋 Requisitos

- Python 3.9+
- CSV de créditos exportado desde GitHub Enterprise
- Excel de licencias con usuarios

## 🛠️ Instalación

1. Clonar el repositorio
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear directorios necesarios (se crean automáticamente al iniciar la app)

## 🎯 Uso

### 1. Ejecutar la aplicación
```bash
streamlit run src/app.py
```

### 2. Cargar datos

1. Sube tu Excel de licencias
2. Sube el CSV de créditos de GitHub
3. Combina los datos
4. Explora dashboards y genera reportes

### 3. Obtener CSV de Créditos

1. Accede a tu consola empresarial de GitHub
2. Ve a Billing > Copilot Usage
3. Exporta el CSV de créditos
4. El CSV debe contener: date, username, product, sku, model, quantity, etc.

## ☁️ Despliegue en Heroku

El proyecto ya incluye los archivos necesarios para Heroku:
- `Procfile`
- `runtime.txt`
- `.streamlit/config.toml`

### 1. Login en Heroku

```bash
heroku login
```

### 2. Commit de cambios

```bash
git add .
git commit -m "Add Heroku deployment files"
```

### 3. Crear app o conectar app existente

App nueva:

```bash
heroku create nombre-unico-de-tu-app
```

App existente:

```bash
heroku git:remote -a nombre-de-tu-app
```

### 4. Desplegar

```bash
git push heroku main
heroku ps:scale web=1
heroku open
```

Si tu rama principal es `master`, usa:

```bash
git push heroku master
```

### 5. Revisar logs

```bash
heroku logs --tail
```

### Nota sobre almacenamiento

Heroku usa un filesystem efímero. Los archivos generados en `Excel-CreditsIA/` y `data/reports/` pueden perderse tras reinicios o redeploys.

Para producción, se recomienda guardar archivos en almacenamiento externo (por ejemplo, S3 o Azure Blob) o forzar descarga inmediata al usuario.

## 📁 Estructura del Proyecto

```
copilot-creditIA-user/
├── src/
│   ├── etl/              # Módulos de transformación ETL y carga de CSV
│   │   ├── process_credits.py   # Procesamiento unificado
│   │   └── csv_credits_loader.py # Carga de CSV
│   ├── dashboard/        # Componentes de la UI
│   ├── models/           # Modelos de datos
│   └── utils/            # Utilidades y helpers
├── data/
│   ├── github_credits/   # CSVs de créditos de GitHub (guardados)
│   └── reports/          # Reportes generados
├── Excel-CreditsIA/      # Excel final procesado (salida)
├── tests/                # Tests unitarios
└── config/               # Archivos de configuración
```

## 📊Todos los Formato de Datos de Entrada

### Excel de Licencias

El archivo Excel debe contener **obligatoriamente** la columna `email`. Otras columnas opcionales:
- cod_empleado: Código del empleado
- nombre_empleado: Nombre completo
- proyecto: Proyecto asignado
- empresa: Empresa
- tipo_licencia: Tipo de licencia
- estado_licencia: Estado (Asignada/Cancelada)
- creditos_base: Créditos base mensuales
- grupo: Grupo o equipo

**Extracción de alias:**
Del email `mcubells@minsait.com` se extrae el alias `mcubells`

### CSV de Créditos de GitHub

Formato esperado (columnas mínimas):
```csv
date,username,aic_gross_amount
2026-05-01,mcubells_indra,0.110440755
2026-05-02,mcubells_indra,0.255678901
```

**Normalización de username:**
Del username `mcubells_indra` se extrae el alias `mcubells`

**Cálculo de créditos:**
Los créditos usados son la **suma de `aic_gross_amount`** por usuario

## 🔒 Seguridad

- Los datos se procesan localmente
- No se envía información a servicios externos
- Mantener los archivos CSV y Excel seguros

## 📝 Licencia

MIT License
