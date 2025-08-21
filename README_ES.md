# Sistema Inteligente de Detección de Fraude

Plataforma avanzada de prevención de fraude basada en inteligencia artificial multiagéntica, diseñada específicamente para el sector de telecomunicaciones. Combina análisis de datos en tiempo real con machine learning para identificar y prevenir actividades fraudulentas.

## Arquitectura del Sistema

### Núcleo de Inteligencia Artificial Multiagéntica

El sistema emplea una arquitectura de agentes especializados que trabajan de forma coordinada:

**🤖 Agente Coordinador Principal** (Puerto 8003)
- Orquesta el análisis de todos los agentes especialistas
- Consolida puntuaciones de riesgo y toma decisiones finales
- Implementa lógica de negocio para aprobación/rechazo de transacciones

**📊 Agentes Especialistas de Análisis:**
- **Historial de Compras** (Puerto 8006): Analiza patrones de comportamiento transaccional
- **Listas Negras** (Puerto 8007): Verifica identidades y dispositivos comprometidos
- **Perfil Sociodemográfico** (Puerto 8008): Evalúa coherencia demográfica del comportamiento
- **Análisis Temporal** (Puerto 8009): Detecta anomalías en patrones de tiempo y velocidad
- **Geolocalización** (Puerto 8010): Identifica ubicaciones sospechosas y viajes imposibles

### Infraestructura de Microservicios

**🌐 Servicios Core:**
- **API Gateway** (Puerto 8000): Punto de entrada unificado y balanceador de carga
- **Recolector de Datos** (Puerto 8001): Ingesta y normalización de datos desde múltiples fuentes
- **Analizador de Patrones** (Puerto 8002): Motor de análisis y correlación de datos
- **Gestión de Usuarios** (Puerto 8004): Autenticación, autorización y control de acceso
- **Sistema de Notificaciones** (Puerto 8005): Alertas en tiempo real y comunicaciones

### Repositorio de Datos en AWS S3

Cada agente especialista accede a repositorios de datos específicos almacenados en Amazon S3:

**📁 Buckets de Datos Especializados:**
- `fraud-detection-purchase-history`: Transacciones históricas y patrones de compra
- `fraud-detection-claims`: Reclamos, chargebacks y disputas de clientes
- `fraud-detection-demographics`: Perfiles demográficos y segmentación de usuarios
- `fraud-detection-blacklists`: Listas negras de entidades sospechosas
- `fraud-detection-geolocation`: Logs de ubicación y análisis geográfico
- `fraud-detection-devices`: Huellas digitales y comportamiento de dispositivos

### Stack Tecnológico

**☁️ Cloud & Storage:**
- **Amazon S3**: Data Lake para almacenamiento masivo de datos históricos
- **PostgreSQL**: Base de datos transaccional para operaciones en tiempo real
- **Redis**: Cache distribuido y gestión de sesiones de alta velocidad
- **RabbitMQ**: Message broker para comunicación asíncrona entre servicios

**🖥️ Frontend:**
- **React 18+**: Aplicación web responsiva con interfaz moderna
- **Material-UI**: Componentes de interfaz profesional
- **Chart.js**: Visualizaciones interactivas y dashboards

## Capacidades de Detección Inteligente

### Motor de Análisis Multiagéntico

**🎯 Proceso de Análisis Coordinado:**
1. **Ingesta de Datos**: Cada agente extrae información relevante desde buckets S3 especializados
2. **Análisis Paralelo**: Los agentes procesan datos simultáneamente en sus dominios de especialización
3. **Consolidación**: El agente coordinador integra resultados y calcula puntuación de riesgo final
4. **Decisión Automatizada**: Sistema de reglas de negocio determina acción (Aprobar/Revisar/Bloquear)

**🔍 Especialización por Agente:**

**Agente de Historial Transaccional:**
- Analiza desviaciones en montos y frecuencia de compras
- Detecta cambios súbitos en patrones de comportamiento
- Identifica transacciones atípicas basadas en historial del cliente

