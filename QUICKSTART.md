# Guía de Inicio Rápido

## 🚀 Configuración Inicial

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Preparar datos de entrada

**Excel de Licencias:**
El Excel debe contener las siguientes columnas:
- **email** (requerido): Email corporativo (ej: mcubells@minsait.com)
- cod_empleado: Código del empleado
- nombre_empleado: Nombre completo
- proyecto: Proyecto asignado
- empresa: Empresa  
- tipo_licencia: Tipo de licencia
- estado_licencia: Estado (Asignada/Cancelada)
- creditos_base: Créditos base mensuales
- grupo: Grupo o equipo

**CSV de Créditos de GitHub:**
El CSV debe contener (mínimo):
- **username** (requerido): Username de GitHub (ej: mcubells_indra)
- **aic_gross_amount** (requerido): Monto de créditos usados
- **date** (requerido): Fecha del uso

## 🎯 Uso

### Ejecutar la aplicación web

```bash
streamlit run src/app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📊 Flujo de trabajo

1. **Cargar Excel de Licencias**: Sube tu archivo Excel con los datos de usuarios
2. **Cargar CSV de Créditos**: Sube el CSV de créditos de GitHub Enterprise
3. **Procesar**: Haz clic en "Procesar Archivos"
   - El sistema extrae el alias del email (`mcubells@minsait.com` → `mcubells`)
   - Normaliza el username del CSV (`mcubells_indra` → `mcubells`)
   - Agrupa y suma los créditos por usuario
   - Combina ambos datos por alias
   - Genera Excel final en `Excel-CreditsIA/`
4. **Visualizar**: Explora dashboards y métricas
5. **Exportar**: Descarga el Excel procesado o genera reportes

## ☁️ Despliegue en Heroku

La aplicación ya está preparada con estos archivos en la raíz del proyecto:
- `Procfile`
- `runtime.txt`
- `.streamlit/config.toml`

### 1. Requisitos previos

- Tener cuenta en Heroku (ya la tienes)
- Tener Heroku CLI instalado
- Tener Git instalado

### 2. Login en Heroku

```bash
heroku login
```

### 3. Commit de los cambios

```bash
git add .
git commit -m "Add Heroku deployment files"
```

### 4. Crear app o conectar una existente

Si es una app nueva:

```bash
heroku create nombre-unico-de-tu-app
```

Si ya existe:

```bash
heroku git:remote -a nombre-de-tu-app
```

### 5. Desplegar

```bash
git push heroku main
heroku ps:scale web=1
heroku open
```

Si tu rama principal se llama `master`, usa:

```bash
git push heroku master
```

### 6. Ver logs en caso de error

```bash
heroku logs --tail
```

### Nota importante sobre archivos

Heroku usa un sistema de archivos efímero. Los archivos generados en carpetas como `Excel-CreditsIA/` o `data/reports/` pueden perderse al reiniciar el dyno.

Para producción, se recomienda almacenar archivos en un servicio externo (por ejemplo, S3 o Azure Blob) o descargar el archivo al usuario en el mismo flujo de ejecución.

## 🔑 Obtener CSV de Créditos de GitHub

1. Accede a tu consola empresarial de GitHub
2. Ve a la sección de Billing o Copilot Usage
3. Exporta el CSV de créditos/uso
4. El CSV debe contener las columnas mencionadas arriba (date, username, product, etc.)

## 🆘 Solución de Problemas

### Error al cargar Excel
- Verifica que el formato del archivo sea .xlsx o .xls
- Asegúrate de que tenga la columna **email** (obligatoria)
- Los emails deben tener formato: usuario@dominio.com

### Error al cargar CSV de créditos
- Verifica que el CSV tenga las columnas: username, aic_gross_amount, date
- Verifica que el archivo use comas como delimitador

### No se combinan los datos correctamente
- El sistema extrae automáticamente el alias:
  - Del email: `mcubells@minsait.com` → `mcubells`
  - Del username: `mcubells_indra` → `mcubells`
- Verifica que coincidan las partes base (antes de @ y antes de _)

### Usuarios sin créditos
- Los usuarios que no aparezcan en el CSV tendrán creditos_usados = 0
- Esto es normal si el usuario no ha usado Copilot
