# Changelog

Todas las versiones y cambios notables del proyecto.

## [2.1.0] - 2026-05-27

### 🔄 REFACTORIZACIÓN MAYOR DEL FLUJO

#### ✨ Nuevo Flujo Simplificado
- **Carga simultánea**: Ahora se cargan ambos archivos (Excel + CSV) a la vez
- **Procesamiento unificado**: Un solo botón "Procesar Archivos" ejecuta todo el ETL
- **Eliminada carpeta Excel-LicenciasIA**: Ya no se guardan archivos intermedios
- **Excel final único**: Se genera directamente en `Excel-CreditsIA/`

#### 🎯 Nuevo Módulo: `process_credits.py`
- Procesamiento unificado de licencias y créditos
- Extracción automática de alias desde email (`usuario@empresa.com` → `usuario`)
- Normalización automática de username del CSV (`usuario_empresa` → `usuario`)
- Agregación de créditos por usuario (suma de `aic_gross_amount`)
- Merge automático por alias normalizado
- Generación de Excel con columnas específicas

#### 📊 Columnas del Excel Final
El Excel generado contiene exactamente:
1. cod_empleado
2. nombre_empleado
3. cdalias (extraído del email)
4. proyecto
5. empresa
6. tipo_licencia
7. estado_licencia
8. creditos_base
9. **creditos_usados** (suma de aic_gross_amount del CSV)
10. grupo

#### 🔧 Cambios Técnicos
- **app.py**: Completamente reescrito con flujo simplificado
- **config/settings.py**: Eliminada variable `INPUT_DIR`
- **Nuevo**: `src/etl/process_credits.py` con toda la lógica de procesamiento
- **UI mejorada**: Dos uploaders + un botón de proceso

#### 📝 Relación entre Archivos
- **Excel**: Campo `email` → se extrae alias (parte antes de @)
- **CSV**: Campo `username` → se normaliza (parte antes de _)
- **Merge**: Por alias normalizado (case-insensitive)
- **Créditos**: Suma de `aic_gross_amount` por usuario (agrupado del CSV)

#### 🗑️ Eliminado
- Carpeta `Excel-LicenciasIA` (ya no se usa)
- Flujo de dos pasos (cargar Excel, luego CSV, luego combinar)
- Módulo `transform_licencias.py` (reemplazado por `process_credits.py`)
- Tab "Combinar Datos" (ahora es automático)

#### 📚 Documentación Actualizada
- README.md con nuevo flujo
- QUICKSTART.md simplificado
- Ejemplos actualizados

## [2.0.0] - 2026-05-27

### 🔄 CAMBIOS IMPORTANTES (BREAKING CHANGES)

#### ⚠️ Eliminada Integración con GitHub API
- **Removido**: Cliente de GitHub API (`src/api/github_client.py`)
- **Razón**: La API de GitHub no proporciona los datos de créditos correctos necesarios para el análisis
- **Solución**: Ahora se usa CSV exportado directamente desde GitHub Enterprise

#### ✨ Nuevas Características
- **Cargador de CSV de Créditos**
  - Nuevo módulo `src/etl/csv_credits_loader.py`
  - Soporte para formato CSV de GitHub Enterprise
  - Procesamiento de datos de uso detallados por usuario
  - Cálculo automático de totales y agregados
  - Combinación automática con datos de licencias
  - **Normalización automática de usernames**: Elimina sufijos como `_indra`, `_empresa` para matching
  - **Uso de aic_gross_amount**: Columna principal para calcular créditos usados
  - **Suma por usuario**: Agrega todos los registros del CSV por usuario

- **Interfaz Actualizada**
  - Nueva sección de carga de CSV en sidebar
  - Tab "Combinar Datos" reemplaza "Sincronización"
  - Estadísticas en tiempo real del CSV cargado
  - Visualización de columnas de créditos disponibles
  - **Tabla de usuarios mejorada**: Eliminada columna "Estado Licencia", agregadas "Proyecto" y "Empresa"

