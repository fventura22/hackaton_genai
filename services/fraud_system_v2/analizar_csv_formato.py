#!/usr/bin/env python3
"""Script para analizar el formato del CSV y corregir la lectura"""

import boto3
import pandas as pd
from config.aws_config import *

def analizar_formato_csv():
    """Analizar formato del CSV y encontrar el separador correcto"""
    try:
        print("🔍 Analizando formato del CSV...")
        
        # Cargar datos desde S3
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE)
        
        # Leer las primeras líneas para analizar formato
        content = response['Body'].read().decode('utf-8')
        lines = content.split('\n')[:5]
        
        print("📄 Primeras 5 líneas del archivo:")
        for i, line in enumerate(lines):
            print(f"   {i+1}: {line[:100]}...")
        
        # Probar diferentes separadores
        separadores = [';', ',', '\t', '|']
        
        for sep in separadores:
            print(f"\n🧪 Probando separador '{sep}':")
            try:
                # Reiniciar el stream
                response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE)
                df_test = pd.read_csv(response['Body'], sep=sep, nrows=5)
                print(f"   ✅ Columnas ({len(df_test.columns)}): {list(df_test.columns)[:5]}")
                
                # Si encontramos las columnas que necesitamos
                if 'CODIGO_RAZON_CONTRACARGO' in df_test.columns and 'importe' in df_test.columns:
                    print(f"   🎯 ¡Separador correcto encontrado: '{sep}'!")
                    return sep
                    
            except Exception as e:
                print(f"   ❌ Error con separador '{sep}': {e}")
        
        print("\n❌ No se pudo determinar el separador correcto")
        return None
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return None

def analizar_con_separador_correcto():
    """Analizar datos con el separador correcto"""
    separador = analizar_formato_csv()
    
    if not separador:
        print("❌ No se pudo determinar el formato del archivo")
        return
    
    try:
        print(f"\n📊 Analizando datos con separador '{separador}'...")
        
        # Cargar datos con separador correcto
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE)
        data = pd.read_csv(response['Body'], sep=separador)
        
        print(f"📈 Total de registros: {len(data):,}")
        print(f"📋 Columnas: {list(data.columns)}")
        
        # Analizar códigos de razón
        if 'CODIGO_RAZON_CONTRACARGO' in data.columns:
            print(f"\n🔍 Códigos de razón únicos:")
            codigos = data['CODIGO_RAZON_CONTRACARGO'].value_counts().head(10)
            for codigo, count in codigos.items():
                print(f"   Código {codigo}: {count:,} registros")
            
            # Analizar fraudes (código 83)
            fraud_data = data[data['CODIGO_RAZON_CONTRACARGO'] == 83]
            print(f"\n💰 Registros con código 83 (fraude): {len(fraud_data):,}")
            
            if len(fraud_data) > 0 and 'importe' in data.columns:
                promedio_fraude = fraud_data['importe'].mean()
                print(f"🎯 PROMEDIO FRAUDULENTO: ${promedio_fraude:,.2f}")
                
                # Estadísticas adicionales
                print(f"📊 Mediana fraudulenta: ${fraud_data['importe'].median():,.2f}")
                print(f"📉 Mínimo fraudulento: ${fraud_data['importe'].min():,.2f}")
                print(f"📈 Máximo fraudulento: ${fraud_data['importe'].max():,.2f}")
                
                # Rango del 10%
                rango_10 = promedio_fraude * 0.1
                print(f"\n🎯 Rango ±10% del promedio:")
                print(f"   ${promedio_fraude - rango_10:,.2f} - ${promedio_fraude + rango_10:,.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analizar_con_separador_correcto()