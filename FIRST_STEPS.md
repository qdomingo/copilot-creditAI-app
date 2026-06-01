# 🎯 Primeros Pasos - Tutorial Completo

## 📝 Pre-requisitos

Antes de comenzar, asegúrate de tener:
- ✅ Python 3.9 o superior instalado
- ✅ Cuenta de GitHub con permisos de administrador de organización
- ✅ Excel con datos de usuarios (o usa el ejemplo que generaremos)

## 🚀 Paso 1: Instalación

### Opción A: Instalación Automática (Recomendada)

**Windows:**
```bash
# Ejecutar instalador
install.bat
```

**Linux/Mac:**
```bash
# Dar permisos y ejecutar
chmod +x install.sh
./install.sh
```

### Opción B: Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar archivo de configuración
cp .env.example .env
```

## 🔑 Paso 2: Configurar GitHub Token

### 2.1 Obtener Token de GitHub

1. **Ir a GitHub**
   - Abre https://github.com/settings/tokens

2. **Crear nuevo token**
   - Click en "Generate new token (classic)"
   - Nombre: "Copilot Credits Control"
   - Expiration: 90 días (o según tu política)

3. **Seleccionar permisos**
   ```
   ✅ read:org          (Leer organización)
   ✅ read:user         (Leer usuarios)
   ✅ copilot           (Acceso a Copilot, si disponible)
   ```

4. **Generar y copiar**
   - Click en "Generate token"
   - ⚠️ IMPORTANTE: Copia el token ahora (solo se muestra una vez)

### 2.2 Configurar .env

Edita el archivo `.env`:

```env
# Pegar tu token aquí
GITHUB_TOKEN=ghp_tu_token_copiado_aqui

# Nombre de tu organización
GITHUB_ORG=nombre_de_tu_organizacion

# Opcional: personalizar
APP_TITLE=Control de Créditos Copilot
APP_ICON=🤖
```

**Ejemplo completo:**
```env
GITHUB_TOKEN=ghp_s3cR3tT0k3nH3r3
GITHUB_ORG=mi-empresa
APP_TITLE=Copilot Control - Mi Empresa
APP_ICON=💻
```

## 📊 Paso 3: Preparar Datos

### Opción A: Usar Excel de Ejemplo

```bash
# Genera un Excel de ejemplo automáticamente
python examples/example_etl.py
```

Esto creará `data/input/ejemplo_usuarios.xlsx` con datos de prueba.

### Opción B: Usar tu Propio Excel

1. **Crear Excel** con estas columnas (nombres flexibles):

   | Email | Nombre Completo | Alias | Tipo Licencia | Fecha |
   |-------|-----------------|-------|---------------|-------|
   | juan.perez@empresa.com | Juan Pérez | jperez | Business | 2024-01-15 |
   | maria.garcia@empresa.com | María García | mgarcia | Enterprise | 2024-01-20 |

   **Columnas aceptadas:**
   - **Email**: email, correo, usuario, user
   - **Nombre**: nombre, name, nombre completo
   - **Alias**: alias, username, usuario github
   - **Licencia**: licencia, license, tipo licencia
   - **Fecha**: fecha, date, fecha asignacion

2. **Guardar en**: `data/input/usuarios_licencias.xlsx`

## 🎨 Paso 4: Ejecutar la Aplicación

### Inicio Rápido

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
chmod +x run_app.sh
./run_app.sh
```

La aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

### Modo Manual

```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Ejecutar Streamlit
streamlit run src/app.py
```

## 📤 Paso 5: Cargar y Procesar Datos

### En la Aplicación Web

1. **Sidebar izquierdo** → "📤 Cargar Datos"
2. **Click en "Browse files"**
3. **Selecciona tu Excel**
4. **Click en "🔄 Procesar Excel"**

El sistema:
- ✅ Detectará las columnas automáticamente
- ✅ Limpiará y normalizará los datos
- ✅ Agregará campos adicionales
- ✅ Guardará el resultado procesado

### Desde Línea de Comandos (Alternativa)

```bash
# Windows
run_etl.bat

# Linux/Mac
./run_etl.sh

# O manualmente
python -m src.etl.transform_excel
```

## 🔗 Paso 6: Conectar a GitHub

1. **En la aplicación**, sidebar → "⚙️ Configuración"
2. **Click en "🔄 Conectar a GitHub"**
3. **Espera confirmación**: "✅ GitHub conectado"

Si hay error:
- Verifica que el token sea correcto en `.env`
- Confirma que el nombre de la organización sea exacto
- Revisa que el token tenga los permisos necesarios

## 🔄 Paso 7: Sincronizar Datos

1. **Ve a la pestaña "🔄 Sincronización"**
2. **Click en "🔄 Sincronizar con GitHub"**

