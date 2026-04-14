# Guía Individual: Emerick - Dataset #4

> **Responsable:** Emerick  
> **ID:** #4  
> **Dataset:** Donaciones de la Fundación Wayne  
> **Descripción:** Registro de ayuda a orfanatos y hospitales. Consolidación de datos de responsabilidad social.  
> **Rama Git:** `emerick`  

---

## ¿Qué es tu Dataset?

Tu trabajo es crear un **sistema ETL** para las donaciones de Wayne Foundation. Debes procesar:

- **Registros de donaciones** a orfanatos
- **Ayuda a hospitales** públicos
- **Becas educativas** otorgadas
- **Proyectos comunitarios** financiados

**Ejemplo real:** Como un sistema que rastrea cuánto dinero dona la fundación y a quién beneficia.

---

## Paso a Paso: Crear tu Sistema ETL

### Paso 1: Crear Estructura de Carpetas

```bash
# Estás en Wayne-Enterprises/
mkdir -p emerick_etl/{data,scripts,output}
cd emerick_etl

# Crear carpetas
touch data/__init__.py
touch scripts/__init__.py
```

Estructura final:
```
emerick_etl/
├── data/
│   ├── raw/              # Datos sin procesar
│   │   ├── donaciones_orfanatos.csv
│   │   ├── ayuda_hospitales.json
│   │   └── becas_educativas.xlsx
│   └── processed/        # Datos limpios
├── scripts/
│   ├── extract.py        # Extraer datos
│   ├── transform.py      # Limpiar y transformar
│   └── load.py           # Cargar a database
└── output/
    └── reporte_donaciones.json
```

---

### Paso 2: Datos Fuente (RAW)

Crea estos archivos de ejemplo en `data/raw/`:

**`donaciones_orfanatos.csv`:**
```csv
id,fecha,orfanato,monto,categoria,estado
1,2024-01-15,Orfanato Gotham Central,50000,alimentos,completado
2,2024-02-01,Hogar Niños Wayne,75000,educacion,completado
3,2024-02-20,Albergue Juvenil,25000,ropa,pendiente
4,2024-03-10,Centro Esperanza,100000,construccion,completado
5,2024-03-15,Orfanato Robinson,45000,tecnologia,procesando
```

**`ayuda_hospitales.json`:**
```json
[
  {
    "hospital": "Hospital General Gotham",
    "tipo_ayuda": "equipamiento",
    "monto": 250000,
    "fecha": "2024-01-20",
    "estado": "entregado"
  },
  {
    "hospital": "Clinica Arkham",
    "tipo_ayuda": "medicamentos",
    "monto": 150000,
    "fecha": "2024-02-15",
    "estado": "entregado"
  },
  {
    "hospital": "Centro Pediatrico",
    "tipo_ayuda": "investigacion",
    "monto": 500000,
    "fecha": "2024-03-01",
    "estado": "pendiente"
  }
]
```

---

### Paso 3: Script Extract (Extraer)

**`scripts/extract.py`:**

```python
"""
Script para EXTRAER datos de múltiples fuentes
"""
import csv
import json


def extract_csv(filepath):
    """Extrae datos de archivo CSV"""
    datos = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            datos.append(dict(row))
    print(f"Extraídos {len(datos)} registros de CSV")
    return datos


def extract_json(filepath):
    """Extrae datos de archivo JSON"""
    with open(filepath, 'r', encoding='utf-8') as file:
        datos = json.load(file)
    print(f"Extraídos {len(datos)} registros de JSON")
    return datos


# Ejecutar extracción
if __name__ == "__main__":
    orfanatos = extract_csv('data/raw/donaciones_orfanatos.csv')
    hospitales = extract_json('data/raw/ayuda_hospitales.json')
    
    print("\n--- Muestra de datos extraídos ---")
    print(f"Orfanatos: {orfanatos[0] if orfanatos else 'Ninguno'}")
    print(f"Hospitales: {hospitales[0] if hospitales else 'Ninguno'}")
```

