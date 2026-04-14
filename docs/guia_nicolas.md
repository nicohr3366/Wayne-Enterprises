# Guía Individual: Nicolás - Dataset #2

> **Responsable:** Nicolás  
> **ID:** #2  
> **Dataset:** Contratos de Defensa Nacional  
> **Descripción:** Licitaciones con el gobierno de EE. UU. Transformación de formatos XML/JSON gubernamentales.  
> **Rama Git:** `nicolas`  

---

## ¿Qué es tu Dataset?

Tu trabajo es crear un **sistema ETL para contratos gubernamentales** que procese:

- **Licitaciones públicas** del Departamento de Defensa
- **Contratos de suministro** militar y tecnológico
- **Transformación de formatos** XML gubernamentales a JSON
- **Análisis de contratistas** y montos

**Ejemplo real:** Como el sistema SAM.gov que rastrea contratos federales.

---

## Paso a Paso: Crear tu Sistema ETL

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p nicolas_defense/{data/{raw,processed},scripts,output}
cd nicolas_defense

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
nicolas_defense/
├── data/
│   ├── raw/
│   │   ├── contratos.xml      # XML del gobierno
│   │   └── licitaciones.json # JSON de licitaciones
│   └── processed/
│       └── contratos_unificados.json
├── scripts/
│   ├── xml_parser.py        # Parsear XML
│   ├── json_transformer.py  # Transformar JSON
│   └── merger.py            # Unir todo
└── output/
    ├── reporte_contratos.json
    └── dashboard.html
```

---

### Paso 2: Datos XML de Ejemplo

**`data/raw/contratos.xml`:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ContratosDefensa>
    <Contrato id="DOD-2024-001">
        <Agencia>Departamento de Defensa</Agencia>
        <División>Fuerza Aérea</División>
        <Titulo>Sistemas de Comunicación Cifrada</Titulo>
        <Contratista>Wayne Technologies</Contratista>
        <Monto>45000000.00</Monto>
        <Moneda>USD</Moneda>
        <FechaInicio>2024-01-15</FechaInicio>
        <FechaFin>2026-01-14</FechaFin>
        <Estado>Activo</Estado>
        <Clasificacion>Confidencial</Clasificacion>
        <Ubicacion>Gotham, EE.UU.</Ubicacion>
    </Contrato>
    
    <Contrato id="DOD-2024-002">
        <Agencia>Departamento de Defensa</Agencia>
        <División>Marina</División>
        <Titulo>Drones de Vigilancia Naval</Titulo>
        <Contratista>Wayne Industries</Contratista>
        <Monto>78000000.00</Monto>
        <Moneda>USD</Moneda>
        <FechaInicio>2024-03-01</FechaInicio>
        <FechaFin>2025-12-31</FechaFin>
        <Estado>Activo</Estado>
        <Clasificacion>Secreto</Clasificacion>
        <Ubicacion>Puerto Gotham, EE.UU.</Ubicacion>
    </Contrato>
    
    <Contrato id="DOD-2024-003">
        <Agencia>Departamento de Defensa</Agencia>
        <División>Ejército</División>
        <Titulo>Blindados Tácticos</Titulo>
        <Contratista>Wayne Heavy Industries</Contratista>
        <Monto>120000000.00</Monto>
        <Moneda>USD</Moneda>
        <FechaInicio>2023-06-15</FechaInicio>
        <FechaFin>2025-06-14</FechaFin>
        <Estado>En Ejecución</Estado>
        <Clasificacion>Confidencial</Clasificacion>
        <Ubicacion>Gotham, EE.UU.</Ubicacion>
    </Contrato>
    
    <Contrato id="DOD-2024-004">
        <Agencia>Departamento de Defensa</Agencia>
        <División>DARPA</División>
        <Titulo>Investigación en Exoesqueletos</Titulo>
        <Contratista>Wayne Advanced Research</Contratista>
        <Monto>25000000.00</Monto>
        <Moneda>USD</Moneda>
        <FechaInicio>2024-02-01</FechaInicio>
        <FechaFin>2027-01-31</FechaFin>
        <Estado>Activo</Estado>
        <Clasificacion>Alto Secreto</Clasificacion>
        <Ubicacion>Wayne Research Facility</Ubicacion>
    </Contrato>
    
    <Contrato id="DOD-2024-005">
        <Agencia>Departamento de Defensa</Agencia>
        <División>NSA</División>
        <Titulo>Ciberseguridad Crítica</Titulo>
        <Contratista>Wayne Cyber Defense</Contratista>
        <Monto>95000000.00</Monto>
        <Moneda>USD</Moneda>
        <FechaInicio>2023-09-01</FechaInicio>
        <FechaFin>2028-08-31</FechaFin>
        <Estado>Activo</Estado>
        <Clasificacion>Alto Secreto</Clasificacion>
        <Ubicacion>Classified Location</Ubicacion>
    </Contrato>
</ContratosDefensa>
```

