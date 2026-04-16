# Guía Individual: Valeria - Wayne Capital

> **Responsable:** Valeria  
> **División:** Wayne Capital (capital)  
> **Estado:** 🔴 PENDIENTE - App no creada  
> **Rama Git:** `valeria`  
> **ID Trabajo:** #5

---

## ¿Qué es Wayne Capital?

Wayne Capital es la división financiera e inversiones del conglomerado Wayne. Es como el "brazo de Wall Street" de Wayne Enterprises:

- **Gestión de activos:** Manejo de portafolios de inversión
- **Banca de inversión:** Fusiones, adquisiciones, IPOs
- **Private Equity:** Inversiones en empresas privadas
- **Hedge Funds:** Fondos de inversión alternativos
- **Banca comercial:** Servicios bancarios para corporaciones

**Ejemplo real:** Como Goldman Sachs, JP Morgan o BlackRock dentro del universo Wayne.

---

## Dataset para Capital

Tu dataset debe incluir **inversiones, portafolios, activos financieros**.

### Tipos de Datos

| Tipo | Ejemplos | Datos Incluidos |
|------|----------|-----------------|
| `fondo` | Fondos de inversión | NAV, rentabilidad, riesgo |
| `inversion` | Inversiones individuales | Empresa, monto, sector |
| `mercado` | Mercados operados | Acciones, forex, crypto |
| `portafolio` | Portafolios de clientes | Balance, performance |

### Ejemplo de Registro

```json
{
  "nombre": "Wayne Growth Fund",
  "tipo": "fondo",
  "categoria": "acciones_crecimiento",
  "valor_bajo_gestion": 2500000000.00,
  "rentabilidad_anual": 15.8,
  "riesgo": "medio",
  "inversion_minima": 100000.00
}
```

---

## Paso a Paso: Crear tu App

### Paso 1: Estructura

```bash
mkdir capital
cd capital

mkdir migrations
echo "" > migrations/__init__.py
mkdir -p templates/capital
mkdir -p static/capital/css
mkdir fixtures

cd ..
```

### Paso 2: Modelo

**`capital/models.py`**:

```python
from django.db import models


class FondoInversion(models.Model):
    """Fondos de inversión gestionados por Wayne Capital"""
    
    TIPO_CHOICES = [
        ('acciones_crecimiento', 'Acciones Crecimiento'),
        ('acciones_valor', 'Acciones Valor'),
        ('renta_fija', 'Renta Fija'),
        ('balanceado', 'Balanceado'),
        ('alternativo', 'Alternativo'),
        ('emergentes', 'Mercados Emergentes'),
    ]
    
    RIESGO_CHOICES = [
        ('conservador', 'Conservador'),
        ('moderado', 'Moderado'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('especulativo', 'Especulativo'),
    ]
    
    nombre = models.CharField(max_length=200)
    codigo_isin = models.CharField(max_length=12, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    riesgo = models.CharField(max_length=20, choices=RIESGO_CHOICES)
    
    # Valores
    nav_actual = models.DecimalField(max_digits=15, decimal_places=2, help_text="Valor del fondo")
    valor_bajo_gestion = models.DecimalField(max_digits=15, decimal_places=2)
    inversion_minima = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Rendimiento (%)
    rentabilidad_anual = models.DecimalField(max_digits=5, decimal_places=2)
    rentabilidad_ytd = models.DecimalField(max_digits=5, decimal_places=2)
    rentabilidad_5_anos = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Detalles
    fecha_creacion = models.DateField()
    manager_principal = models.CharField(max_length=200)
    comision_gestion = models.DecimalField(max_digits=4, decimal_places=2)
    numero_inversores = models.PositiveIntegerField()
    
    # Estado
    abierto_nuevas_inversiones = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Fondo de Inversión'
        verbose_name_plural = 'Fondos de Inversión'
        ordering = ['-valor_bajo_gestion']
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_isin})"


class Inversion(models.Model):
    """Inversiones individuales realizadas"""
    
    SECTOR_CHOICES = [
        ('tecnologia', 'Tecnología'),
        ('salud', 'Salud'),
        ('energia', 'Energía'),
        ('financiero', 'Financiero'),
        ('industrial', 'Industrial'),
        ('consumo', 'Consumo'),
        ('inmobiliario', 'Inmobiliario'),
        ('educacion', 'Educación'),
    ]
    
    empresa = models.CharField(max_length=200)
    ticker = models.CharField(max_length=10, blank=True)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES)
    
    # Montos
    monto_invertido = models.DecimalField(max_digits=15, decimal_places=2)
    valor_actual = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Fechas
    fecha_inversion = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    
    # Rendimiento
    retorno = models.DecimalField(max_digits=7, decimal_places=2)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Inversión'
        verbose_name_plural = 'Inversiones'
    
    @property
    def ganancia_perdida(self):
        return self.valor_actual - self.monto_invertido
    
    @property
    def porcentaje_retorno(self):
        if self.monto_invertido > 0:
            return (self.retorno / self.monto_invertido) * 100
        return 0


class PortafolioCliente(models.Model):
    """Portafolios de clientes de Wayne Capital"""
    
    PERFIL_CHOICES = [
        ('conservador', 'Conservador'),
        ('moderado', 'Moderado'),
        ('agresivo', 'Agresivo'),
    ]
    
    nombre_cliente = models.CharField(max_length=200)
    codigo_portafolio = models.CharField(max_length=20, unique=True)
    perfil_riesgo = models.CharField(max_length=20, choices=PERFIL_CHOICES)
    
    # Valores
    valor_inicial = models.DecimalField(max_digits=15, decimal_places=2)
    valor_actual = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Composición
    fondos = models.ManyToManyField(FondoInversion, related_name='portafolios', blank=True)
    
    # Rendimiento
    rendimiento_total = models.DecimalField(max_digits=7, decimal_places=2)
    rendimiento_anualizado = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Fechas
    fecha_creacion = models.DateField()
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Portafolio de Cliente'
        verbose_name_plural = 'Portafolios de Clientes'
    
    def __str__(self):
        return f"{self.codigo_portafolio} - {self.nombre_cliente}"
```

