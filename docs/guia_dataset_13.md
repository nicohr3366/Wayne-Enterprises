# Guía Individual: Dataset #13 - Adquisiciones de Startups Tech

> **Responsable:** *Por asignar*  
> **ID:** #13  
> **Dataset:** Adquisiciones de Startups Tech  
> **Descripción:** Historial de compras de empresas pequeñas. Fusión de bases de datos heterogéneas.  
> **Rama Git:** `dataset_13`  

---

## ¿Qué es este Dataset?

Tu trabajo es crear un **sistema ETL para fusionar datos de adquisiciones** de Wayne Enterprises. Debes procesar:

- **Historial de compras** de startups por parte de Wayne
- **Fusión de múltiples fuentes** de datos (CSV, JSON, Excel)
- **Análisis de tendencias** de adquisiciones
- **Valoración de empresas** compradas

**Ejemplo real:** Como Crunchbase o PitchBook, pero para el ecosistema Wayne.

---

## Paso a Paso: Crear tu Sistema ETL de Fusión

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p dataset_13_acquisitions/{data/{sources,merged},scripts,reports}
cd dataset_13_acquisitions

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
dataset_13_acquisitions/
├── data/
│   ├── sources/
│   │   ├── financial_data.csv      # Datos financieros
│   │   ├── companies.json          # Info de empresas
│   │   └── acquisition_dates.xlsx  # Fechas (simulado)
│   └── merged/
│       └── acquisitions_complete.json
├── scripts/
│   ├── data_fusion.py             # Fusión principal
│   ├── validator.py               # Validar datos
│   └── trend_analyzer.py          # Análisis de tendencias
└── reports/
    └── acquisition_report.html
```

---

### Paso 2: Datos de Fuentes Heterogéneas

**`data/sources/financial_data.csv`:**

```csv
company_id,company_name,valuation_pre,valuation_post,acquisition_cost,employees,sector
ACQ001,CyberShield Security,45000000,65000000,58000000,85,Cybersecurity
ACQ002,GreenEnergy Solutions,32000000,48000000,42000000,120,Clean Energy
ACQ003,AI Dynamics,78000000,120000000,95000000,200,Artificial Intelligence
ACQ004,RoboTech Industries,55000000,82000000,75000000,150,Robotics
ACQ005,BioMed Innovations,89000000,140000000,110000000,300,Biotechnology
ACQ006,Quantum Computing Labs,120000000,180000000,145000000,85,Quantum Computing
ACQ007,DroneVision Systems,28000000,42000000,35000000,65,Drone Technology
ACQ008,NanoMaterials Corp,67000000,95000000,82000000,180,Nanotechnology
```

**`data/sources/companies.json`:**

```json
{
  "companies": [
    {
      "id": "ACQ001",
      "name": "CyberShield Security",
      "founded": "2015-03-20",
      "headquarters": "Silicon Valley, CA",
      "founders": ["Sarah Chen", "Michael Torres"],
      "products": ["Firewall AI", "Threat Detection"],
      "patents": 12,
      "revenue_annual": 18000000,
      "profitable": true
    },
    {
      "id": "ACQ002",
      "name": "GreenEnergy Solutions",
      "founded": "2012-08-15",
      "headquarters": "Austin, TX",
      "founders": ["Emma Rodriguez"],
      "products": ["Solar Storage", "Wind Analytics"],
      "patents": 8,
      "revenue_annual": 25000000,
      "profitable": true
    },
    {
      "id": "ACQ003",
      "name": "AI Dynamics",
      "founded": "2018-01-10",
      "headquarters": "Boston, MA",
      "founders": ["Dr. James Liu", "Lisa Park"],
      "products": ["Neural Engine", "ML Platform"],
      "patents": 25,
      "revenue_annual": 35000000,
      "profitable": false
    },
    {
      "id": "ACQ004",
      "name": "RoboTech Industries",
      "founded": "2014-06-22",
      "headquarters": "Detroit, MI",
      "founders": ["Robert Hayes", "Anna Schmidt"],
      "products": ["Industrial Bots", "Automation Suite"],
      "patents": 18,
      "revenue_annual": 42000000,
      "profitable": true
    },
    {
      "id": "ACQ005",
      "name": "BioMed Innovations",
      "founded": "2010-11-05",
      "headquarters": "San Diego, CA",
      "founders": ["Dr. Maria Gonzalez"],
      "products": ["Gene Therapy", "Medical AI"],
      "patents": 45,
      "revenue_annual": 55000000,
      "profitable": true
    }
  ]
}
```

**`data/sources/acquisition_dates.txt`** (simulando Excel):

```
company_id|acquisition_date|integration_status|wayne_division|strategic_value
ACQ001|2022-05-15|Complete|Wayne Tech|High
ACQ002|2021-11-20|Complete|Wayne Energy|Medium
ACQ003|2023-03-10|In Progress|Wayne AI Labs|Critical
ACQ004|2022-08-05|Complete|Wayne Robotics|High
ACQ005|2021-02-28|Complete|Wayne Healthcare|Critical
ACQ006|2023-07-01|Planning|Wayne Research|Critical
ACQ007|2022-12-10|Complete|Wayne Defense|Medium
ACQ008|2023-01-15|In Progress|Wayne Materials|High
```

---

### Paso 3: Script de Fusión de Datos

**`scripts/data_fusion.py`:**

```python
"""
Sistema de Fusión de Datos Heterogéneos
Une CSV + JSON + TXT en un solo dataset consolidado
"""
import csv
import json
from datetime import datetime


