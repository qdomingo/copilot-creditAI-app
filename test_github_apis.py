"""
Script para probar las APIs de GitHub Copilot y ver qué información proporcionan
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.api.github_client import GitHubClient
from src.utils.logger import setup_logger

logger = setup_logger("logs/test_github_apis.log")


def test_copilot_seats(client: GitHubClient):
    """Probar API de Copilot Seats"""
    print("\n" + "="*80)
    print("🔍 PROBANDO: Copilot Billing Seats API")
    print("="*80)
    
    seats = client.get_copilot_seats()
    
    if seats:
        print(f"✅ Se encontraron {len(seats)} seats")
        print("\n📋 Ejemplo de un seat:")
        print(json.dumps(seats[0], indent=2, default=str))
        
        print("\n📊 Información disponible por seat:")
        if seats:
            seat_keys = seats[0].keys()
            for key in seat_keys:
                print(f"  - {key}")
    else:
        print("❌ No se encontraron seats o error al obtener datos")
    
    return seats


def test_copilot_usage(client: GitHubClient):
    """Probar API de Copilot Usage"""
    print("\n" + "="*80)
    print("🔍 PROBANDO: Copilot Usage API")
    print("="*80)
    
    # Obtener uso de los últimos 30 días
    until = datetime.now()
    since = until - timedelta(days=30)
    
    since_str = since.strftime('%Y-%m-%d')
    until_str = until.strftime('%Y-%m-%d')
    
    print(f"📅 Periodo: {since_str} a {until_str}")
    
    usage = client.get_copilot_usage(since=since_str, until=until_str)
    
    if usage:
        print(f"✅ Se encontraron métricas para {len(usage)} días")
        print("\n📋 Ejemplo de un día:")
        print(json.dumps(usage[0] if usage else {}, indent=2, default=str))
        
        print("\n📊 Información disponible por día:")
        if usage and len(usage) > 0:
            day_keys = usage[0].keys()
            for key in day_keys:
                print(f"  - {key}")
    else:
        print("❌ No se encontraron métricas de uso")
        print("ℹ️ Esto puede significar:")
        print("   - La API no está disponible en tu plan")
        print("   - No hay datos para el periodo solicitado")
        print("   - El endpoint no existe o ha cambiado")
    
    return usage


def test_copilot_billing(client: GitHubClient):
    """Probar API de Copilot Billing Summary"""
    print("\n" + "="*80)
    print("🔍 PROBANDO: Copilot Billing Summary API")
    print("="*80)
    
    summary = client.get_copilot_metrics_summary()
    
    if summary:
        print("✅ Resumen de billing obtenido")
        print("\n📋 Datos de billing:")
        print(json.dumps(summary, indent=2, default=str))
        
        print("\n📊 Campos disponibles:")
        for key in summary.keys():
            print(f"  - {key}: {type(summary[key]).__name__}")
    else:
        print("❌ No se pudo obtener el resumen de billing")
    
    return summary


def analyze_credits_possibility(seats, usage, billing):
    """Analizar si es posible obtener créditos por usuario"""
    print("\n" + "="*80)
    print("🎯 ANÁLISIS: ¿Podemos obtener créditos por usuario?")
    print("="*80)
    
    print("\n1️⃣ Desde Seats API:")
    if seats and len(seats) > 0:
        seat = seats[0]
        has_credits = 'credits' in seat or 'usage' in seat or 'consumption' in seat
        if has_credits:
            print("   ✅ Hay información de créditos/uso en los seats")
        else:
            print("   ❌ NO hay información directa de créditos en los seats")
            print("   ℹ️ Campos disponibles:", list(seat.keys()))
    
    print("\n2️⃣ Desde Usage API:")
    if usage and len(usage) > 0:
        day = usage[0]
        has_user_breakdown = 'users' in day or 'user_breakdown' in day
        if has_user_breakdown:
            print("   ✅ Hay desglose por usuario en las métricas")
        else:
            print("   ❌ NO hay desglose por usuario (solo métricas agregadas)")
            print("   ℹ️ Campos disponibles:", list(day.keys()))
    
    print("\n3️⃣ Desde Billing API:")
    if billing:
        has_user_costs = 'user_costs' in billing or 'per_user' in billing
        if has_user_costs:
            print("   ✅ Hay información de costos por usuario")
        else:
            print("   ❌ NO hay información de costos individuales")
            print("   ℹ️ Campos disponibles:", list(billing.keys()))
    
    print("\n" + "="*80)
    print("💡 CONCLUSIONES Y RECOMENDACIONES")
    print("="*80)
    
    print("\nSi NO hay datos de créditos por usuario:")
    print("  📌 Opción A: Estimar basándose en actividad")
    print("     - Usar 'last_activity_at' de cada seat")
    print("     - Calcular días activos en el periodo")
    print("     - Aplicar fórmula: dias_activos * factor_uso")
    
    print("\n  📌 Opción B: Contactar a GitHub Support")
    print("     - Verificar si hay APIs adicionales en tu plan")
    print("     - Preguntar por GitHub Copilot Enterprise APIs")
    
    print("\n  📌 Opción C: Usar datos de facturación")
    print("     - Importar datos del portal de facturación")
    print("     - Procesar CSV/Excel de costos por usuario")


def main():
    """Función principal"""
    print("="*80)
    print("🚀 TEST DE APIs DE GITHUB COPILOT")
    print("="*80)
    print("\nEste script probará las APIs disponibles de GitHub Copilot")
    print("para determinar qué información podemos obtener sobre uso de créditos.\n")
    
    try:
        # Crear cliente de GitHub
        print("🔐 Conectando a GitHub...")
        client = GitHubClient()
        client.connect()
        print(f"✅ Conectado a: {client.org_name}\n")
        
        # Probar cada API
        seats = test_copilot_seats(client)
        usage = test_copilot_usage(client)
        billing = test_copilot_billing(client)
        
        # Analizar resultados
        analyze_credits_possibility(seats, usage, billing)
        
        print("\n" + "="*80)
        print("✨ PRUEBA COMPLETADA")
        print("="*80)
        print("\nRevisa los resultados arriba para ver qué APIs están disponibles")
        print("y qué información proporcionan.\n")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        logger.error(f"Error en pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