#### 📝 Cambios en Documentación
- Actualizado README.md con instrucciones de CSV
- Actualizado QUICKSTART.md eliminando referencias a GitHub API
- Actualizado docs/API.md con nueva estructura
- Agregado ejemplo de CSV en `examples/github_credits_example.csv`
- Nuevo script de prueba `examples/test_csv_loader.py`

#### 🔧 Cambios en Configuración
- Eliminadas variables `GITHUB_TOKEN` y `GITHUB_ORG` de settings.py
- Agregado directorio `CSV_CREDITS_DIR` para almacenar CSVs
- Actualizado .env.example sin configuración de GitHub
- Removida dependencia `PyGithub` de requirements.txt

#### 📊 Formato de CSV Esperado
```csv
date,username,product,sku,model,quantity,unit_type,applied_cost_per_quantity,gross_amount,discount_amount,net_amount,exceeds_quota,total_monthly_quota,organization,cost_center_name,aic_quantity,aic_gross_amount
```

#### 🔄 Migración desde v1.x
1. No es necesario configurar token de GitHub
2. Exporta el CSV de créditos desde la consola empresarial de GitHub
3. Carga el CSV directamente en la aplicación
4. Combina con tus datos de licencias existentes

## [1.0.0] - 2024-XX-XX

### 🎉 Release Inicial

#### ✨ Características Nuevas
- **ETL de Excel**
  - Carga automática de archivos Excel
  - Detección inteligente de columnas
  - Transformación y limpieza de datos
  - Exportación a Excel procesado

- **Integración GitHub API**
  - Conexión a organizaciones de GitHub
  - Obtención de Copilot seats
  - Métricas de uso por usuario
  - Sincronización automática de datos

- **Dashboard Web (Streamlit)**
  - Interfaz moderna y responsive
  - Métricas en tiempo real
  - Gráficos interactivos con Plotly
  - Sistema de filtros avanzado
  - Tablas de usuarios
  - Exportación de reportes

- **Componentes de Visualización**
  - Tarjetas de métricas
  - Gráfico de barras de uso por usuario
  - Gráfico circular de distribución de licencias
  - Líneas temporales de consumo
  - Tabla formateada de usuarios

#### 🔧 Configuración
- Sistema de configuración con `.env`
- Validación de configuración
- Gestión de rutas y directorios

#### 📝 Documentación
- README completo
- Guía de inicio rápido
- Referencia de API
- Documentación de arquitectura

#### 🛠️ Herramientas
- Scripts de instalación (Windows/Linux)
- Scripts de ejecución
- Ejemplos de uso
- Tests básicos

#### 📦 Dependencias
- Python 3.9+
- Streamlit 1.29.0
- Pandas 2.1.4
- PyGithub 2.1.1
- Plotly 5.18.0
- Y más...

### 🔒 Seguridad
- Tokens en variables de entorno
- Archivos sensibles en .gitignore
- Validación de entrada de datos

### 📁 Estructura del Proyecto
```
copilot-creditIA-user/
├── src/              # Código fuente
├── config/           # Configuración
├── data/             # Datos y reportes
├── tests/            # Tests
├── examples/         # Ejemplos
├── docs/             # Documentación
└── .streamlit/       # Config Streamlit
```

---

## Futuras Versiones

### [1.1.0] - Planificado
- [ ] Base de datos SQLite para persistencia
- [ ] Histórico de uso de créditos
- [ ] Alertas de consumo excesivo
- [ ] Exportación a PDF
- [ ] API REST propia

### [1.2.0] - Planificado
- [ ] Autenticación de usuarios
- [ ] Múltiples organizaciones
- [ ] Dashboard personalizable
- [ ] Notificaciones por email
- [ ] Integración con Slack

### [2.0.0] - Futuro
- [ ] Migración a base de datos PostgreSQL
- [ ] Procesamiento asíncrono
- [ ] Cache distribuido
- [ ] Containerización con Docker
- [ ] CI/CD con GitHub Actions

---

## Formato

Tipos de cambios:
- `✨ Added` - Nuevas características
- `🔧 Changed` - Cambios en funcionalidad existente
- `🐛 Fixed` - Corrección de bugs
- `🗑️ Deprecated` - Características obsoletas
- `🔥 Removed` - Características eliminadas
- `🔒 Security` - Mejoras de seguridad
