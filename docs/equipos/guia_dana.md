# Guía Individual: Dana - Dataset #8

> **Responsable:** Dana  
> **ID:** #8  
> **Dataset:** Ciberseguridad de la Baticueva  
> **Descripción:** Intentos de hackeo a servidores centrales. Clasificación de amenazas (Machine Learning).  
> **Rama Git:** `dana`  

---

## ¿Qué es tu Dataset?

Tu trabajo es crear un **sistema de análisis de ciberseguridad** que procese:

- **Logs de intentos de hackeo** a servidores Wayne
- **Patrones de ataque** (fuerza bruta, SQL injection, DDoS)
- **Clasificación de amenazas** usando Machine Learning simple
- **Dashboard de seguridad** con estadísticas

**Ejemplo real:** Como un IDS (Intrusion Detection System) que alerta sobre ataques.

---

## Paso a Paso: Crear tu Sistema de Ciberseguridad

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p dana_cyber/{logs,scripts,ml_model,output}
cd dana_cyber

touch logs/__init__.py
touch scripts/__init__.py
```

Estructura:
```
dana_cyber/
├── logs/
│   ├── security_logs_raw.csv    # Logs sin procesar
│   └── attacks_labeled.csv      # Logs clasificados
├── scripts/
│   ├── parser.py                # Parsear logs
│   ├── classifier.py            # Clasificar amenazas
│   └── dashboard.py             # Generar reportes
├── ml_model/
│   └── threat_classifier.py     # ML simple
└── output/
    ├── threats_detected.json    # Amenazas encontradas
    └── security_report.html     # Reporte visual
```

---

### Paso 2: Crear Logs de Ejemplo

**`logs/security_logs_raw.csv`:**

```csv
fecha,hora,ip_origen,tipo_peticion,endpoint,status,user_agent,nivel_sospecha
2024-04-01,08:15:23,192.168.1.100,GET,/api/users,200,Mozilla/5.0,bajo
2024-04-01,08:15:24,192.168.1.100,GET,/api/users,200,Mozilla/5.0,bajo
2024-04-01,08:15:25,10.0.0.50,POST,/login,401,Python-requests/2.28,medio
2024-04-01,08:15:26,10.0.0.50,POST,/login,401,Python-requests/2.28,medio
2024-04-01,08:15:27,10.0.0.50,POST,/login,401,Python-requests/2.28,alto
2024-04-01,08:15:28,10.0.0.50,POST,/login,401,Python-requests/2.28,alto
2024-04-01,08:16:00,172.16.0.20,GET,/admin,403,sqlmap/1.5,alto
2024-04-01,08:16:01,172.16.0.20,GET,/admin?user=admin'--,403,sqlmap/1.5,critico
2024-04-01,08:16:02,172.16.0.20,GET,/admin?user=1 OR 1=1,403,sqlmap/1.5,critico
2024-04-01,08:20:00,192.168.1.100,GET,/dashboard,200,Mozilla/5.0,bajo
```

---

### Paso 3: Script Parser (Analizar Logs)

**`scripts/parser.py`:**

```python
"""
Parser de logs de seguridad - Extrae información relevante
"""
import csv
from datetime import datetime
import re


def parse_logs(filepath):
    """Parsea archivo CSV de logs"""
    events = []
    
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            event = {
                'timestamp': f"{row['fecha']} {row['hora']}",
                'ip': row['ip_origen'],
                'method': row['tipo_peticion'],
                'endpoint': row['endpoint'],
                'status': int(row['status']),
                'user_agent': row['user_agent'],
                'suspicion': row['nivel_sospecha']
            }
            events.append(event)
    
    return events


def detect_attack_type(event):
    """
    Detecta tipo de ataque basado en patrones
    """
    endpoint = event['endpoint'].lower()
    user_agent = event['user_agent'].lower()
    status = event['status']
    
    # SQL Injection
    sql_patterns = ["'", "'--", "or 1=1", "union select", "drop table"]
    if any(pattern in endpoint for pattern in sql_patterns):
        return "SQL Injection"
    
    # Fuerza Bruta (múltiples 401s)
    if status == 401 and event['suspicion'] in ['medio', 'alto']:
        return "Fuerza Bruta"
    
    # Escaneo con herramientas
    if 'sqlmap' in user_agent or 'nmap' in user_agent:
        return "Escaneo Malicioso"
    
    # Acceso no autorizado
    if status == 403:
        return "Acceso No Autorizado"
    
    return "Normal"


def detect_brute_force(events, time_window=60):
    """
    Detecta ataques de fuerza bruta por IP
    """
    ip_attempts = {}
    threats = []
    
    for event in events:
        ip = event['ip']
        
        if ip not in ip_attempts:
            ip_attempts[ip] = []
        
        ip_attempts[ip].append(event)
        
        # Si hay más de 3 intentos fallidos en poco tiempo
        if len(ip_attempts[ip]) >= 3:
            failed = [e for e in ip_attempts[ip] if e['status'] == 401]
            if len(failed) >= 3:
                threats.append({
                    'tipo': 'Fuerza Bruta Detectada',
                    'ip': ip,
                    'intentos': len(failed),
                    'ultimo_intento': event['timestamp'],
                    'riesgo': 'ALTO'
                })
    
    return threats


