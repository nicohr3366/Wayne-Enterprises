# Guía Individual: Cuervo - Wayne Technologies

> **Responsable:** Cuervo  
> **División:** Wayne Technologies (tech)  
> **Estado:** 🔴 PENDIENTE - App no creada  
> **Rama Git:** `cuervo` o `Cuervo_Nieto`  
> **ID Trabajo:** #1

---

## ¿Qué es Wayne Technologies?

Wayne Technologies es la división de investigación y desarrollo tecnológico. Es el corazón de innovación de Wayne Enterprises, responsable de:

- **Investigación avanzada:** IA, robótica, biotecnología
- **Defensa de Gotham:** Tecnología para protección de la ciudad
- **Desarrollo de software:** Aplicaciones empresariales
- **Hardware militar:** Proyectos para el gobierno
- **Energía renovable:** Tecnologías verdes

**Ejemplo del mundo real:** Como el "Wayne R&D" de los comics, desarrollan los gadgets de Batman y tecnología avanzada.

---

## Paso 0: Antes de Empezar (Importante)

### 1. Asegúrate de tener todo instalado:
- ✅ Python 3.13
- ✅ VS Code
- ✅ XAMPP (MySQL)
- ✅ Git

### 2. Verifica tu rama en GitHub:
```bash
# Ver todas las ramas remotas
git branch -r

# Si NO ves tu rama (origin/cuervo), créala:
git checkout -b cuervo
```

### 3. Si ya trabajaste antes y tienes cambios:
```bash
# Guardar cambios actuales temporalmente
git stash

# Bajar última versión del main
git checkout main
git pull origin main

# Volver a tu rama y aplicar cambios
git checkout cuervo
git stash pop
```

---

## Paso 1: Crear tu App

### 1.1 Crear la estructura de carpetas

Copia ESTO EXACTAMENTE en VS Code (terminal):

```bash
# Estás en Wayne-Enterprises/
# Crear carpeta tech con toda la estructura

mkdir tech
cd tech

mkdir migrations
echo "# Migrations" > migrations\__init__.py

mkdir -p templates\tech
mkdir -p static\tech\css
mkdir -p static\tech\js
mkdir -p fixtures

cd ..
```

**Verificación:** Debes ver esta estructura:
```
tech/
├── migrations/
│   └── __init__.py
├── templates/
│   └── tech/
├── static/
│   └── tech/
│       ├── css/
│       └── js/
├── fixtures/
```

---

## Paso 2: Archivos de tu App

### 2.1 Archivo `tech/__init__.py`

Crea archivo `tech/__init__.py` y escribe:
```python
# Wayne Technologies App
```

### 2.2 Archivo `tech/apps.py`

Crea `tech/apps.py`:
```python
from django.apps import AppConfig


class TechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech'
    verbose_name = 'Wayne Technologies'
```

### 2.3 Archivo `tech/models.py` (Dataset)

Aquí defines los datos que guardarás. Para Technologies, sugerimos:

