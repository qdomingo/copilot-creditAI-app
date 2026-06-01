# Ejemplos

Este directorio contiene archivos de ejemplo para probar la aplicación.

## Archivos de Ejemplo

### 📄 github_credits_example.csv

Archivo CSV de ejemplo con el formato esperado de GitHub Enterprise para créditos de Copilot.

**Columnas del CSV:**
- `date`: Fecha del uso (formato YYYY-MM-DD)
- `username`: Nombre de usuario de GitHub
- `product`: Producto utilizado (ej: "copilot")
- `sku`: SKU del servicio
- `model`: Modelo de IA usado (ej: "Auto: Claude Haiku 4.5", "Auto: GPT-4o")
- `quantity`: Cantidad de requests realizados
- `unit_type`: Tipo de unidad (ej: "requests")
- `applied_cost_per_quantity`: Costo aplicado por unidad
- `gross_amount`: Monto bruto total
- `discount_amount`: Descuento aplicado
- `net_amount`: Monto neto
- `exceeds_quota`: Indica si excede la cuota ("True"/"False")
- `total_monthly_quota`: Cuota mensual total
- `organization`: Nombre de la organización
- `cost_center_name`: Nombre del centro de costos
- `aic_quantity`: Cantidad AIC
- `aic_gross_amount`: Monto bruto AIC ⭐ **(usado para calcular créditos)**

### 📊 licencias_example.csv

Archivo CSV de ejemplo con el formato de licencias esperado.

**Columnas requeridas:**
- `email`: Email del usuario (se extrae el alias de la parte antes de @)
- `cod_empleado`: Código único del empleado
- `nombre_empleado`: Nombre completo
- `proyecto`: Proyecto asignado
- `empresa`: Nombre de la empresa
- `tipo_licencia`: Tipo (Premium, Business, etc.)
- `estado_licencia`: Estado (Asignada, Cancelada)
- `creditos_base`: Créditos base mensuales
- `grupo`: Grupo o equipo

**Nota:** Puedes usar formato `.csv` o `.xlsx`

## Cómo usar estos ejemplos

### 🚀 Prueba Rápida

1. Abre la aplicación:
   ```bash
   streamlit run src/app.py
   ```

2. En la barra lateral:
   - **📊 Subir Excel de licencias**: Selecciona `licencias_example.csv`
   - **📄 Subir CSV de créditos**: Selecciona `github_credits_example.csv`

3. Haz clic en **"Procesar Archivos"**

4. Explora los resultados:
   - **Dashboard**: Métricas generales y gráficos
   - **Usuarios**: Tabla detallada
   - **Reportes**: Descarga Excel procesado

### 💡 Normalización de Usernames

El sistema automáticamente normaliza los usernames del CSV para hacer match con los alias del Excel:

**CSV (username)** → **Email (extrae alias)** → **Match**

Ejemplos:
- `mcubells_indra` → `mcubells@minsait.com` → `mcubells` → ✅
- `jcreyg_indra` → `jcreyg@indra.com` → `jcreyg` → ✅
- `maria_lopez` → `maria_lopez@empresa.com` → `maria_lopez` → ✅

### 📊 Cálculo de Créditos

Los **créditos usados** se calculan como:
- **Suma de `aic_gross_amount`** de todos los registros del usuario en el CSV
- Por ejemplo: Si un usuario tiene 3 registros con valores 0.11, 0.25, 0.18
- Su total de créditos usados será: 0.54

### 📁 Resultado

El Excel final en `Excel-CreditsIA/` contiene todas las columnas:

| cod_empleado | nombre_empleado | cdalias | proyecto | empresa | tipo_licencia | creditos_usados |
|--------------|-----------------|---------|----------|---------|---------------|-----------------|
| E001 | María Cubells | mcubells | Alpha | Minsait | Premium | 0.54 |

## Otros ejemplos

- `example_etl.py`: Script de ejemplo para ejecutar ETL desde Python
- `test_api.py`: Script de ejemplo para probar la carga de CSV
- `transform_licencias.py`: Script de ejemplo para transformar Excel de licencias