def load_financial_data(filepath):
    """Carga datos financieros desde CSV"""
    data = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['company_id']] = {
                'valuation_pre': float(row['valuation_pre']),
                'valuation_post': float(row['valuation_post']),
                'acquisition_cost': float(row['acquisition_cost']),
                'employees': int(row['employees']),
                'sector': row['sector']
            }
    return data


def load_company_info(filepath):
    """Carga información de empresas desde JSON"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    companies = {}
    for company in data['companies']:
        companies[company['id']] = {
            'founded': company['founded'],
            'headquarters': company['headquarters'],
            'founders': company['founders'],
            'products': company['products'],
            'patents': company['patents'],
            'revenue_annual': company['revenue_annual'],
            'profitable': company['profitable']
        }
    return companies


def load_acquisition_dates(filepath):
    """Carga fechas de adquisición desde TXT (simula Excel)"""
    data = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('company_id'):
                parts = line.strip().split('|')
                data[parts[0]] = {
                    'acquisition_date': parts[1],
                    'integration_status': parts[2],
                    'wayne_division': parts[3],
                    'strategic_value': parts[4]
                }
    return data


def merge_datasets(financial, companies, acquisitions):
    """Fusiona los tres datasets en uno solo"""
    merged = []
    
    all_ids = set(financial.keys()) | set(companies.keys()) | set(acquisitions.keys())
    
    for company_id in all_ids:
        record = {'company_id': company_id}
        
        # Agregar datos financieros
        if company_id in financial:
            record.update(financial[company_id])
        
        # Agregar info de empresa
        if company_id in companies:
            record.update(companies[company_id])
        
        # Agregar datos de adquisición
        if company_id in acquisitions:
            record.update(acquisitions[company_id])
        
        # Calcular métricas adicionales
        if 'acquisition_cost' in record and 'revenue_annual' in record:
            record['revenue_multiple'] = record['acquisition_cost'] / record['revenue_annual']
        
        if 'founded' in record and 'acquisition_date' in record:
            founded = datetime.strptime(record['founded'], '%Y-%m-%d')
            acquired = datetime.strptime(record['acquisition_date'], '%Y-%m-%d')
            record['company_age_at_acquisition'] = (acquired - founded).days // 365
        
        if 'valuation_pre' in record and 'valuation_post' in record:
            record['value_increase_pct'] = ((record['valuation_post'] - record['valuation_pre']) 
                                           / record['valuation_pre'] * 100)
        
        merged.append(record)
    
    return merged


def save_merged_dataset(data, filepath):
    """Guarda dataset fusionado"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Dataset fusionado guardado: {filepath}")