**Agente de Verificación de Listas Negras:**
- Consulta bases de datos de entidades comprometidas
- Verifica dispositivos, IPs y números de tarjeta en tiempo real
- Mantiene índices actualizados de amenazas conocidas

**Agente de Análisis Demográfico:**
- Evalúa coherencia entre perfil del cliente y comportamiento de compra
- Detecta anomalías basadas en segmentación demográfica
- Analiza patrones típicos por grupo socioeconómico

**Agente de Análisis Temporal:**
- Identifica transacciones en horarios inusuales para el perfil del cliente
- Detecta velocidad anómala de transacciones (burst patterns)
- Analiza secuencias temporales sospechosas

**Agente de Inteligencia Geográfica:**
- Detecta ubicaciones imposibles o improbables
- Analiza patrones de movilidad y zonas de riesgo
- Identifica transacciones desde ubicaciones no habituales

### Interfaz de Usuario Avanzada

**💻 Aplicación Web Responsiva:**
- **Dashboard Ejecutivo**: Métricas en tiempo real y KPIs de fraude
- **Centro de Análisis**: Herramientas interactivas para investigación de casos
- **Panel de Control**: Gestión de reglas de negocio y configuración de umbrales
- **Sistema de Alertas**: Notificaciones inteligentes y gestión de casos críticos
- **Reportería Avanzada**: Análisis histórico y tendencias de fraude

### Algoritmos de Detección Avanzados

**🎯 Técnicas de Machine Learning por Especialidad:**

**Análisis Comportamental:**
- Detección de anomalías en patrones de gasto
- Análisis de desviación estadística en comportamiento transaccional
- Modelos predictivos de riesgo basados en historial

**Verificación de Identidad:**
- Matching en tiempo real contra bases de datos de amenazas
- Análisis de reputación de dispositivos y direcciones IP
- Correlación de identidades sospechosas

**Inteligencia Geoespacial:**
- Algoritmos de detección de viajes imposibles
- Análisis de riesgo por zona geográfica
- Modelos de movilidad y patrones de ubicación

**Análisis Temporal:**
- Detección de patrones de velocidad anómala
- Análisis de ventanas temporales sospechosas
- Correlación de eventos temporales

## Guía de Implementación

### Requisitos del Sistema

**🔧 Infraestructura Mínima:**
- Docker Engine 20.10+ y Docker Compose 2.0+
- Node.js 18+ LTS para desarrollo frontend
- AWS CLI configurado con credenciales S3
- Mínimo 8GB RAM y 4 CPU cores

### Despliegue Rápido

**1️⃣ Configuración Inicial**
```bash
# Clonar repositorio
git clone <repository-url>
cd hackaton-genai

# Configurar variables de entorno
cp .env.example .env
# Editar .env con credenciales AWS y configuración
```

**2️⃣ Inicialización de Servicios**
```bash
# Levantar infraestructura completa
docker-compose up -d

# Verificar salud del sistema
curl http://localhost:8000/api/health

# Acceder a la aplicación web
open http://localhost:3000
```

**3️⃣ Prueba del Sistema**
```bash
# Ejecutar análisis de fraude de prueba
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "DEMO_001",
    "transaction_data": {
      "amount": 15000,
      "timestamp": "2024-01-15T03:30:00Z",
      "location": "Unknown_Location",
      "merchant_category": "high_risk"
    }
  }'
```

### Credenciales de Demostración

**👤 Usuarios de Prueba:**
- **Analista Senior**: `fraud_analyst` / `analyst123`
- **Administrador del Sistema**: `admin` / `admin1234`
- **Supervisor de Fraude**: `supervisor` / `super123`

## API de Análisis de Fraude

### Endpoint Principal

**POST** `/api/analyze-fraud`