---

### Paso 3: Datos JSON de Licitaciones

**`data/raw/licitaciones.json`:**

```json
{
  "licitaciones": [
    {
      "id": "RFP-2024-001",
      "titulo": "Suministro de Energía para Bases Militares",
      "descripcion": "Contrato para suministro energético renovable en bases militares de la costa este",
      "agencia": "Departamento de Defensa",
      "monto_estimado": 150000000,
      "fecha_publicacion": "2024-01-10",
      "fecha_cierre": "2024-03-15",
      "estado": "Abierta",
      "requisitos": [
        "Certificación ISO 14001",
        "Experiencia mínima 5 años",
        "Capacidad de suministro 500MW"
      ],
      "postores": ["Wayne Energy", "LexCorp Power", "Oscorp Industries"]
    },
    {
      "id": "RFP-2024-002",
      "titulo": "Sistemas de IA para Análisis de Inteligencia",
      "descripcion": "Plataforma de machine learning para procesamiento de datos de inteligencia",
      "agencia": "CIA",
      "monto_estimado": 85000000,
      "fecha_publicacion": "2024-02-01",
      "fecha_cierre": "2024-04-30",
      "estado": "Evaluación",
      "requisitos": [
        "Clearance de seguridad nivel TS/SCI",
        "Certificación CMMI nivel 3",
        "Personal con CISSP"
      ],
      "postores": ["Wayne AI Labs", "Stark Intelligence", "LexCorp AI"]
    },
    {
      "id": "RFP-2024-003",
      "titulo": "Vehículos Eléctricos Militares",
      "descripcion": "Flota de 500 vehículos eléctricos para transporte base",
      "agencia": "Departamento de Defensa",
      "monto_estimado": 45000000,
      "fecha_publicacion": "2023-12-01",
      "fecha_cierre": "2024-02-28",
      "estado": "Adjudicada",
      "ganador": "Wayne Automotive",
      "monto_final": 42000000
    }
  ]
}
```

---

### Paso 4: Parser XML

**`scripts/xml_parser.py`:**

```python
"""
Parser de contratos XML del Departamento de Defensa
"""
import xml.etree.ElementTree as ET
import json


def parse_xml_contratos(filepath):
    """
    Parsea archivo XML de contratos y retorna lista de diccionarios
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    contratos = []
    
    for contrato_elem in root.findall('Contrato'):
        contrato = {
            'id': contrato_elem.get('id'),
            'agencia': contrato_elem.find('Agencia').text,
            'division': contrato_elem.find('División').text,
            'titulo': contrato_elem.find('Titulo').text,
            'contratista': contrato_elem.find('Contratista').text,
            'monto': float(contrato_elem.find('Monto').text),
            'moneda': contrato_elem.find('Moneda').text,
            'fecha_inicio': contrato_elem.find('FechaInicio').text,
            'fecha_fin': contrato_elem.find('FechaFin').text,
            'estado': contrato_elem.find('Estado').text,
            'clasificacion': contrato_elem.find('Clasificacion').text,
            'ubicacion': contrato_elem.find('Ubicacion').text
        }
        contratos.append(contrato)
    
    return contratos


def save_to_json(data, filepath):
    """Guarda datos en formato JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Guardados {len(data)} registros en {filepath}")


def analyze_contratos(contratos):
    """Genera análisis de contratos"""
    
    total_monto = sum(c['monto'] for c in contratos)
    
    # Por división
    por_division = {}
    for c in contratos:
        div = c['division']
        if div not in por_division:
            por_division[div] = {'count': 0, 'total': 0}
        por_division[div]['count'] += 1
        por_division[div]['total'] += c['monto']
    
    # Por clasificación
    por_clasificacion = {}
    for c in contratos:
        cla = c['clasificacion']
        if cla not in por_clasificacion:
            por_clasificacion[cla] = {'count': 0, 'total': 0}
        por_clasificacion[cla]['count'] += 1
        por_clasificacion[cla]['total'] += c['monto']
    
    return {
        'total_contratos': len(contratos),
        'monto_total': total_monto,
        'monto_promedio': total_monto / len(contratos) if contratos else 0,
        'por_division': por_division,
        'por_clasificacion': por_clasificacion
    }


if __name__ == "__main__":
    print("=" * 60)
    print("📄 PARSER XML - Contratos de Defensa")
    print("=" * 60)
    
    # Parsear XML
    contratos = parse_xml_contratos('data/raw/contratos.xml')
    
    print(f"\n📊 Contratos parseados: {len(contratos)}")
    
    for c in contratos:
        print(f"\n   📝 {c['id']}")
        print(f"      {c['titulo']}")
        print(f"      Contratista: {c['contratista']}")
        print(f"      Monto: ${c['monto']:,.2f}")
        print(f"      División: {c['division']}")
    
    # Análisis
    analisis = analyze_contratos(contratos)
    
    print(f"\n💰 Resumen Financiero:")
    print(f"   Total contratos: {analisis['total_contratos']}")
    print(f"   Monto total: ${analisis['monto_total']:,.2f}")
    print(f"   Monto promedio: ${analisis['monto_promedio']:,.2f}")
    
    print(f"\n🏛️ Por División:")
    for div, data in analisis['por_division'].items():
        print(f"   {div}: {data['count']} contratos, ${data['total']:,.2f}")
    
    # Guardar como JSON
    save_to_json(contratos, 'data/processed/contratos_parseados.json')
    save_to_json(analisis, 'data/processed/analisis_contratos.json')
```

