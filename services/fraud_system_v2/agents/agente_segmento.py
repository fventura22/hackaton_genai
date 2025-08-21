"""Agente para analizar riesgo por segmento de cliente"""
import pandas as pd

class agente_segmento:
    def __init__(self, data: pd.DataFrame):
        """
        Inicializar agente segmento
        CANT_PREPAGOS > 0 = Segmento_A (50% probabilidad)
        CANT_POSPAGOS > 0 = Segmento_B (20% probabilidad)
        """
        self.data = data
        # Probabilidades por segmento
        self.probabilidades = {
            'Segmento_A': 0.5,
            'Segmento_B': 0.2,
            'Segmento_C': 0.3,      # Tiene ambos
            'sin_datos': 0.25   # No tiene información
        }
    
    def determinar_segmento(self, numero_documento: str) -> str:
        """Determinar segmento del cliente basado en CANT_PREPAGOS y CANT_POSPAGOS"""
        if 'NUMERO_DOCUMENTO' not in self.data.columns:
            return 'sin_datos'
        
        cliente_data = self.data[self.data['NUMERO_DOCUMENTO'] == numero_documento]
        
        if cliente_data.empty:
            return 'sin_datos'
        
        # Obtener cantidades (usar primera fila si hay múltiples)
        prepagos = cliente_data['CANT_PREPAGOS'].iloc[0] if 'CANT_PREPAGOS' in cliente_data.columns else 0
        pospagos = cliente_data['CANT_POSPAGOS'].iloc[0] if 'CANT_POSPAGOS' in cliente_data.columns else 0
        
        # Determinar segmento
        if prepagos > 0 and pospagos > 0:
            return 'Segmento_C'
        elif prepagos > 0:
            return 'Segmento_A'
        elif pospagos > 0:
            return 'Segmento_B'
        else:
            return 'sin_datos'
    
    def analizar_segmento(self, numero_documento: str) -> dict:
        """Analizar riesgo basado en segmento del cliente"""
        segmento = self.determinar_segmento(numero_documento)
        probabilidad = self.probabilidades[segmento]
        
        razones = {
            'Segmento_A': 'Segmento_A - mayor riesgo de fraude',
            'Segmento_B': 'Segmento_B - riesgo moderado',
            'Segmento_C': 'Segmento_C - riesgo medio-alto',
            'sin_datos': 'Sin información de segmento - riesgo por defecto'
        }
        
        return {
            'agente': 'segmento',
            'segmento': segmento,
            'probabilidad_fraude': probabilidad,
            'razon': razones[segmento]
        }