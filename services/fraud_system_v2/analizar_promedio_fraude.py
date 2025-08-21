#!/usr/bin/env python3
"""Script para analizar el promedio fraudulento de la base de datos"""

import boto3
import pandas as pd
from config.aws_config import *

def analizar_promedio_fraude():
    """Analizar estadísticas de fraude en la base de datos"""
    try:
        print("📊 Analizando promedio fraudulento...")
        print(f"🔗 Conectando a S3: {S3_BUCKET}/{S3_FILE}")
        
        # Cargar datos desde S3
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE)
        data = pd.read_csv(response['Body'])
        
        print(f"📈 Total de registros: {len(data):,}")
        print(f"📋 Columnas disponibles: {list(data.columns)}")
        
        # Verificar si existen las columnas necesarias
        if 'CODIGO_RAZON_CONTRACARGO' not in data.columns:
            print("❌ Columna CODIGO_RAZON_CONTRACARGO no encontrada")
            return
        
        if 'importe' not in data.columns:
            print("❌ Columna importe no encontrada")
            return
        
        # Analizar códigos de razón
        print("\n🔍 Análisis de códigos de razón:")
        codigos_count = data['CODIGO_RAZON_CONTRACARGO'].value_counts().head(10)
        for codigo, count in codigos_count.items():
            print(f"   Código {codigo}: {count:,} registros")
        
        # Filtrar registros fraudulentos (código 83)
        fraud_data = data[data['CODIGO_RAZON_CONTRACARGO'] == 83]
        
        print(f"\n💰 Análisis de fraude (código 83):")
        print(f"   📊 Registros fraudulentos: {len(fraud_data):,}")
        print(f"   📈 Porcentaje del total: {(len(fraud_data)/len(data)*100):.2f}%")
        
        if len(fraud_data) > 0:
            # Estadísticas de importes fraudulentos
            promedio_fraude = fraud_data['importe'].mean()
            mediana_fraude = fraud_data['importe'].median()
            min_fraude = fraud_data['importe'].min()
            max_fraude = fraud_data['importe'].max()
            std_fraude = fraud_data['importe'].std()
            
            print(f"\n💵 Estadísticas de importes fraudulentos:")
            print(f"   🎯 Promedio: ${promedio_fraude:,.2f}")
            print(f"   📊 Mediana: ${mediana_fraude:,.2f}")
            print(f"   📉 Mínimo: ${min_fraude:,.2f}")
            print(f"   📈 Máximo: ${max_fraude:,.2f}")
            print(f"   📏 Desviación estándar: ${std_fraude:,.2f}")
            
            # Rangos de análisis (10% del promedio)
            rango_10_pct = promedio_fraude * 0.1
            limite_inferior = promedio_fraude - rango_10_pct
            limite_superior = promedio_fraude + rango_10_pct
            
            print(f"\n🎯 Rango de alta probabilidad (±10% del promedio):")
            print(f"   📉 Límite inferior: ${limite_inferior:,.2f}")
            print(f"   📈 Límite superior: ${limite_superior:,.2f}")
            print(f"   📏 Rango: ${rango_10_pct:,.2f}")
            
            # Contar registros en el rango del 10%
            en_rango = fraud_data[
                (fraud_data['importe'] >= limite_inferior) & 
                (fraud_data['importe'] <= limite_superior)
            ]
            
            print(f"   📊 Registros fraudulentos en rango ±10%: {len(en_rango):,}")
            print(f"   📈 Porcentaje en rango: {(len(en_rango)/len(fraud_data)*100):.1f}%")
            
        else:
            print("❌ No se encontraron registros con código 83 (fraude)")
        
        # Análisis de todos los importes para comparación
        print(f"\n📊 Estadísticas generales de importes:")
        promedio_general = data['importe'].mean()
        mediana_general = data['importe'].median()
        
        print(f"   🎯 Promedio general: ${promedio_general:,.2f}")
        print(f"   📊 Mediana general: ${mediana_general:,.2f}")
        
        if len(fraud_data) > 0:
            diferencia = ((promedio_fraude - promedio_general) / promedio_general) * 100
            print(f"   📈 Diferencia fraude vs general: {diferencia:+.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analizar_promedio_fraude()