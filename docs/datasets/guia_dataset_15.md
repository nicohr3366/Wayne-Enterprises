# Guía Individual: Dataset #15 - Brother Eye AI

> **Responsable:** *Por asignar*  
> **ID:** #15  
> **Dataset:** Investigación en Inteligencia Artificial  
> **Descripción:** Avances en el sistema de vigilancia Brother Eye. Auditoría de ética algorítmica.  
> **Rama Git:** `dataset_15`  

---

## ¿Qué es este Dataset?

Tu trabajo es crear un **sistema de auditoría de IA** para el proyecto Brother Eye de Wayne Tech. Debes procesar:

- **Logs del sistema de vigilancia** Brother Eye
- **Decisiones algorítmicas** y sus justificaciones
- **Detección de sesgos** en el sistema
- **Auditoría de ética** algorítmica

**Ejemplo real:** Como sistemas de explicabilidad de IA (XAI) para detectar decisiones injustas.

---

## Paso a Paso: Crear tu Sistema de Auditoría de IA

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p dataset_15_brother_eye/{data/{logs,decisions},scripts,reports}
cd dataset_15_brother_eye

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
dataset_15_brother_eye/
├── data/
│   ├── logs/
│   │   ├── system_logs.csv       # Logs del sistema
│   │   └── alert_logs.json       # Alertas generadas
│   └── decisions/
│       └── decision_audit.json   # Decisiones auditadas
├── scripts/
│   ├── log_analyzer.py          # Analizador de logs
│   ├── bias_detector.py         # Detector de sesgos
│   └── ethics_auditor.py        # Auditor de ética
└── reports/
    └── brother_eye_audit.html
```

---

### Paso 2: Datos de Logs del Sistema

**`data/logs/system_logs.csv`:**

```csv
timestamp,event_type,location,subject_id,risk_score,algorithm_version,decision,confidence,human_reviewed
2024-04-01T08:15:00,potential_threat,Downtown Gotham,SGT-001,0.85,v2.1.4,alert_generated,0.92,false
2024-04-01T08:16:30,anomaly_detected,Arkham District,SGT-002,0.72,v2.1.4,monitoring,0.78,false
2024-04-01T08:20:15,false_positive,Residential Area,SGT-003,0.45,v2.1.4,dismissed,0.65,true
2024-04-01T08:25:00,potential_threat,Industrial Zone,SGT-004,0.91,v2.1.4,alert_generated,0.89,false
2024-04-01T08:30:45,bias_flagged,Low Income Area,SGT-005,0.68,v2.1.4,under_review,0.71,true
2024-04-01T08:35:20,anomaly_detected,Downtown Gotham,SGT-006,0.55,v2.1.4,monitoring,0.82,false
2024-04-01T08:40:00,false_positive,Commercial Zone,SGT-007,0.38,v2.1.4,dismissed,0.69,true
2024-04-01T08:45:30,potential_threat,Port Area,SGT-008,0.94,v2.1.4,alert_generated,0.95,false
2024-04-01T08:50:15,anomaly_detected,Suburbs,SGT-009,0.62,v2.1.4,monitoring,0.74,false
2024-04-01T08:55:00,bias_flagged,Low Income Area,SGT-010,0.71,v2.1.4,under_review,0.68,true
```

**`data/logs/alert_logs.json`:**

```json
{
  "alerts": [
    {
      "alert_id": "ALT-2024-001",
      "timestamp": "2024-04-01T08:15:00",
      "severity": "high",
      "location": "Downtown Gotham",
      "subject_profile": {
        "age_estimate": 28,
        "gender": "male",
        "behavior_flags": ["loitering", "suspicious_movement"],
        "criminal_history": false
      },
      "ai_decision": {
        "action": "notify_gcpd",
        "justification": "Pattern matches known criminal behavior",
        "confidence": 0.92,
        "factors": ["location", "time", "movement_pattern"]
      },
      "outcome": {
        "actual_threat": false,
        "subject_identity": "Delivery person",
        "resolution": "false_positive"
      }
    },
    {
      "alert_id": "ALT-2024-002",
      "timestamp": "2024-04-01T08:25:00",
      "severity": "critical",
      "location": "Industrial Zone",
      "subject_profile": {
        "age_estimate": 35,
        "gender": "male",
        "behavior_flags": ["unauthorized_access", "carrying_object"],
        "criminal_history": true
      },
      "ai_decision": {
        "action": "immediate_alert",
        "justification": "High-risk individual in restricted area",
        "confidence": 0.89,
        "factors": ["criminal_history", "location", "time"]
      },
      "outcome": {
        "actual_threat": true,
        "subject_identity": "Confirmed suspect",
        "resolution": "apprehended"
      }
    },
    {
      "alert_id": "ALT-2024-003",
      "timestamp": "2024-04-01T08:30:45",
      "severity": "medium",
      "location": "Low Income Area",
      "subject_profile": {
        "age_estimate": 22,
        "gender": "female",
        "behavior_flags": ["group_gathering"],
        "criminal_history": false
      },
      "ai_decision": {
        "action": "flag_for_review",
        "justification": "Unusual gathering in high-crime area",
        "confidence": 0.71,
        "factors": ["location_crime_rate", "group_size"]
      },
      "outcome": {
        "actual_threat": false,
        "subject_identity": "Community meeting",
        "resolution": "false_positive",
        "bias_concern": "location_based_profiling"
      }
    }
  ]
}
```

---

### Paso 3: Analizador de Logs

**`scripts/log_analyzer.py`:**

```python
"""
Analizador de logs de Brother Eye AI
"""
import csv
import json
from collections import defaultdict, Counter