---

### Paso 5: Transformador JSON

**`scripts/json_transformer.py`:**

```python
"""
Transformador de licitaciones JSON
"""
import json
from datetime import datetime


def load_licitaciones(filepath):
    """Carga archivo JSON de licitaciones"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('licitaciones', [])


def transform_licitaciones(licitaciones):
    """Transforma y enriquece datos de licitaciones"""
    transformadas = []
    
    for lic in licitaciones:
        # Calcular días restantes
        fecha_cierre = datetime.strptime(lic['fecha_cierre'], '%Y-%m-%d')
        hoy = datetime.now()
        dias_restantes = (fecha_cierre - hoy).days
        
        # Determinar urgencia
        if dias_restantes < 0:
            urgencia = 'Cerrada'
        elif dias_restantes <= 7:
            urgencia = 'Crítica'
        elif dias_restantes <= 30:
            urgencia = 'Alta'
        else:
            urgencia = 'Normal'
        
        # Calcular competencia (número de postores)
        num_postores = len(lic.get('postores', []))
        
        transformed = {
            'id': lic['id'],
            'titulo': lic['titulo'],
            'agencia': lic['agencia'],
            'monto_estimado': lic['monto_estimado'],
            'estado': lic['estado'],
            'dias_restantes': dias_restantes,
            'urgencia': urgencia,
            'numero_postores': num_postores,
            'competencia': 'Alta' if num_postores > 2 else 'Media' if num_postores > 1 else 'Baja',
            'wayne_participando': any('Wayne' in p for p in lic.get('postores', [])),
            'requisitos_count': len(lic.get('requisitos', [])),
            'categoria': categorizar_licitacion(lic['titulo'])
        }
        
        transformadas.append(transformed)
    
    return transformadas


def categorizar_licitacion(titulo):
    """Categoriza licitación por palabras clave"""
    titulo_lower = titulo.lower()
    
    if any(word in titulo_lower for word in ['energía', 'power', 'eléctrico']):
        return 'Energía'
    elif any(word in titulo_lower for word in ['ia', 'inteligencia', 'software', 'ciber']):
        return 'Tecnología/Software'
    elif any(word in titulo_lower for word in ['vehículo', 'automotriz', 'transporte']):
        return 'Transporte'
    elif any(word in titulo_lower for word in ['comunicación', 'radio', 'satélite']):
        return 'Comunicaciones'
    else:
        return 'Otros'


def analyze_opportunities(licitaciones):
    """Analiza oportunidades para Wayne"""
    
    oportunidades_wayne = [l for l in licitaciones if l['wayne_participando']]
    abiertas = [l for l in licitaciones if l['estado'] == 'Abierta']
    
    # Por urgencia
    criticas = [l for l in licitaciones if l['urgencia'] == 'Crítica']
    
    return {
        'total_licitaciones': len(licitaciones),
        'wayne_participando': len(oportunidades_wayne),
        'licitaciones_abiertas': len(abiertas),
        'oportunidades_criticas': len(criticas),
        'oportunidades_wayne': oportunidades_wayne,
        'montos_potenciales': sum(l['monto_estimado'] for l in oportunidades_wayne)
    }


def save_transformed(data, filepath):
    """Guarda datos transformados"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Guardado: {filepath}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 TRANSFORMADOR JSON - Licitaciones")
    print("=" * 60)
    
    # Cargar
    licitaciones = load_licitaciones('data/raw/licitaciones.json')
    print(f"\n📥 Licitaciones cargadas: {len(licitaciones)}")
    
    # Transformar
    transformadas = transform_licitaciones(licitaciones)
    
    print(f"\n📊 Datos transformados:")
    for lic in transformadas:
        print(f"\n   🎯 {lic['id']}")
        print(f"      {lic['titulo']}")
        print(f"      Monto: ${lic['monto_estimado']:,.0f}")
        print(f"      Urgencia: {lic['urgencia']} ({lic['dias_restantes']} días)")
        print(f"      Wayne participando: {'Sí' if lic['wayne_participando'] else 'No'}")
    
    # Análisis
    analisis = analyze_opportunities(transformadas)
    
    print(f"\n💡 Oportunidades para Wayne:")
    print(f"   Total licitaciones: {analisis['total_licitaciones']}")
    print(f"   Wayne participando: {analisis['wayne_participando']}")
    print(f"   Abiertas: {analisis['licitaciones_abiertas']}")
    print(f"   Críticas: {analisis['oportunidades_criticas']}")
    print(f"   Monto potencial: ${analisis['montos_potenciales']:,.0f}")
    
    # Guardar
    save_transformed(transformadas, 'data/processed/licitaciones_transformadas.json')
    save_transformed(analisis, 'data/processed/oportunidades_wayne.json')
```

