# Guía Individual: Diego Granja - Wayne Industries

> **Responsable:** Diego Granja  
> **División:** Wayne Industries (industries)  
> **Estado:** 🔴 PENDIENTE - App no creada  
> **Rama Git:** `diego_granja`  
> **ID Trabajo:** #2

---

## ¿Qué es Wayne Industries?

Wayne Industries es la división de manufactura y producción masiva del conglomerado. Es el brazo industrial que produce:

- **Componentes automotrices:** Motores, baterías, sistemas eléctricos
- **Maquinaria pesada:** Equipos de construcción, minería, agricultura
- **Aeroespacial:** Partes para aviones y drones comerciales
- **Energía:** Turbinas eólicas, paneles solares, baterías industriales
- **Textiles industriales:** Materiales avanzados, kevlar, fibras sintéticas

**Ejemplo real:** Como Toyota o General Motors pero dentro del universo Wayne.

---

## Dataset para Industries

Tu dataset debe incluir **productos manufacturados** con datos como:

### Ejemplo de Producto

```json
{
  "nombre": "Motor Eléctrico Industrial W-500",
  "codigo": "IND-MOT-500",
  "categoria": "motores",
  "precio": 45000.00,
  "stock": 120,
  "descripcion": "Motor eléctrico de alta eficiencia...",
  "peso_kg": 850.5,
  "fabricado_en": "Planta Gotham Norte",
  "certificacion_iso": true
}
```

### Categorías Sugeridas

| Categoría | Ejemplos de Productos |
|-----------|----------------------|
| `motores` | Eléctricos, combustion, híbridos |
| `baterias` | Industriales, automotrices, portátiles |
| `maquinaria` | Excavadoras, grúas, tractores |
| `componentes` | Transmisiones, frenos, suspensión |
| `aerospace` | Turbinas, sistemas de navegación |
| `energia` | Turbinas eólicas, inversores |

---

## Paso a Paso: Crear tu App

### Paso 1: Crear Estructura

En la terminal de VS Code (estando en `Wayne-Enterprises/`):

```bash
mkdir industries
cd industries

mkdir migrations
echo "" > migrations/__init__.py

mkdir -p templates/industries
mkdir -p static/industries/css
mkdir -p static/industries/js
mkdir fixtures

cd ..
```

### Paso 2: Archivos Básicos

**`industries/__init__.py`**:
```python
# Wayne Industries App
```

**`industries/apps.py`**:
```python
from django.apps import AppConfig

class IndustriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'industries'
    verbose_name = 'Wayne Industries'
```

### Paso 3: Modelo de Datos (Dataset)

**`industries/models.py`**:

```python
from django.db import models


class Producto(models.Model):
    """Productos manufacturados por Wayne Industries"""
    
    CATEGORIAS = [
        ('motores', 'Motores'),
        ('baterias', 'Baterías'),
        ('maquinaria', 'Maquinaria Pesada'),
        ('componentes', 'Componentes Automotrices'),
        ('aerospace', 'Aeroespacial'),
        ('energia', 'Energía Renovable'),
        ('textiles', 'Textiles Industriales'),
    ]
    
    nombre = models.CharField(max_length=200)
    codigo_sku = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    descripcion = models.TextField()
    
    # Datos comerciales
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    costo_produccion = models.DecimalField(max_digits=12, decimal_places=2)
    stock_unidades = models.PositiveIntegerField(default=0)
    
    # Especificaciones técnicas
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2)
    dimensiones = models.CharField(max_length=100, help_text="Largo x Ancho x Alto")
    capacidad = models.CharField(max_length=100, blank=True, help_text="Ej: 500 HP, 1000L")
    
    # Producción
    fabricado_en = models.CharField(max_length=200)
    fecha_produccion = models.DateField()
    certificacion_iso = models.BooleanField(default=True)
    garantia_meses = models.PositiveIntegerField(default=12)
    
    # Estado
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='industries/productos/', blank=True, null=True)
    
    # Metadata
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto Industrial'
        verbose_name_plural = 'Productos Industriales'
        ordering = ['-destacado', 'nombre']
    
    def __str__(self):
        return f"{self.codigo_sku} - {self.nombre}"
    
    @property
    def margen_ganancia(self):
        """Calcula el margen de ganancia"""
        if self.costo_produccion > 0:
            return ((self.precio - self.costo_produccion) / self.costo_produccion) * 100
        return 0


class PlantaProduccion(models.Model):
    """Plantas de manufactura de Wayne Industries"""
    
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=300)
    empleados = models.PositiveIntegerField()
    capacidad_diaria = models.PositiveIntegerField(help_text="Unidades por día")
    activa = models.BooleanField(default=True)
    fecha_inauguracion = models.DateField()
    
    class Meta:
        verbose_name = 'Planta de Producción'
        verbose_name_plural = 'Plantas de Producción'
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
```