### Paso 3: Dataset

**`capital/fixtures/datos.json`**:

```json
[
  {
    "model": "capital.fondoinversion",
    "pk": 1,
    "fields": {
      "nombre": "Wayne Growth Equity Fund",
      "codigo_isin": "US1234567890",
      "tipo": "acciones_crecimiento",
      "riesgo": "medio",
      "nav_actual": "145.75",
      "valor_bajo_gestion": 2500000000.00,
      "inversion_minima": 100000.00,
      "rentabilidad_anual": 15.80,
      "rentabilidad_ytd": 8.50,
      "rentabilidad_5_anos": 82.40,
      "fecha_creacion": "2018-03-15",
      "manager_principal": "Robert Wayne Jr.",
      "comision_gestion": 1.50,
      "numero_inversores": 1250,
      "abierto_nuevas_inversiones": true
    }
  },
  {
    "model": "capital.fondoinversion",
    "pk": 2,
    "fields": {
      "nombre": "Wayne Tech Ventures Fund",
      "codigo_isin": "US9876543210",
      "tipo": "alternativo",
      "riesgo": "alto",
      "nav_actual": "203.40",
      "valor_bajo_gestion": 1200000000.00,
      "inversion_minima": 500000.00,
      "rentabilidad_anual": 24.50,
      "rentabilidad_ytd": 12.30,
      "rentabilidad_5_anos": 145.80,
      "fecha_creacion": "2019-06-01",
      "manager_principal": "Lucius Fox III",
      "comision_gestion": 2.00,
      "numero_inversores": 450,
      "abierto_nuevas_inversiones": true
    }
  },
  {
    "model": "capital.fondoinversion",
    "pk": 3,
    "fields": {
      "nombre": "Wayne Fixed Income Plus",
      "codigo_isin": "US5555666677",
      "tipo": "renta_fija",
      "riesgo": "conservador",
      "nav_actual": "98.50",
      "valor_bajo_gestion": 5800000000.00,
      "inversion_minima": 25000.00,
      "rentabilidad_anual": 4.20,
      "rentabilidad_ytd": 2.80,
      "rentabilidad_5_anos": 22.50,
      "fecha_creacion": "2015-01-10",
      "manager_principal": "Martha Wayne Foundation",
      "comision_gestion": 0.75,
      "numero_inversores": 8500,
      "abierto_nuevas_inversiones": true
    }
  },
  {
    "model": "capital.fondoinversion",
    "pk": 4,
    "fields": {
      "nombre": "Wayne Emerging Markets",
      "codigo_isin": "US1122334455",
      "tipo": "emergentes",
      "riesgo": "alto",
      "nav_actual": "89.30",
      "valor_bajo_gestion": 890000000.00,
      "inversion_minima": 50000.00,
      "rentabilidad_anual": 18.90,
      "rentabilidad_ytd": 5.20,
      "rentabilidad_5_anos": 95.60,
      "fecha_creacion": "2017-09-20",
      "manager_principal": "James Chen",
      "comision_gestion": 1.75,
      "numero_inversores": 680,
      "abierto_nuevas_inversiones": true
    }
  },
  {
    "model": "capital.fondoinversion",
    "pk": 5,
    "fields": {
      "nombre": "Wayne Balanced Strategy",
      "codigo_isin": "US9999888877",
      "tipo": "balanceado",
      "riesgo": "moderado",
      "nav_actual": "112.40",
      "valor_bajo_gestion": 3200000000.00,
      "inversion_minima": 50000.00,
      "rentabilidad_anual": 11.50,
      "rentabilidad_ytd": 6.40,
      "rentabilidad_5_anos": 58.20,
      "fecha_creacion": "2016-05-12",
      "manager_principal": "Thomas Elliot",
      "comision_gestion": 1.25,
      "numero_inversores": 2400,
      "abierto_nuevas_inversiones": true
    }
  },
  {
    "model": "capital.inversion",
    "pk": 1,
    "fields": {
      "empresa": "Stark Industries",
      "ticker": "STRK",
      "sector": "tecnologia",
      "monto_invertido": 150000000.00,
      "valor_actual": 285000000.00,
      "fecha_inversion": "2020-03-15",
      "fecha_salida": null,
      "retorno": 135000000.00,
      "activa": true
    }
  },
  {
    "model": "capital.inversion",
    "pk": 2,
    "fields": {
      "empresa": "LexCorp",
      "ticker": "LEXC",
      "sector": "industrial",
      "monto_invertido": 200000000.00,
      "valor_actual": 180000000.00,
      "fecha_inversion": "2019-08-10",
      "fecha_salida": null,
      "retorno": -20000000.00,
      "activa": true
    }
  },
  {
    "model": "capital.inversion",
    "pk": 3,
    "fields": {
      "empresa": "Gotham General Hospital",
      "ticker": "",
      "sector": "salud",
      "monto_invertido": 50000000.00,
      "valor_actual": 87500000.00,
      "fecha_inversion": "2021-01-20",
      "fecha_salida": null,
      "retorno": 37500000.00,
      "activa": true
    }
  },
  {
    "model": "capital.inversion",
    "pk": 4,
    "fields": {
      "empresa": "Ace Chemicals",
      "ticker": "ACEC",
      "sector": "industrial",
      "monto_invertido": 80000000.00,
      "valor_actual": 45000000.00,
      "fecha_inversion": "2018-06-01",
      "fecha_salida": "2023-12-01",
      "retorno": -35000000.00,
      "activa": false
    }
  },
  {
    "model": "capital.inversion",
    "pk": 5,
    "fields": {
      "empresa": "Kord Enterprises",
      "ticker": "KORD",
      "sector": "tecnologia",
      "monto_invertido": 95000000.00,
      "valor_actual": 185000000.00,
      "fecha_inversion": "2022-04-15",
      "fecha_salida": null,
      "retorno": 90000000.00,
      "activa": true
    }
  }
]
```