**Request Body:**
```json
{
  "customer_id": "string",
  "transaction_id": "string",
  "transaction_data": {
    "amount": 15000,
    "timestamp": "2024-01-15T03:30:00Z",
    "location": "string",
    "merchant_category": "string",
    "device_fingerprint": "string",
    "ip_address": "string"
  }
}
```

**Response:**
```json
{
  "transaction_id": "TXN_123456",
  "risk_score": 0.85,
  "decision": "BLOCK",
  "confidence": 0.92,
  "agent_analysis": {
    "purchase_history": {
      "score": 0.8,
      "factors": ["unusual_amount", "frequency_anomaly"]
    },
    "blacklist": {
      "score": 0.9,
      "factors": ["device_compromised"]
    },
    "demographics": {
      "score": 0.7,
      "factors": ["profile_mismatch"]
    },
    "temporal": {
      "score": 0.85,
      "factors": ["unusual_hour", "high_velocity"]
    },
    "geolocation": {
      "score": 0.95,
      "factors": ["impossible_travel", "high_risk_zone"]
    }
  },
  "recommended_actions": [
    "Block transaction immediately",
    "Flag customer for manual review",
    "Notify security team"
  ]
}
```

## Configuración Avanzada

### Variables de Entorno

```bash
# Base de Datos y Cache
DATABASE_URL=postgresql://fraud_user:secure_pass@localhost:5432/fraud_detection
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://fraud_user:secure_pass@localhost:5672/fraud_vhost

# Seguridad
JWT_SECRET=your-ultra-secure-jwt-secret-key-256-bits
ENCRYPTION_KEY=your-aes-256-encryption-key

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
AWS_S3_ENDPOINT=https://s3.us-east-1.amazonaws.com

# S3 Buckets por Agente Especialista
S3_BUCKET_PURCHASE_HISTORY=fraud-detection-purchase-history
S3_BUCKET_CLAIMS=fraud-detection-claims-disputes
S3_BUCKET_DEMOGRAPHICS=fraud-detection-demographics
S3_BUCKET_BLACKLISTS=fraud-detection-blacklists
S3_BUCKET_GEOLOCATION=fraud-detection-geolocation
S3_BUCKET_DEVICES=fraud-detection-device-fingerprints

# Configuración de Agentes
AGENT_COORDINATOR_PORT=8003
AGENT_PURCHASE_HISTORY_PORT=8006
AGENT_BLACKLIST_PORT=8007
AGENT_DEMOGRAPHICS_PORT=8008
AGENT_TEMPORAL_PORT=8009
AGENT_GEOLOCATION_PORT=8010
```

### Umbrales de Riesgo

```bash
# Configuración de Scoring
RISK_THRESHOLD_LOW=0.3
RISK_THRESHOLD_MEDIUM=0.6
RISK_THRESHOLD_HIGH=0.8

# Pesos por Agente
WEIGHT_PURCHASE_HISTORY=0.25
WEIGHT_BLACKLIST=0.30
WEIGHT_DEMOGRAPHICS=0.15
WEIGHT_TEMPORAL=0.15
WEIGHT_GEOLOCATION=0.15
```

## Monitoreo y Observabilidad

### Métricas Clave

**📈 KPIs de Rendimiento:**
- Tasa de detección de fraude (True Positive Rate)
- Tasa de falsos positivos (False Positive Rate)
- Tiempo promedio de respuesta por análisis
- Throughput de transacciones procesadas
- Disponibilidad del sistema (SLA 99.9%)

**🔍 Alertas Automáticas:**
- Picos anómalos en volumen de transacciones
- Degradación en tiempo de respuesta de agentes
- Fallos en conectividad con buckets S3
- Umbrales críticos de memoria/CPU

### Dashboards de Monitoreo

**Grafana Dashboards:**
- Panel ejecutivo con métricas de negocio
- Monitoreo técnico de infraestructura
- Análisis de tendencias de fraude
- Performance de agentes individuales

## Estructura del Proyecto

