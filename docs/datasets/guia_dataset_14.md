# Guía Individual: Dataset #14 - Logística de Wayne Shipping

> **Responsable:** *Por asignar*  
> **ID:** #14  
> **Dataset:** Logística de Wayne Shipping  
> **Descripción:** Movimiento de barcos en los muelles de Gotham. Optimización de rutas marítimas.  
> **Rama Git:** `dataset_14`  

---

## ¿Qué es este Dataset?

Tu trabajo es crear un **sistema de optimización de logística marítima** que procese:

- **Movimiento de barcos** en los muelles de Gotham
- **Rutas de envío** internacionales
- **Optimización de tiempos** y costos
- **Monitoreo de carga** y descarga

**Ejemplo real:** Como el sistema Port Management para control de puertos.

---

## Paso a Paso: Crear tu Sistema de Logística

### Paso 1: Crear Estructura

```bash
# Estás en Wayne-Enterprises/
mkdir -p dataset_14_shipping/{data/{routes,vessels},scripts,maps}
cd dataset_14_shipping

touch data/__init__.py
touch scripts/__init__.py
```

Estructura:
```
dataset_14_shipping/
├── data/
│   ├── routes/
│   │   ├── shipping_routes.csv    # Rutas marítimas
│   │   └── port_schedules.json    # Horarios de puertos
│   ├── vessels/
│   │   └── fleet_status.csv       # Estado de la flota
│   └── cargo/
│       └── manifest.json          # Manifiestos de carga
├── scripts/
│   ├── route_optimizer.py         # Optimizador de rutas
│   ├── port_scheduler.py          # Planificador de puertos
│   └── cost_calculator.py         # Calculadora de costos
└── maps/
    └── shipping_dashboard.html
```

---

### Paso 2: Datos de Rutas y Barcos

**`data/routes/shipping_routes.csv`:**

```csv
route_id,origin,destination,distance_nm,avg_time_days,base_cost_usd,vessel_type,frequency_per_week
RT001,Gotham Port,Rotterdam,3800,14,450000,Cargo Ship,3
RT002,Gotham Port,Singapore,9500,28,890000,Container Ship,2
RT003,Gotham Port,Los Angeles,5200,18,580000,Cargo Ship,4
RT004,Gotham Port,Santos,5200,16,620000,Bulk Carrier,2
RT005,Gotham Port,Shanghai,8800,24,820000,Container Ship,3
RT006,Gotham Port,Dubai,6200,20,680000,Cargo Ship,2
RT007,Gotham Port,Sydney,8500,22,750000,Container Ship,1
RT008,Gotham Port,Hamburg,4100,15,490000,Cargo Ship,3
RT009,Gotham Port,Mumbai,7200,19,710000,Cargo Ship,2
RT010,Gotham Port,Tokyo,9200,26,860000,Container Ship,2
```

**`data/routes/port_schedules.json`:**

```json
{
  "port_schedules": [
    {
      "port": "Gotham Port",
      "location": "Gotham, USA",
      "timezone": "EST",
      "berths": 12,
      "operating_hours": "24/7",
      "current_vessels": 8,
      "average_wait_hours": 6,
      "fees": {
        "docking_per_day": 5000,
        "loading_per_container": 150,
        "unloading_per_container": 150
      }
    },
    {
      "port": "Rotterdam",
      "location": "Netherlands",
      "timezone": "CET",
      "berths": 20,
      "operating_hours": "24/7",
      "current_vessels": 15,
      "average_wait_hours": 4,
      "fees": {
        "docking_per_day": 4500,
        "loading_per_container": 120,
        "unloading_per_container": 120
      }
    },
    {
      "port": "Singapore",
      "location": "Singapore",
      "timezone": "SGT",
      "berths": 25,
      "operating_hours": "24/7",
      "current_vessels": 22,
      "average_wait_hours": 8,
      "fees": {
        "docking_per_day": 6000,
        "loading_per_container": 180,
        "unloading_per_container": 180
      }
    },
    {
      "port": "Shanghai",
      "location": "China",
      "timezone": "CST",
      "berths": 30,
      "operating_hours": "24/7",
      "current_vessels": 28,
      "average_wait_hours": 12,
      "fees": {
        "docking_per_day": 5500,
        "loading_per_container": 100,
        "unloading_per_container": 100
      }
    }
  ]
}
```