### Paso 4: URLs

**`capital/urls.py`**:

```python
from django.urls import path
from . import views

app_name = 'capital'

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Paso 5: Vistas

**`capital/views.py`**:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FondoInversion, Inversion


@login_required
def home(request):
    """Página principal de Wayne Capital"""
    
    fondos = FondoInversion.objects.filter(abierto_nuevas_inversiones=True)
    total_gestionado = sum(f.valor_bajo_gestion for f in fondos)
    
    inversiones_activas = Inversion.objects.filter(activa=True)
    total_invertido = sum(i.monto_invertido for i in inversiones_activas)
    
    context = {
        'fondos': fondos,
        'total_gestionado': total_gestionado,
        'inversiones': inversiones_activas[:5],
        'total_invertido': total_invertido,
    }
    
    return render(request, 'capital/home.html', context)
```

### Paso 6: Template

**`capital/templates/capital/home.html`**:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Wayne Capital{% endblock %}

{% block extra_css %}
<style>
    .capital-hero {
        background: linear-gradient(135deg, #1a1a20 0%, #0d0d10 100%);
        border: 1px solid rgba(201, 168, 76, 0.3);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        text-align: center;
    }
    
    .capital-title {
        font-family: 'Cinzel', serif;
        font-size: 36px;
        color: var(--gold);
    }
    
    .hero-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 24px;
        margin: 32px 0;
    }
    
    .hero-stat {
        background: rgba(201, 168, 76, 0.1);
        border-radius: 12px;
        padding: 20px;
    }
    
    .stat-value {
        font-family: 'Cinzel', serif;
        font-size: 28px;
        color: var(--gold);
    }
    
    .stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 8px;
    }
    
    .fondos-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
    }
    
    .fondo-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(201, 168, 76, 0.2);
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    .fondo-card:hover {
        border-color: rgba(201, 168, 76, 0.5);
    }
    
    .fondo-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
    }
    
    .fondo-nombre {
        font-family: 'Cinzel', serif;
        font-size: 18px;
    }
    
    .fondo-tipo {
        font-size: 11px;
        color: var(--gold);
        background: rgba(201, 168, 76, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
    }
    
    .fondo-nav {
        font-size: 24px;
        color: var(--gold);
        font-weight: 600;
        margin: 12px 0;
    }
    
    .rendimiento {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid rgba(201, 168, 76, 0.1);
    }
    
    .rend-item {
        text-align: center;
    }
    
    .rend-label {
        font-size: 10px;
        color: var(--text-muted);
    }
    
    .rend-value {
        font-size: 16px;
        font-weight: 600;
    }
    
    .positivo { color: #51cf66; }
    .negativo { color: #ff6b6b; }
</style>
{% endblock %}

{% block content %}
<div class="capital-hero">
    <h1 class="capital-title">Wayne Capital</h1>
    <p style="color: var(--text-secondary); margin-top: 8px;">
        Gestión de Inversiones y Banca Privada
    </p>
    
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="stat-value">${{ total_gestionado|floatformat:0 }}M</div>
            <div class="stat-label">Activos Bajo Gestión</div>
        </div>
        <div class="hero-stat">
            <div class="stat-value">15.2%</div>
            <div class="stat-label">Rendimiento Promedio</div>
        </div>
        <div class="hero-stat">
            <div class="stat-value">12,000+</div>
            <div class="stat-label">Clientes</div>
        </div>
    </div>
</div>

<h2 style="font-family: 'Cinzel', serif; margin-bottom: 24px;">Fondos de Inversión</h2>

<div class="fondos-grid">
    {% for fondo in fondos %}
    <div class="fondo-card">
        <div class="fondo-header">
            <div>
                <div class="fondo-nombre">{{ fondo.nombre }}</div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                    {{ fondo.codigo_isin }}
                </div>
            </div>
            <div class="fondo-tipo">{{ fondo.get_tipo_display }}</div>
        </div>
        
        <div class="fondo-nav">${{ fondo.nav_actual }}</div>
        
        <div style="font-size: 13px; color: var(--text-secondary);">
            Bajo gestión: ${{ fondo.valor_bajo_gestion|floatformat:0 }}
        </div>
        
        <div class="rendimiento">
            <div class="rend-item">
                <div class="rend-label">YTD</div>
                <div class="rend-value {% if fondo.rentabilidad_ytd > 0 %}positivo{% else %}negativo{% endif %}">
                    {{ fondo.rentabilidad_ytd }}%
                </div>
            </div>
            <div class="rend-item">
                <div class="rend-label">1 Año</div>
                <div class="rend-value {% if fondo.rentabilidad_anual > 0 %}positivo{% else %}negativo{% endif %}">
                    {{ fondo.rentabilidad_anual }}%
                </div>
            </div>
            <div class="rend-item">
                <div class="rend-label">5 Años</div>
                <div class="rend-value {% if fondo.rentabilidad_5_anos > 0 %}positivo{% else %}negativo{% endif %}">
                    {{ fondo.rentabilidad_5_anos }}%
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <p style="color: var(--text-muted);">Cargar datos: python manage.py loaddata capital/fixtures/datos.json</p>
    {% endfor %}
</div>

<div style="margin-top: 48px;">
    <h2 style="font-family: 'Cinzel', serif; margin-bottom: 24px;">Inversiones Destacadas</h2>
    
    <div class="fondos-grid">
        {% for inversion in inversiones %}
        <div class="fondo-card">
            <div class="fondo-nombre">{{ inversion.empresa }}</div>
            <div style="font-size: 12px; color: var(--text-muted); margin: 8px 0;">
                {{ inversion.get_sector_display }} | ${{ inversion.monto_invertido|floatformat:0 }}
            </div>
            
            <div style="font-size: 18px; font-weight: 600; {% if inversion.retorno > 0 %}color: #51cf66;{% else %}color: #ff6b6b;{% endif %}">
                {% if inversion.retorno > 0 %}+{% endif %}{{ inversion.retorno|floatformat:0 }}
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### Paso 7: Integrar

**`settings.py`**:
```python
INSTALLED_APPS = [
    # ... otras ...
    'capital',
]
```

**`urls.py`**:
```python
path('capital/', include('capital.urls')),
```

### Paso 8: Ejecutar

```bash
python manage.py makemigrations capital
python manage.py migrate
python manage.py loaddata capital/fixtures/datos.json
python manage.py runserver
```

---

## Checklist

- [ ] Modelo `FondoInversion` con 5 fondos
- [ ] Modelo `Inversion` con empresas
- [ ] Dataset JSON con datos financieros
- [ ] Template que muestre rendimientos
- [ ] Colores verde/rojo para ganancias/pérdidas
- [ ] `'capital'` en `INSTALLED_APPS`
- [ ] URL `/capital/` configurada

---

## Referencias

Mira ejemplos completos en:
- `foundation/`, `realestate/`, `ventures/`
