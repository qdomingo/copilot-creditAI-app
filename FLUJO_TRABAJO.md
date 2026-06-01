# 📝 Flujo de Trabajo Actualizado

## 🎯 Descripción del Nuevo Flujo

La aplicación ahora trabaja con dos carpetas principales:

### 📂 Carpetas

1. **Excel-LicenciasIA**: Almacena los archivos originales de licencias cargados
2. **Excel-CreditsIA**: Almacena los archivos transformados listos para análisis

### 🔄 Proceso Paso a Paso

#### 1. Estado Inicial
- Las carpetas `Excel-LicenciasIA` y `Excel-CreditsIA` están vacías al arrancar
- No hay datos en el dashboard hasta que se cargue y procese un archivo

#### 2. Cargar Archivo de Licencias
1. En la barra lateral, haz clic en "📤 Cargar Datos"
2. Selecciona un archivo Excel de licencias desde tu computadora
3. Haz clic en el botón "🔄 Procesar Excel"

#### 3. Procesamiento Automático
Al hacer clic en "Procesar Excel":
- ✅ El archivo original se guarda en `Excel-LicenciasIA` con un timestamp
- ✅ Se ejecuta la transformación automática
- ✅ El archivo transformado se guarda en `Excel-CreditsIA`
- ✅ Los datos se cargan en la aplicación
- ✅ El dashboard se actualiza con las métricas

#### 4. Visualizar Dashboard
- El dashboard muestra solo usuarios con licencias **asignadas** (no canceladas)
- Se muestran 4 métricas principales:
  - 👥 **Total Usuarios** (solo licencias asignadas)
  - 💳 **Créditos Totales** (suma de creditos_base)
  - 📊 **Créditos Usados** (suma de creditos_usados)
  - 📜 **Tipos de Licencia** (cantidad de tipos distintos)
- Gráficos interactivos de uso y distribución

#### 5. Descargar Excel Transformado
- En la barra lateral aparece un botón "📄 Descargar Excel Transformado"
- Descarga el archivo procesado para uso externo

## 📊 Estructura del Excel de Entrada

El archivo de entrada debe tener las siguientes columnas en las posiciones especificadas:

| Columna | Índice | Descripción |
|---------|--------|-------------|
| B | 1 | Estado de la Licencia (Asignada/Cancelada) |
| C | 2 | Tipo de Licencia |
| F | 5 | Proyecto |
| H | 7 | Empresa |
| J | 9 | Código de Empleado |
| K | 10 | Nombre del Empleado |
| L | 11 | Email (se extrae el alias antes de @) |

## 📊 Estructura del Excel de Salida

El archivo transformado contiene:

| Columna | Descripción |
|---------|-------------|
| cod_empleado | Código del empleado |
| nombre_empleado | Nombre completo |
| cdalias | Alias de GitHub (sin @dominio) |
| proyecto | Proyecto asignado |
| empresa | Empresa |
| tipo_licencia | Tipo de licencia |
| estado_licencia | Estado original (Asignada) |
| creditos_base | Créditos base calculados: Con DebtDoctor=30, CB sin DebtDoctor=30, CE sin DebtDoctor=70 |
| creditos_usados | Créditos consumidos |
| grupo | Grupo (vacío para completar) |
| ultimo_uso | Fecha de último uso |
| fecha_procesamiento | Fecha de procesamiento |
| email | Email generado (cdalias@empresa.com) |
| licencia | Copia de tipo_licencia para compatibilidad |

**Nota**: Las columnas `alias`, `nombre` y `estado` NO se guardan en el Excel transformado. La columna `estado` solo se usa internamente en la aplicación para sincronización con GitHub.

### 💳 Cálculo de Créditos Base

Los créditos base se calculan automáticamente según el tipo de licencia:

| Tipo de Licencia | Créditos Base | Lógica |
|------------------|---------------|--------|
| **Con DebtDoctor** (CB o CE) | **30** | Cualquier licencia que contenga "DebtDoctor" |
| Copilot Business (CB) | 30 | Sin DebtDoctor |
| Copilot Enterprise (CE) | 70 | Sin DebtDoctor |
| Otros | 0 | Cualquier otro tipo |

**Ejemplos de licencias con DebtDoctor (todas = 30):**
- "Github + CB + DebtDoctor Grupo10" → 30 créditos
- "Github + CB + DebtDoctor Grupo5" → 30 créditos
- "Github + CB + DebtDoctor Base" → 30 créditos
- "Github + CE + DebtDoctor Grupo10" → 30 créditos
- "Github + CE + DebtDoctor Grupo5" → 30 créditos
- "Github + CE + DebtDoctor Base" → 30 créditos

**Ejemplos sin DebtDoctor:**
- "Copilot Business" → 30 créditos
- "CB" → 30 créditos
- "Copilot Enterprise" → 70 créditos
- "CE" → 70 créditos

**Regla importante:** Si la licencia contiene "DebtDoctor" o "Debt Doctor", siempre son 30 créditos independientemente de si es CB o CE.

## 🔄 Sincronización con GitHub

Para obtener datos reales de uso:

1. Conecta a GitHub usando el botón "🔄 Conectar a GitHub"
2. Ve a la tab "🔄 Sincronización"
3. Haz clic en "🔄 Sincronizar con GitHub"
4. Los datos se actualizarán con información real de uso de Copilot

## 🧹 Limpiar Carpetas

Si deseas empezar de cero:

```bash
python limpiar_carpetas.py
```

Este script eliminará todos los archivos Excel de ambas carpetas.

## 📋 Pestañas de la Aplicación

### 📊 Dashboard
- Métricas principales (solo licencias asignadas)
- Gráfico de top 20 usuarios por consumo
- Distribución de tipos de licencia

### 👥 Usuarios
- Lista completa de usuarios
- Búsqueda y filtros
- Exportación a CSV

### 🔄 Sincronización
- Conexión con GitHub
- Sincronización de datos reales
- Recarga de datos locales

### 📈 Reportes
- Resumen ejecutivo
- Estadísticas por tipo de licencia
- Estadísticas por estado
- Generación de reportes completos en Excel

## ⚠️ Notas Importantes

1. **Filtrado Automático**: El dashboard solo muestra usuarios con `estado_licencia = "Asignada"`
2. **Múltiples Archivos**: Cada carga crea un nuevo archivo con timestamp
3. **Último Archivo**: La aplicación siempre carga el archivo más reciente de `Excel-CreditsIA`
4. **Preservación de Datos**: Los archivos originales se mantienen en `Excel-LicenciasIA`

## 🆘 Solución de Problemas

### No se cargan datos al iniciar
- Normal: Las carpetas están vacías, debes cargar y procesar un archivo primero

### Error al procesar
- Verifica que el Excel tenga las columnas en las posiciones correctas
- Revisa los logs en la carpeta `logs/`

### No se sincroniza con GitHub
- Verifica que el token de GitHub esté configurado en `.env`
- Asegúrate de que tu organización tenga Copilot habilitado
- Revisa que el token tenga los permisos necesarios

## 🚀 Inicio Rápido

```bash
# 1. Activar entorno virtual
.\venv\Scripts\activate

# 2. Ejecutar aplicación
streamlit run src/app.py

# 3. En la aplicación:
#    - Cargar Excel de licencias
#    - Procesar Excel
#    - ¡Dashboard listo!
```
