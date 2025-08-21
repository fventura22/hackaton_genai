# Sistema de Detección de Fraude para Telecomunicaciones

Un sistema integral de detección de fraude construido con arquitectura de microservicios, que incluye agentes de IA para análisis automatizado de fraude y una aplicación web React para analistas de fraude.

## Descripción General de la Arquitectura

### Sistema Multiagéntico de IA
- **Agente Principal Coordinador** (Puerto 8003) - Orquesta y toma decisiones finales basadas en análisis de agentes especialistas
- **Agente Especialista en Historial de Reclamos** (Puerto 8006) - Analiza patrones de comportamiento de reclamos
- **Agente Especialista en Historial de Compras** (Puerto 8006) - Analiza patrones de comportamiento de compra y transacciones históricas
- **Agente Especialista en Black List** (Puerto 8007) - Verifica contra listas negras de clientes, dispositivos y ubicaciones sospechosas
- **Agente Especialista en Datos Sociodemográficos** (Puerto 8008) - Analiza perfiles demográficos y comportamientos asociados


### Microservicios de Soporte
- **API Gateway** (Puerto 8000) - Punto de entrada central y orquestación de solicitudes
- **Servicio de Recolección de Datos** (Puerto 8001) - Obtiene datos de múltiples fuentes para alimentar agentes
- **Servicio de Análisis de Patrones** (Puerto 8002) - Consolida análisis de todos los agentes especialistas
- **Servicio de Gestión de Usuarios** (Puerto 8004) - Autenticación y autorización
- **Servicio de Notificaciones** (Puerto 8005) - Alertas y notificaciones

### Fuentes de Datos en AWS S3
- **Historial de Compras** - Datos históricos de transacciones y patrones de compra almacenados en S3
- **Reclamos y Disputas** - Registros de reclamos, chargebacks y disputas de clientes en S3
- **Datos Sociodemográficos** - Perfiles demográficos y segmentación de clientes en S3
- **Black Lists** - Listas negras de clientes, dispositivos y ubicaciones sospechosas en S3

### Infraestructura
- **AWS S3** - Almacenamiento de datos históricos y fuentes de información para agentes
- **PostgreSQL** - Base de datos principal para datos operacionales
- **Redis** - Caché y gestión de sesiones
- **RabbitMQ** - Cola de mensajes para comunicación entre servicios

### Frontend
- **Aplicación Web React** - Interfaz web responsiva para analistas de fraude (funciona en PC y móvil)

## Características

### Detección de Fraude con Sistema Multiagéntico
- **Agente Principal**: Coordina análisis de todos los agentes especialistas y toma decisión final
- **Agente de Historial de Compras**: Extrae datos de S3 (transacciones históricas) y analiza patrones de comportamiento de compra, frecuencia, montos típicos y desviaciones
- **Agente de Analisis de reclamos**: Extrae datos de S3 (transacciones históricas) y analiza patrones de comportamiento de reclamos, frecuencia
- **Agente de Black List**: Consulta listas negras almacenadas en S3 para verificar clientes fraudulentos, dispositivos comprometidos y ubicaciones de riesgo
- **Agente Sociodemográfico**: Accede a datos demográficos en S3 para analizar edad, ubicación, ingresos, comportamiento típico por segmento

### Aplicación Web
- Diseño responsivo (funciona en PC y móvil)
- Autenticación segura
- Panel de control en tiempo real con estadísticas de fraude
- Gráficos interactivos y visualizaciones
- Interfaz de análisis de transacciones
- Vistas detalladas de investigación de fraude
- Acciones de Aprobar/Bloquear/Revisar

### Capacidades de Detección por Agente Especialista
- **Agente de Historial de Compras**: Detecta montos inusuales vs. historial, cambios en patrones de compra, frecuencia anómala
- **Agente de Historial de Reclamos**: Detecta los reclamos similares del mismo productos o servicios
- **Agente de Black List**: Verifica identidades, números de tarjeta, dispositivos y IPs en listas negras
- **Agente Sociodemográfico**: Analiza coherencia entre perfil demográfico y comportamiento de compra

## Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose
- Node.js 16+ (para desarrollo de la aplicación web)

### 1. Iniciar Servicios Backend
```bash
# Clonar y navegar al proyecto
cd hackaton-genai

# Iniciar todos los servicios
docker-compose up -d

# Verificar estado de servicios
curl http://localhost:8000/api/health
```

### 2. Acceder a la Aplicación Web
```bash
# La aplicación web estará disponible en:
http://localhost:3000

# Para desarrollo (opcional):
cd services/web-frontend
npm install
npm start
```

### 3. Probar el Sistema
```bash
# Probar endpoint de análisis de fraude
curl -X POST http://localhost:8000/api/analyze-fraud \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST001",
    "transaction_id": "TXN123",
    "transaction_data": {
      "amount": 5000,
      "timestamp": "2024-01-15T02:30:00Z",
      "location": "Unknown",
      "merchant_category": "online_gaming"
    }
  }'
```