**`data/vessels/fleet_status.csv`:**

```csv
vessel_id,name,type,capacity_teus,current_location,status,next_departure,destination,load_pct
VES001,Wayne Enterprise,Container Ship,8500,Gotham Port,Loading,2024-04-15 08:00,Rotterdam,78
VES002,Gotham Mariner,Cargo Ship,4200,Rotterdam,Unloading,2024-04-16 14:00,Gotham Port,85
VES003,Wayne Voyager,Container Ship,9200,Singapore,Loading,2024-04-17 06:00,Los Angeles,65
VES004,Wayne Merchant,Bulk Carrier,6800,Santos,Loading,2024-04-18 10:00,Gotham Port,92
VES005,Wayne Explorer,Container Ship,7800,Shanghai,Maintenance,2024-04-20 08:00,Dubai,45
VES006,Wayne Pioneer,Cargo Ship,5500,Dubai,At Sea,2024-04-14 16:00,Rotterdam,80
VES007,Wayne Atlantic,Container Ship,8200,At Sea,En Route,2024-04-13 20:00,Gotham Port,90
VES008,Wayne Pacific,Cargo Ship,4800,Tokyo,Loading,2024-04-19 12:00,Sydney,70
```

---

### Paso 3: Optimizador de Rutas

**`scripts/route_optimizer.py`:**