---

### Paso 6: Reporte Final

**`scripts/generate_report.py`:**

```python
"""
Generador de reporte HTML de contratos
"""
import json


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_html_report():
    # Cargar datos procesados
    contratos = load_json('data/processed/contratos_parseados.json')
    analisis_contratos = load_json('data/processed/analisis_contratos.json')
    licitaciones = load_json('data/processed/licitaciones_transformadas.json')
    oportunidades = load_json('data/processed/oportunidades_wayne.json')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Wayne Defense Contracts Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #e94560; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        h2 {{ color: #3498db; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 36px; font-weight: bold; color: white; }}
        .stat-label {{ font-size: 14px; opacity: 0.9; margin-top: 5px; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #16213e; }}
        th {{ background: #e94560; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #333; }}
        tr:hover {{ background: #1f2d4a; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }}
        .confidencial {{ background: #f39c12; color: black; }}
        .secreto {{ background: #e74c3c; color: white; }}
        .alto-secreto {{ background: #2c3e50; color: white; border: 1px solid #e74c3c; }}
        .critica {{ background: #e74c3c; color: white; }}
        .alta {{ background: #f39c12; color: black; }}
        .normal {{ background: #27ae60; color: white; }}
        .wayne-yes {{ color: #27ae60; font-weight: bold; }}
        .wayne-no {{ color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Wayne Defense Contracts Dashboard</h1>
        <p>Departamento de Defensa de EE.UU. - Licitaciones y Contratos</p>
        
        <h2>📊 Resumen General</h2>
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{analisis_contratos['total_contratos']}</div>
                <div class="stat-label">Contratos Activos</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analisis_contratos['monto_total']/1e9:.2f}B</div>
                <div class="stat-label">Valor Total</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${analisis_contratos['monto_promedio']/1e6:.1f}M</div>
                <div class="stat-label">Promedio por Contrato</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{oportunidades['total_licitaciones']}</div>
                <div class="stat-label">Licitaciones Totales</div>
            </div>
        </div>
        
        <h2>📋 Contratos Vigentes</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>División</th>
                <th>Contratista</th>
                <th>Monto</th>
                <th>Clasificación</th>
                <th>Estado</th>
            </tr>
"""
    
    for c in contratos:
        badge_class = c['clasificacion'].lower().replace(' ', '-')
        html += f"""
            <tr>
                <td>{c['id']}</td>
                <td>{c['titulo']}</td>
                <td>{c['division']}</td>
                <td>{c['contratista']}</td>
                <td>${c['monto']:,.0f}</td>
                <td><span class="badge {badge_class}">{c['clasificacion']}</span></td>
                <td>{c['estado']}</td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>🎯 Oportunidades de Licitación</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Agencia</th>
                <th>Monto Estimado</th>
                <th>Estado</th>
                <th>Urgencia</th>
                <th>Wayne</th>
            </tr>
"""
    
    for lic in licitaciones:
        urgencia_class = lic['urgencia'].lower()
        wayne_class = 'wayne-yes' if lic['wayne_participando'] else 'wayne-no'
        wayne_text = '✓ Participando' if lic['wayne_participando'] else '✗ No participa'
        
        html += f"""
            <tr>
                <td>{lic['id']}</td>
                <td>{lic['titulo']}</td>
                <td>{lic['agencia']}</td>
                <td>${lic['monto_estimado']:,.0f}</td>
                <td>{lic['estado']}</td>
                <td><span class="badge {urgencia_class}">{lic['urgencia']}</span></td>
                <td class="{wayne_class}">{wayne_text}</td>
            </tr>
"""
    
    html += """
        </table>
        
        <div style="margin-top: 40px; padding: 20px; background: #16213e; border-radius: 10px;">
            <h3>📈 Análisis por División</h3>
            <ul style="line-height: 2;">
"""
    
    for div, data in analisis_contratos['por_division'].items():
        html += f"<li><strong>{div}</strong>: {data['count']} contratos, ${data['total']:,.0f}</li>"
    
    html += """
            </ul>
        </div>
        
        <p style="margin-top: 40px; color: #7f8c8d; font-size: 12px; text-align: center;">
            Reporte generado automáticamente - Wayne Enterprises Defense Division
        </p>
    </div>
</body>
</html>
"""
    
    with open('output/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Reporte HTML generado: output/dashboard.html")


if __name__ == "__main__":
    generate_html_report()
```