---

### Paso 4: Script Transform (Transformar)

**`scripts/transform.py`:**

```python
"""
Script para TRANSFORMAR y limpiar datos
"""
import json
from datetime import datetime


def clean_monto(monto_str):
    """Convierte monto a número"""
    try:
        return float(monto_str)
    except:
        return 0.0


def validate_fecha(fecha_str):
    """Valida formato de fecha"""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_str
    except:
        return None


def transform_donaciones(orfanatos, hospitales):
    """
    Transforma datos crudos en formato estandarizado
    """
    donaciones_unificadas = []
    
    # Transformar orfanatos
    for registro in orfanatos:
        donaciones_unificadas.append({
            'id': int(registro['id']),
            'fecha': validate_fecha(registro['fecha']),
            'beneficiario': registro['orfanato'],
            'tipo': 'orfanato',
            'categoria': registro['categoria'],
            'monto_usd': clean_monto(registro['monto']),
            'estado': registro['estado'],
            'fuente': 'csv_orfanatos'
        })
    
    # Transformar hospitales
    for i, registro in enumerate(hospitales, start=100):
        donaciones_unificadas.append({
            'id': i,
            'fecha': validate_fecha(registro['fecha']),
            'beneficiario': registro['hospital'],
            'tipo': 'hospital',
            'categoria': registro['tipo_ayuda'],
            'monto_usd': float(registro['monto']),
            'estado': registro['estado'],
            'fuente': 'json_hospitales'
        })
    
    return donaciones_unificadas


def calculate_totals(donaciones):
    """Calcula totales por categoría"""
    totales = {}
    for d in donaciones:
        cat = d['categoria']
        if cat not in totales:
            totales[cat] = {'count': 0, 'total': 0}
        totales[cat]['count'] += 1
        totales[cat]['total'] += d['monto_usd']
    return totales


# Ejecutar transformación
if __name__ == "__main__":
    # Simular datos extraídos
    orfanatos = [
        {'id': '1', 'fecha': '2024-01-15', 'orfanato': 'Orfanato Gotham', 
         'monto': '50000', 'categoria': 'alimentos', 'estado': 'completado'}
    ]
    
    hospitales = [
        {'hospital': 'Hospital General', 'tipo_ayuda': 'equipamiento', 
         'monto': 250000, 'fecha': '2024-01-20', 'estado': 'entregado'}
    ]
    
    datos_limpios = transform_donaciones(orfanatos, hospitales)
    totales = calculate_totals(datos_limpios)
    
    print("Datos transformados:", len(datos_limpios))
    print("Totales por categoría:", totales)
```

---

### Paso 5: Script Load (Cargar)

**`scripts/load.py`:**

```python
"""
Script para CARGAR datos transformados
"""
import json
import csv


def load_to_json(datos, filepath):
    """Guarda datos en archivo JSON"""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(datos, file, indent=2, ensure_ascii=False)
    print(f"Guardados {len(datos)} registros en {filepath}")


def load_to_csv(datos, filepath):
    """Guarda datos en archivo CSV"""
    if not datos:
        print("No hay datos para guardar")
        return
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)
    print(f"Guardados {len(datos)} registros en {filepath}")


def generate_report(datos, totales):
    """Genera reporte resumen"""
    reporte = {
        'fecha_generacion': '2024-04-13',
        'total_donaciones': len(datos),
        'monto_total': sum(d['monto_usd'] for d in datos),
        'por_categoria': totales,
        'donaciones': datos
    }
    return reporte


# Ejecutar carga
if __name__ == "__main__":
    # Datos de ejemplo transformados
    datos = [
        {
            'id': 1,
            'fecha': '2024-01-15',
            'beneficiario': 'Orfanato Gotham',
            'tipo': 'orfanato',
            'categoria': 'alimentos',
            'monto_usd': 50000.0,
            'estado': 'completado',
            'fuente': 'csv_orfanatos'
        }
    ]
    
    totales = {'alimentos': {'count': 1, 'total': 50000.0}}
    
    # Cargar a archivos
    load_to_json(datos, 'output/donaciones_limpias.json')
    load_to_csv(datos, 'output/donaciones_limpias.csv')
    
    # Generar reporte
    reporte = generate_report(datos, totales)
    load_to_json(reporte, 'output/reporte_completo.json')
    
    print("\n✅ ETL completado exitosamente!")
```

