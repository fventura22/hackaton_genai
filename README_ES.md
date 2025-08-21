# Sistema de Detección de Fraude para Telecomunicaciones

Un sistema integral de detección de fraude construido con arquitectura de microservicios, que incluye agentes de IA para análisis automatizado de fraude y una aplicación web React para analistas de fraude.

## Descripción General de la Arquitectura

### Microservicios
- **API Gateway** (Puerto 8000) - Punto de entrada central y orquestación de solicitudes
- **Agente de Detección de Fraude** (Puerto 8003) - Agente de IA principal para toma de decisiones
- **Servicio de Recolección de Datos** (Puerto 8001) - Obtiene datos de múltiples fuentes
- **Servicio de Análisis de Patrones** (Puerto 8002) - Analiza patrones de fraude
- **Servicio de Gestión de Usuarios** (Puerto 8004) - Autenticación y autorización
- **Servicio de Notificaciones** (Puerto 8005) - Alertas y notificaciones

### Infraestructura
- **PostgreSQL** - Base de datos principal
- **Redis** - Caché y gestión de sesiones
- **RabbitMQ** - Cola de mensajes para comunicación entre servicios

### Frontend
- **Aplicación Web React** - Interfaz web responsiva para analistas de fraude (funciona en PC y móvil)

## Características

### Detección de Fraude con IA
- Recolección de datos de múltiples fuentes (perfiles de clientes, historial de transacciones, información de dispositivos, APIs externas)
- Análisis de patrones basado en conocimientos del equipo de fraude
- Puntuación de riesgo con niveles de confianza
- Toma de decisiones automatizada con supervisión humana
- Alertas de fraude en tiempo real

### Aplicación Web
- Diseño responsivo (funciona en PC y móvil)
- Autenticación segura
- Panel de control en tiempo real con estadísticas de fraude
- Gráficos interactivos y visualizaciones
- Interfaz de análisis de transacciones
- Vistas detalladas de investigación de fraude
- Acciones de Aprobar/Bloquear/Revisar

### Capacidades de Detección de Fraude
- **Análisis de Montos**: Detecta montos de transacción inusuales
- **Análisis Temporal**: Identifica patrones de tiempo sospechosos
- **Análisis de Ubicación**: Marca transacciones desde ubicaciones inusuales
- **Análisis de Velocidad**: Detecta secuencias rápidas de transacciones
- **Análisis de Dispositivos**: Analiza huellas digitales y comportamiento de dispositivos
- **Coincidencia de Patrones**: Identifica patrones de fraude conocidos

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
1. **Monto Alto**: Transacciones superiores a $10,000 o 3 veces el promedio del cliente
2. **Tiempo Inusual**: Transacciones durante 12 AM - 6 AM
3. **Ubicación Sospechosa**: Ubicaciones desconocidas o de alto riesgo
4. **Alta Velocidad**: Más de 5 transacciones por hora
5. **Riesgo de Dispositivo**: Puntuaciones altas de riesgo de dispositivo (>0.7)

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