```python
from django.db import models


class ProyectoTech(models.Model):
    """Proyectos de investigación y desarrollo tecnológico"""
    
    TIPO_CHOICES = [
        ('ia', 'Inteligencia Artificial'),
        ('robotica', 'Robótica'),
        ('defensa', 'Sistemas de Defensa'),
        ('software', 'Desarrollo de Software'),
        ('hardware', 'Hardware Avanzado'),
        ('biotech', 'Biotecnología'),
        ('energia', 'Energía Renovable'),
    ]
    
    ESTADO_CHOICES = [
        ('investigacion', 'En Investigación'),
        ('desarrollo', 'En Desarrollo'),
        ('pruebas', 'En Pruebas'),
        ('produccion', 'En Producción'),
        ('completado', 'Completado'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Proyecto')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código Interno')
    descripcion = models.TextField(verbose_name='Descripción Técnica')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name='Tipo de Proyecto')
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='investigacion', verbose_name='Estado')
    
    # Datos numéricos
    presupuesto = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Presupuesto ($)')
    equipo_investigadores = models.PositiveIntegerField(default=5, verbose_name='Investigadores')
    progreso = models.PositiveIntegerField(default=0, verbose_name='Progreso (%)', help_text='0-100')
    
    # Fechas
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_estimada_fin = models.DateField(verbose_name='Fecha Estimada de Fin', null=True, blank=True)
    
    # Campos booleanos y extras
    confidencial = models.BooleanField(default=False, verbose_name='Proyecto Confidencial')
    aplicacion_gotham = models.BooleanField(default=False, verbose_name='Uso en Gotham')
    imagen = models.ImageField(upload_to='tech/proyectos/', null=True, blank=True, verbose_name='Imagen')
    
    # Metadata
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Proyecto Tech'
        verbose_name_plural = 'Proyectos Tech'
        ordering = ['-creado']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Investigador(models.Model):
    """Investigadores asignados a proyectos"""
    
    ESPECIALIDAD_CHOICES = [
        ('ia', 'IA/Machine Learning'),
        ('robotica', 'Robótica'),
        ('ciberseguridad', 'Ciberseguridad'),
        ('biotech', 'Biotecnología'),
        ('nanotech', 'Nanotecnología'),
        ('energia', 'Ingeniería Energética'),
    ]
    
    nombre = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDAD_CHOICES)
    doctorado = models.BooleanField(default=True)
    proyectos = models.ManyToManyField(ProyectoTech, related_name='investigadores', blank=True)
    fecha_contratacion = models.DateField()
    
    class Meta:
        verbose_name = 'Investigador'
        verbose_name_plural = 'Investigadores'
    
    def __str__(self):
        return f"Dr. {self.nombre} - {self.get_especialidad_display()}"
```

---

## Paso 3: URLs (MUY IMPORTANTE)

### 3.1 Archivo `tech/urls.py`

Crea `tech/urls.py` con ESTO EXACTO:

```python
from django.urls import path
from . import views

# ESTA LÍNEA ES OBLIGATORIA - Sin esto el portal no detecta tu app
app_name = 'tech'

urlpatterns = [
    # Página principal de Technologies
    path('', views.home, name='home'),
    
    # Puedes agregar más páginas:
    # path('proyectos/', views.proyectos, name='proyectos'),
    # path('equipo/', views.equipo, name='equipo'),
]
```

**⚠️ IMPORTANTE:** La línea `app_name = 'tech'` es OBLIGATORIA. Sin ella, tu tarjeta aparecerá en "Próximamente".

---

## Paso 4: Vistas

### 4.1 Archivo `tech/views.py`

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProyectoTech, Investigador


@login_required  # Esto protege con login
def home(request):
    """Página principal de Wayne Technologies"""
    
    # Obtener datos del modelo (si existen)
    proyectos_destacados = ProyectoTech.objects.filter(
        activo=True
    ).order_by('-progreso')[:5]
    
    investigadores_count = Investigador.objects.count()
    
    # Contadores por tipo
    proyectos_ia = ProyectoTech.objects.filter(tipo='ia').count()
    proyectos_robotica = ProyectoTech.objects.filter(tipo='robotica').count()
    
    context = {
        'titulo': 'Wayne Technologies',
        'subtitulo': 'Innovando para el futuro de Gotham',
        'proyectos': proyectos_destacados,
        'stats': {
            'total_investigadores': investigadores_count,
            'proyectos_ia': proyectos_ia,
            'proyectos_robotica': proyectos_robotica,
        }
    }
    
    return render(request, 'tech/home.html', context)
