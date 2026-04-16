# Guía Individual: Drada - Dataset #12

> **Responsable:** Drada  
> **ID:** #12  
> **Dataset:** Monitoreo de "Clean Energy"  
> **Descripción:** Rendimiento del reactor de fusión de Wayne. ETL de datos ambientales y sostenibilidad.  
> **Rama Git:** `drada`  

---

## ¿Qué es tu Dataset?

Tu trabajo es crear un **sistema de monitoreo de energía limpia** que procese:

- **Datos del reactor de fusión** de Wayne Energy
- **Métricas ambientales** (CO2 evitado, eficiencia)
- **Producción energética** en tiempo real
- **Alertas de mantenimiento** y anomalías

**Ejemplo real:** Como un SCADA (Sistema de Control y Adquisición de Datos) de una planta de energía.

---

## Paso a Paso: Crear tu Sistema de Monitoreo

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p drada_energy/{sensors,data,scripts,dashboard}
cd drada_energy

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
drada_energy/
├── sensors/
│   └── reactor_logs.csv       # Datos del reactor
├── data/
│   ├── energy_production.json # Producción por hora
│   └── environmental.json     # Métricas ambientales
├── scripts/
│   ├── data_collector.py      # Recolectar datos
│   ├── efficiency_analyzer.py # Análisis de eficiencia
│   └── alert_system.py        # Sistema de alertas
└── dashboard/
    └── energy_dashboard.html  # Panel de monitoreo
```

---

### Paso 2: Datos del Reactor

**`sensors/reactor_logs.csv`:**

```csv
fecha,hora,temperatura_core,pression_bar,energia_mw,eficiencia_pct,estado,alarma
2024-04-01,00:00,150000000,2.5,450,98.5,operando,normal
2024-04-01,01:00,151000000,2.6,455,98.2,operando,normal
2024-04-01,02:00,152000000,2.8,460,97.8,operando,normal
2024-04-01,03:00,155000000,3.2,470,96.5,operando,advertencia
2024-04-01,04:00,149000000,2.4,448,98.8,operando,normal
2024-04-01,05:00,148500000,2.3,445,99.0,operando,normal
2024-04-01,06:00,150500000,2.7,452,98.0,operando,normal
2024-04-01,07:00,156000000,3.5,475,95.5,operando,advertencia
2024-04-01,08:00,160000000,4.0,490,93.2,operando,critico
2024-04-01,09:00,149500000,2.4,447,98.9,operando,normal
2024-04-01,10:00,150200000,2.5,451,98.4,operando,normal
2024-04-01,11:00,151500000,2.9,458,97.5,operando,normal
```

**`data/energy_production.json`:**

```json
{
  "reactor_id": "WAYNE-FUSION-001",
  "ubicacion": "Wayne Energy Plant, Gotham",
  "capacidad_total_mw": 500,
  "produccion_diaria": [
    {"hora": "00:00", "mw": 450, "demanda": 420, "excedente": 30},
    {"hora": "01:00", "mw": 455, "demanda": 410, "excedente": 45},
    {"hora": "02:00", "mw": 460, "demanda": 400, "excedente": 60},
    {"hora": "03:00", "mw": 470, "demanda": 390, "excedente": 80},
    {"hora": "04:00", "mw": 448, "demanda": 380, "excedente": 68},
    {"hora": "05:00", "mw": 445, "demanda": 395, "excedente": 50},
    {"hora": "06:00", "mw": 452, "demanda": 450, "excedente": 2},
    {"hora": "07:00", "mw": 475, "demanda": 480, "deficit": 5},
    {"hora": "08:00", "mw": 490, "demanda": 520, "deficit": 30},
    {"hora": "09:00", "mw": 447, "demanda": 510, "deficit": 63},
    {"hora": "10:00", "mw": 451, "demanda": 500, "deficit": 49},
    {"hora": "11:00", "mw": 458, "demanda": 490, "deficit": 32}
  ],
  "estadisticas": {
    "produccion_promedio_mw": 458.5,
    "eficiencia_promedio": 97.2,
    "horas_operacion": 24,
    "energia_total_mwh": 11004
  }
}
```

**`data/environmental.json`:**

```json
{
  "metricas_ambientales": {
    "co2_evitado_ton": 1250,
    "comparacion_carbon": "Equivalente a sacar 270 autos de circulación",
    "ahorro_agua_m3": 50000,
    "tiempo_recuperacion_energia": "18 meses"
  },
  "objetivos_sostenibilidad": {
    "carbono_neutro_fecha": "2030-01-01",
    "reduccion_emisiones_pct": 100,
    "energia_renovable_pct": 95,
    "progreso_actual": 87
  },
  "impacto_comunidad": [
    {
      "area": "Gotham Downtown",
      "energia_suministrada_pct": 65,
      "hogares_beneficiados": 125000
    },
    {
      "area": "Gotham Industrial",
      "energia_suministrada_pct": 80,
      "empresas_beneficiadas": 450
    },
    {
      "area": "Arkham District",
      "energia_suministrada_pct": 45,
      "hogares_beneficiados": 35000
    }
  ]
}
```

---

### Paso 3: Recolector de Datos

**`scripts/data_collector.py`:**

```python
"""
Recolector de datos del reactor de fusión
"""
import csv
import json
from datetime import datetime


