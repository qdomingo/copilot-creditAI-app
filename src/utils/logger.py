"""
Configuración del sistema de logging
"""
import sys
from loguru import logger
from pathlib import Path


def setup_logger(log_file: str = "logs/app.log"):
    """Configurar logger de la aplicación"""
    
    # Crear directorio de logs si no existe
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Remover handler por defecto
    logger.remove()
    
    # Agregar handler para consola
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    
    # Agregar handler para archivo
    logger.add(
        log_file,
        rotation="10 MB",
        retention="1 week",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
    
    return logger
