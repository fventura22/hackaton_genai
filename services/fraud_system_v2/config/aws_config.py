"""Configuración AWS y variables de entorno"""
import os

# Use environment variables for AWS credentials (secure)
# These will be provided by ECS task role
os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_REGION', 'us-east-1')

# Only set credentials if not running in ECS (for local development)
if not os.getenv('AWS_EXECUTION_ENV'):
    # Use environment variables or default to empty (will use IAM role)
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    aws_session_token = os.getenv('AWS_SESSION_TOKEN', '')
    
    if aws_access_key:
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key
    if aws_secret_key:
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key
    if aws_session_token:
        os.environ['AWS_SESSION_TOKEN'] = aws_session_token

# Configuración S3
S3_BUCKET = os.getenv('S3_BUCKET', 'fraud-detection-purchase-history-tf')
S3_FILE = os.getenv('S3_FILE', 'BaseFinal.csv')

# Mapeo de campos del CSV
CAMPOS = {
    'monto': 'importe',
    'fecha': 'fecha_de_compra', 
    'blacklist': 'CODIGO_RAZON_CONTRACARGO',
    'cliente_id': 'NUMERO_DOCUMENTO',
    'prepagos': 'CANT_PREPAGOS',
    'pospagos': 'CANT_POSPAGOS'
}