### Paso 4: Dataset JSON

**`industries/fixtures/datos.json`**:

```json
[
  {
    "model": "industries.producto",
    "pk": 1,
    "fields": {
      "nombre": "Motor Eléctrico Industrial W-500",
      "codigo_sku": "IND-MOT-500",
      "categoria": "motores",
      "descripcion": "Motor eléctrico trifásico de alta eficiencia energética. Potencia: 500 HP, RPM: 1800. Ideal para industria pesada y minería. Certificación ISO 9001.",
      "precio": "45000.00",
      "costo_produccion": "32000.00",
      "stock_unidades": 45,
      "peso_kg": "850.50",
      "dimensiones": "120cm x 80cm x 95cm",
      "capacidad": "500 HP - 373 kW",
      "fabricado_en": "Planta Gotham Norte",
      "fecha_produccion": "2024-01-15",
      "certificacion_iso": true,
      "garantia_meses": 24,
      "disponible": true,
      "destacado": true
    }
  },
  {
    "model": "industries.producto",
    "pk": 2,
    "fields": {
      "nombre": "Batería Industrial Litio-Ion W-Power",
      "codigo_sku": "IND-BAT-LI-200",
      "categoria": "baterias",
      "descripcion": "Sistema de almacenamiento de energía de 200kWh para uso industrial. Duración: 5000 ciclos de carga. Incluye sistema de gestión térmica.",
      "precio": "125000.00",
      "costo_produccion": "89000.00",
      "stock_unidades": 18,
      "peso_kg": "1200.00",
      "dimensiones": "200cm x 120cm x 150cm",
      "capacidad": "200 kWh",
      "fabricado_en": "Planta Energética Central",
      "fecha_produccion": "2024-02-01",
      "certificacion_iso": true,
      "garantia_meses": 60,
      "disponible": true,
      "destacado": true
    }
  },
  {
    "model": "industries.producto",
    "pk": 3,
    "fields": {
      "nombre": "Excavadora Hidráulica W-Excavator 300",
      "codigo_sku": "IND-EXC-300",
      "categoria": "maquinaria",
      "descripcion": "Excavadora de orugas con brazo extendible de 15m. Motor diesel Wayne D-400. Capacidad de cuchara: 2.5 m³. Cabina climatizada con sistema GPS.",
      "precio": "285000.00",
      "costo_produccion": "198000.00",
      "stock_unidades": 8,
      "peso_kg": "28500.00",
      "dimensiones": "1100cm x 350cm x 420cm",
      "capacidad": "2.5 m³ - Alcance 15m",
      "fabricado_en": "Planta Maquinaria Pesada",
      "fecha_produccion": "2023-11-20",
      "certificacion_iso": true,
      "garantia_meses": 36,
      "disponible": true,
      "destacado": false
    }
  },
  {
    "model": "industries.producto",
    "pk": 4,
    "fields": {
      "nombre": "Transmisión Automática W-Shift 8",
      "codigo_sku": "IND-TRA-AS8",
      "categoria": "componentes",
      "descripcion": "Transmisión automática de 8 velocidades para vehículos comerciales. Compatible con motores de 300-800 HP. Incluye modo económico de combustible.",
      "precio": "18500.00",
      "costo_produccion": "12800.00",
      "stock_unidades": 120,
      "peso_kg": "145.00",
      "dimensiones": "85cm x 65cm x 55cm",
      "capacidad": "8 velocidades - 800 Nm",
      "fabricado_en": "Planta Componentes Auto",
      "fecha_produccion": "2024-03-10",
      "certificacion_iso": true,
      "garantia_meses": 24,
      "disponible": true,
      "destacado": false
    }
  },
  {
    "model": "industries.producto",
    "pk": 5,
    "fields": {
      "nombre": "Turbina Eólica W-Wind 5MW",
      "codigo_sku": "IND-TUR-5MW",
      "categoria": "energia",
      "descripcion": "Turbina eólica de gran escala para parques eólicos. Altura: 120m, diámetro rotor: 140m. Generación: 5 MW pico. Sistema de control inteligente.",
      "precio": "4500000.00",
      "costo_produccion": "3200000.00",
      "stock_unidades": 3,
      "peso_kg": "450000.00",
      "dimensiones": "1400cm x 1400cm x 1200cm",
      "capacidad": "5 MW pico",
      "fabricado_en": "Planta Energética Central",
      "fecha_produccion": "2024-01-05",
      "certificacion_iso": true,
      "garantia_meses": 120,
      "disponible": true,
      "destacado": true
    }
  },
  {
    "model": "industries.plantaproduccion",
    "pk": 1,
    "fields": {
      "nombre": "Planta Gotham Norte",
      "ubicacion": "Zona Industrial Norte, Gotham City",
      "empleados": 2500,
      "capacidad_diaria": 500,
      "activa": true,
      "fecha_inauguracion": "1995-03-15"
    }
  },
  {
    "model": "industries.plantaproduccion",
    "pk": 2,
    "fields": {
      "nombre": "Planta Maquinaria Pesada",
      "ubicacion": "Puerto Industrial, Gotham Bay",
      "empleados": 1800,
      "capacidad_diaria": 25,
      "activa": true,
      "fecha_inauguracion": "2002-08-20"
    }
  },
  {
    "model": "industries.plantaproduccion",
    "pk": 3,
    "fields": {
      "nombre": "Planta Energética Central",
      "ubicacion": "Parque Tecnológico, Gotham",
      "empleados": 950,
      "capacidad_diaria": 100,
      "activa": true,
      "fecha_inauguracion": "2010-11-10"
    }
  }
]
```

