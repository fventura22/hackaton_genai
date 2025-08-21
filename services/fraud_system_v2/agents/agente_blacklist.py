"""Agente para verificar si cliente está en blacklist"""
import pandas as pd

class agente_blacklist:
    def __init__(self, data: pd.DataFrame):
        """
        Inicializar agente blacklist
        CODIGO_RAZON_CONTRACARGO = 83 indica fraude (blacklist)
        """
        self.data = data
        # Crear blacklist: clientes con código 83 (fraude)
        if 'CODIGO_RAZON_CONTRACARGO' in data.columns and 'NUMERO_DOCUMENTO' in data.columns:
            # Filtrar registros con código 83 (fraude) - probar tanto string como número
            fraud_records = data[(data['CODIGO_RAZON_CONTRACARGO'] == 83) | (data['CODIGO_RAZON_CONTRACARGO'] == '83')]
            blacklist_clientes = fraud_records['NUMERO_DOCUMENTO'].unique()
            
            # Convert all to strings for consistent comparison
            self.blacklist = set(str(cliente) for cliente in blacklist_clientes)
            print(f"🚨 Blacklist inicializada: {len(self.blacklist):,} clientes con fraude previo")
            print(f"🔍 Primeros 10 clientes en blacklist: {list(self.blacklist)[:10]}")
        else:
            self.blacklist = set()
            print("⚠️ No se pudieron cargar datos de blacklist - columnas faltantes")
    
    def verificar_cliente(self, numero_documento: str) -> dict:
        """Verificar si cliente está en blacklist por fraude previo"""
        en_blacklist = numero_documento in self.blacklist
        
        return {
            'agente': 'blacklist',
            'en_blacklist': en_blacklist,
            'probabilidad_fraude': 1.0 if en_blacklist else 0.0,
            'razon': 'Cliente con fraude previo (código 83)' if en_blacklist else 'Cliente sin fraudes previos'
        }