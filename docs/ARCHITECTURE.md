# Arquitectura del Sistema

## Visión General

```
┌─────────────────────────────────────────────────────────────┐
│                    APLICACIÓN WEB (Streamlit)                │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Usuarios │  │   Sync   │  │ Reportes │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
    ┌───────────┐           ┌───────────┐
    │    ETL    │           │GitHub API │
    │  Module   │           │  Client   │
    └───────────┘           └───────────┘
            │                       │
            ▼                       ▼
    ┌───────────┐           ┌───────────┐
    │   Excel   │           │  GitHub   │
    │  Input    │           │   Cloud   │
    └───────────┘           └───────────┘
            │
            ▼
    ┌───────────┐
    │   Excel   │
    │  Output   │
    └───────────┘
```

## Componentes Principales

### 1. Capa de Presentación (UI)
- **Tecnología**: Streamlit
- **Responsabilidad**: Interfaz web moderna y responsive
- **Características**:
  - Dashboard con métricas en tiempo real
  - Tablas interactivas de usuarios
  - Gráficos con Plotly
  - Sistema de filtros
  - Exportación de reportes

### 2. Capa de Negocio

#### 2.1 Módulo ETL
- **Ubicación**: `src/etl/`
- **Componentes**:
  - `ExcelLoader`: Carga y validación de archivos
  - `ExcelTransformer`: Transformación y limpieza de datos
- **Flujo**:
  1. Carga de Excel
  2. Detección automática de columnas
  3. Normalización y limpieza
  4. Enriquecimiento con campos adicionales
  5. Generación de Excel procesado

#### 2.2 Módulo API
- **Ubicación**: `src/api/`
- **Componentes**:
  - `GitHubClient`: Cliente para GitHub REST API
- **Funcionalidades**:
  - Autenticación con token
  - Obtención de Copilot seats
  - Métricas de uso
  - Gestión de organización

#### 2.3 Modelos de Datos
- **Ubicación**: `src/models/`
- **Entidades**:
  - `Usuario`: Datos de usuario con licencia
  - `MetricasOrganizacion`: Estadísticas globales

### 3. Capa de Datos

#### 3.1 Archivos Excel
- **Input**: Datos brutos de usuarios
- **Processed**: Datos transformados y enriquecidos
- **Reports**: Reportes generados

#### 3.2 GitHub API
- **Endpoints utilizados**:
  - `/orgs/{org}/copilot/billing/seats`
  - `/orgs/{org}/copilot/billing`
  - `/orgs/{org}/members`

### 4. Utilidades
- **Logger**: Sistema de logging con Loguru
- **Config**: Gestión centralizada de configuración
- **Dashboard Components**: Componentes reutilizables UI

## Flujo de Datos

### Flujo ETL
```
Excel Input → Load → Validate → Detect Columns → 
Transform → Clean → Enrich → Save → Excel Output
```

### Flujo de Sincronización
```
Excel Processed → GitHub Client → API Request → 
Parse Response → Update Data → Save → Display
```

### Flujo de Visualización
```
Data → Apply Filters → Generate Charts → 
Render Components → Display Dashboard
```

## Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Python | 3.9+ |
| UI Framework | Streamlit | 1.29.0 |
| Data Processing | Pandas | 2.1.4 |
| Excel I/O | OpenPyXL | 3.1.2 |
| GitHub API | PyGithub | 2.1.1 |
| HTTP Client | Requests | 2.31.0 |
| Charts | Plotly | 5.18.0 |
| Logging | Loguru | 0.7.2 |
| Config | python-dotenv | 1.0.0 |

## Patrones de Diseño

### 1. Repository Pattern
- `GitHubClient` abstrae la comunicación con GitHub API
- Facilita testing y cambios de implementación

### 2. Pipeline Pattern
- ETL implementa un pipeline de transformación
- Cada paso es independiente y testeable

### 3. Component Pattern
- Dashboard usa componentes reutilizables
- Separación de lógica de presentación

### 4. Configuration Pattern
- Configuración centralizada en `config/`
- Variables de entorno para sensibilidad

## Seguridad

### Autenticación
- Token de GitHub almacenado en `.env`
- Nunca incluido en control de versiones

### Datos Sensibles
- Archivos Excel ignorados en git
- Logs excluidos del repositorio

### Permisos GitHub
Scopes requeridos para el token:
- `read:org` - Leer información de organización
- `read:user` - Leer información de usuarios
- `copilot` - Acceso a Copilot billing (si disponible)

## Escalabilidad

### Actual
- Diseñado para organizaciones medianas (< 1000 usuarios)
- Procesamiento síncrono
- Datos en memoria

### Futuras Mejoras
- Base de datos (PostgreSQL/SQLite)
- Procesamiento asíncrono
- Cache de datos de GitHub
- API REST propia
- Autenticación de usuarios
- Múltiples organizaciones

## Testing

### Estructura
```
tests/
├── test_etl.py          # Tests de transformación
├── test_github_client.py # Tests de API
└── test_models.py        # Tests de modelos
```

### Ejecutar Tests
```bash
pytest tests/ -v --cov=src
```

## Deployment

### Desarrollo Local
```bash
streamlit run src/app.py
```

### Producción (Streamlit Cloud)
1. Push a GitHub
2. Conectar con Streamlit Cloud
3. Configurar secrets (token GitHub)
4. Deploy automático

### Docker (Futuro)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "src/app.py"]
```

## Monitoreo y Logs

### Niveles de Log
- **DEBUG**: Información detallada
- **INFO**: Eventos importantes
- **WARNING**: Advertencias
- **ERROR**: Errores recuperables
- **CRITICAL**: Errores críticos

### Ubicación
- Console: Output estándar
- Files: `logs/` (rotación automática)

## Mantenimiento

### Actualizaciones
```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Verificar seguridad
pip-audit
```

### Backup
- Excel procesados: `data/processed/`
- Reportes: `data/reports/`
- Configuración: `.env` (excluir del repo)