### Paso 5: URLs (IMPORTANTE)

**`industries/urls.py`**:

```python
from django.urls import path
from . import views

app_name = 'industries'  # ← OBLIGATORIO

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
]
```

### Paso 6: Vistas

**`industries/views.py`**:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Producto, PlantaProduccion


@login_required
def home(request):
    """Página principal de Wayne Industries"""
    
    productos_destacados = Producto.objects.filter(destacado=True, disponible=True)[:4]
    total_productos = Producto.objects.filter(disponible=True).count()
    total_plantas = PlantaProduccion.objects.filter(activa=True).count()
    
    # Calcular valor total de inventario
    productos_stock = Producto.objects.filter(disponible=True)
    valor_inventario = sum(p.precio * p.stock_unidades for p in productos_stock)
    
    context = {
        'titulo': 'Wayne Industries',
        'productos': productos_destacados,
        'stats': {
            'productos': total_productos,
            'plantas': total_plantas,
            'inventario_valor': valor_inventario,
        }
    }
    return render(request, 'industries/home.html', context)


@login_required
def productos(request):
    """Lista todos los productos"""
    productos_list = Producto.objects.filter(disponible=True)
    
    # Filtrar por categoría si se especifica
    categoria = request.GET.get('categoria')
    if categoria:
        productos_list = productos_list.filter(categoria=categoria)
    
    context = {
        'productos': productos_list,
        'categoria_actual': categoria,
    }
    return render(request, 'industries/productos.html', context)