```python
"""
Optimizador de rutas marítimas para Wayne Shipping
"""
import csv
import json
from datetime import datetime, timedelta


def load_routes(filepath):
    """Carga rutas desde CSV"""
    routes = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            routes.append({
                'route_id': row['route_id'],
                'origin': row['origin'],
                'destination': row['destination'],
                'distance_nm': int(row['distance_nm']),
                'avg_time_days': int(row['avg_time_days']),
                'base_cost_usd': float(row['base_cost_usd']),
                'vessel_type': row['vessel_type'],
                'frequency_per_week': int(row['frequency_per_week'])
            })
    return routes


def load_port_schedules(filepath):
    """Carga horarios de puertos"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    schedules = {}
    for port in data['port_schedules']:
        schedules[port['port']] = port
    
    return schedules


def load_fleet(filepath):
    """Carga estado de la flota"""
    vessels = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vessels.append({
                'vessel_id': row['vessel_id'],
                'name': row['name'],
                'type': row['type'],
                'capacity_teus': int(row['capacity_teus']),
                'current_location': row['current_location'],
                'status': row['status'],
                'next_departure': row['next_departure'],
                'destination': row['destination'],
                'load_pct': int(row['load_pct'])
            })
    return vessels


def calculate_route_efficiency(route, origin_port, dest_port):
    """
    Calcula eficiencia de una ruta considerando múltiples factores
    """
    distance = route['distance_nm']
    time_days = route['avg_time_days']
    base_cost = route['base_cost_usd']
    
    # Obtener tiempos de espera en puertos
    wait_origin = origin_port.get('average_wait_hours', 6)
    wait_dest = dest_port.get('average_wait_hours', 6)
    total_wait_hours = wait_origin + wait_dest
    
    # Calcular costos totales
    origin_fees = origin_port.get('fees', {})
    dest_fees = dest_port.get('fees', {})
    
    docking_cost = (origin_fees.get('docking_per_day', 5000) + 
                   dest_fees.get('docking_per_day', 5000))
    
    total_cost = base_cost + docking_cost
    
    # Velocidad efectiva (considerando esperas)
    total_time_hours = (time_days * 24) + total_wait_hours
    effective_speed = distance / total_time_hours if total_time_hours > 0 else 0
    
    # Score de eficiencia (mayor es mejor)
    # Considera: velocidad, costo, frecuencia
    efficiency_score = (
        (effective_speed / 15) * 0.4 +  # Velocidad normalizada
        (1 / (total_cost / 500000)) * 0.4 +  # Costo inverso
        (route['frequency_per_week'] / 7) * 0.2  # Frecuencia
    )
    
    return {
        'total_cost': total_cost,
        'total_time_hours': total_time_hours,
        'effective_speed_knots': effective_speed,
        'wait_time_hours': total_wait_hours,
        'efficiency_score': round(efficiency_score, 2)
    }


def optimize_routes(routes, ports):
    """Optimiza todas las rutas y genera rankings"""
    optimized = []
    
    for route in routes:
        origin_port = ports.get(route['origin'], {})
        dest_port = ports.get(route['destination'], {})
        
        metrics = calculate_route_efficiency(route, origin_port, dest_port)
        
        optimized.append({
            **route,
            **metrics
        })
    
    # Ordenar por eficiencia
    optimized.sort(key=lambda x: x['efficiency_score'], reverse=True)
    
    return optimized


def find_best_route(routes, origin, destination):
    """Encuentra la mejor ruta entre dos puertos"""
    candidates = [r for r in routes 
                  if r['origin'] == origin and r['destination'] == destination]
    
    if not candidates:
        return None
    
    return max(candidates, key=lambda x: x['efficiency_score'])


def generate_optimization_report(optimized_routes):
    """Genera reporte de optimización"""
    
    total_routes = len(optimized_routes)
    avg_cost = sum(r['total_cost'] for r in optimized_routes) / total_routes
    avg_time = sum(r['total_time_hours'] for r in optimized_routes) / total_routes
    
    # Por tipo de barco
    by_vessel_type = {}
    for r in optimized_routes:
        vtype = r['vessel_type']
        if vtype not in by_vessel_type:
            by_vessel_type[vtype] = {'count': 0, 'avg_efficiency': 0}
        by_vessel_type[vtype]['count'] += 1
        by_vessel_type[vtype]['avg_efficiency'] += r['efficiency_score']
    
    for vtype in by_vessel_type:
        by_vessel_type[vtype]['avg_efficiency'] /= by_vessel_type[vtype]['count']
    
    return {
        'total_routes': total_routes,
        'avg_cost': avg_cost,
        'avg_time_hours': avg_time,
        'most_efficient_route': optimized_routes[0] if optimized_routes else None,
        'least_efficient_route': optimized_routes[-1] if optimized_routes else None,
        'by_vessel_type': by_vessel_type
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🚢 WAYNE SHIPPING - Optimizador de Rutas")
    print("=" * 60)
    
    # Cargar datos
    print("\n📥 Cargando datos...")
    routes = load_routes('data/routes/shipping_routes.csv')
    ports = load_port_schedules('data/routes/port_schedules.json')
    vessels = load_fleet('data/vessels/fleet_status.csv')
    
    print(f"   Rutas: {len(routes)}")
    print(f"   Puertos: {len(ports)}")
    print(f"   Barcos: {len(vessels)}")
    
    # Optimizar
    print("\n🧮 Optimizando rutas...")
    optimized = optimize_routes(routes, ports)
    
    # Mostrar top 5
    print("\n🏆 Top 5 Rutas más Eficientes:")
    for i, route in enumerate(optimized[:5], 1):
        print(f"\n   {i}. {route['origin']} → {route['destination']}")
        print(f"      Score: {route['efficiency_score']:.2f}")
        print(f"      Costo: ${route['total_cost']:,.0f}")
        print(f"      Tiempo: {route['total_time_hours']/24:.1f} días")
        print(f"      Tipo: {route['vessel_type']}")
    
    # Reporte
    report = generate_optimization_report(optimized)
    
    print(f"\n📊 Reporte General:")
    print(f"   Costo promedio: ${report['avg_cost']:,.0f}")
    print(f"   Tiempo promedio: {report['avg_time_hours']/24:.1f} días")
    
    if report['most_efficient_route']:
        best = report['most_efficient_route']
        print(f"\n   ✅ Ruta más eficiente: {best['origin']} → {best['destination']}")
        print(f"      Score: {best['efficiency_score']:.2f}")
    
    # Guardar
    with open('data/optimized_routes.json', 'w') as f:
        json.dump(optimized, f, indent=2)
    
    print("\n✅ Optimización guardada en data/optimized_routes.json")
```

