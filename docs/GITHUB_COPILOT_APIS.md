# 📚 APIs de GitHub para Copilot - Guía de Referencia

## 🔑 APIs Disponibles

### 1. **Copilot Billing Seats API**
**Endpoint actual en uso:** ✅
```
GET /orgs/{org}/copilot/billing/seats
```

**Headers requeridos:**
```
Authorization: Bearer {token}
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

**Respuesta:**
```json
{
  "total_seats": 12,
  "seats": [
    {
      "created_at": "2021-08-03T18:00:00-06:00",
      "updated_at": "2021-09-23T15:00:00-06:00",
      "pending_cancellation_date": null,
      "last_activity_at": "2021-10-14T00:53:32-06:00",
      "last_activity_editor": "vscode/1.77.3/copilot/1.86.82",
      "assignee": {
        "login": "octocat",
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "type": "User",
        "site_admin": false
      }
    }
  ]
}
```

**Información disponible por usuario:**
- ❌ **NO proporciona créditos usados**
- ✅ Fecha de última actividad
- ✅ Editor usado
- ✅ Estado del seat

---

### 2. **Copilot Usage Metrics API** 🆕
**Endpoint para métricas de uso:**
```
GET /orgs/{org}/copilot/usage
```

**Query Parameters:**
- `since` (opcional): Fecha desde (ISO 8601)
- `until` (opcional): Fecha hasta (ISO 8601)
- `page` (opcional): Número de página
- `per_page` (opcional): Resultados por página (máx 100)

**Headers requeridos:**
```
Authorization: Bearer {token}
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

**Respuesta esperada:**
```json
[
  {
    "day": "2023-10-15",
    "total_suggestions_count": 5000,
    "total_acceptances_count": 3000,
    "total_lines_suggested": 10000,
    "total_lines_accepted": 6000,
    "total_active_users": 45,
    "breakdown": [
      {
        "language": "python",
        "editor": "vscode",
        "suggestions_count": 1500,
        "acceptances_count": 900,
        "lines_suggested": 3000,
        "lines_accepted": 1800,
        "active_users": 15
      }
    ]
  }
]
```

**Información disponible:**
- ✅ Métricas agregadas por día
- ✅ Sugerencias y aceptaciones
- ✅ Usuarios activos
- ❌ **NO proporciona créditos por usuario individual**

---

### 3. **Copilot Metrics API (Individual User)** 🎯
**Endpoint potencial (verificar disponibilidad):**
```
GET /orgs/{org}/copilot/billing/seats/{username}/usage
```

**Este endpoint NO está documentado públicamente** pero podría existir en versiones enterprise.

---

### 4. **GitHub Enterprise Audit Log API** 
**Endpoint:**
```
GET /orgs/{org}/audit-log
```

**Query Parameters:**
- `phrase`: Buscar eventos específicos de Copilot
- `include`: copilot

**Puede proporcionar:**
- Eventos de uso de Copilot
- Actividades por usuario
- ⚠️ **Requiere GitHub Enterprise Cloud**

---

## 🔍 Investigación de Créditos por Usuario

### Opción 1: API de Métricas de Uso (Recomendada)
GitHub proporciona una API para obtener métricas de uso, pero **a nivel agregado de organización**, no por usuario individual.

**Endpoint:**
```
GET https://api.github.com/orgs/{org}/copilot/usage
```

### Opción 2: GitHub Copilot Metrics API (Beta/Preview)
GitHub está desarrollando APIs más detalladas para Enterprise. Verifica:
- GitHub Copilot Business API
- GitHub Copilot Enterprise API

**Documentación:**
- https://docs.github.com/en/rest/copilot/copilot-usage
- https://docs.github.com/en/rest/copilot/copilot-user-management

### Opción 3: Webhooks de Copilot
Configurar webhooks para capturar eventos de uso en tiempo real.

---

## 💡 Estrategias para Obtener Créditos Usados

### Estrategia A: Calcular desde Métricas de Actividad
```python
# Pseudocódigo
creditos_usados = (
    total_suggestions_count * peso_sugerencia +
    total_acceptances_count * peso_aceptacion +
    total_active_days * creditos_por_dia
)
```

### Estrategia B: Usar Audit Logs (Enterprise)
Si tienes GitHub Enterprise Cloud, puedes analizar los logs de auditoría para calcular el uso.

### Estrategia C: Integración con Billing
Acceder a los datos de facturación si están disponibles vía API o exportación.

---

## 🧪 APIs a Probar

### 1. Copilot Usage API (Priority 1) 🔥
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/<ORG>/copilot/usage
```

### 2. Copilot Metrics API (si existe)
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/<ORG>/copilot/metrics
```

### 3. User-specific Usage (si existe)
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/<USERNAME>/copilot/usage
```

---

## 📊 Información Actualmente Disponible

| API | Créditos por Usuario | Métricas Agregadas | Última Actividad | Estado del Seat |
|-----|---------------------|-------------------|------------------|-----------------|
| `/copilot/billing/seats` | ❌ | ❌ | ✅ | ✅ |
| `/copilot/usage` | ❌ | ✅ | ❌ | ❌ |
| `/copilot/billing` | ❌ | ✅ | ❌ | ❌ |

---

## 🎯 Siguiente Paso Recomendado

1. **Probar la API de Usage:**
   ```python
   GET /orgs/{org}/copilot/usage?since=2024-01-01&until=2024-12-31
   ```

2. **Analizar la respuesta** para ver si proporciona datos por usuario

3. **Si no hay datos por usuario:**
   - Contactar a GitHub Support
   - Verificar si hay APIs adicionales en tu plan (Business/Enterprise)
   - Considerar usar métricas estimadas basadas en actividad

---

## 📖 Referencias

- [GitHub REST API - Copilot](https://docs.github.com/en/rest/copilot)
- [Copilot Billing Management](https://docs.github.com/en/rest/copilot/copilot-user-management)
- [Copilot Usage Metrics](https://docs.github.com/en/enterprise-cloud@latest/billing/managing-billing-for-github-copilot/viewing-your-github-copilot-usage)
- [GitHub Audit Log](https://docs.github.com/en/rest/orgs/orgs#get-the-audit-log-for-an-organization)

---

## ⚠️ Limitaciones Conocidas

1. **No hay API pública para créditos individuales por usuario** (a fecha de mayo 2026)
2. Las métricas de uso son principalmente agregadas a nivel de organización
3. Puede requerir GitHub Enterprise Cloud para métricas avanzadas
4. Los "créditos" de Copilot no son un concepto oficial de GitHub - es un modelo interno de tracking

---

## 🔄 Alternativa: Modelo de Estimación

Mientras no haya API directa, podemos estimar créditos basándonos en:

1. **Días activos** (de `last_activity_at`)
2. **Tipo de licencia** (Business vs Enterprise)
3. **Editor usado** (puede indicar intensidad de uso)

Fórmula propuesta:
```
creditos_estimados = dias_activos * factor_uso * multiplicador_licencia
```

Donde:
- `factor_uso` = 1.0 (uso normal), 1.5 (uso intensivo), 0.5 (uso bajo)
- `multiplicador_licencia` = 1.0 (Business), 2.33 (Enterprise)