---

### Paso 7: Pipeline Completo

**`scripts/run_pipeline.py`:**

```python
"""
Pipeline completo de procesamiento de contratos
"""
import subprocess
import sys


def run_step(name, command):
    """Ejecuta un paso del pipeline"""
    print(f"\n{'='*60}")
    print(f"🚀 Ejecutando: {name}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=False)
    
    if result.returncode != 0:
        print(f"❌ Error en: {name}")
        sys.exit(1)
    
    print(f"✅ Completado: {name}")


def main():
    print("=" * 60)
    print("🛡️ WAYNE DEFENSE - Pipeline ETL Completo")
    print("=" * 60)
    
    steps = [
        ("Parsear XML de Contratos", "cd scripts && python xml_parser.py"),
        ("Transformar JSON de Licitaciones", "cd scripts && python json_transformer.py"),
        ("Generar Reporte HTML", "cd scripts && python generate_report.py")
    ]
    
    for name, command in steps:
        run_step(name, command)
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("\n📁 Archivos generados:")
    print("   • data/processed/contratos_parseados.json")
    print("   • data/processed/licitaciones_transformadas.json")
    print("   • output/dashboard.html")
    print("\n🌎 Abre output/dashboard.html en tu navegador")


if __name__ == "__main__":
    main()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout nicolas

# Agregar archivos
git add nicolas_defense/
git commit -m "feat: agrega sistema ETL para contratos de defensa"
git push origin nicolas
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Archivo XML con 5+ contratos
- [ ] Archivo JSON con 3+ licitaciones
- [ ] `xml_parser.py` funciona
- [ ] `json_transformer.py` funciona
- [ ] `generate_report.py` crea HTML
- [ ] `run_pipeline.py` ejecuta todo
- [ ] Dashboard HTML se ve correctamente
- [ ] Subir a GitHub

---

## Integración

Puedes vincular tu sistema al portal Django:

```python
# core/views.py - Agregar vista de contratos
from django.shortcuts import render
import json

@login_required
def defense_contracts(request):
    with open('nicolas_defense/data/processed/contratos_parseados.json') as f:
        contratos = json.load(f)
    return render(request, 'core/defense.html', {'contratos': contratos})
```

---

## Contacto

Eres el coordinador del proyecto. Esta guía es para tu propio trabajo de dataset.

¿Preguntas? Revisa las guías de tus compañeros en `/docs/`
