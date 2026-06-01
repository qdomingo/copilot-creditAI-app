"""
Modelos de datos para usuarios y licencias
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    """Modelo de usuario con licencia de Copilot"""
    email: str
    nombre: str
    alias: str
    tipo_licencia: str
    fecha_asignacion: Optional[datetime] = None
    creditos_usados: float = 0.0
    ultimo_uso: Optional[datetime] = None
    estado: str = "activo"
    
    def to_dict(self) -> dict:
        """Convertir a diccionario"""
        return {
            "email": self.email,
            "nombre": self.nombre,
            "alias": self.alias,
            "tipo_licencia": self.tipo_licencia,
            "fecha_asignacion": self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            "creditos_usados": self.creditos_usados,
            "ultimo_uso": self.ultimo_uso.isoformat() if self.ultimo_uso else None,
            "estado": self.estado
        }


@dataclass
class MetricasOrganizacion:
    """Métricas a nivel de organización"""
    total_usuarios: int = 0
    usuarios_activos: int = 0
    total_creditos_usados: float = 0.0
    creditos_disponibles: float = 0.0
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convertir a diccionario"""
        return {
            "total_usuarios": self.total_usuarios,
            "usuarios_activos": self.usuarios_activos,
            "total_creditos_usados": self.total_creditos_usados,
            "creditos_disponibles": self.creditos_disponibles,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat()
        }