if __name__ == "__main__":
    events = parse_logs('logs/security_logs_raw.csv')
    
    print(f"Total eventos parseados: {len(events)}")
    print("\n--- Tipos de Ataque Detectados ---")
    
    for event in events[:5]:
        attack = detect_attack_type(event)
        print(f"{event['ip']} -> {event['endpoint']}: {attack}")
    
    threats = detect_brute_force(events)
    print(f"\n--- Amenazas Detectadas: {len(threats)} ---")
    for t in threats:
        print(f"⚠️  {t['tipo']} desde {t['ip']}: {t['intentos']} intentos")
```

---

### Paso 4: Clasificador de Amenazas (ML Simple)

**`scripts/classifier.py`:**

```python
"""
Clasificador simple de amenazas usando reglas
(Puede extenderse a ML real con scikit-learn)
"""
import json


def classify_threat_level(event):
    """
    Clasifica nivel de amenaza 1-10
    """
    score = 0
    
    # Basado en status code
    if event['status'] == 401:
        score += 3
    elif event['status'] == 403:
        score += 5
    
    # Basado en user agent
    ua = event['user_agent'].lower()
    if 'bot' in ua or 'sqlmap' in ua or 'scanner' in ua:
        score += 4
    
    # Basado en endpoint
    endpoint = event['endpoint'].lower()
    if 'admin' in endpoint or 'login' in endpoint:
        score += 2
    if "'" in endpoint or '"' in endpoint:
        score += 5  # SQL Injection
    
    # Basado en sospecha predefinida
    suspicion_scores = {
        'bajo': 1,
        'medio': 3,
        'alto': 5,
        'critico': 8
    }
    score += suspicion_scores.get(event['suspicion'], 0)
    
    return min(score, 10)  # Max 10


def categorize_threat(event, threat_score):
    """
    Categoriza la amenaza
    """
    if threat_score >= 8:
        return "CRÍTICA", "Acción inmediata requerida"
    elif threat_score >= 6:
        return "ALTA", "Monitoreo continuo"
    elif threat_score >= 4:
        return "MEDIA", "Revisar en próximas horas"
    elif threat_score >= 2:
        return "BAJA", "Registro estándar"
    else:
        return "NORMAL", "Sin acción requerida"


def generate_threat_report(events):
    """Genera reporte de amenazas"""
    report = {
        'total_events': len(events),
        'threats_by_level': {'CRÍTICA': 0, 'ALTA': 0, 'MEDIA': 0, 'BAJA': 0, 'NORMAL': 0},
        'top_attackers': {},
        'attack_types': {}
    }
    
    for event in events:
        score = classify_threat_level(event)
        level, action = categorize_threat(event, score)
        
        report['threats_by_level'][level] += 1
        
        # Contar por IP
        ip = event['ip']
        if ip not in report['top_attackers']:
            report['top_attackers'][ip] = 0
        report['top_attackers'][ip] += 1
        
        # Tipo de ataque
        from parser import detect_attack_type
        attack = detect_attack_type(event)
        if attack not in report['attack_types']:
            report['attack_types'][attack] = 0
        report['attack_types'][attack] += 1
    
    return report


if __name__ == "__main__":
    from parser import parse_logs
    
    events = parse_logs('../logs/security_logs_raw.csv')
    
    print("=" * 50)
    print("CLASIFICACIÓN DE AMENAZAS - WAYNE SECURITY")
    print("=" * 50)
    
    for event in events:
        score = classify_threat_level(event)
        level, action = categorize_threat(event, score)
        
        print(f"\n🌐 {event['ip']}")
        print(f"   Endpoint: {event['endpoint']}")
        print(f"   Status: {event['status']}")
        print(f"   Score: {score}/10 - {level}")
        print(f"   Acción: {action}")
    
    # Reporte general
    report = generate_threat_report(events)
    print("\n" + "=" * 50)
    print("REPORTE GENERAL")
    print("=" * 50)
    print(f"Eventos totales: {report['total_events']}")
    print(f"Distribución de amenazas: {report['threats_by_level']}")
    print(f"Tipos de ataque: {report['attack_types']}")
```

---

### Paso 5: Dashboard/Reporte HTML

**`scripts/dashboard.py`:**

```python
"""
Genera dashboard HTML de seguridad
"""
import json
from parser import parse_logs, detect_brute_force
from classifier import generate_threat_report, classify_threat_level, categorize_threat


