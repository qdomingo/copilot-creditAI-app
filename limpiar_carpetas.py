"""
Script para limpiar las carpetas Excel-LicenciasIA y Excel-CreditsIA
"""
import shutil
from pathlib import Path

def limpiar_carpetas():
    """Eliminar todos los archivos Excel de las carpetas"""
    base_dir = Path(__file__).parent
    
    carpetas = [
        base_dir / "Excel-LicenciasIA",
        base_dir / "Excel-CreditsIA"
    ]
    
    for carpeta in carpetas:
        if carpeta.exists():
            # Eliminar todos los archivos Excel
            for archivo in carpeta.glob("*.xlsx"):
                archivo.unlink()
                print(f"✅ Eliminado: {archivo.name}")
            for archivo in carpeta.glob("*.xls"):
                archivo.unlink()
                print(f"✅ Eliminado: {archivo.name}")
    
    print("\n✨ Carpetas limpiadas exitosamente")


if __name__ == "__main__":
    respuesta = input("¿Estás seguro de que quieres limpiar las carpetas? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'yes', 'y']:
        limpiar_carpetas()
    else:
        print("Operación cancelada")