def load_system_logs(filepath):
    """Carga logs del sistema"""
    logs = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    return logs


def load_alert_logs(filepath):
    """Carga logs de alertas"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get('alerts', [])


def analyze_decision_patterns(logs):
    """Analiza patrones de decisiones del sistema"""
    
    # Contar por tipo de evento
    event_types = Counter(log['event_type'] for log in logs)
    
    # Contar decisiones
    decisions = Counter(log['decision'] for log in logs)
    
    # Promedio de confianza
    avg_confidence = sum(float(log['confidence']) for log in logs) / len(logs)
    
    # Por ubicación
    by_location = defaultdict(lambda: {'count': 0, 'avg_risk': 0})
    for log in logs:
        loc = log['location']
        by_location[loc]['count'] += 1
        by_location[loc]['avg_risk'] += float(log['risk_score'])
    
    # Calcular promedios
    for loc in by_location:
        by_location[loc]['avg_risk'] /= by_location[loc]['count']
    
    return {
        'event_types': dict(event_types),
        'decisions': dict(decisions),
        'avg_confidence': avg_confidence,
        'by_location': dict(by_location),
        'total_logs': len(logs)
    }


def analyze_alert_accuracy(alerts):
    """Analiza precisión de las alertas"""
    
    total = len(alerts)
    true_positives = sum(1 for a in alerts if a['outcome']['actual_threat'])
    false_positives = sum(1 for a in alerts if not a['outcome']['actual_threat'])
    
    # Por severidad
    by_severity = defaultdict(lambda: {'total': 0, 'correct': 0})
    for alert in alerts:
        sev = alert['severity']
        by_severity[sev]['total'] += 1
        if alert['outcome']['actual_threat']:
            by_severity[sev]['correct'] += 1
    
    # Por confianza del AI
    high_conf_correct = sum(1 for a in alerts 
                           if a['ai_decision']['confidence'] > 0.8 and a['outcome']['actual_threat'])
    high_conf_total = sum(1 for a in alerts if a['ai_decision']['confidence'] > 0.8)
    
    return {
        'total_alerts': total,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'precision': true_positives / total if total > 0 else 0,
        'by_severity': dict(by_severity),
        'high_confidence_accuracy': high_conf_correct / high_conf_total if high_conf_total > 0 else 0
    }


def detect_location_bias(logs):
    """Detecta sesgos basados en ubicación"""
    
    # Analizar riesgo promedio por zona
    location_risk = defaultdict(list)
    for log in logs:
        location_risk[log['location']].append(float(log['risk_score']))
    
    bias_flags = []
    overall_avg = sum(sum(scores) / len(scores) for scores in location_risk.values()) / len(location_risk)
    
    for location, scores in location_risk.items():
        avg_risk = sum(scores) / len(scores)
        if avg_risk > overall_avg * 1.3:  # 30% más alto
            bias_flags.append({
                'location': location,
                'avg_risk': avg_risk,
                'overall_avg': overall_avg,
                'deviation_pct': ((avg_risk - overall_avg) / overall_avg) * 100,
                'concern': 'Elevated risk scoring'
            })
    
    return bias_flags


if __name__ == "__main__":
    print("=" * 60)
    print("👁️ BROTHER EYE - Log Analyzer")
    print("=" * 60)
    
    # Cargar datos
    logs = load_system_logs('data/logs/system_logs.csv')
    alerts = load_alert_logs('data/logs/alert_logs.json')
    
    print(f"\n📊 Logs del sistema: {len(logs)}")
    print(f"📊 Alertas analizadas: {len(alerts)}")
    
    # Analizar patrones
    patterns = analyze_decision_patterns(logs)
    
    print(f"\n🔍 Patrones de Decisiones:")
    print(f"   Tipos de eventos: {patterns['event_types']}")
    print(f"   Decisiones: {patterns['decisions']}")
    print(f"   Confianza promedio: {patterns['avg_confidence']:.2%}")
    
    print(f"\n🌍 Por Ubicación:")
    for loc, data in patterns['by_location'].items():
        print(f"   {loc}: {data['count']} eventos, riesgo promedio {data['avg_risk']:.2f}")
    
    # Precisión
    accuracy = analyze_alert_accuracy(alerts)
    
    print(f"\n🎯 Precisión del Sistema:")
    print(f"   Total alertas: {accuracy['total_alerts']}")
    print(f"   Verdaderos positivos: {accuracy['true_positives']}")
    print(f"   Falsos positivos: {accuracy['false_positives']}")
    print(f"   Precisión: {accuracy['precision']:.2%}")
    print(f"   Precisión (alta confianza): {accuracy['high_confidence_accuracy']:.2%}")
    
    # Sesgos
    bias = detect_location_bias(logs)
    
    if bias:
        print(f"\n⚠️  Banderas de Sesgo Detectadas:")
        for b in bias:
            print(f"   {b['location']}: {b['deviation_pct']:.1f}% sobre promedio")
```

---

### Paso 4: Detector de Sesgos

**`scripts/bias_detector.py`:**

```python
"""
Detector de sesgos algorítmicos en Brother Eye
"""
import json
import csv
from collections import defaultdict


def load_logs(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def analyze_demographic_bias(logs):
    """Analiza posibles sesgos demográficos"""
    
    # Simulación de datos demográficos basados en ubicación
    demographic_map = {
        'Low Income Area': {'economic_level': 'low', 'minority_pct': 0.75},
        'Downtown Gotham': {'economic_level': 'mixed', 'minority_pct': 0.45},
        'Residential Area': {'economic_level': 'middle', 'minority_pct': 0.30},
        'Commercial Zone': {'economic_level': 'mixed', 'minority_pct': 0.40},
        'Industrial Zone': {'economic_level': 'mixed', 'minority_pct': 0.50},
        'Suburbs': {'economic_level': 'high', 'minority_pct': 0.15},
        'Port Area': {'economic_level': 'mixed', 'minority_pct': 0.55},
        'Arkham District': {'economic_level': 'low', 'minority_pct': 0.80}
    }
    
    # Analizar riesgo por nivel económico
    risk_by_economic = defaultdict(list)
    
    for log in logs:
        loc = log['location']
        if loc in demographic_map:
            econ_level = demographic_map[loc]['economic_level']
            risk_by_economic[econ_level].append(float(log['risk_score']))
    
    # Calcular promedios
    results = {}
    for level, scores in risk_by_economic.items():
        results[level] = {
            'avg_risk': sum(scores) / len(scores),
            'count': len(scores)
        }
    
    return results, demographic_map


def calculate_disparate_impact(logs, demographic_map):
    """Calcula impacto dispar (métrica legal de sesgo)"""
    
    # Tasa de alertas por grupo
    alerts_by_group = defaultdict(lambda: {'total': 0, 'flagged': 0})
    
    for log in logs:
        loc = log['location']
        if loc in demographic_map:
            # Determinar grupo mayoritario vs minoritario
            minority_pct = demographic_map[loc]['minority_pct']
            group = 'minority_area' if minority_pct > 0.5 else 'majority_area'
            
            alerts_by_group[group]['total'] += 1
            if log['decision'] in ['alert_generated', 'under_review']:
                alerts_by_group[group]['flagged'] += 1
    
    # Calcular tasas
    for group in alerts_by_group:
        total = alerts_by_group[group]['total']
        flagged = alerts_by_group[group]['flagged']
        alerts_by_group[group]['flag_rate'] = flagged / total if total > 0 else 0
    
    # Calcular ratio de impacto dispar (80% rule)
    minority_rate = alerts_by_group.get('minority_area', {}).get('flag_rate', 0)
    majority_rate = alerts_by_group.get('majority_area', {}).get('flag_rate', 0)
    
    if majority_rate > 0:
        disparate_impact_ratio = minority_rate / majority_rate
    else:
        disparate_impact_ratio = 0
    
    return alerts_by_group, disparate_impact_ratio


def generate_bias_report(logs, demographic_map):
    """Genera reporte completo de sesgos"""
    
    economic_analysis, _ = analyze_demographic_bias(logs)
    disparate_analysis, di_ratio = calculate_disparate_impact(logs, demographic_map)
    
    report = {
        'timestamp': '2024-04-01',
        'system': 'Brother Eye AI v2.1.4',
        'bias_indicators': [],
        'recommendations': []
    }
    
    # Detectar sesgos
    if di_ratio < 0.8:
        report['bias_indicators'].append({
            'type': 'disparate_impact',
            'severity': 'high',
            'description': f'Ratio de impacto dispar: {di_ratio:.2f} (umbral: 0.80)',
            'affected_group': 'minority_areas'
        })
        report['recommendations'].append('Revisar algoritmo de riesgo por ubicación')
    
    # Comparar niveles económicos
    if economic_analysis:
        low_income_risk = economic_analysis.get('low', {}).get('avg_risk', 0)
        high_income_risk = economic_analysis.get('high', {}).get('avg_risk', 0)
        
        if low_income_risk > high_income_risk * 1.5:
            report['bias_indicators'].append({
                'type': 'socioeconomic_bias',
                'severity': 'medium',
                'description': f'Riesgo en zonas de bajos ingresos {low_income_risk:.2f} vs zonas altos {high_income_risk:.2f}',
                'affected_group': 'low_income_areas'
            })
            report['recommendations'].append('Agregar controles de equidad socioeconómica')
    
    report['disparate_impact_ratio'] = di_ratio
    report['economic_analysis'] = economic_analysis
    report['flag_rates'] = {k: v['flag_rate'] for k, v in disparate_analysis.items()}
    
    return report


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 BROTHER EYE - Bias Detector")
    print("=" * 60)
    
    logs = load_logs('data/logs/system_logs.csv')
    
    _, demographic_map = analyze_demographic_bias(logs)
    
    # Análisis económico
    economic_analysis, _ = analyze_demographic_bias(logs)
    
    print("\n📊 Análisis por Nivel Socioeconómico:")
    for level, data in economic_analysis.items():
        print(f"   {level}: riesgo promedio {data['avg_risk']:.2f} ({data['count']} eventos)")
    
    # Impacto dispar
    disparate_analysis, di_ratio = calculate_disparate_impact(logs, demographic_map)
    
    print(f"\n⚖️  Análisis de Impacto Dispar:")
    for group, data in disparate_analysis.items():
        print(f"   {group}: {data['flag_rate']:.2%} tasa de alertas")
    
    print(f"\n   Ratio de Impacto Dispar: {di_ratio:.2f}")
    if di_ratio < 0.8:
        print("   ⚠️  ALERTA: Posible discriminación (ratio < 0.80)")
    else:
        print("   ✅ Dentro de parámetros aceptables")
    
    # Reporte completo
    report = generate_bias_report(logs, demographic_map)
    
    if report['bias_indicators']:
        print(f"\n🚩 Banderas de Sesgo Detectadas:")
        for indicator in report['bias_indicators']:
            print(f"   [{indicator['severity'].upper()}] {indicator['type']}")
            print(f"      {indicator['description']}")
    
    if report['recommendations']:
        print(f"\n💡 Recomendaciones:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
    
    # Guardar reporte
    with open('reports/bias_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ Reporte guardado en reports/bias_report.json")
```

---

### Paso 5: Reporte HTML

**`scripts/generate_audit_report.py`:**

```python
"""
Generador de reporte de auditoría de Brother Eye
"""
import json
import csv


def generate_html():
    # Cargar datos
    with open('data/logs/alert_logs.json', 'r') as f:
        alerts = json.load(f)['alerts']
    
    with open('reports/bias_report.json', 'r') as f:
        bias_report = json.load(f)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Brother Eye - Ethics Audit Report</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #00ff00; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #ff0000; text-shadow: 0 0 10px #ff0000; }}
        h2 {{ color: #00ff00; border-bottom: 1px solid #00ff00; padding-bottom: 10px; }}
        .alert-box {{ background: #1a1a1a; border: 1px solid #ff0000; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .warning {{ color: #ffaa00; }}
        .critical {{ color: #ff0000; font-weight: bold; }}
        .ok {{ color: #00ff00; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #333; color: #00ff00; padding: 10px; text-align: left; border: 1px solid #555; }}
        td {{ padding: 10px; border: 1px solid #333; }}
        .metric {{ display: inline-block; background: #1a1a1a; padding: 15px 30px; margin: 10px; border: 1px solid #00ff00; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👁️ BROTHER EYE - Ethics Audit Report</h1>
        <p>Sistema de Vigilancia AI - Auditoría de Ética Algorítmica</p>
        <p>Generado: {bias_report['timestamp']} | Versión: {bias_report['system']}</p>
        
        <h2>⚠️ Alertas de Sesgo</h2>
"""
    
    if bias_report['bias_indicators']:
        for indicator in bias_report['bias_indicators']:
            severity_class = 'critical' if indicator['severity'] == 'high' else 'warning'
            html += f"""
        <div class="alert-box {severity_class}">
            <strong>[{indicator['severity'].upper()}] {indicator['type']}</strong>
            <p>{indicator['description']}</p>
            <p>Grupo afectado: {indicator['affected_group']}</p>
        </div>
"""
    else:
        html += '<p class="ok">✅ No se detectaron sesgos significativos</p>'
    
    html += f"""
        <h2>📊 Métricas de Impacto Dispar</h2>
        <div class="metric">
            <strong>Ratio DI:</strong> {bias_report['disparate_impact_ratio']:.2f}
            {'<span class="critical">⚠️ Bajo umbral</span>' if bias_report['disparate_impact_ratio'] < 0.8 else '<span class="ok">✅ OK</span>'}
        </div>
"""
    
    html += """
        <h2>🚨 Alertas Analizadas</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Severidad</th>
                <th>Ubicación</th>
                <th>Decisión AI</th>
                <th>Resultado Real</th>
                <th>Confianza</th>
            </tr>
"""
    
    for alert in alerts:
        outcome_class = 'ok' if alert['outcome']['actual_threat'] else 'warning'
        html += f"""
            <tr>
                <td>{alert['alert_id']}</td>
                <td>{alert['severity']}</td>
                <td>{alert['location']}</td>
                <td>{alert['ai_decision']['action']}</td>
                <td class="{outcome_class}">{alert['outcome']['resolution']}</td>
                <td>{alert['ai_decision']['confidence']:.0%}</td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>💡 Recomendaciones</h2>
        <ul>
"""
    
    for rec in bias_report.get('recommendations', []):
        html += f"<li>{rec}</li>"
    
    html += """
        </ul>
        
        <p style="margin-top: 40px; color: #666; font-size: 12px;">
            Reporte generado automáticamente por sistema de auditoría Brother Eye<br>
            Wayne Enterprises - Ethics Division
        </p>
    </div>
</body>
</html>
"""
    
    with open('reports/brother_eye_audit.html', 'w') as f:
        f.write(html)
    
    print("✅ Reporte HTML generado: reports/brother_eye_audit.html")


if __name__ == "__main__":
    generate_html()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout dataset_15

# Agregar archivos
git add dataset_15_brother_eye/
git commit -m "feat: agrega sistema de auditoría de ética para Brother Eye AI"
git push origin dataset_15
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Archivo CSV con logs del sistema
- [ ] Archivo JSON con alertas
- [ ] `log_analyzer.py` funciona
- [ ] `bias_detector.py` detecta sesgos
- [ ] Reporte HTML generado
- [ ] Subir a GitHub

---

## Integración

Puedes vincular este sistema a `tech`:

```python
# tech/views.py
import json
from django.shortcuts import render

@login_required
def ai_ethics_dashboard(request):
    with open('dataset_15_brother_eye/reports/bias_report.json') as f:
        audit = json.load(f)
    return render(request, 'tech/ethics.html', {'audit': audit})
```
