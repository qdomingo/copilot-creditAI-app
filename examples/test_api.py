"""
Script de ejemplo para probar la conexión con GitHub API
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.api.github_client import GitHubClient
from src.utils.logger import setup_logger
from config import validate_config

logger = setup_logger("logs/test_api.log")


def test_github_connection():
    """Probar conexión y obtención de datos"""
    try:
        # Validar configuración
        logger.info("Validando configuración...")
        validate_config()
        
        # Crear cliente
        logger.info("Creando cliente de GitHub...")
        client = GitHubClient()
        
        # Conectar
        logger.info("Conectando a GitHub...")
        client.connect()
        
        # Obtener seats
        logger.info("Obteniendo Copilot seats...")
        seats = client.get_copilot_seats()
        logger.info(f"Seats encontrados: {len(seats)}")
        
        if seats:
            logger.info("Ejemplo de primer seat:")
            logger.info(seats[0])
        
        # Obtener métricas
        logger.info("Obteniendo métricas de uso...")
        usage = client.get_copilot_usage()
        logger.info(f"Métricas: {usage}")
        
        # Obtener miembros
        logger.info("Obteniendo miembros de la organización...")
        members = client.get_organization_members()
        logger.info(f"Miembros encontrados: {len(members)}")
        
        logger.success("✅ Todas las pruebas pasaron exitosamente")
        
        # Cerrar
        client.close()
        
    except Exception as e:
        logger.error(f"❌ Error en las pruebas: {e}")
        raise


if __name__ == "__main__":
    test_github_connection()
