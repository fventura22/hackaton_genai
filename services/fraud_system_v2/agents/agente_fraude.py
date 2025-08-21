"""Agente para detectar fraude basado en promedio de importes fraudulentos"""
import pandas as pd
import numpy as np

class agente_fraude:
    def __init__(self, data: pd.DataFrame):
        """
        Inicializar agente fraude
        Calcula promedio de importes donde CODIGO_RAZON_CONTRACARGO = 83
        """
        self.data = data
        # Calcular promedio de importes fraudulentos (código 83)
        if 'CODIGO_RAZON_CONTRACARGO' in data.columns and 'importe' in data.columns:
            # Filtrar código 83 como número o string
            fraud_data = data[(data['CODIGO_RAZON_CONTRACARGO'] == 83) | (data['CODIGO_RAZON_CONTRACARGO'] == '83')]
            self.promedio_fraude = fraud_data['importe'].mean() if not fraud_data.empty else 1000
            print(f"📊 Promedio fraudulento calculado: ${self.promedio_fraude:,.2f} ({len(fraud_data):,} registros)")
        else:
            self.promedio_fraude = 1000
            print("⚠️ Usando promedio por defecto: $1,000")
    
    def analizar_importe(self, importe: float) -> dict:
        """
        Analizar si importe está cerca del promedio fraudulento
        Alta probabilidad si está en 10% del promedio
        """
        if self.promedio_fraude == 0:
            return {
                'agente': 'fraude',
                'probabilidad_fraude': 0.1,
                'promedio_fraude': 0,
                'razon': 'Sin datos de fraude para comparar'
            }
        porc_80 = self.promedio_fraude *0.8
        porc_50 = self.promedio_fraude *0.5

        # Calcular diferencia porcentual con promedio fraudulento
        #diferencia = abs(importe - self.promedio_fraude) / self.promedio_fraude
        #
        #if diferencia <= 0.1:  # Dentro del 10%
        #    probabilidad = 0.8
        #    razon = f'Importe ${importe:.2f} muy cercano al promedio fraudulento ${self.promedio_fraude:.2f}'
        #elif diferencia <= 0.2:  # Dentro del 20%
        #    probabilidad = 0.6
        #    razon = f'Importe ${importe:.2f} cercano al promedio fraudulento'
        #else:
        #    probabilidad = max(0.1, 0.6 - (diferencia * 0.5))
        #    razon = f'Importe ${importe:.2f} alejado del promedio fraudulento'
        


        # Calculate percentage difference from fraud average
        diferencia_porcentual = abs(importe - self.promedio_fraude) / self.promedio_fraude
        
        # Very high amounts should be flagged as suspicious
        if importe > self.promedio_fraude * 100:  # 100x average
            probabilidad = 0.9
            razon = f'Importe ${importe:,.2f} extremadamente alto (100x promedio fraudulento)'
        elif importe > self.promedio_fraude * 10:  # 10x average
            probabilidad = 0.7
            razon = f'Importe ${importe:,.2f} muy alto (10x promedio fraudulento)'
        elif diferencia_porcentual <= 0.2:  # Within 20% of fraud average
            probabilidad = 0.8
            razon = f'Importe ${importe:,.2f} muy cercano al promedio fraudulento ${self.promedio_fraude:,.2f}'
        elif diferencia_porcentual <= 0.5:  # Within 50% of fraud average
            probabilidad = 0.6
            razon = f'Importe ${importe:,.2f} cercano al promedio fraudulento'
        else:
            probabilidad = max(0.1, 0.5 - (diferencia_porcentual * 0.1))
            razon = f'Importe ${importe:,.2f} alejado del promedio fraudulento'
        return {
            'agente': 'fraude',
            'probabilidad_fraude': round(probabilidad, 2),
            'promedio_fraude': round(self.promedio_fraude, 2),
            #'diferencia_porcentual': round(diferencia * 100, 1),
            'razon': razon
        }