```

---

## Paso 5: Template (HTML)

### 5.1 Archivo `tech/templates/tech/home.html`

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Wayne Technologies{% endblock %}

{% block extra_css %}
<style>
    .tech-hero {
        background: linear-gradient(135deg, #1a1a20 0%, #0d0d10 100%);
        border: 1px solid rgba(201, 168, 76, 0.3);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        text-align: center;
    }
    
    .tech-title {
        font-family: 'Cinzel', serif;
        font-size: 36px;
        color: var(--gold);
        margin-bottom: 16px;
    }
    
    .tech-subtitle {
        color: var(--text-secondary);
        font-size: 18px;
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
        font-size: 32px;
        color: var(--gold);
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 14px;
        margin-top: 8px;
    }
    
    .proyectos-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 24px;
    }
    
    .proyecto-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(201, 168, 76, 0.2);
        border-radius: 12px;
        padding: 24px;
        transition: all 0.3s ease;
    }
    
    .proyecto-card:hover {
        border-color: rgba(201, 168, 76, 0.5);
        transform: translateY(-4px);
    }
    
    .proyecto-badge {
        display: inline-block;
        background: rgba(201, 168, 76, 0.1);
        color: var(--gold);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .proyecto-nombre {
        font-family: 'Cinzel', serif;
        font-size: 18px;
        margin-bottom: 8px;
    }
    
    .proyecto-desc {
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 16px;
    }
    
    .proyecto-progress {
        background: rgba(0, 0, 0, 0.3);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .proyecto-progress-bar {
        background: linear-gradient(90deg, var(--gold), #d4af37);
        height: 100%;
        border-radius: 4px;
    }
</style>
{% endblock %}

{% block content %}
<div class="tech-hero">
    <h1 class="tech-title">Wayne Technologies</h1>
    <p class="tech-subtitle">Centro de Investigación y Desarrollo Avanzado</p>
    <p style="color: var(--text-muted); margin-top: 16px;">
        Innovando para el futuro de Gotham desde 1939
    </p>
</div>

<!-- Estadísticas -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">{{ stats.total_investigadores }}</div>
        <div class="stat-label">Investigadores</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{{ stats.proyectos_ia }}</div>
        <div class="stat-label">Proyectos IA</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{{ stats.proyectos_robotica }}</div>
        <div class="stat-label">Proyectos Robótica</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">500+</div>
        <div class="stat-label">Patentes Registradas</div>
    </div>
</div>

<!-- Proyectos Destacados -->
<h2 style="font-family: 'Cinzel', serif; margin-bottom: 24px;">Proyectos Destacados</h2>

<div class="proyectos-grid">
    {% for proyecto in proyectos %}
    <div class="proyecto-card">
        <span class="proyecto-badge">{{ proyecto.get_tipo_display }}</span>
        <h3 class="proyecto-nombre">{{ proyecto.nombre }}</h3>
        <p class="proyecto-desc">{{ proyecto.descripcion|truncatewords:20 }}</p>
        
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px;">
            <span style="color: var(--text-muted);">Progreso</span>
            <span style="color: var(--gold);">{{ proyecto.progreso }}%</span>
        </div>
        <div class="proyecto-progress">
            <div class="proyecto-progress-bar" style="width: {{ proyecto.progreso }}%"></div>
        </div>
        
        <div style="margin-top: 16px; font-size: 12px; color: var(--text-muted);">
            Investigadores: {{ proyecto.equipo_investigadores }} | 
            Estado: {{ proyecto.get_estado_display }}
        </div>
    </div>
    {% empty %}
    <div style="text-align: center; padding: 40px; color: var(--text-muted);">
        <p>Los proyectos se cargarán desde el dataset.</p>
        <p style="font-size: 14px; margin-top: 8px;">
            Ejecuta: python manage.py loaddata tech/fixtures/datos.json
        </p>
    </div>
    {% endfor %}
</div>

<!-- Tipos de Investigación -->
<div style="margin-top: 48px;">
    <h2 style="font-family: 'Cinzel', serif; margin-bottom: 24px;">Áreas de Investigación</h2>
    
    <div class="proyectos-grid">
        <div class="proyecto-card">
            <span class="proyecto-badge">Inteligencia Artificial</span>
            <h3 class="proyecto-nombre">Wayne AI Division</h3>
            <p class="proyecto-desc">
                Desarrollo de sistemas de inteligencia artificial para seguridad de Gotham,
                análisis predictivo de crímenes y asistencia médica avanzada.
            </p>
        </div>
        
        <div class="proyecto-card">
            <span class="proyecto-badge">Robótica</span>
            <h3 class="proyecto-nombre">Robotics Lab</h3>
            <p class="proyecto-desc">
                Robots de rescate, drones de vigilancia y exoesqueletos de carga
                para uso industrial y de emergencias.
            </p>
        </div>
        
        <div class="proyecto-card">
            <span class="proyecto-badge">Defensa</span>
            <h3 class="proyecto-nombre">Defense Systems</h3>
            <p class="proyecto-desc">
                Tecnología de defensa no letal, sistemas de detección de amenazas
                y protección perimetral para Gotham City.
            </p>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    console.log('Wayne Technologies cargado');
</script>
{% endblock %}
```

