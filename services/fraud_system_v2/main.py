#!/usr/bin/env python3
"""Sistema multiagente de detección de fraude - Versión corregida"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.aws_config import *
from agents.agente_master import agente_master

def main():
    """Función principal del sistema"""
    print("🚀 Sistema Multiagente de Detección de Fraude v2.0")
    print(f"📊 Bucket S3: {S3_BUCKET}")
    print(f"📄 Archivo: {S3_FILE}")
    print("=" * 60)
    
    try:
        # Inicializar agente master
        master = agente_master()
        
        # Casos de prueba con datos reales
        casos_prueba = [
            {'numero_documento': 5258, 'importe': 15000.00},
            {'numero_documento': 1072, 'importe': 600000.00},
            {'numero_documento': 4324,  'importe': 20000.00},
            {'numero_documento': 2083, 'importe': 189000.00},
            {'numero_documento': 1111,  'importe': 10000.00}

        ]
        
        print("\n🧪 Ejecutando casos de prueba:")
        print("-" * 60)
        
        for i, caso in enumerate(casos_prueba, 1):
            print(f"\n📋 Caso {i}: Cliente {caso['numero_documento']}, Importe ${caso['importe']}")
            
            resultado = master.analizar_transaccion(
                numero_documento=caso['numero_documento'],
                importe=caso['importe']
            )
            
            print(f"   🎯 Probabilidad Final: {resultado['probabilidad_final']}")
            print(f"   📋 Decisión: {resultado['decision']}")
            print(f"   ⚡ Acción: {resultado['accion_recomendada']}")
            
            # Mostrar análisis detallado
            print("   📊 Análisis por agente:")
            for agente, detalle in resultado['analisis_detallado'].items():
                prob = detalle.get('probabilidad_fraude', 0)
                razon = detalle.get('razon', 'Sin razón')
                print(f"      - {agente.capitalize()}: {prob} - {razon}")
        
        print("\n✅ Análisis completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())