def generate_fusion_report(merged_data):
    """Genera reporte de la fusión"""
    
    total_cost = sum(d.get('acquisition_cost', 0) for d in merged_data)
    total_employees = sum(d.get('employees', 0) for d in merged_data)
    total_patents = sum(d.get('patents', 0) for d in merged_data)
    
    # Por sector
    by_sector = {}
    for d in merged_data:
        sector = d.get('sector', 'Unknown')
        if sector not in by_sector:
            by_sector[sector] = {'count': 0, 'total_cost': 0}
        by_sector[sector]['count'] += 1
        by_sector[sector]['total_cost'] += d.get('acquisition_cost', 0)
    
    # Por división Wayne
    by_division = {}
    for d in merged_data:
        div = d.get('wayne_division', 'Unknown')
        if div not in by_division:
            by_division[div] = {'count': 0, 'total_cost': 0}
        by_division[div]['count'] += 1
        by_division[div]['total_cost'] += d.get('acquisition_cost', 0)
    
    return {
        'total_acquisitions': len(merged_data),
        'total_investment': total_cost,
        'total_employees_acquired': total_employees,
        'total_patents_acquired': total_patents,
        'by_sector': by_sector,
        'by_division': by_division,
        'avg_company_age': sum(d.get('company_age_at_acquisition', 0) 
                               for d in merged_data) / len(merged_data) if merged_data else 0
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 DATA FUSION - Adquisiciones Wayne Enterprises")
    print("=" * 60)
    
    # Cargar todas las fuentes
    print("\n📥 Cargando fuentes de datos...")
    financial = load_financial_data('data/sources/financial_data.csv')
    companies = load_company_info('data/sources/companies.json')
    acquisitions = load_acquisition_dates('data/sources/acquisition_dates.txt')
    
    print(f"   Registros financieros: {len(financial)}")
    print(f"   Registros de empresas: {len(companies)}")
    print(f"   Registros de adquisiciones: {len(acquisitions)}")
    
    # Fusionar
    print("\n🔗 Fusionando datasets...")
    merged = merge_datasets(financial, companies, acquisitions)
    
    # Guardar
    save_merged_dataset(merged, 'data/merged/acquisitions_complete.json')
    
    # Reporte
    report = generate_fusion_report(merged)
    
    print(f"\n📊 Reporte de Fusión:")
    print(f"   Total adquisiciones: {report['total_acquisitions']}")
    print(f"   Inversión total: ${report['total_investment']:,.0f}")
    print(f"   Empleados adquiridos: {report['total_employees_acquired']}")
    print(f"   Patentes adquiridas: {report['total_patents_acquired']}")
    print(f"   Edad promedio: {report['avg_company_age']:.1f} años")
    
    print(f"\n🏢 Por Sector:")
    for sector, data in report['by_sector'].items():
        print(f"   {sector}: {data['count']} empresas, ${data['total_cost']:,.0f}")
    
    print(f"\n🦇 Por División Wayne:")
    for div, data in report['by_division'].items():
        print(f"   {div}: {data['count']} empresas, ${data['total_cost']:,.0f}")
```

---

### Paso 4: Análisis de Tendencias

**`scripts/trend_analyzer.py`:**

```python
"""
Analizador de tendencias de adquisiciones
"""
import json
from datetime import datetime
from collections import defaultdict


def load_merged_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def analyze_yearly_trends(data):
    """Analiza tendencias por año"""
    yearly = defaultdict(lambda: {'count': 0, 'total_cost': 0})
    
    for d in data:
        if 'acquisition_date' in d:
            year = datetime.strptime(d['acquisition_date'], '%Y-%m-%d').year
            yearly[year]['count'] += 1
            yearly[year]['total_cost'] += d.get('acquisition_cost', 0)
    
    return dict(yearly)


def analyze_sector_trends(data):
    """Analiza tendencias por sector"""
    sectors = defaultdict(lambda: {'count': 0, 'investment': 0, 'avg_age': []})
    
    for d in data:
        sector = d.get('sector', 'Unknown')
        sectors[sector]['count'] += 1
        sectors[sector]['investment'] += d.get('acquisition_cost', 0)
        if 'company_age_at_acquisition' in d:
            sectors[sector]['avg_age'].append(d['company_age_at_acquisition'])
    
    # Calcular promedios
    for sector in sectors:
        ages = sectors[sector]['avg_age']
        sectors[sector]['avg_age'] = sum(ages) / len(ages) if ages else 0
    
    return dict(sectors)


def find_success_indicators(data):
    """Identifica indicadores de adquisiciones exitosas"""
    
    # Empresas rentables vs no rentables
    profitable = [d for d in data if d.get('profitable', False)]
    non_profitable = [d for d in data if not d.get('profitable', False)]
    
    avg_cost_profitable = sum(d.get('acquisition_cost', 0) for d in profitable) / len(profitable) if profitable else 0
    avg_cost_non_profitable = sum(d.get('acquisition_cost', 0) for d in non_profitable) / len(non_profitable) if non_profitable else 0
    
    return {
        'profitable_companies': len(profitable),
        'non_profitable_companies': len(non_profitable),
        'avg_cost_profitable': avg_cost_profitable,
        'avg_cost_non_profitable': avg_cost_non_profitable,
        'patent_correlation': len([d for d in data if d.get('patents', 0) > 20])
    }


def generate_trend_report(data):
    """Genera reporte completo de tendencias"""
    
    yearly = analyze_yearly_trends(data)
    sectors = analyze_sector_trends(data)
    success = find_success_indicators(data)
    
    report = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'yearly_trends': yearly,
        'sector_analysis': sectors,
        'success_indicators': success,
        'insights': []
    }
    
    # Generar insights
    if yearly:
        peak_year = max(yearly.items(), key=lambda x: x[1]['count'])
        report['insights'].append(f"Año pico de adquisiciones: {peak_year[0]} ({peak_year[1]['count']} empresas)")
    
    if sectors:
        top_sector = max(sectors.items(), key=lambda x: x[1]['investment'])
        report['insights'].append(f"Sector más invertido: {top_sector[0]} (${top_sector[1]['investment']:,.0f})")
    
    report['insights'].append(f"{(success['profitable_companies']/len(data)*100):.1f}% de empresas adquiridas eran rentables")
    
    return report