---

## Paso 6: Dataset (Datos de Ejemplo)

### 6.1 Crear archivo JSON

Crea `tech/fixtures/datos.json`:

```json
[
  {
    "model": "tech.proyectotech",
    "pk": 1,
    "fields": {
      "nombre": "Wayne AI Guardian",
      "codigo": "AI-2024-001",
      "descripcion": "Sistema de inteligencia artificial para predicción y prevención de crímenes en Gotham City. Analiza patrones históricos y datos en tiempo real.",
      "tipo": "ia",
      "estado": "desarrollo",
      "presupuesto": 15000000.00,
      "equipo_investigadores": 12,
      "progreso": 65,
      "fecha_inicio": "2023-03-15",
      "fecha_estimada_fin": "2025-12-31",
      "confidencial": true,
      "aplicacion_gotham": true
    }
  },
  {
    "model": "tech.proyectotech",
    "pk": 2,
    "fields": {
      "nombre": "Bat-Drone Pro",
      "codigo": "ROB-2024-003",
      "descripcion": "Drone de vigilancia autónomo con capacidad de sigilo, visión nocturna y comunicación encriptada. Diseñado para operaciones de búsqueda y rescate.",
      "tipo": "robotica",
      "estado": "produccion",
      "presupuesto": 8200000.00,
      "equipo_investigadores": 8,
      "progreso": 95,
      "fecha_inicio": "2022-08-10",
      "fecha_estimada_fin": "2024-06-30",
      "confidencial": false,
      "aplicacion_gotham": true
    }
  },
  {
    "model": "tech.proyectotech",
    "pk": 3,
    "fields": {
      "nombre": "Batería Cuántica Wayne",
      "codigo": "ENR-2024-007",
      "descripcion": "Sistema de almacenamiento de energía de próxima generación con 10x capacidad de baterías de litio. Aplicaciones en transporte y redes eléctricas.",
      "tipo": "energia",
      "estado": "investigacion",
      "presupuesto": 22000000.00,
      "equipo_investigadores": 15,
      "progreso": 30,
      "fecha_inicio": "2024-01-20",
      "fecha_estimada_fin": "2027-12-31",
      "confidencial": true,
      "aplicacion_gotham": false
    }
  },
  {
    "model": "tech.proyectotech",
    "pk": 4,
    "fields": {
      "nombre": "Gotham OS",
      "codigo": "SW-2024-002",
      "descripcion": "Sistema operativo seguro para infraestructura crítica de Gotham. Incluye encriptación militar y protección contra ciberataques.",
      "tipo": "software",
      "estado": "pruebas",
      "presupuesto": 6800000.00,
      "equipo_investigadores": 20,
      "progreso": 80,
      "fecha_inicio": "2023-06-01",
      "fecha_estimada_fin": "2024-09-15",
      "confidencial": false,
      "aplicacion_gotham": true
    }
  },
  {
    "model": "tech.proyectotech",
    "pk": 5,
    "fields": {
      "nombre": "Exoesqueleto H-200",
      "codigo": "HARD-2024-005",
      "descripcion": "Exoesqueleto de asistencia mecánica para carga pesada en industria y operaciones de emergencia. Aumenta fuerza del usuario 5x.",
      "tipo": "hardware",
      "estado": "desarrollo",
      "presupuesto": 12000000.00,
      "equipo_investigadores": 10,
      "progreso": 55,
      "fecha_inicio": "2023-09-15",
      "fecha_estimada_fin": "2025-06-30",
      "confidencial": false,
      "aplicacion_gotham": true
    }
  },
  {
    "model": "tech.investigador",
    "pk": 1,
    "fields": {
      "nombre": "Lucius Fox Jr.",
      "especialidad": "robotica",
      "doctorado": true,
      "fecha_contratacion": "2020-01-15"
    }
  },
  {
    "model": "tech.investigador",
    "pk": 2,
    "fields": {
      "nombre": "Sarah Chen",
      "especialidad": "ia",
      "doctorado": true,
      "fecha_contratacion": "2021-03-20"
    }
  },
  {
    "model": "tech.investigador",
    "pk": 3,
    "fields": {
      "nombre": "Marcus Rodriguez",
      "especialidad": "ciberseguridad",
      "doctorado": false,
      "fecha_contratacion": "2022-07-10"
    }
  }
]
```