```
hackaton-genai/
├── agents/
│   ├── coordinator/              # Agente coordinador principal
│   ├── purchase-history/         # Agente de historial de compras
│   ├── blacklist/               # Agente de listas negras
│   ├── demographics/            # Agente sociodemográfico
│   ├── temporal/                # Agente de análisis temporal
│   └── geolocation/             # Agente de geolocalización
├── services/
│   ├── api-gateway/             # Gateway principal de API
│   ├── data-collector/          # Recolector de datos S3
│   ├── pattern-analyzer/        # Motor de análisis
│   ├── user-service/            # Gestión de usuarios
│   ├── notification-service/    # Sistema de notificaciones
│   └── web-frontend/            # Aplicación React
├── infrastructure/
│   ├── docker-compose.yml       # Orquestación de servicios
│   ├── kubernetes/              # Manifiestos K8s
│   └── terraform/               # Infraestructura como código
├── data/
│   ├── sample-datasets/         # Datos de prueba
│   └── ml-models/               # Modelos entrenados
├── docs/
│   ├── api/                     # Documentación de API
│   ├── architecture/            # Diagramas de arquitectura
│   └── deployment/              # Guías de despliegue
└── scripts/
    ├── setup.sh                 # Script de configuración inicial
    ├── deploy.sh                # Script de despliegue
    └── test-suite.sh            # Suite de pruebas
```

## Casos de Uso Avanzados

### Escenarios de Fraude Detectados

**💳 Fraude de Tarjeta de Crédito:**
- Transacciones con montos inusuales
- Uso de tarjetas reportadas como robadas
- Patrones de compra inconsistentes con el perfil

**📱 Fraude de Identidad:**
- Creación de cuentas con datos falsos
- Uso de dispositivos comprometidos
- Patrones de comportamiento sintético

**🌍 Fraude Geográfico:**
- Transacciones desde ubicaciones imposibles
- Uso simultáneo en múltiples países
- Actividad en zonas de alto riesgo

**⏰ Fraude Temporal:**
- Ráfagas de transacciones sospechosas
- Actividad en horarios inusuales
- Patrones de velocidad anómala

## Seguridad y Cumplimiento

### Medidas de Seguridad

**🔒 Protección de Datos:**
- Encriptación AES-256 para datos en reposo
- TLS 1.3 para datos en tránsito
- Tokenización de información sensible
- Anonimización de datos personales

**🛡️ Control de Acceso:**
- Autenticación multifactor (MFA)
- Control de acceso basado en roles (RBAC)
- Auditoría completa de accesos
- Rotación automática de credenciales

### Cumplimiento Regulatorio

**📋 Estándares Soportados:**
- PCI DSS Level 1 compliance
- GDPR para protección de datos
- SOX para controles financieros
- ISO 27001 para seguridad de información

## Soporte y Mantenimiento

### Comandos Útiles

**🔧 Operaciones Diarias:**
```bash
# Verificar estado del sistema
./scripts/health-check.sh

# Reiniciar agentes específicos
docker-compose restart agent-coordinator

# Ver logs en tiempo real
docker-compose logs -f --tail=100

# Backup de configuración
./scripts/backup-config.sh
```

**📊 Análisis y Debugging:**
```bash
# Generar reporte de performance
./scripts/performance-report.sh

# Analizar logs de errores
./scripts/analyze-errors.sh

# Ejecutar suite de pruebas
./scripts/test-suite.sh --full
```

### Contacto y Soporte

**📞 Canales de Soporte:**
- **Soporte Técnico**: support@fraud-detection.com
- **Documentación**: https://docs.fraud-detection.com
- **Issues GitHub**: https://github.com/org/fraud-detection/issues
- **Slack Community**: #fraud-detection-support

---

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Ver archivo `LICENSE` para más detalles.

## Contribución

Las contribuciones son bienvenidas. Por favor, lee `CONTRIBUTING.md` para conocer nuestras pautas de contribución y proceso de pull requests.

---

**Desarrollado con ❤️ por el Equipo de Inteligencia Artificial**