```

### Paso 7: Template

**`industries/templates/industries/home.html`**:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Wayne Industries{% endblock %}

{% block extra_css %}
<style>
    .industries-hero {
        background: linear-gradient(135deg, #1a1a20 0%, #0d0d10 100%);
        border: 1px solid rgba(201, 168, 76, 0.3);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        text-align: center;
    }
    
    .industries-title {
        font-family: 'Cinzel', serif;
        font-size: 36px;
        color: var(--gold);
        margin-bottom: 16px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 24px;
        margin-bottom: 40px;
    }
    
    .stat-card {
        background: rgba(201, 168, 76, 0.05);
        border: 1px solid rgba(201, 168, 76, 0.2);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Cinzel', serif;
        font-size: 28px;
        color: var(--gold);
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 14px;
        margin-top: 8px;
    }
    
    .productos-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
    }
    
    .producto-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(201, 168, 76, 0.2);
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    .producto-card:hover {
        border-color: rgba(201, 168, 76, 0.5);
    }
    
    .producto-codigo {
        font-family: 'Rajdhani', monospace;
        font-size: 12px;
        color: var(--gold);
        margin-bottom: 8px;
    }
    
    .producto-nombre {
        font-family: 'Cinzel', serif;
        font-size: 18px;
        margin-bottom: 12px;
    }
    
    .producto-precio {
        font-size: 24px;
        color: var(--gold);
        font-weight: 600;
    }
    
    .producto-stock {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 8px;
    }
</style>
{% endblock %}

{% block content %}
<div class="industries-hero">
    <h1 class="industries-title">Wayne Industries</h1>
    <p style="color: var(--text-secondary); font-size: 18px;">
        Manufactura de Excelencia Mundial desde 1939
    </p>
</div>

<!-- Estadísticas -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">{{ stats.productos }}</div>
        <div class="stat-label">Productos Disponibles</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{{ stats.plantas }}</div>
        <div class="stat-label">Plantas Activas</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">${{ stats.inventario_valor|floatformat:0 }}</div>
        <div class="stat-label">Valor en Inventario</div>
    </div>
</div>

<!-- Productos Destacados -->
<h2 style="font-family: 'Cinzel', serif; margin-bottom: 24px;">Productos Destacados</h2>

<div class="productos-grid">
    {% for producto in productos %}
    <div class="producto-card">
        <div class="producto-codigo">{{ producto.codigo_sku }}</div>
        <h3 class="producto-nombre">{{ producto.nombre }}</h3>
        <p style="color: var(--text-secondary); font-size: 14px; margin-bottom: 12px;">
            {{ producto.descripcion|truncatewords:15 }}
        </p>
        <div class="producto-precio">${{ producto.precio|floatformat:2 }}</div>
        <div class="producto-stock">
            Stock: {{ producto.stock_unidades }} unidades | 
            {{ producto.fabricado_en }}
        </div>
    </div>
    {% empty %}
    <p style="color: var(--text-muted);">Cargar datos: python manage.py loaddata industries/fixtures/datos.json</p>
    {% endfor %}
</div>

<div style="text-align: center; margin-top: 32px;">
    <a href="{% url 'industries:productos' %}" class="btn-action" style="background: rgba(201,168,76,0.2); padding: 12px 24px; border-radius: 8px; color: var(--gold); text-decoration: none;">
        Ver Todos los Productos →
    </a>
</div>
{% endblock %}
```

### Paso 8: Integrar al Portal

**Editar `settings.py`**:
```python
INSTALLED_APPS = [
    # ... otras apps ...
    'industries',  # ← AGREGAR
]
```

**Editar `urls.py` principal**:
```python
path('industries/', include('industries.urls')),
```

### Paso 9: Migraciones y Datos

```bash
python manage.py makemigrations industries
python manage.py migrate
python manage.py loaddata industries/fixtures/datos.json
python manage.py runserver
```

---

## Checklist de Entrega

- [ ] Carpeta `industries/` creada con toda la estructura
- [ ] Modelo `Producto` con 5 productos de ejemplo
- [ ] Dataset JSON con datos reales
- [ ] Template `home.html` visualmente atractivo
- [ ] `'industries'` en `INSTALLED_APPS`
- [ ] URL `/industries/` configurada
- [ ] Datos cargados y mostrándose
- [ ] Commiteado y pusheado a tu rama

---

## Ayuda

¿Problemas? Ver ejemplos en:
- `foundation/` - App de Camilo
- `realestate/` - App de Perlaza
- `ventures/` - App de Juliana