def load_reactor_logs(filepath='sensors/reactor_logs.csv'):
    """Carga logs del reactor"""
    logs = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            logs.append({
                'fecha': row['fecha'],
                'hora': row['hora'],
                'temperatura_core': float(row['temperatura_core']),
                'pression_bar': float(row['pression_bar']),
                'energia_mw': float(row['energia_mw']),
                'eficiencia_pct': float(row['eficiencia_pct']),
                'estado': row['estado'],
                'alarma': row['alarma']
            })
    return logs


def load_energy_production(filepath='data/energy_production.json'):
    """Carga datos de producción"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_environmental_data(filepath='data/environmental.json'):
    """Carga métricas ambientales"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def calculate_daily_stats(logs):
    """Calcula estadísticas del día"""
    if not logs:
        return {}
    
    energias = [log['energia_mw'] for log in logs]
    eficiencias = [log['eficiencia_pct'] for log in logs]
    temperaturas = [log['temperatura_core'] for log in logs]
    
    return {
        'energia_max': max(energias),
        'energia_min': min(energias),
        'energia_promedio': sum(energias) / len(energias),
        'energia_total_mwh': sum(energias),
        'eficiencia_promedio': sum(eficiencias) / len(eficiencias),
        'temperatura_max': max(temperaturas),
        'temperatura_min': min(temperaturas),
        'total_registros': len(logs)
    }


def detect_anomalies(logs):
    """Detecta anomalías en los datos"""
    anomalies = []
    
    for log in logs:
        # Temperatura muy alta
        if log['temperatura_core'] > 155000000:
            anomalies.append({
                'tipo': 'temperatura_alta',
                'timestamp': f"{log['fecha']} {log['hora']}",
                'valor': log['temperatura_core'],
                'umbral': 155000000,
                'nivel': 'critico' if log['temperatura_core'] > 158000000 else 'advertencia'
            })
        
        # Presión muy alta
        if log['pression_bar'] > 3.5:
            anomalies.append({
                'tipo': 'presion_alta',
                'timestamp': f"{log['fecha']} {log['hora']}",
                'valor': log['pression_bar'],
                'umbral': 3.5,
                'nivel': 'critico' if log['pression_bar'] > 4.0 else 'advertencia'
            })
        
        # Eficiencia baja
        if log['eficiencia_pct'] < 95.0:
            anomalies.append({
                'tipo': 'eficiencia_baja',
                'timestamp': f"{log['fecha']} {log['hora']}",
                'valor': log['eficiencia_pct'],
                'umbral': 95.0,
                'nivel': 'advertencia'
            })
    
    return anomalies


def generate_sensor_summary(logs, energy_data, env_data):
    """Genera resumen completo"""
    stats = calculate_daily_stats(logs)
    anomalies = detect_anomalies(logs)
    
    summary = {
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'reactor_id': energy_data.get('reactor_id', 'UNKNOWN'),
        'estadisticas_diarias': stats,
        'anomalias_detectadas': anomalies,
        'total_anomalias': len(anomalies),
        'impacto_ambiental': env_data.get('metricas_ambientales', {}),
        'objetivos': env_data.get('objetivos_sostenibilidad', {})
    }
    
    return summary


