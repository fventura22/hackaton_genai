"""Agente master que centraliza las salidas de todos los agentes"""
import boto3
import pandas as pd
import os
from agents.agente_blacklist import agente_blacklist
from agents.agente_fraude import agente_fraude
from agents.agente_segmento import agente_segmento

class agente_master:
    def __init__(self):
        """Inicializar agente master y cargar datos de S3"""
        self.s3_client = boto3.client('s3')
        self.bucket = os.getenv('S3_BUCKET', 'fraud-detection-purchase-history-tf')
        self.file_key = os.getenv('S3_FILE', 'BaseFinal.csv')
        
        # Cargar datos
        print("📥 Cargando datos desde S3...")
        self.data = self._cargar_datos_s3()
        print(f"✅ Datos cargados: {len(self.data)} registros")
        
        # Inicializar agentes especializados
        print("🤖 Inicializando agentes...")
        self.agente_blacklist = agente_blacklist(self.data)
        self.agente_fraude = agente_fraude(self.data)
        self.agente_segmento = agente_segmento(self.data)
        
        # Pesos para cálculo final
        self.pesos = {
            'blacklist': 0.5,   # Mayor peso para blacklist
            'fraude': 0.3,      # Peso medio para análisis de fraude
            'segmento': 0.2     # Menor peso para segmento
        }
        
        print(f"✅ Agentes inicializados exitosamente")
        print(f"🚫 Blacklist: {len(self.agente_blacklist.blacklist)} clientes")
        print(f"💰 Promedio fraude: ${self.agente_fraude.promedio_fraude:.2f}")
        print(f"⚖️ Pesos configurados: {self.pesos}")
        print(f"🎆 Sistema Multi-Agente listo para análisis")
    
    def _cargar_datos_s3(self) -> pd.DataFrame:
        """Cargar datos desde S3 con separador correcto"""
        print(f"🔗 Conectando a S3...")
        print(f"📦 Bucket: {self.bucket}")
        print(f"📄 Archivo: {self.file_key}")
        
        try:
            print(f"📥 Descargando archivo desde S3...")
            response = self.s3_client.get_object(Bucket=self.bucket, Key=self.file_key)
            print(f"✅ Archivo descargado exitosamente")
            
            print(f"📊 Parseando CSV con estructura personalizada...")
            import io
            csv_content = response['Body'].read().decode('utf-8')
            lines = csv_content.strip().split('\n')
            
            # Procesar cada línea para extraer los datos estructurados
            processed_records = []
            for line_num, line in enumerate(lines[1:], 1):  # Skip header
                if ';83;' in line:  # Solo procesar líneas con código 83 (fraude)
                    try:
                        # Extraer datos del primer campo quoted
                        import re
                        first_quote_match = re.search(r'"([^"]+)"', line)
                        if first_quote_match:
                            first_section = first_quote_match.group(1)
                            parts = first_section.split(';')
                            if len(parts) >= 3:
                                numero_documento = parts[0]
                                importe_str = parts[1]
                                # Convert importe to float, handle any conversion errors
                                try:
                                    importe = float(importe_str.replace(',', ''))
                                except (ValueError, TypeError):
                                    importe = 0.0  # Default value for invalid amounts
                                    print(f"⚠️ Invalid amount '{importe_str}' for document {numero_documento}")
                                
                                # El código 83 está en la sección UTC, confirmamos que está presente
                                processed_records.append({
                                    'NUMERO_DOCUMENTO': numero_documento,
                                    'importe': importe,
                                    'CODIGO_RAZON_CONTRACARGO': 83  # Confirmed by ';83;' presence
                                })
                    except Exception as e:
                        print(f"⚠️ Error procesando línea {line_num}: {e}")
                        continue
            
            # Crear DataFrame con registros procesados
            data = pd.DataFrame(processed_records)
            print(f"✅ CSV procesado - encontrados {len(processed_records)} registros con código 83")
            
            print(f"✅ CSV parseado exitosamente")
            print(f"📊 Registros cargados: {len(data):,}")
            print(f"📋 Columnas encontradas: {len(data.columns)}")
            print(f"📝 Columnas: {list(data.columns)[:10]}...")  # Mostrar primeras 10 columnas
            
            # Verificar columnas críticas
            required_columns = ['NUMERO_DOCUMENTO', 'importe', 'CODIGO_RAZON_CONTRACARGO']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                print(f"⚠️ Columnas faltantes: {missing_columns}")
                print(f"📋 Columnas disponibles: {list(data.columns)}")
            else:
                print(f"✅ Todas las columnas requeridas están presentes")
            
            return data
            
        except Exception as e:
            print(f"❌ Error crítico cargando S3: {e}")
            print(f"🔍 Tipo de error: {type(e).__name__}")
            import traceback
            print(f"📋 Stack trace:")
            traceback.print_exc()
            raise Exception(f"No se pudo cargar datos de S3: {e}")
    
    def calcular_probabilidad_final(self, resultados: dict) -> float:
        """Calcular probabilidad final ponderada"""
        # Si está en blacklist, probabilidad máxima
        if resultados['blacklist']['en_blacklist']:
            return 1.0
        
        # Calcular promedio ponderado
        probabilidad_total = (
            resultados['blacklist']['probabilidad_fraude'] * self.pesos['blacklist'] +
            resultados['fraude']['probabilidad_fraude'] * self.pesos['fraude'] +
            resultados['segmento']['probabilidad_fraude'] * self.pesos['segmento']
        )
        
        return round(probabilidad_total, 3)
    
    def generar_decision(self, probabilidad: float) -> dict:
        """Generar decisión final basada en probabilidad"""
        if probabilidad >= 0.8:
            return {'decision': 'BLOQUEAR', 'accion': 'Bloquear transacción inmediatamente'}
        elif probabilidad >= 0.5:
            return {'decision': 'REVISAR', 'accion': 'Requiere revisión manual'}
        elif probabilidad >= 0.3:
            return {'decision': 'MONITOREAR', 'accion': 'Monitorear actividad del cliente'}
        else:
            return {'decision': 'OK', 'accion': 'Transacción OK'}
    
    def analizar_transaccion(self, numero_documento: str, importe: float) -> dict:
        """Análisis completo de transacción usando todos los agentes"""
        # Ejecutar análisis con cada agente
        resultado_blacklist = self.agente_blacklist.verificar_cliente(numero_documento)
        resultado_fraude = self.agente_fraude.analizar_importe(importe)
        resultado_segmento = self.agente_segmento.analizar_segmento(numero_documento)
        
        # Consolidar resultados
        resultados = {
            'blacklist': resultado_blacklist,
            'fraude': resultado_fraude,
            'segmento': resultado_segmento
        }
        
        # Calcular probabilidad final
        probabilidad_final = self.calcular_probabilidad_final(resultados)
        
        # Generar decisión
        decision_info = self.generar_decision(probabilidad_final)
        
        return {
            'numero_documento': numero_documento,
            'importe': importe,
            'probabilidad_final': probabilidad_final,
            'decision': decision_info['decision'],
            'accion_recomendada': decision_info['accion'],
            'analisis_detallado': resultados,
            'pesos_utilizados': self.pesos
        }