---

## Paso 7: Integrar al Portal

### 7.1 Agregar a INSTALLED_APPS

Edita `wayne_enterprise/settings.py`, busca `INSTALLED_APPS` y agrega `'tech',`:

```python
INSTALLED_APPS = [
    # ... otras apps ...
    'core',
    'ventures',
    'foundation',
    'accounts',
    'realestate',
    'tech',  # ← AGREGAR AQUÍ
]
```

### 7.2 Agregar URL

Edita `wayne_enterprise/urls.py`, agrega la línea:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('ventures/', include('ventures.urls')),
    path('foundation/', include('foundation.urls')),
    path('accounts/', include('accounts.urls')),
    path('realestate/', include('realestate.urls')),
    path('tech/', include('tech.urls')),  # ← AGREGAR AQUÍ
]
```

---

## Paso 8: Migraciones y Datos

Ejecuta ESTOS COMANDOS en orden:

```bash
# 1. Crear migraciones (esto crea la tabla en MySQL)
python manage.py makemigrations tech

# 2. Aplicar migraciones
python manage.py migrate

# 3. Cargar datos de ejemplo (tu dataset)
python manage.py loaddata tech/fixtures/datos.json

# 4. Iniciar servidor
python manage.py runserver
```

---

## Paso 9: Verificar Funcionamiento

1. **Abre navegador**: `http://127.0.0.1:8000/`
2. **Inicia sesión** con tu usuario
3. **Ve al portal**: La tarjeta "Wayne Technologies" ya no debe decir "Próximamente"
4. **Clic en la tarjeta**: Debe abrir tu app
5. **Ver tu página**: Debes ver "Wayne Technologies" con tus proyectos

---

## Paso 10: Git (Subir Cambios)

```bash
# 1. Ver qué cambiaste
git status

# 2. Agregar tu app
git add tech/

# 3. Commit con mensaje claro
git commit -m "feat: agrega app tech con modelo ProyectoTech y dataset de 5 proyectos"

# 4. Subir a tu rama
git push origin cuervo
```

---

## Checklist Final

- [ ] Carpeta `tech/` creada con estructura completa
- [ ] `app_name = 'tech'` en `urls.py`
- [ ] Modelo `ProyectoTech` creado
- [ ] Dataset con 5 proyectos en `fixtures/datos.json`
- [ ] Template `home.html` estilizado
- [ ] `'tech'` en `INSTALLED_APPS`
- [ ] `path('tech/', ...)` en `urls.py` principal
- [ ] Migraciones aplicadas (`migrate`)
- [ ] Datos cargados (`loaddata`)
- [ ] App funciona en navegador
- [ ] Cambios subidos a Git (`push`)

---

## Ayuda

¿Problemas? Verifica:

1. **¿Tarjeta en "Próximamente"?**
   - ¿Tienes `app_name = 'tech'`?
   - ¿Está `'tech'` en `INSTALLED_APPS`?
   - ¿Hiciste `migrate`?

2. **¿Error "No module named 'tech'"?**
   - ¿Creaste el archivo `tech/__init__.py`?
   - ¿Está la carpeta `tech` en el lugar correcto?

3. **¿No aparecen datos?**
   - ¿Ejecutaste `python manage.py loaddata tech/fixtures/datos.json`?
   - ¿El archivo `datos.json` tiene la estructura correcta?

---

## Contacto

¿Ayuda? Contacta a:
- **Nicolás** - Git/Django general
- **Camilo/Perlaza/Juliana** - Ya tienen apps funcionando (ejemplo)

---

## Ejemplo Real

Mira las apps que ya funcionan:
- `foundation/` - App de Camilo
- `realestate/` - App de Perlaza
- `ventures/` - App de Juliana

Copia su estructura y adapta a tu contenido.