if __name__ == "__main__":
    print("=" * 60)
    print("⚡ WAYNE ENERGY - Recolector de Datos")
    print("=" * 60)
    
    # Cargar datos
    logs = load_reactor_logs()
    energy = load_energy_production()
    env = load_environmental_data()
    
    print(f"\n📊 Datos cargados:")
    print(f"   Logs del reactor: {len(logs)} registros")
    print(f"   Reactor: {energy.get('reactor_id')}")
    print(f"   Capacidad: {energy.get('capacidad_total_mw')} MW")
    
    # Calcular estadísticas
    stats = calculate_daily_stats(logs)
    print(f"\n📈 Estadísticas del día:")
    print(f"   Energía promedio: {stats['energia_promedio']:.2f} MW")
    print(f"   Eficiencia promedio: {stats['eficiencia_promedio']:.2f}%")
    print(f"   Temperatura máx: {stats['temperatura_max']:,.0f}°C")
    print(f"   Energía total: {stats['energia_total_mwh']:.2f} MWh")
    
    # Detectar anomalías
    anomalies = detect_anomalies(logs)
    print(f"\n⚠️  Anomalías detectadas: {len(anomalies)}")
    for anom in anomalies:
        print(f"   [{anom['nivel'].upper()}] {anom['tipo']}: {anom['valor']}")
    
    # Métricas ambientales
    print(f"\n🌱 Impacto ambiental:")
    impacto = env.get('metricas_ambientales', {})
    print(f"   CO2 evitado: {impacto.get('co2_evitado_ton')} toneladas")
    print(f"   {impacto.get('comparacion_carbon')}")
```

---

### Paso 4: Analizador de Eficiencia

**`scripts/efficiency_analyzer.py`:**

```python
"""
Analizador de eficiencia energética
"""
import json
from data_collector import load_reactor_logs, load_energy_production


