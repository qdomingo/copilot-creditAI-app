# 📁 Estructura Completa del Proyecto

```
copilot-creditIA-user/
│
├── 📄 README.md                    # Documentación principal
├── 📄 LICENSE                      # Licencia MIT
├── 📄 CHANGELOG.md                 # Historial de cambios
├── 📄 CONTRIBUTING.md              # Guía de contribución
├── 📄 QUICKSTART.md                # Guía de inicio rápido
├── 📄 requirements.txt             # Dependencias Python
├── 📄 .env.example                 # Ejemplo de configuración
├── 📄 .gitignore                   # Archivos ignorados por Git
│
├── 🔧 install.bat                  # Instalador Windows
├── 🔧 install.sh                   # Instalador Linux/Mac
├── 🚀 run_app.bat                  # Ejecutar app Windows
├── 🚀 run_app.sh                   # Ejecutar app Linux/Mac
├── 🔄 run_etl.bat                  # Ejecutar ETL Windows
├── 🔄 run_etl.sh                   # Ejecutar ETL Linux/Mac
│
├── 📁 .streamlit/                  # Configuración Streamlit
│   └── config.toml                 # Tema y ajustes UI
│
├── 📁 config/                      # Configuración de la app
│   ├── __init__.py
│   └── settings.py                 # Settings centralizados
│
├── 📁 src/                         # Código fuente principal
│   ├── __init__.py
│   ├── 🎨 app.py                   # Aplicación Streamlit principal
│   │
│   ├── 📁 models/                  # Modelos de datos
│   │   ├── __init__.py
│   │   └── user.py                 # Usuario, MetricasOrganizacion
│   │
│   ├── 📁 etl/                     # Extract, Transform, Load
│   │   ├── __init__.py
│   │   ├── excel_loader.py         # Cargador de Excel
│   │   ├── excel_transformer.py    # Transformador ETL
│   │   └── transform_excel.py      # Script principal ETL
│   │
│   ├── 📁 api/                     # Integración con APIs
│   │   ├── __init__.py
│   │   └── github_client.py        # Cliente GitHub API
│   │
│   ├── 📁 dashboard/               # Componentes UI
│   │   ├── __init__.py
│   │   └── components.py           # Componentes Streamlit
│   │
│   └── 📁 utils/                   # Utilidades
│       ├── __init__.py
│       └── logger.py               # Sistema de logging
│
├── 📁 data/                        # Directorio de datos
│   ├── 📁 input/                   # Excel de entrada
│   │   └── .gitkeep
│   ├── 📁 processed/               # Excel procesado
│   │   └── .gitkeep
│   └── 📁 reports/                 # Reportes generados
│       └── .gitkeep
│
├── 📁 tests/                       # Tests unitarios
│   ├── test_etl.py
│   └── test_github_client.py
│
├── 📁 examples/                    # Ejemplos de uso
│   ├── test_api.py                 # Prueba de API GitHub
│   └── example_etl.py              # Ejemplo de ETL
│
├── 📁 docs/                        # Documentación extendida
│   ├── API.md                      # Referencia de API
│   ├── ARCHITECTURE.md             # Arquitectura del sistema
│   └── SCREENSHOTS.md              # Guía visual
│
└── 📁 logs/                        # Logs (generados)
    └── (archivos .log)
```

## 📊 Estadísticas del Proyecto

- **Archivos Python**: 15+
- **Módulos principales**: 5
- **Scripts de utilidad**: 6
- **Archivos de documentación**: 8
- **Tests**: 2
- **Ejemplos**: 2

## 🎯 Archivos Clave

### Para Usuarios
- `README.md` - Comenzar aquí
- `QUICKSTART.md` - Guía rápida de instalación
- `install.bat` / `install.sh` - Instalación automática
- `run_app.bat` / `run_app.sh` - Ejecutar aplicación

### Para Desarrolladores
- `src/app.py` - Aplicación principal
- `src/etl/` - Lógica de transformación
- `src/api/github_client.py` - Integración GitHub
- `config/settings.py` - Configuración
- `tests/` - Tests unitarios

### Para Operaciones
- `.env.example` - Plantilla de configuración
- `requirements.txt` - Dependencias
- `logs/` - Registros de la aplicación
- `data/` - Datos y reportes

## 🔄 Flujo de Datos

```
┌─────────────┐
│ Excel Input │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ ETL Loader  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Transform   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│Excel Output │────▶│  Streamlit   │
└─────────────┘     │  Dashboard   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ GitHub API   │
                    └──────────────┘
```

## 📦 Dependencias Principales

```
Aplicación Web
├── streamlit (UI Framework)
├── plotly (Gráficos)
└── altair (Visualizaciones)

Procesamiento de Datos
├── pandas (Análisis)
├── openpyxl (Excel I/O)
└── xlsxwriter (Excel export)

GitHub Integration
├── PyGithub (API wrapper)
└── requests (HTTP client)

Utilidades
├── python-dotenv (Config)
├── loguru (Logging)
└── pydantic (Validación)

Testing
└── pytest (Framework)
```

## 🚀 Comandos Rápidos

### Instalación
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

### Ejecución
```bash
# Aplicación web
run_app.bat    # Windows
./run_app.sh   # Linux/Mac

# ETL standalone
run_etl.bat    # Windows
./run_etl.sh   # Linux/Mac
```

### Desarrollo
```bash
# Activar entorno virtual
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Ejecutar tests
pytest tests/ -v

# Ejecutar con hot reload
streamlit run src/app.py --server.runOnSave true
```

## 📝 Archivos Generados en Runtime

```
copilot-creditIA-user/
├── .env                    # Configuración personal (no en Git)
├── venv/                   # Entorno virtual Python (no en Git)
├── logs/                   # Archivos de log (no en Git)
│   ├── app_*.log
│   ├── etl_*.log
│   └── test_api_*.log
├── data/
│   ├── input/
│   │   └── usuarios_licencias.xlsx
│   ├── processed/
│   │   └── usuarios_procesados.xlsx
│   └── reports/
│       └── reporte_*.xlsx
└── __pycache__/           # Cache Python (no en Git)
```

## 🔒 Archivos Sensibles (No incluir en Git)

- ❌ `.env` - Contiene tokens y credenciales
- ❌ `data/input/*.xlsx` - Datos de usuarios
- ❌ `data/processed/*.xlsx` - Datos procesados
- ❌ `data/reports/*.xlsx` - Reportes
- ❌ `logs/*.log` - Logs de aplicación
- ❌ `venv/` - Entorno virtual

## ✅ Archivos a Mantener en Git

- ✅ `.env.example` - Plantilla de configuración
- ✅ `data/*/.gitkeep` - Mantener estructura de carpetas
- ✅ Código fuente en `src/`
- ✅ Tests en `tests/`
- ✅ Documentación en `docs/`
- ✅ Scripts de utilidad

## 🎓 Recursos de Aprendizaje

- **Streamlit**: https://docs.streamlit.io
- **Pandas**: https://pandas.pydata.org/docs
- **GitHub API**: https://docs.github.com/rest
- **Plotly**: https://plotly.com/python

## 🆘 Ayuda

Para más información:
- 📖 Ver `README.md`
- 🚀 Ver `QUICKSTART.md`
- 🏗️ Ver `docs/ARCHITECTURE.md`
- 📸 Ver `docs/SCREENSHOTS.md`
- 🔧 Ver `docs/API.md`
