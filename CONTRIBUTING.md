# Contribuyendo a GitHub Copilot Credits Control

¡Gracias por tu interés en contribuir! 🎉

## Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor crea un issue con:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica
- Información del entorno (OS, Python version, etc.)

### Sugerir Mejoras

Las sugerencias son bienvenidas! Crea un issue con:
- Descripción clara de la mejora
- Casos de uso
- Posible implementación

### Pull Requests

1. **Fork el repositorio**
2. **Crea una rama** para tu feature
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. **Haz tus cambios**
   - Sigue el estilo de código existente
   - Agrega tests si es necesario
   - Actualiza documentación

4. **Commit tus cambios**
   ```bash
   git commit -m "✨ Add: Nueva funcionalidad"
   ```

5. **Push a tu fork**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

6. **Crea un Pull Request**

## Estándares de Código

### Python Style Guide
Seguimos [PEP 8](https://pep8.org/)

```python
# Bueno
def calculate_credits(user_data: dict) -> float:
    """Calcular créditos de usuario"""
    return sum(user_data.values())

# Evitar
def calc(d):
    return sum(d.values())
```

### Convenciones de Nombres
- **Variables**: `snake_case`
- **Funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_CASE`

### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Descripción breve de la función.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        ValueError: Cuando ocurre X
    """
    pass
```

### Type Hints
```python
from typing import List, Dict, Optional

def process_users(users: List[Dict]) -> Optional[pd.DataFrame]:
    """Procesar lista de usuarios"""
    if not users:
        return None
    return pd.DataFrame(users)
```

## Testing

### Ejecutar Tests
```bash
pytest tests/ -v
```

### Cobertura
```bash
pytest tests/ --cov=src --cov-report=html
```

### Escribir Tests
```python
import pytest
from src.etl.excel_loader import ExcelLoader

def test_load_excel():
    """Test de carga de Excel"""
    loader = ExcelLoader("test_file.xlsx")
    df = loader.load()
    assert len(df) > 0
```

## Estructura de Commits

### Tipos de Commit
- `✨ Add:` Nueva funcionalidad
- `🐛 Fix:` Corrección de bug
- `📝 Docs:` Documentación
- `🎨 Style:` Formato, no afecta código
- `♻️ Refactor:` Refactorización
- `⚡ Perf:` Mejora de rendimiento
- `✅ Test:` Agregar tests
- `🔧 Config:` Cambios de configuración

### Ejemplos
```bash
✨ Add: Implementar cache de datos GitHub
🐛 Fix: Corregir error en detección de columnas
📝 Docs: Actualizar README con ejemplos
♻️ Refactor: Simplificar lógica de transformación
```

## Proceso de Revisión

1. **Revisión de código** por maintainers
2. **Tests** deben pasar
3. **Documentación** actualizada
4. **Sin conflictos** con main

## Código de Conducta

### Nuestros Estándares
- Ser respetuoso y profesional
- Aceptar críticas constructivas
- Enfocarse en lo mejor para el proyecto
- Mostrar empatía con otros contribuyentes

### Comportamiento Inaceptable
- Lenguaje ofensivo o discriminatorio
- Ataques personales
- Trolling o comentarios despectivos
- Acoso de cualquier tipo

## Preguntas?

Si tienes preguntas, puedes:
- Crear un issue con la etiqueta `question`
- Contactar a los maintainers

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia del proyecto (MIT).
