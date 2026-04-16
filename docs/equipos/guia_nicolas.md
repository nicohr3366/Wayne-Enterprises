# Guía - Sistema ETL de Contratos de Defensa

> **Dataset:** #2 - Contratos de Defensa Nacional  
> **Descripción:** Licitaciones con el gobierno de EE. UU. Transformación de formatos XML/JSON gubernamentales.

---

## ¿Qué es este Dataset?

Sistema **ETL para contratos gubernamentales** que procesa:

- **Licitaciones públicas** del Departamento de Defensa
- **Contratos de suministro** militar y tecnológico
- **Transformación de formatos** XML gubernamentales a JSON
- **Análisis de contratistas** y montos

**Ejemplo real:** Como el sistema SAM.gov que rastrea contratos federales.

---

## Estructura del Sistema

```
defense_contracts/
├── data/
│   ├── raw/                    # Datos originales
│   │   ├── contratos.xml       # XML del gobierno
│   │   └── licitaciones.json   # JSON de licitaciones
│   └── processed/              # Datos procesados
│       ├── contratos_parseados.json
│       ├── analisis_contratos.json
│       ├── licitaciones_transformadas.json
│       └── oportunidades_wayne.json
├── scripts/
│   ├── xml_parser.py           # Parsear XML
│   ├── json_transformer.py     # Transformar JSON
│   ├── generate_report.py        # Generar HTML
│   └── run_pipeline.py           # Ejecutar pipeline
└── output/
    └── dashboard.html            # Reporte visual
```

---

## Ejecución

```bash
# Ejecutar pipeline completo
cd defense_contracts/scripts
python run_pipeline.py

# O ejecutar pasos individuales
python xml_parser.py
python json_transformer.py
python generate_report.py
```

---

## Salida del Sistema

| Archivo | Descripción |
|---------|-------------|
| `contratos_parseados.json` | 5 contratos parseados del XML |
| `analisis_contratos.json` | Análisis por división y clasificación |
| `licitaciones_transformadas.json` | 3 licitaciones con datos enriquecidos |
| `oportunidades_wayne.json` | Oportunidades identificadas para Wayne |
| `dashboard.html` | Reporte visual interactivo |

---

## Componentes del Pipeline

### 1. xml_parser.py
- Parsea XML de contratos del DoD
- Extrae: ID, agencia, división, contratista, monto, fechas, clasificación
- Genera análisis por división (Fuerza Aérea, Marina, Ejército, DARPA, NSA)
- Análisis por clasificación (Confidencial, Secreto, Alto Secreto)

### 2. json_transformer.py
- Carga licitaciones desde JSON
- Calcula días restantes y urgencia
- Identifica participación de Wayne Enterprises
- Categoriza por tipo (Energía, Tecnología, Transporte, etc.)

### 3. generate_report.py
- Genera dashboard HTML profesional
- Tablas de contratos y licitaciones
- Estadísticas visuales
- Diseño oscuro corporativo

### 4. run_pipeline.py
- Orquesta los 3 scripts anteriores
- Maneja errores y reporta progreso
- Un solo comando para todo el flujo

---

## Datos de Ejemplo

### Contratos XML (5 registros)
- DOD-2024-001: Sistemas de Comunicación Cifrada ($45M)
- DOD-2024-002: Drones de Vigilancia Naval ($78M)
- DOD-2024-003: Blindados Tácticos ($120M)
- DOD-2024-004: Investigación en Exoesqueletos ($25M)
- DOD-2024-005: Ciberseguridad Crítica ($95M)

**Total:** $363,000,000 en contratos

### Licitaciones JSON (3 registros)
- RFP-2024-001: Suministro de Energía ($150M)
- RFP-2024-002: Sistemas de IA ($85M)
- RFP-2024-003: Vehículos Eléctricos ($45M)

**Total:** $280,000,000 en oportunidades

---

## Integración con Portal Django (Opcional)

```python
# core/views.py
from django.shortcuts import render
import json

@login_required
def defense_contracts(request):
    with open('defense_contracts/data/processed/contratos_parseados.json') as f:
        contratos = json.load(f)
    return render(request, 'core/defense.html', {'contratos': contratos})
```

---

## Checklist

- [x] Estructura de carpetas creada
- [x] Archivo XML con 5+ contratos
- [x] Archivo JSON con 3+ licitaciones
- [x] `xml_parser.py` funciona
- [x] `json_transformer.py` funciona
- [x] `generate_report.py` crea HTML
- [x] `run_pipeline.py` ejecuta todo
- [x] Dashboard HTML se ve correctamente

---

## Contacto

¿Preguntas? Revisa las guías de tus compañeros en `/docs/`
