"""Template de configuración AWS - Copiar a aws_config.py y completar"""
import os

# Configurar credenciales AWS
# IMPORTANTE: Nunca subir credenciales reales a Git
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
os.environ['AWS_ACCESS_KEY_ID'] = 'TU_ACCESS_KEY_AQUI'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'TU_SECRET_KEY_AQUI'
os.environ['AWS_SESSION_TOKEN'] = 'TU_SESSION_TOKEN_AQUI'

# Configuración S3
S3_BUCKET = 'fraud-detection-purchase-history'
S3_FILE = 'Base.csv'

# Mapeo de campos del CSV
CAMPOS = {
    'monto': 'importe',
    'fecha': 'fecha_de_compra', 
    'blacklist': 'CODIGO_RAZON_CONTRACARGO',
    'cliente_id': 'NUMERO_DOCUMENTO',
    'prepagos': 'CANT_PREPAGOS',
    'pospagos': 'CANT_POSPAGOS'
}