## Credenciales de Demostración

### Inicio de Sesión en Aplicación Web
- **Analista de Fraude**: `fraud_analyst` / `analyst123`
- **Administrador**: `admin` / `1234`

## Documentación de API

### Endpoints Principales

#### Analizar Fraude
```
POST /api/analyze-fraud
Content-Type: application/json

{
  "customer_id": "string",
  "transaction_id": "string", 
  "transaction_data": {
    "amount": number,
    "timestamp": "string",
    "location": "string",
    "merchant_category": "string"
  }
}
```

#### Respuesta
```json
{
  "is_fraud": boolean,
  "confidence_score": number,
  "risk_factors": ["string"],
  "recommendation": "string"
}
```

## Lógica de Detección de Fraude

### Factores de Riesgo
1. **Monto Alto**: Transacciones superiores a $1.200,000 o 3 veces el promedio del cliente
2. **Tiempo Inusual**: Transacciones durante 12 AM - 6 AM
3. **Ubicación Sospechosa**: Ubicaciones desconocidas o de alto riesgo
4. **Alta Velocidad**: Más de 5 transacciones por hora
5. **Riesgo del Segmento**: Si es prepago es más alto que pospago

### Umbrales de Decisión
- **Bloquear** (>80%): Alto riesgo de fraude - bloqueo automático
- **Revisar** (50-80%): Riesgo medio - revisión manual requerida
- **Aprobar** (<50%): Bajo riesgo - permitir transacción

## Monitoreo y Alertas

### Monitoreo en Tiempo Real
- Volumen de transacciones y tasas de fraude
- Métricas de salud y rendimiento del sistema
- Notificaciones de alerta vía email/SMS

### Integración con Equipo de Fraude
- Actualizaciones de patrones del análisis del equipo de fraude
- Umbrales de riesgo configurables
- Análisis de datos históricos de fraude

## Despliegue

### Despliegue en Producción
1. Configurar variables de entorno
2. Configurar certificados SSL
3. Configurar fuentes de datos externas
4. Configurar monitoreo y logging
5. Desplegar con Docker Compose o Kubernetes

### Variables de Entorno
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
RABBITMQ_URL=amqp://user:pass@host:5672
JWT_SECRET=your-secret-key

# Configuración AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_STORE=fraud-detection-history

```

## Características de Seguridad

- Autenticación basada en JWT
- Control de acceso basado en roles
- Transmisión de datos encriptada
- Endpoints de API seguros
- Validación y sanitización de entrada

## Estructura del Proyecto

```
hackaton-genai/
├── services/
│   ├── api-gateway/          # Gateway principal de API
│   ├── fraud-agent/          # Agente de detección de fraude
│   ├── data-collector/       # Recolector de datos
│   ├── pattern-analyzer/     # Analizador de patrones
│   ├── user-service/         # Gestión de usuarios
│   ├── notification-service/ # Servicio de notificaciones
│   └── web-frontend/         # Aplicación web React
├── docker-compose.yml        # Configuración de servicios
├── start.sh                  # Script de inicio
├── test-api.sh              # Script de pruebas
└── README.md                # Documentación
```

## Uso del Sistema

### Panel de Control
- Visualización de estadísticas de fraude en tiempo real
- Gráficos interactivos de tendencias
- Lista de alertas recientes
- Acciones rápidas para análisis

### Análisis de Transacciones
- Formulario de entrada de datos de transacción
- Análisis en tiempo real con puntuación de riesgo
- Factores de riesgo detallados
- Recomendaciones de acción

### Gestión de Casos
- Vista detallada de transacciones sospechosas
- Historial del cliente y patrones
- Herramientas de decisión (Aprobar/Bloquear/Revisar)
- Seguimiento de casos

## Solución de Problemas

### Problemas Comunes

#### Los servicios no responden
```bash
# Verificar estado de contenedores
docker-compose ps

# Reiniciar servicios
docker-compose restart

# Ver logs de servicios
docker-compose logs [service-name]
```

#### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker-compose logs postgres

# Reiniciar base de datos
docker-compose restart postgres
```

#### Problemas de CORS en aplicación web
- Verificar que el servicio de usuarios tenga configurado CORS
- Confirmar que las URLs de API sean correctas
- Revisar configuración de proxy en nginx

## Contribución

1. Hacer fork del repositorio
2. Crear rama de característica
3. Implementar cambios con pruebas
4. Enviar pull request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## Soporte

Para soporte técnico o preguntas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Consultar la documentación wiki

## Comandos Útiles

### Desarrollo
```bash
# Iniciar sistema completo
./start.sh

# Probar APIs
./test-api.sh

# Ver logs en tiempo real
docker-compose logs -f

# Reconstruir servicios
docker-compose up -d --build
```

### Mantenimiento
```bash
# Detener todos los servicios
docker-compose down

# Limpiar volúmenes
docker-compose down -v

# Actualizar imágenes
docker-compose pull
```