# 🔄 Guía de Uso - v2.1: Flujo Unificado

## ⚠️ Cambios Principales

La aplicación ya **NO requiere** acceso a la API de GitHub. Todo se procesa con archivos locales.

## ✅ Ventajas del Flujo Actual

1. **Más simple**: Cargas 2 archivos y procesas con 1 clic
2. **Más rápido**: Procesamiento unificado sin pasos intermedios
3. **Más preciso**: Extracción automática de alias y normalización
4. **Más limpio**: Sin carpetas intermedias, solo Excel final

## 📋 Pasos para Usar la Aplicación

### 1. Preparar tus Archivos

#### Excel de Licencias
Debe tener **obligatoriamente** la columna `email`. Ejemplo:

```
email,cod_empleado,nombre_empleado,proyecto,empresa,tipo_licencia,estado_licencia,creditos_base,grupo
mcubells@minsait.com,E001,María Cubells,Proyecto A,Minsait,Premium,Asignada,300,Team Alpha
jgarcia@minsait.com,E002,Juan García,Proyecto B,Indra,Business,Asignada,300,Team Beta
```

**Nota**: El sistema extraerá automáticamente `mcubells` del email `mcubells@minsait.com`

#### CSV de Créditos de GitHub
Debe tener mínimo: `date`, `username`, `aic_gross_amount`. Ejemplo:

```csv
date,username,aic_gross_amount
2026-05-01,mcubells_indra,0.110440755
2026-05-02,mcubells_indra,0.255678901
2026-05-01,jgarcia_empresa,0.187654321
```

**Nota**: El sistema normalizará `mcubells_indra` → `mcubells`

### 2. Ejecutar la Aplicación

```bash
streamlit run src/app.py
```

### 3. Cargar y Procesar

#### En la Barra Lateral:

1. **📊 Excel de Licencias**
   - Haz clic en "Subir Excel de licencias"
   - Selecciona tu archivo .xlsx o .xls

2. **📄 CSV de Créditos GitHub**
   - Haz clic en "Subir CSV de créditos"
   - Selecciona tu archivo .csv

3. **🔄 Procesar Archivos**
   - Una vez ambos archivos cargados, haz clic en "Procesar Archivos"
   - El sistema ejecutará automáticamente:
     * Extracción de alias del email
     * Normalización de username del CSV
     * Agregación de créditos por usuario
     * Combinación de datos
     * Generación de Excel final en `Excel-CreditsIA/`

4. **📥 Descargar**
   - Descarga el Excel procesado desde el botón de descarga

### 4. Visualizar y Analizar

- **Dashboard**: Métricas generales, gráficos de uso
- **Usuarios**: Tabla detallada filtrable y buscable
- **Reportes**: Genera reportes adicionales por licencia, empresa, etc.

## 📝 Formato del CSV de GitHub

El CSV debe tener estas columnas (GitHub Enterprise las genera automáticamente):

```csv
date,username,product,sku,model,quantity,unit_type,applied_cost_per_quantity,gross_amount,discount_amount,net_amount,exceeds_quota,total_monthly_quota,organization,cost_center_name,aic_quantity,aic_gross_amount
```

## 🔍 Ejemplo de Datos

Ver archivo: `examples/github_credits_example.csv`

## 🆘 Solución de Problemas

### Error: "Columnas faltantes en el CSV"
- Asegúrate de descargar el CSV completo desde GitHub
- No modifiques las columnas del CSV original

### No se combinan los datos
- El sistema **normaliza automáticamente** los usernames del CSV eliminando sufijos
- Ejemplo: `mcubells_indra` en el CSV se matchea con `mcubells` en el Excel
- Los usernames son case-insensitive (mayúsculas/minúsculas no importan)
- Si aún no se combinan, verifica que el alias base coincida (la parte antes del `_`)

### CSV muy grande
- La aplicación puede procesar archivos grandes sin problemas
- Si es muy lento, considera filtrar por fechas antes de exportar

## 📊 Nuevas Columnas Después de Combinar

Después de combinar los datos, verás estas nuevas columnas:

- `creditos_usados`: **Total de créditos usados** (suma de `aic_gross_amount` del CSV)
- `total_quantity`: Total de requests/llamadas realizadas
- `total_aic_quantity`: Cantidad AIC total
- `first_date`: Primera fecha de uso registrada
- `last_date`: Última fecha de uso registrada
- `records_count`: Número de registros del usuario en el CSV

### 📝 Nota Importante sobre Username Matching

El sistema normaliza automáticamente los usernames para facilitar el matching:

**Ejemplo:**
- CSV: `mcubells_indra`, `jgarcia_empresa`, `alopez_minsait`
- Excel alias: `mcubells`, `jgarcia`, `alopez`
- ✅ **Se matchean correctamente** eliminando el sufijo después del `_`

## 🚀 Próximos Pasos

1. Elimina cualquier archivo `.env` antiguo (ya no es necesario)
2. Prueba con el CSV de ejemplo en `examples/`
3. Exporta tu CSV real de GitHub y úsalo
4. Explora las nuevas visualizaciones y reportes

## 💡 Tips

- Puedes cargar múltiples CSVs de diferentes períodos
- Los datos se guardan automáticamente al combinar
- Usa la función de descarga para conservar tus reportes

## 📚 Más Información

- [README.md](README.md) - Documentación completa
- [QUICKSTART.md](QUICKSTART.md) - Guía de inicio rápido
- [examples/README.md](examples/README.md) - Ejemplos y casos de uso