def calculate_efficiency_trend(logs):
    """Calcula tendencia de eficiencia"""
    if len(logs) < 2:
        return "insuficiente"
    
    eficiencias = [log['eficiencia_pct'] for log in logs]
    
    # Calcular tendencia (simple)
    primera_mitad = sum(eficiencias[:len(eficiencias)//2]) / (len(eficiencias)//2)
    segunda_mitad = sum(eficiencias[len(eficiencias)//2:]) / (len(eficiencias) - len(eficiencias)//2)
    
    diferencia = segunda_mitad - primera_mitad
    
    if diferencia > 1:
        return "mejorando", diferencia
    elif diferencia < -1:
        return "degradando", diferencia
    else:
        return "estable", diferencia


def calculate_capacity_factor(logs, capacidad_max=500):
    """Calcula factor de capacidad"""
    energias = [log['energia_mw'] for log in logs]
    promedio = sum(energias) / len(energias)
    return (promedio / capacidad_max) * 100


def analyze_production_vs_demand(energy_data):
    """Analiza producción vs demanda"""
    produccion = energy_data.get('produccion_diaria', [])
    
    horas_deficit = 0
    horas_excedente = 0
    max_deficit = 0
    max_excedente = 0
    
    for hora in produccion:
        if 'deficit' in hora:
            horas_deficit += 1
            max_deficit = max(max_deficit, hora.get('deficit', 0))
        elif 'excedente' in hora:
            horas_excedente += 1
            max_excedente = max(max_excedente, hora.get('excedente', 0))
    
    return {
        'horas_deficit': horas_deficit,
        'horas_excedente': horas_excedente,
        'max_deficit_mw': max_deficit,
        'max_excedente_mw': max_excedente,
        'balance': 'positivo' if horas_excedente > horas_deficit else 'negativo'
    }


def generate_efficiency_report(logs, energy_data):
    """Genera reporte completo de eficiencia"""
    
    tendencia, diferencia = calculate_efficiency_trend(logs)
    factor_capacidad = calculate_capacity_factor(logs)
    balance = analyze_production_vs_demand(energy_data)
    
    eficiencias = [log['eficiencia_pct'] for log in logs]
    
    report = {
        'reactor': energy_data.get('reactor_id'),
        'fecha_analisis': '2024-04-01',
        'resumen': {
            'eficiencia_promedio': sum(eficiencias) / len(eficiencias),
            'eficiencia_max': max(eficiencias),
            'eficiencia_min': min(eficiencias),
            'tendencia': tendencia,
            'cambio_tendencia': diferencia
        },
        'factor_capacidad': factor_capacidad,
        'balance_demanda': balance,
        'recomendaciones': []
    }
    
    # Generar recomendaciones
    if tendencia == "degradando":
        report['recomendaciones'].append("Programar mantenimiento preventivo")
        report['recomendaciones'].append("Revisar sistema de refrigeración")
    
    if factor_capacidad < 90:
        report['recomendaciones'].append("Optimizar parámetros de operación")
    
    if balance['horas_deficit'] > 3:
        report['recomendaciones'].append("Considerar aumento de capacidad")
    
    return report


if __name__ == "__main__":
    logs = load_reactor_logs()
    energy = load_energy_production()
    
    print("=" * 60)
    print("📊 WAYNE ENERGY - Análisis de Eficiencia")
    print("=" * 60)
    
    report = generate_efficiency_report(logs, energy)
    
    print(f"\n⚡ Reactor: {report['reactor']}")
    print(f"📅 Fecha: {report['fecha_analisis']}")
    
    print(f"\n📈 Resumen de Eficiencia:")
    resumen = report['resumen']
    print(f"   Promedio: {resumen['eficiencia_promedio']:.2f}%")
    print(f"   Máxima: {resumen['eficiencia_max']:.2f}%")
    print(f"   Mínima: {resumen['eficiencia_min']:.2f}%")
    print(f"   Tendencia: {resumen['tendencia']} ({resumen['cambio_tendencia']:+.2f}%)")
    
    print(f"\n🏭 Factor de Capacidad: {report['factor_capacidad']:.2f}%")
    
    balance = report['balance_demanda']
    print(f"\n⚖️  Balance Demanda:")
    print(f"   Horas con déficit: {balance['horas_deficit']}")
    print(f"   Horas con excedente: {balance['horas_excedente']}")
    print(f"   Resultado: {balance['balance']}")
    
    if report['recomendaciones']:
        print(f"\n💡 Recomendaciones:")
        for rec in report['recomendaciones']:
            print(f"   • {rec}")
    else:
        print(f"\n✅ Sistema operando dentro de parámetros normales")
```

---

### Paso 5: Sistema de Alertas

**`scripts/alert_system.py`:**

```python
"""
Sistema de alertas para el reactor
"""
import json
from data_collector import load_reactor_logs, detect_anomalies


class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'temperatura': {'advertencia': 155000000, 'critico': 158000000},
            'presion': {'advertencia': 3.5, 'critico': 4.0},
            'eficiencia': {'advertencia': 95.0, 'critico': 90.0}
        }
    
    def check_temperature(self, log):
        """Verifica temperatura"""
        temp = log['temperatura_core']
        
        if temp > self.thresholds['temperatura']['critico']:
            return {
                'tipo': 'CRÍTICA',
                'sensor': 'temperatura_core',
                'valor': temp,
                'mensaje': f'Temperatura CRÍTICA: {temp:,.0f}°C',
                'accion': 'Reducir inmediatamente potencia del reactor'
            }
        elif temp > self.thresholds['temperatura']['advertencia']:
            return {
                'tipo': 'ADVERTENCIA',
                'sensor': 'temperatura_core',
                'valor': temp,
                'mensaje': f'Temperatura elevada: {temp:,.0f}°C',
                'accion': 'Monitorear sistema de refrigeración'
            }
        return None
    
    def check_pressure(self, log):
        """Verifica presión"""
        pres = log['pression_bar']
        
        if pres > self.thresholds['presion']['critico']:
            return {
                'tipo': 'CRÍTICA',
                'sensor': 'pression_bar',
                'valor': pres,
                'mensaje': f'Presión CRÍTICA: {pres} bar',
                'accion': 'Activar válvulas de alivio de emergencia'
            }
        elif pres > self.thresholds['presion']['advertencia']:
            return {
                'tipo': 'ADVERTENCIA',
                'sensor': 'pression_bar',
                'valor': pres,
                'mensaje': f'Presión elevada: {pres} bar',
                'accion': 'Verificar sellos y conexiones'
            }
        return None
    
    def check_efficiency(self, log):
        """Verifica eficiencia"""
        efic = log['eficiencia_pct']
        
        if efic < self.thresholds['eficiencia']['critico']:
            return {
                'tipo': 'CRÍTICA',
                'sensor': 'eficiencia_pct',
                'valor': efic,
                'mensaje': f'Eficiencia CRÍTICA: {efic}%',
                'accion': 'Detener reactor para inspección'
            }
        elif efic < self.thresholds['eficiencia']['advertencia']:
            return {
                'tipo': 'ADVERTENCIA',
                'sensor': 'eficiencia_pct',
                'valor': efic,
                'mensaje': f'Eficiencia baja: {efic}%',
                'accion': 'Revisar calibración de sensores'
            }
        return None
    
    def process_logs(self, logs):
        """Procesa todos los logs y genera alertas"""
        for log in logs:
            for check in [self.check_temperature, self.check_pressure, self.check_efficiency]:
                alert = check(log)
                if alert:
                    alert['timestamp'] = f"{log['fecha']} {log['hora']}"
                    self.alerts.append(alert)
        
        return self.alerts
    
    def generate_alert_report(self):
        """Genera reporte de alertas"""
        critica = [a for a in self.alerts if a['tipo'] == 'CRÍTICA']
        advertencia = [a for a in self.alerts if a['tipo'] == 'ADVERTENCIA']
        
        return {
            'total_alertas': len(self.alerts),
            'criticas': critica,
            'advertencias': advertencia,
            'resumen': {
                'total_criticas': len(critica),
                'total_advertencias': len(advertencia)
            }
        }


def main():
    print("=" * 60)
    print("🚨 WAYNE ENERGY - Sistema de Alertas")
    print("=" * 60)
    
    logs = load_reactor_logs()
    alert_system = AlertSystem()
    alert_system.process_logs(logs)
    
    report = alert_system.generate_alert_report()
    
    print(f"\n📊 Resumen de Alertas:")
    print(f"   Total: {report['total_alertas']}")
    print(f"   Críticas: {report['resumen']['total_criticas']}")
    print(f"   Advertencias: {report['resumen']['total_advertencias']}")
    
    if report['criticas']:
        print(f"\n🚨 ALERTAS CRÍTICAS:")
        for alert in report['criticas']:
            print(f"   [{alert['timestamp']}] {alert['mensaje']}")
            print(f"   Acción: {alert['accion']}")
    
    if report['advertencias']:
        print(f"\n⚠️  ADVERTENCIAS:")
        for alert in report['advertencias']:
            print(f"   [{alert['timestamp']}] {alert['mensaje']}")
            print(f"   Acción: {alert['accion']}")
    
    if not report['criticas'] and not report['advertencias']:
        print(f"\n✅ No hay alertas activas. Sistema funcionando normalmente.")


if __name__ == "__main__":
    main()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout drada

# Agregar archivos
git add drada_energy/
git commit -m "feat: agrega sistema de monitoreo de energía Clean Energy"
git push origin drada
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Datos del reactor (`reactor_logs.csv`)
- [ ] Datos de producción (`energy_production.json`)
- [ ] Datos ambientales (`environmental.json`)
- [ ] `data_collector.py` funcionando
- [ ] `efficiency_analyzer.py` con análisis
- [ ] `alert_system.py` detecta anomalías
- [ ] Sistema genera alertas correctamente
- [ ] Subir a GitHub

---

## Integración

Puedes vincular tu sistema a `industries` o `tech`:

```python
# industries/views.py
from django.shortcuts import render
import json

@login_required
def energy_monitor(request):
    with open('drada_energy/dashboard/summary.json') as f:
        data = json.load(f)
    return render(request, 'industries/energy.html', data)
```

Contacto: **Nicolás** - Coordinación
