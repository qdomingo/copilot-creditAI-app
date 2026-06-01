"""
Configuración centralizada de la aplicación
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = BASE_DIR / "Excel-CreditsIA"
CSV_CREDITS_DIR = BASE_DIR / "data" / "github_credits"
REPORTS_DIR = DATA_DIR / "reports"

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "GitHub Copilot Credits Control")
APP_ICON = os.getenv("APP_ICON", "🤖")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Excel Configuration
# INPUT_EXCEL_PATH se determina dinámicamente al cargar
OUTPUT_EXCEL_PATH = os.getenv("OUTPUT_EXCEL_PATH", str(PROCESSED_DIR / "licencias_transformadas.xlsx"))

# API Settings
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Excel Column Mapping (columnas esperadas en el Excel de entrada)
EXCEL_COLUMNS = {
    "email": ["email", "correo", "usuario", "user"],
    "nombre": ["nombre", "name", "nombre completo", "full name"],
    "alias": ["alias", "username", "usuario github"],
    "licencia": ["licencia", "license", "tipo licencia", "license type"],
    "fecha": ["fecha", "date", "fecha asignacion", "assignment date"]
}

def ensure_directories():
    """Crear directorios necesarios si no existen"""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CSV_CREDITS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def validate_config():
    """Validar configuración necesaria"""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN no configurado en .env")
    if not GITHUB_ORG:
        raise ValueError("GITHUB_ORG no configurado en .env")
    return True
