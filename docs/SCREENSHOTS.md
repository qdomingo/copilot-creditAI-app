# 🎨 Screenshots y Guía Visual

## 🏠 Pantalla Principal - Dashboard

El dashboard principal muestra un resumen ejecutivo del uso de créditos:

### Métricas Principales
- **Total Usuarios**: Número de usuarios en el sistema
- **Usuarios Activos**: Usuarios con actividad reciente en Copilot
- **Créditos Totales**: Suma de créditos consumidos
- **Tipos de Licencia**: Variedad de licencias en uso

### Visualizaciones
1. **Gráfico de Barras Horizontal**: Top 20 usuarios por consumo
2. **Gráfico Circular**: Distribución de tipos de licencia

---

## 👥 Gestión de Usuarios

### Funcionalidades
- ✅ Tabla completa de usuarios
- 🔍 Búsqueda en tiempo real
- 🎯 Filtros por licencia, estado y créditos
- 📥 Exportación a CSV

### Columnas Visibles
- Nombre completo
- Email corporativo
- Alias de GitHub
- Tipo de licencia
- Créditos consumidos
- Estado actual

---

## 🔄 Sincronización con GitHub

### Proceso
1. Conectar a organización de GitHub
2. Obtener datos de Copilot Billing API
3. Actualizar información de usuarios
4. Guardar cambios localmente

### Estados Posibles
- ✅ **Activo**: Usuario con seat de Copilot
- ⚠️ **Sin Seat**: Usuario sin asignación de Copilot
- ⏸️ **Pendiente**: Datos aún no sincronizados

---

## 📈 Reportes y Análisis

### Tipos de Reportes

#### 1. Resumen Ejecutivo
- Por tipo de licencia
- Por estado de usuario
- Totales y promedios

#### 2. Reporte Completo (Excel)
Contiene múltiples hojas:
- **Datos**: Información completa de usuarios
- **Por Licencia**: Agrupación por tipo
- **Por Estado**: Distribución de estados

#### 3. Exportación Filtrada
- Aplicar filtros personalizados
- Exportar subconjunto específico
- Formato CSV o Excel

---

## 📤 Carga de Datos

### Excel de Entrada

#### Formato Flexible
El sistema detecta automáticamente columnas con nombres como:

**Email:**
- email, correo, usuario, user

**Nombre:**
- nombre, name, nombre completo, full name

**Alias:**
- alias, username, usuario github

**Licencia:**
- licencia, license, tipo licencia

**Fecha:**
- fecha, date, fecha asignacion

#### Ejemplo de Excel
```
| Email                    | Nombre Completo | Alias      | Tipo Licencia | Fecha       |
|--------------------------|-----------------|------------|---------------|-------------|
| juan.perez@empresa.com   | Juan Pérez      | jperez     | Business      | 2024-01-15  |
| maria.garcia@empresa.com | María García    | mgarcia    | Enterprise    | 2024-01-20  |
```

---

## ⚙️ Configuración

### Archivo .env

```env
# GitHub Configuration
GITHUB_TOKEN=ghp_tu_token_aqui
GITHUB_ORG=nombre_organizacion

# Application Settings
APP_TITLE=GitHub Copilot Credits Control
DEBUG=False
```

### Obtener Token de GitHub

1. **Ir a GitHub Settings**
   - Profile → Settings → Developer settings

2. **Personal Access Tokens**
   - Tokens (classic) → Generate new token

3. **Seleccionar Scopes**
   ```
   ✅ read:org
   ✅ read:user
   ✅ copilot (si disponible)
   ```

4. **Copiar y Guardar**
   - Copiar el token generado
   - Pegarlo en el archivo .env

---

## 🎨 Personalización

### Tema de Colores
Editar `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"     # Azul principal
backgroundColor = "#FFFFFF"   # Fondo blanco
secondaryBackgroundColor = "#f0f2f6"  # Gris claro
textColor = "#262730"        # Texto oscuro
```

### Logo y Título
Editar `.env`:

```env
APP_TITLE=Mi Control de Copilot
APP_ICON=🤖
```

---

## 📊 Interpretación de Métricas

### Créditos Usados
- **0.0**: Sin actividad registrada
- **< 100**: Uso ligero
- **100-500**: Uso moderado
- **> 500**: Uso intensivo

### Estados
- **Activo**: Consume créditos regularmente
- **Sin Seat**: No tiene licencia asignada
- **Pendiente**: Requiere sincronización

### Alertas Sugeridas
- 🔴 **Crítico**: > 80% del límite organizacional
- 🟡 **Advertencia**: > 60% del límite
- 🟢 **Normal**: < 60% del límite

---

## 🔧 Solución de Problemas Visuales

### Gráficos No Se Muestran
- Verificar que hay datos cargados
- Comprobar conexión a Internet (para Plotly)
- Refrescar la página (Ctrl+R)

### Tabla Vacía
- Cargar archivo Excel desde sidebar
- Verificar formato de Excel
- Revisar logs en `logs/`

### Errores de Sincronización
- Verificar token de GitHub
- Comprobar permisos del token
- Ver documentación de API GitHub

---

## 📱 Responsive Design

La aplicación se adapta a diferentes tamaños de pantalla:

- **Desktop**: Vista completa con gráficos lado a lado
- **Tablet**: Vista adaptada con gráficos apilados
- **Mobile**: Optimizado para visualización vertical

---

## 🚀 Tips de Uso

### Flujo Recomendado
1. ✅ Instalar dependencias
2. ✅ Configurar .env
3. ✅ Cargar Excel de usuarios
4. ✅ Procesar y transformar
5. ✅ Conectar a GitHub
6. ✅ Sincronizar datos
7. ✅ Explorar dashboard
8. ✅ Generar reportes

### Mejores Prácticas
- 🔄 Sincronizar semanalmente
- 💾 Guardar reportes mensuales
- 📊 Monitorear tendencias de uso
- ⚠️ Configurar alertas de consumo
- 🔒 Rotar tokens periódicamente

---

## 🎯 Casos de Uso

### 1. Auditoría de Licencias
Identificar usuarios con licencia pero sin uso

### 2. Optimización de Costos
Detectar licencias infrautilizadas

### 3. Planificación de Recursos
Predecir necesidades futuras

### 4. Reporte a Dirección
Generar informes ejecutivos

### 5. Control de Presupuesto
Monitorear gasto mensual