El sistema:
- Obtendrá los seats de Copilot activos
- Actualizará los datos de uso por usuario
- Marcará usuarios sin seat
- Guardará los cambios

## 📊 Paso 8: Explorar el Dashboard

### Pestaña "📊 Dashboard"
- Métricas principales en tarjetas
- Gráfico de Top 20 usuarios
- Distribución de licencias

### Pestaña "👥 Usuarios"
- Tabla completa de usuarios
- Búsqueda y filtros
- Exportar datos filtrados

### Pestaña "📈 Reportes"
- Resumen ejecutivo
- Generar reporte completo en Excel
- Análisis por licencia y estado

## 🎓 Paso 9: Entender los Datos

### Estados Posibles

| Estado | Significado | Acción Sugerida |
|--------|-------------|-----------------|
| ✅ Activo | Usuario con seat de Copilot | Monitorear uso |
| ⚠️ Sin Seat | Usuario sin licencia asignada | Evaluar necesidad |
| ⏸️ Pendiente | Sin sincronizar con GitHub | Ejecutar sincronización |

### Métricas Clave

- **Total Usuarios**: Cantidad en tu base de datos
- **Usuarios Activos**: Con seat y actividad reciente
- **Créditos Totales**: Suma de consumo
- **Tipos de Licencia**: Variedad de planes

## 📥 Paso 10: Generar Reportes

### Reporte Rápido (CSV)
1. Pestaña "👥 Usuarios"
2. Aplicar filtros deseados
3. Click "📥 Descargar datos filtrados"

### Reporte Completo (Excel)
1. Pestaña "📈 Reportes"
2. Click "📥 Generar Reporte Completo"
3. Descargar el archivo Excel generado

El reporte incluye:
- Hoja "Datos": Información completa
- Hoja "Por Licencia": Agrupación por tipo
- Hoja "Por Estado": Distribución de estados

## 🔄 Flujo de Trabajo Recomendado

### Configuración Inicial (Una vez)
```
1. Instalar → 2. Configurar token → 3. Conectar GitHub
```

### Uso Regular (Semanal/Mensual)
```
1. Cargar Excel actualizado
2. Procesar datos
3. Sincronizar con GitHub
4. Revisar dashboard
5. Generar reportes
```

### Monitoreo Continuo
```
1. Abrir dashboard
2. Verificar métricas
3. Identificar anomalías
4. Tomar decisiones
```

## 🆘 Solución de Problemas Comunes

### Error: "GITHUB_TOKEN no configurado"
```bash
# Verificar archivo .env
cat .env  # Linux/Mac
type .env  # Windows

# Debe contener:
GITHUB_TOKEN=ghp_...
GITHUB_ORG=...
```

### Error: "Archivo Excel no encontrado"
```bash
# Verificar ruta
ls data/input/  # Linux/Mac
dir data\input\  # Windows

# O generar ejemplo
python examples/example_etl.py
```

### Error: "Columnas no detectadas"
```bash
# Asegúrate que el Excel tenga al menos:
# - Una columna de email
# - Una columna de nombre
# - Una columna de alias

# Nombres aceptados (cualquier variante):
# email, correo, usuario
# nombre, name
# alias, username
```

### Error de Conexión a GitHub
```bash
# Verificar token
# 1. ¿Es válido? (no expirado)
# 2. ¿Tiene permisos correctos?
# 3. ¿Nombre de organización correcto?

# Probar conexión manualmente
python examples/test_api.py
```

### La App No Abre en el Navegador
```bash
# Abrir manualmente:
# http://localhost:8501

# Si el puerto está ocupado:
streamlit run src/app.py --server.port 8502
```

## 📚 Próximos Pasos

### Explorar Más
- 📖 Lee la [documentación completa](README.md)
- 🏗️ Revisa la [arquitectura](docs/ARCHITECTURE.md)
- 🔧 Consulta la [referencia de API](docs/API.md)

### Personalizar
- 🎨 Cambia colores en `.streamlit/config.toml`
- ⚙️ Ajusta configuración en `config/settings.py`
- 📊 Agrega nuevos gráficos en `src/dashboard/components.py`

### Contribuir
- 🤝 Lee la [guía de contribución](CONTRIBUTING.md)
- 🐛 Reporta bugs en GitHub Issues
- ✨ Propón nuevas características

## 🎉 ¡Listo!

Ahora tienes tu sistema de control de créditos de Copilot funcionando.

**¿Necesitas ayuda?**
- Consulta los logs en `logs/`
- Revisa los ejemplos en `examples/`
- Abre un issue en el repositorio

**¡Disfruta monitoreando tus créditos de Copilot! 🚀**