---

### Paso 6: Pipeline Completo (Ejecutar Todo)

**`scripts/run_etl.py`:**

```python
"""
Pipeline completo ETL
Ejecuta: python scripts/run_etl.py
"""
from extract import extract_csv, extract_json
from transform import transform_donaciones, calculate_totals
from load import load_to_json, load_to_csv, generate_report


def main():
    print("=" * 50)
    print("ETL WAYNE FOUNDATION - Donaciones")
    print("=" * 50)
    
    # 1. EXTRACT
    print("\n📥 PASO 1: EXTRAYENDO DATOS...")
    orfanatos = extract_csv('data/raw/donaciones_orfanatos.csv')
    hospitales = extract_json('data/raw/ayuda_hospitales.json')
    
    # 2. TRANSFORM
    print("\n🔧 PASO 2: TRANSFORMANDO DATOS...")
    datos_limpios = transform_donaciones(orfanatos, hospitales)
    totales = calculate_totals(datos_limpios)
    
    print(f"   - Registros transformados: {len(datos_limpios)}")
    print(f"   - Categorías encontradas: {list(totales.keys())}")
    
    # 3. LOAD
    print("\n💾 PASO 3: CARGANDO DATOS...")
    load_to_json(datos_limpios, 'output/donaciones_limpias.json')
    load_to_csv(datos_limpios, 'output/donaciones_limpias.csv')
    
    # Generar reporte
    reporte = generate_report(datos_limpios, totales)
    load_to_json(reporte, 'output/reporte_completo.json')
    
    # Resumen
    print("\n" + "=" * 50)
    print("✅ ETL COMPLETADO")
    print("=" * 50)
    print(f"Total donaciones procesadas: {len(datos_limpios)}")
    print(f"Monto total: ${sum(d['monto_usd'] for d in datos_limpios):,.2f}")
    print(f"\nArchivos generados:")
    print(f"  - output/donaciones_limpias.json")
    print(f"  - output/donaciones_limpias.csv")
    print(f"  - output/reporte_completo.json")


if __name__ == "__main__":
    main()
```

---

## Trabajo en Git

```bash
# Cambiar a tu rama
git checkout emerick

# Agregar archivos
git add emerick_etl/

# Commit
git commit -m "feat: agrega sistema ETL para donaciones Wayne Foundation"

# Push
git push origin emerick
```

---

## Checklist

- [ ] Crear estructura de carpetas `emerick_etl/`
- [ ] Crear datos de ejemplo (CSV + JSON)
- [ ] Script `extract.py` funcionando
- [ ] Script `transform.py` funcionando
- [ ] Script `load.py` funcionando
- [ ] Pipeline `run_etl.py` que ejecuta todo
- [ ] Generar reporte final con totales
- [ ] Subir a GitHub

---

## Integración con Django

Puedes integrar tu ETL a la app `foundation`:

```python
# En foundation/views.py, agregar:
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def reporte_donaciones(request):
    with open('emerick_etl/output/reporte_completo.json') as f:
        reporte = json.load(f)
    
    return render(request, 'foundation/reporte.html', {
        'total_donaciones': reporte['total_donaciones'],
        'monto_total': reporte['monto_total'],
        'por_categoria': reporte['por_categoria'],
        'donaciones': reporte['donaciones']
    })
```

---

## Ayuda

¿Problemas?
- Verifica que los archivos CSV tengan codificación UTF-8
- Revisa que las fechas estén en formato YYYY-MM-DD
- Asegúrate de crear la carpeta `output/` antes de ejecutar

Contacto: **Nicolás** - Coordinación