---

### Paso 4: Reporte HTML

**`scripts/generate_dashboard.py`:**

```python
"""
Generador de dashboard HTML para Wayne Shipping
"""
import csv
import json


def load_data():
    with open('data/optimized_routes.json', 'r') as f:
        routes = json.load(f)
    
    vessels = []
    with open('data/vessels/fleet_status.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vessels.append(row)
    
    return routes, vessels


def generate_html():
    routes, vessels = load_data()
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Wayne Shipping - Operations Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #3b82f6; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 20px; border-radius: 10px; border: 1px solid #475569; }}
        .stat-value {{ font-size: 32px; color: #3b82f6; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #1e293b; }}
        th {{ background: #3b82f6; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #334155; }}
        .status-loading {{ color: #fbbf24; }}
        .status-sea {{ color: #3b82f6; }}
        .status-port {{ color: #10b981; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚢 Wayne Shipping Operations Dashboard</h1>
        <p>Control de rutas marítimas y flota</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{len(vessels)}</div>
                <div>Barcos Activos</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(routes)}</div>
                <div>Rutas Optimizadas</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{sum(int(v['capacity_teus']) for v in vessels):,}</div>
                <div>Capacidad Total (TEUs)</div>
            </div>
        </div>
        
        <h2>🚢 Estado de la Flota</h2>
        <table>
            <tr>
                <th>Barco</th>
                <th>Tipo</th>
                <th>Ubicación</th>
                <th>Estado</th>
                <th>Destino</th>
                <th>Carga</th>
            </tr>
"""
    
    for v in vessels:
        status_class = {
            'Loading': 'status-loading',
            'Unloading': 'status-loading',
            'At Sea': 'status-sea',
            'En Route': 'status-sea'
        }.get(v['status'], 'status-port')
        
        html += f"""
            <tr>
                <td><strong>{v['vessel_id']}</strong><br><small>{v['name']}</small></td>
                <td>{v['type']}</td>
                <td>{v['current_location']}</td>
                <td class="{status_class}">{v['status']}</td>
                <td>{v['destination']}</td>
                <td>{v['load_pct']}%</td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>🗺️ Top Rutas Optimizadas</h2>
        <table>
            <tr>
                <th>Ruta</th>
                <th>Distancia</th>
                <th>Tiempo Est.</th>
                <th>Costo Total</th>
                <th>Eficiencia</th>
            </tr>
"""
    
    for route in routes[:8]:
        html += f"""
            <tr>
                <td>{route['origin']} → {route['destination']}</td>
                <td>{route['distance_nm']:,} nm</td>
                <td>{route['total_time_hours']/24:.1f} días</td>
                <td>${route['total_cost']:,.0f}</td>
                <td>{route['efficiency_score']:.2f}</td>
            </tr>
"""
    
    html += """
        </table>
    </div>
</body>
</html>
"""
    
    with open('maps/shipping_dashboard.html', 'w') as f:
        f.write(html)
    
    print("✅ Dashboard generado: maps/shipping_dashboard.html")


if __name__ == "__main__":
    generate_html()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout dataset_14

# Agregar archivos
git add dataset_14_shipping/
git commit -m "feat: agrega sistema de logística marítima y optimización"
git push origin dataset_14
```

---

## Checklist

- [ ] Estructura de carpetas creada
- [ ] Archivo CSV con rutas de envío
- [ ] Archivo JSON con horarios de puertos
- [ ] Archivo CSV con estado de la flota
- [ ] `route_optimizer.py` funciona
- [ ] Optimización genera scores de eficiencia
- [ ] Dashboard HTML creado
- [ ] Subir a GitHub

---

## Integración

Puedes vincular este sistema a `industries`:

```python
# industries/views.py
import json
from django.shortcuts import render

@login_required
def shipping_logistics(request):
    with open('dataset_14_shipping/data/optimized_routes.json') as f:
        routes = json.load(f)
    return render(request, 'industries/shipping.html', {'routes': routes})
```
