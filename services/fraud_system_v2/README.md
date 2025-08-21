# Sistema Multiagente de Detección de Fraude v2.0

Sistema multiagente que analiza transacciones para detectar fraude usando datos reales de S3 con **52,690 registros** y **30 clientes en blacklist**.

## 🏗️ Arquitectura

### Agentes Especializados:

1. **Agente Blacklist** (`agente_blacklist.py`)
   - Verifica si cliente tiene `CODIGO_RAZON_CONTRACARGO = 83` (fraude)
   - **Dataset real**: 30 clientes únicos en blacklist de 33 registros fraudulentos
   - Probabilidad: 1.0 si está en blacklist, 0.0 si no

2. **Agente Fraude** (`agente_fraude.py`)
   - Analiza si `importe` está cerca del **promedio fraudulento real: $358,698.94**
   - Rango de alta probabilidad: $322,829 - $394,569 (±10%)
   - Probabilidad: 0.8 si está en 10% del promedio, decrece con distancia

3. **Agente Segmento** (`agente_segmento.py`)
   - Determina segmento basado en `CANT_SEGMENTO_A` y `CANT_SEGMENTO_B`
   - Probabilidades: segmento_a=50%, segmento_b=20%, segmento_c=30%, sin_datos=25%

4. **Agente Master** (`agente_master.py`)
   - Centraliza resultados y calcula probabilidad final
   - Pesos: blacklist=50%, fraude=30%, segmento=20%
   - **Si cliente está en blacklist → Probabilidad automática = 1.0**

## 📊 Datos del CSV (Base.csv)

### Estadísticas del Dataset:
- **Total de registros**: 52,690
- **Separador**: Punto y coma (`;`)
- **Registros fraudulentos**: 33 (0.06%)
- **Clientes únicos en blacklist**: 30
- **Promedio fraudulento**: $358,698.94

### Campos Principales:
- **importe**: Monto de la transacción
- **fecha_de_compra**: Fecha de la compra
- **CODIGO_RAZON_CONTRACARGO**: 
  - `83` = fraude confirmado (blacklist)
  - `0` = sin fraude (99.94% de los casos)
- **NUMERO_DOCUMENTO**: ID del cliente
- **CANT_SEGMENTO_A**: Si > 0 es segmento_a
- **CANT_SEGMENTO_B**: Si > 0 es segmento_b

## ⚙️ Configuración

### Variables de Entorno (en `config/aws_config.py`):
```python
AWS_DEFAULT_REGION = 'us-west-2'
AWS_ACCESS_KEY_ID = 'ASIA2QBQ5Y7H2RX7JKX7'
S3_BUCKET = 'fraud-detection-purchase-history'
S3_FILE = 'Base.csv'
```

## 🚀 Uso

### Instalación:
```bash
pip install -r requirements.txt
```

### Ejecución:
```bash
python main.py
```

### Uso Programático:
```python
from agents.agente_master import agente_master

master = agente_master()
resultado = master.analizar_transaccion(
    numero_documento='12345678',
    importe=1500.00
)

print(f"Probabilidad: {resultado['probabilidad_final']}")
print(f"Decisión: {resultado['decision']}")
```

## 📋 Decisiones Finales

- **BLOQUEAR**: Probabilidad ≥ 0.8
- **REVISAR**: Probabilidad ≥ 0.5
- **MONITOREAR**: Probabilidad ≥ 0.3
- **APROBAR**: Probabilidad < 0.3

## 📁 Estructura

```
fraud_system_v2/
├── agents/
│   ├── agente_blacklist.py    # Verificación blacklist (código 83)
│   ├── agente_fraude.py       # Análisis por importe
│   ├── agente_segmento.py     # Análisis segmentos
│   └── agente_master.py       # Coordinador principal
├── config/
│   └── aws_config.py          # Configuración AWS y campos
├── main.py                    # Punto de entrada
├── verificar_blacklist.py     # Script de verificación
├── ANALISIS_DATASET.md        # Análisis detallado del dataset
└── README.md                  # Documentación
```

## 📈 Análisis del Dataset

Ver [ANALISIS_DATASET.md](ANALISIS_DATASET.md) para estadísticas detalladas:
- 52,690 registros totales
- Solo 30 clientes en blacklist (0.06% fraude)
- Promedio fraudulento: $358,698.94
- Sistema calibrado para minimizar falsos positivos

## 🔍 Ejemplos de Salida

### Cliente EN Blacklist (Automático BLOQUEAR)
```json
{
  "numero_documento": "6291",
  "importe": 100000.0,
  "probabilidad_final": 1.0,
  "decision": "BLOQUEAR",
  "accion_recomendada": "Bloquear transacción inmediatamente",
  "analisis_detallado": {
    "blacklist": {
      "probabilidad_fraude": 1.0,
      "razon": "Cliente con fraude previo (código 83)"
    }
  }
}
```

### Importe Cercano al Promedio Fraudulento ($358,698.94)
```json
{
  "numero_documento": "99999999",
  "importe": 350000.0,
  "probabilidad_final": 0.44,
  "decision": "MONITOREAR",
  "analisis_detallado": {
    "fraude": {
      "probabilidad_fraude": 0.8,
      "diferencia_porcentual": 2.4,
      "razon": "Importe muy cercano al promedio fraudulento"
    }
  }
}
```