if __name__ == "__main__":
    print("=" * 60)
    print("📈 TREND ANALYZER - Análisis de Adquisiciones")
    print("=" * 60)
    
    data = load_merged_data('data/merged/acquisitions_complete.json')
    
    # Tendencias anuales
    yearly = analyze_yearly_trends(data)
    print("\n📅 Tendencias Anuales:")
    for year in sorted(yearly.keys()):
        info = yearly[year]
        print(f"   {year}: {info['count']} adquisiciones, ${info['total_cost']:,.0f}")
    
    # Análisis de sectores
    sectors = analyze_sector_trends(data)
    print("\n🏭 Análisis por Sector:")
    for sector, info in sorted(sectors.items(), key=lambda x: x[1]['investment'], reverse=True):
        print(f"   {sector}: {info['count']} empresas, ${info['investment']:,.0f}, edad promedio: {info['avg_age']:.1f} años")
    
    # Indicadores de éxito
    success = find_success_indicators(data)
    print("\n✅ Indicadores de Éxito:")
    print(f"   Empresas rentables adquiridas: {success['profitable_companies']}")
    print(f"   Empresas no rentables: {success['non_profitable_companies']}")
    print(f"   Costo promedio (rentables): ${success['avg_cost_profitable']:,.0f}")
    print(f"   Costo promedio (no rentables): ${success['avg_cost_non_profitable']:,.0f}")
    print(f"   Empresas con 20+ patentes: {success['patent_correlation']}")
    
    # Guardar reporte
    report = generate_trend_report(data)
    with open('reports/trend_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💡 Insights:")
    for insight in report['insights']:
        print(f"   • {insight}")
    
    print("\n✅ Reporte guardado en reports/trend_report.json")
```

---

### Paso 5: Reporte HTML

**`scripts/generate_html_report.py`:**

```python
"""
Generador de reporte HTML de adquisiciones
"""
import json


def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def generate_html():
    data = load_json('data/merged/acquisitions_complete.json')
    trends = load_json('reports/trend_report.json')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Wayne Enterprises - Adquisiciones</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #e94560; }}
        h2 {{ color: #3498db; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #16213e; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #e94560; }}
        .stat-value {{ font-size: 28px; color: #e94560; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #e94560; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #333; }}
        .sector-tag {{ background: #3498db; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🦇 Wayne Enterprises - Adquisiciones de Startups</h1>
        <p>Historial de compras y análisis de integración</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{len(data)}</div>
                <div>Adquisiciones Totales</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">${sum(d.get('acquisition_cost', 0) for d in data)/1e9:.2f}B</div>
                <div>Inversión Total</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{sum(d.get('employees', 0) for d in data)}</div>
                <div>Empleados Adquiridos</div>
            </div>
        </div>
        
        <h2>📋 Empresas Adquiridas</h2>
        <table>
            <tr>
                <th>Empresa</th>
                <th>Sector</th>
                <th>División</th>
                <th>Costo</th>
                <th>Empleados</th>
                <th>Estado</th>
            </tr>
"""
    
    for d in data:
        html += f"""
            <tr>
                <td><strong>{d.get('company_id', 'N/A')}</strong><br><small>{d.get('name', 'Unknown')}</small></td>
                <td><span class="sector-tag">{d.get('sector', 'N/A')}</span></td>
                <td>{d.get('wayne_division', 'N/A')}</td>
                <td>${d.get('acquisition_cost', 0):,.0f}</td>
                <td>{d.get('employees', 0)}</td>
                <td>{d.get('integration_status', 'N/A')}</td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>💡 Insights</h2>
        <ul>
"""
    
    for insight in trends.get('insights', []):
        html += f"<li>{insight}</li>"
    
    html += """
        </ul>
    </div>
</body>
</html>
"""
    
    with open('reports/acquisition_report.html', 'w') as f:
        f.write(html)
    
    print("✅ Reporte HTML generado: reports/acquisition_report.html")


if __name__ == "__main__":
    generate_html()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout dataset_13

# Agregar archivos
git add dataset_13_acquisitions/
git commit -m "feat: agrega sistema ETL de fusión de adquisiciones"
git push origin dataset_13
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Archivo CSV con datos financieros
- [ ] Archivo JSON con info de empresas
- [ ] Archivo TXT con fechas de adquisición
- [ ] `data_fusion.py` fusiona todo correctamente
- [ ] `trend_analyzer.py` genera insights
- [ ] Reporte HTML creado
- [ ] Subir a GitHub

---

## Integración

Puedes vincular este sistema a `ventures` o `tech`:

```python
# ventures/views.py
import json
from django.shortcuts import render

@login_required
def acquisitions_portfolio(request):
    with open('dataset_13_acquisitions/data/merged/acquisitions_complete.json') as f:
        acquisitions = json.load(f)
    return render(request, 'ventures/acquisitions.html', {'acquisitions': acquisitions})
```
