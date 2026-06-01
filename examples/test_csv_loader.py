"""
Script de ejemplo para cargar y analizar CSV de créditos de GitHub
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.etl.csv_credits_loader import GitHubCreditsCSVLoader
from src.utils.logger import setup_logger

# Configurar logger
logger = setup_logger()


def main():
    """Función principal"""
    
    # Ruta al CSV de ejemplo
    csv_path = Path(__file__).parent / "github_credits_example.csv"
    
    if not csv_path.exists():
        logger.error(f"No se encontró el archivo: {csv_path}")
        return
    
    logger.info("=== Probando cargador de CSV de créditos ===")
    
    # Crear loader
    loader = GitHubCreditsCSVLoader()
    
    # Cargar CSV
    logger.info(f"Cargando CSV: {csv_path}")
    df_credits = loader.load_csv(str(csv_path))
    
    # Mostrar primeras filas
    logger.info("\n=== Primeras filas del CSV ===")
    print(df_credits.head())
    
    # Obtener estadísticas
    logger.info("\n=== Estadísticas generales ===")
    stats = loader.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Obtener resumen por usuario
    logger.info("\n=== Resumen por usuario ===")
    df_summary = loader.get_all_users_summary()
    print(df_summary)
    
    # Probar resumen de un usuario específico
    logger.info("\n=== Resumen de usuario específico ===")
    username = "jcreyg_indra"
    user_summary = loader.get_user_credits_summary(username)
    
    if user_summary:
        print(f"\nUsuario: {username}")
        print(f"  Créditos usados: {user_summary['creditos_usados']}")
        print(f"  Total quantity: {user_summary['total_quantity']}")
        print(f"  Total AIC quantity: {user_summary['total_aic_quantity']}")
        print(f"  Records count: {user_summary['records_count']}")
        print(f"  Models used: {user_summary['models_used']}")
    
    logger.success("\n✅ Prueba completada exitosamente")


if __name__ == "__main__":
    main()
