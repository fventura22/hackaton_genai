# Análisis del Dataset - Base.csv

## 📊 Estadísticas Generales

- **Total de registros**: 52,690
- **Separador CSV**: Punto y coma (`;`)
- **Columnas**: 20 campos
- **Tamaño**: Aproximadamente 8.5 MB

## 🚨 Análisis de Fraude (CODIGO_RAZON_CONTRACARGO)

### Distribución de Códigos:
- **Código 0** (Sin fraude): 52,657 registros (99.94%)
- **Código 83** (Fraude): 33 registros (0.06%)

### Blacklist Real:
- **Clientes únicos en blacklist**: 30
- **Registros fraudulentos totales**: 33
- **Algunos clientes tienen múltiples fraudes**

### Ejemplos de Clientes en Blacklist:
1. Cliente 6291: 3 registros fraudulentos
2. Cliente 9034: 1 registro fraudulento
3. Cliente 8776: 1 registro fraudulento
4. Cliente 6351: 1 registro fraudulento
5. Cliente 5258: 1 registro fraudulento

## 💰 Análisis de Importes Fraudulentos

### Estadísticas:
- **Promedio**: $358,698.94
- **Mediana**: $283,998.99
- **Mínimo**: $23,999.01
- **Máximo**: $1,799,999.00

### Rango de Alta Probabilidad (±10% del promedio):
- **Límite inferior**: $322,829.05
- **Límite superior**: $394,568.84
- **Rango**: $35,869.89

## 🎯 Implicaciones para el Sistema

### 1. Blacklist (Peso: 50%)
- Solo 30 clientes → Probabilidad 1.0 automática
- Muy selectiva pero efectiva

### 2. Análisis de Fraude por Monto (Peso: 30%)
- Promedio alto ($358K) → Detecta transacciones grandes
- Rango ±10% muy específico

### 3. Análisis por Segmento (Peso: 20%)
- Basado en CANT_PREPAGOS/CANT_POSPAGOS
- Complementa otros análisis

## ⚠️ Consideraciones

1. **Dataset desbalanceado**: Solo 0.06% de fraudes
2. **Fraudes de alto valor**: Promedio $358K vs general
3. **Blacklist pequeña pero precisa**: 30 clientes conocidos
4. **Sistema conservador**: Pocos falsos positivos esperados

## 🔧 Configuración Óptima

El sistema está calibrado para:
- **Bloquear automáticamente** clientes en blacklist
- **Detectar transacciones** cercanas al patrón fraudulento ($358K)
- **Considerar segmento** como factor complementario
- **Minimizar falsos positivos** dado el bajo % de fraude real