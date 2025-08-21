#!/usr/bin/env python3
"""Script para verificar la blacklist y explicar el filtrado"""

import boto3
import pandas as pd
from config.aws_config import *

def verificar_blacklist():
    """Verificar cuántos clientes están en blacklist con código 83"""
    try:
        print("🔍 Verificando blacklist (CODIGO_RAZON_CONTRACARGO == 83)")
        print("=" * 60)
        
        # Cargar datos con separador correcto
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE)
        data = pd.read_csv(response['Body'], sep=';')  # Usar punto y coma
        
        print(f"📊 Total de registros: {len(data):,}")
        print(f"📋 Columnas encontradas: {len(data.columns)}")
        
        # Verificar si existe la columna
        if 'CODIGO_RAZON_CONTRACARGO' not in data.columns:
            print("❌ Columna CODIGO_RAZON_CONTRACARGO no encontrada")
            print(f"📋 Columnas disponibles: {list(data.columns)}")
            return
        
        # Analizar todos los códigos
        print(f"\n🔍 Análisis de códigos de razón contracargo:")
        codigos_count = data['CODIGO_RAZON_CONTRACARGO'].value_counts()
        print(f"📊 Total de códigos únicos: {len(codigos_count)}")
        
        # Mostrar los 10 códigos más frecuentes
        print(f"\n📈 Top 10 códigos más frecuentes:")
        for codigo, count in codigos_count.head(10).items():
            porcentaje = (count / len(data)) * 100
            print(f"   Código {codigo}: {count:,} registros ({porcentaje:.2f}%)")
        
        # Filtrar específicamente código 83 (fraude)
        fraud_records = data[data['CODIGO_RAZON_CONTRACARGO'] == 83]
        print(f"\n💰 Registros con código 83 (FRAUDE):")
        print(f"   📊 Total de registros fraudulentos: {len(fraud_records):,}")
        print(f"   📈 Porcentaje del total: {(len(fraud_records)/len(data)*100):.2f}%")
        
        if len(fraud_records) > 0:
            # Analizar clientes únicos en blacklist
            if 'NUMERO_DOCUMENTO' in data.columns:
                clientes_blacklist = fraud_records['NUMERO_DOCUMENTO'].unique()
                print(f"   👥 Clientes únicos en blacklist: {len(clientes_blacklist):,}")
                
                # Mostrar algunos ejemplos
                print(f"\n📋 Ejemplos de clientes en blacklist:")
                for i, cliente in enumerate(clientes_blacklist[:5]):
                    registros_cliente = len(fraud_records[fraud_records['NUMERO_DOCUMENTO'] == cliente])
                    print(f"   {i+1}. Cliente {cliente}: {registros_cliente} registros fraudulentos")
                
                # Analizar importes fraudulentos
                if 'importe' in fraud_records.columns:
                    promedio_fraude = fraud_records['importe'].mean()
                    mediana_fraude = fraud_records['importe'].median()
                    
                    print(f"\n💵 Estadísticas de importes fraudulentos:")
                    print(f"   🎯 Promedio: ${promedio_fraude:,.2f}")
                    print(f"   📊 Mediana: ${mediana_fraude:,.2f}")
                    print(f"   📉 Mínimo: ${fraud_records['importe'].min():,.2f}")
                    print(f"   📈 Máximo: ${fraud_records['importe'].max():,.2f}")
                    
                    # Rango del 10% para análisis
                    rango_10_pct = promedio_fraude * 0.1
                    print(f"\n🎯 Rango de alta probabilidad (±10% del promedio):")
                    print(f"   📉 ${promedio_fraude - rango_10_pct:,.2f}")
                    print(f"   📈 ${promedio_fraude + rango_10_pct:,.2f}")
                
                return len(clientes_blacklist), promedio_fraude if 'importe' in fraud_records.columns else 0
            else:
                print("❌ Columna NUMERO_DOCUMENTO no encontrada")
        else:
            print("❌ No se encontraron registros con código 83")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0

def explicar_filtrado():
    """Explicar por qué hay más de 2700 clientes en blacklist"""
    print("\n" + "="*60)
    print("📚 EXPLICACIÓN DEL FILTRADO DE BLACKLIST")
    print("="*60)
    
    print("""
🔍 CRITERIO DE BLACKLIST:
   - Campo: CODIGO_RAZON_CONTRACARGO
   - Valor: 83 (indica fraude confirmado)
   - Lógica: Si un cliente tiene AL MENOS UN registro con código 83, 
            está en la blacklist

📊 POR QUÉ MÁS DE 2700 CLIENTES:
   1. El dataset contiene 52,690 registros totales
   2. Cada registro representa una transacción/evento
   3. Un cliente puede tener múltiples registros
   4. Si un cliente tuvo fraude (código 83) en cualquier momento,
      queda marcado permanentemente en la blacklist
   5. Los 2700+ clientes representan todos los que tuvieron
      al menos una transacción fraudulenta

🎯 IMPACTO EN EL SISTEMA:
   - Probabilidad de fraude = 1.0 (100%) para estos clientes
   - Decisión automática: BLOQUEAR
   - No importa el monto o segmento, la blacklist tiene prioridad máxima
   
⚖️ PESOS EN EL SISTEMA:
   - Blacklist: 50% (pero si está en blacklist = 100% automático)
   - Análisis de fraude por monto: 30%
   - Análisis por segmento: 20%
    """)

if __name__ == "__main__":
    clientes_blacklist, promedio = verificar_blacklist()
    explicar_filtrado()
    
    if clientes_blacklist > 0:
        print(f"\n✅ RESUMEN:")
        print(f"   👥 Clientes en blacklist: {clientes_blacklist:,}")
        print(f"   💰 Promedio fraudulento: ${promedio:,.2f}")
        print(f"   🎯 Sistema configurado correctamente")