def generate_html_report(events, output_path='output/security_report.html'):
    """Genera reporte HTML"""
    
    report = generate_threat_report(events)
    threats = detect_brute_force(events)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Wayne Security - Reporte de Ciberseguridad</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .header {{ text-align: center; border-bottom: 3px solid #e94560; padding-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #16213e; padding: 20px; border-radius: 8px; text-align: center; }}
        .critical {{ border-left: 4px solid #ff0000; }}
        .high {{ border-left: 4px solid #ff6b00; }}
        .medium {{ border-left: 4px solid #ffd700; }}
        .low {{ border-left: 4px solid #00ff00; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
        th {{ background: #0f3460; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Wayne Security Dashboard</h1>
        <p>Sistema de Monitoreo de Ciberseguridad - Baticueva</p>
        <p>Generado: 2024-04-13</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h3>{report['total_events']}</h3>
            <p>Eventos Totales</p>
        </div>
        <div class="stat-box critical">
            <h3>{report['threats_by_level']['CRÍTICA']}</h3>
            <p>Amenazas Críticas</p>
        </div>
        <div class="stat-box high">
            <h3>{report['threats_by_level']['ALTA']}</h3>
            <p>Amenazas Altas</p>
        </div>
        <div class="stat-box medium">
            <h3>{report['threats_by_level']['MEDIA']}</h3>
            <p>Amenazas Medias</p>
        </div>
    </div>
    
    <h2>🚨 Amenazas Detectadas</h2>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>IP Origen</th>
            <th>Tipo Ataque</th>
            <th>Nivel</th>
            <th>Score</th>
        </tr>
"""
    
    for event in events:
        score = classify_threat_level(event)
        level, _ = categorize_threat(event, score)
        
        from parser import detect_attack_type
        attack = detect_attack_type(event)
        
        css_class = ''
        if level == 'CRÍTICA':
            css_class = 'critical'
        elif level == 'ALTA':
            css_class = 'high'
        elif level == 'MEDIA':
            css_class = 'medium'
        
        html += f"""
        <tr class="{css_class}">
            <td>{event['timestamp']}</td>
            <td>{event['ip']}</td>
            <td>{attack}</td>
            <td><span class="badge" style="background: {'#ff0000' if level=='CRÍTICA' else '#ff6b00' if level=='ALTA' else '#ffd700'};">{level}</span></td>
            <td>{score}/10</td>
        </tr>
"""
    
    html += """
    </table>
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✅ Reporte HTML generado: {output_path}")


if __name__ == "__main__":
    events = parse_logs('../logs/security_logs_raw.csv')
    generate_html_report(events)
```

---

### Paso 6: Pipeline Completo

**`scripts/run_security_etl.py`:**

```python
"""
Pipeline completo de ciberseguridad
"""
from parser import parse_logs, detect_brute_force, detect_attack_type
from classifier import generate_threat_report, classify_threat_level, categorize_threat
from dashboard import generate_html_report
import json


def main():
    print("=" * 60)
    print("🛡️ WAYNE SECURITY - Sistema de Detección de Amenazas")
    print("=" * 60)
    
    # 1. Parsear logs
    print("\n📊 Analizando logs de seguridad...")
    events = parse_logs('../logs/security_logs_raw.csv')
    print(f"   Eventos cargados: {len(events)}")
    
    # 2. Detectar ataques
    print("\n🔍 Detectando patrones de ataque...")
    threats = detect_brute_force(events)
    
    print(f"\n   Amenazas detectadas:")
    for t in threats:
        print(f"   ⚠️  {t['tipo']} - IP: {t['ip']} ({t['intentos']} intentos)")
    
    # 3. Clasificar
    print("\n🤖 Clasificando nivel de amenazas...")
    critical = high = medium = low = 0
    
    for event in events:
        score = classify_threat_level(event)
        level, _ = categorize_threat(event, score)
        if level == 'CRÍTICA':
            critical += 1
        elif level == 'ALTA':
            high += 1
        elif level == 'MEDIA':
            medium += 1
        else:
            low += 1
    
    print(f"   Críticas: {critical} | Altas: {high} | Medias: {medium} | Bajas: {low}")
    
    # 4. Generar reportes
    print("\n📄 Generando reportes...")
    
    # JSON
    report = generate_threat_report(events)
    with open('../output/threats_detected.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # HTML
    generate_html_report(events)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 60)
    print("\nArchivos generados:")
    print("  📁 output/threats_detected.json")
    print("  📁 output/security_report.html")


if __name__ == "__main__":
    main()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout dana

# Agregar archivos
git add dana_cyber/
git commit -m "feat: agrega sistema de ciberseguridad con ML simple"
git push origin dana
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Logs de ejemplo generados
- [ ] `parser.py` detecta ataques
- [ ] `classifier.py` asigna scores
- [ ] `dashboard.py` genera HTML
- [ ] Pipeline completo funciona
- [ ] Reportes se generan correctamente
- [ ] Subido a GitHub

---

## Integración con Tech

Puedes vincular tu sistema a la app `tech`:

```python
# tech/views.py - Agregar vista de seguridad
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

@login_required
def security_dashboard(request):
    with open('dana_cyber/output/threats_detected.json') as f:
        threats = json.load(f)
    return render(request, 'tech/security.html', {'threats': threats})
```

Contacto: **Nicolás** - Coordinación
