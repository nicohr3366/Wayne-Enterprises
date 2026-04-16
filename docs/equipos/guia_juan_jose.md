# Guía Individual: Juan José - Wayne Healthcare

> **Responsable:** Juan José  
> **División:** Wayne Healthcare (healthcare)  
> **Estado:** 🔴 PENDIENTE - App no creada  
> **Rama Git:** `juan_jose`  
> **ID Trabajo:** #3

---

## ¿Qué es Wayne Healthcare?

Wayne Healthcare es la división de salud y bienestar del conglomerado. Gestiona:

- **Hospitales Wayne:** Red de centros médicos en Gotham
- **Clínicas especializadas:** Cardiología, oncología, pediatría
- **Investigación médica:** Desarrollo de tratamientos innovadores
- **Telemedicina:** Servicios de salud digital
- **Seguros médicos:** Wayne Health Insurance

**Ejemplo real:** Como Kaiser Permanente o Mayo Clinic dentro del universo Wayne.

---

## Dataset para Healthcare

Tu dataset debe incluir **servicios médicos, hospitales, doctores o tratamientos**.

### Ejemplo de Registro

```json
{
  "nombre": "Hospital General Wayne",
  "tipo": "hospital",
  "especialidades": ["emergencias", "cirugia", "maternidad"],
  "capacidad_camas": 500,
  "medicos": 120,
  "direccion": "Medical District, Gotham",
  "telefono": "555-WAYNE-01",
  "emergencias_24h": true
}
```

### Tipos de Datos Sugeridos

| Tipo | Ejemplos | Datos Incluidos |
|------|----------|-----------------|
| `hospital` | Centros médicos | Camas, médicos, especialidades |
| `clinica` | Centros especializados | Horario, servicios, ubicación |
| `doctor` | Personal médico | Especialidad, experiencia, rating |
| `servicio` | Tratamientos | Precio, duración, descripción |
| `seguro` | Planes de salud | Cobertura, prima, deducible |

---

## Paso a Paso: Crear tu App

### Paso 1: Crear Estructura

```bash
mkdir healthcare
cd healthcare

mkdir migrations
echo "" > migrations/__init__.py
mkdir -p templates/healthcare
mkdir -p static/healthcare/css
mkdir fixtures

cd ..
```

### Paso 2: Archivos Básicos

**`healthcare/__init__.py`**:
```python
# Wayne Healthcare App
```

**`healthcare/apps.py`**:
```python
from django.apps import AppConfig

class HealthcareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthcare'
    verbose_name = 'Wayne Healthcare'
```

### Paso 3: Modelo de Datos

**`healthcare/models.py`**:

```python
from django.db import models


class Hospital(models.Model):
    """Centros médicos de Wayne Healthcare"""
    
    TIPO_CHOICES = [
        ('hospital', 'Hospital General'),
        ('clinica', 'Clínica Especializada'),
        ('centro_urgencias', 'Centro de Urgencias'),
        ('centro_diagnostico', 'Centro de Diagnóstico'),
        ('hospicio', 'Hospicio'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    direccion = models.CharField(max_length=300)
    telefono = models.CharField(max_length=50)
    email = models.EmailField()
    
    # Capacidad
    capacidad_camas = models.PositiveIntegerField()
    medicos_activos = models.PositiveIntegerField()
    enfermeras = models.PositiveIntegerField()
    
    # Servicios
    emergencias_24h = models.BooleanField(default=True)
    unidad_cuidados_intensivos = models.BooleanField(default=True)
    quirofanos = models.PositiveIntegerField(default=5)
    
    # Especialidades (lista separada por comas)
    especialidades = models.CharField(max_length=500, help_text="Separadas por comas")
    
    # Estado
    acepta_seguro_wayne = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    
    # Metadata
    fecha_apertura = models.DateField()
    imagen = models.ImageField(upload_to='healthcare/hospitales/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Hospital/Centro'
        verbose_name_plural = 'Hospitales y Centros'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    @property
    def personal_total(self):
        return self.medicos_activos + self.enfermeras
    
    @property
    def especialidades_lista(self):
        return [e.strip() for e in self.especialidades.split(',')]


class ServicioMedico(models.Model):
    """Servicios y tratamientos ofrecidos"""
    
    CATEGORIAS = [
        ('consulta', 'Consulta Médica'),
        ('cirugia', 'Cirugía'),
        ('emergencia', 'Emergencia'),
        ('diagnostico', 'Diagnóstico'),
        ('tratamiento', 'Tratamiento'),
        ('rehabilitacion', 'Rehabilitación'),
        ('prevencion', 'Medicina Preventiva'),
    ]
    
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    descripcion = models.TextField()
    
    # Precios (en USD)
    precio_sin_seguro = models.DecimalField(max_digits=10, decimal_places=2)
    precio_con_seguro_wayne = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Detalles
    duracion_minutos = models.PositiveIntegerField(help_text="Duración estimada")
    requiere_cita_previa = models.BooleanField(default=True)
    disponible_emergencias = models.BooleanField(default=False)
    
    # Hospitales que ofrecen este servicio
    hospitales = models.ManyToManyField(Hospital, related_name='servicios', blank=True)
    
    class Meta:
        verbose_name = 'Servicio Médico'
        verbose_name_plural = 'Servicios Médicos'
    
    def __str__(self):
        return self.nombre
    
    @property
    def ahorro_seguro(self):
        return self.precio_sin_seguro - self.precio_con_seguro_wayne


class Doctor(models.Model):
    """Personal médico de Wayne Healthcare"""
    
    ESPECIALIDADES = [
        ('medicina_general', 'Medicina General'),
        ('cardiologia', 'Cardiología'),
        ('neurologia', 'Neurología'),
        ('oncologia', 'Oncología'),
        ('pediatria', 'Pediatría'),
        ('traumatologia', 'Traumatología'),
        ('ginecologia', 'Ginecología'),
        ('dermatologia', 'Dermatología'),
        ('psiquiatria', 'Psiquiatría'),
        ('cirugia', 'Cirugía General'),
    ]
    
    nombre_completo = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES)
    hospital_principal = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='medicos')
    
    # Perfil
    anos_experiencia = models.PositiveIntegerField()
    certificaciones = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    
    # Contacto
    email = models.EmailField()
    telefono_consulta = models.CharField(max_length=50)
    
    # Disponibilidad
    acepta_nuevos_pacientes = models.BooleanField(default=True)
    horario_atencion = models.CharField(max_length=200)
    
    imagen = models.ImageField(upload_to='healthcare/doctores/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
        ordering = ['nombre_completo']
    
    def __str__(self):
        return f"Dr. {self.nombre_completo} - {self.get_especialidad_display()}"
```

### Paso 4: Dataset JSON

**`healthcare/fixtures/datos.json`**:

```json
[
  {
    "model": "healthcare.hospital",
    "pk": 1,
    "fields": {
      "nombre": "Hospital General Wayne",
      "tipo": "hospital",
      "direccion": "1000 Medical Plaza, Gotham Medical District",
      "telefono": "(555) 100-2000",
      "email": "info@hospital-wayne.gotham",
      "capacidad_camas": 450,
      "medicos_activos": 180,
      "enfermeras": 420,
      "emergencias_24h": true,
      "unidad_cuidados_intensivos": true,
      "quirofanos": 12,
      "especialidades": "Cardiología, Neurología, Oncología, Pediatría, Cirugía, Emergencias, Maternidad",
      "acepta_seguro_wayne": true,
      "activo": true,
      "fecha_apertura": "1975-03-15"
    }
  },
  {
    "model": "healthcare.hospital",
    "pk": 2,
    "fields": {
      "nombre": "Centro de Cáncer Wayne",
      "tipo": "clinica",
      "direccion": "250 Hope Avenue, Gotham North",
      "telefono": "(555) 100-3000",
      "email": "cancer@wayne-healthcare.gotham",
      "capacidad_camas": 120,
      "medicos_activos": 45,
      "enfermeras": 150,
      "emergencias_24h": false,
      "unidad_cuidados_intensivos": true,
      "quirofanos": 4,
      "especialidades": "Oncología, Radioterapia, Quimioterapia, Medicina Paliativa",
      "acepta_seguro_wayne": true,
      "activo": true,
      "fecha_apertura": "1990-06-20"
    }
  },
  {
    "model": "healthcare.hospital",
    "pk": 3,
    "fields": {
      "nombre": "Urgencias Wayne Express",
      "tipo": "centro_urgencias",
      "direccion": "500 Emergency Lane, Downtown Gotham",
      "telefono": "(555) 911-0000",
      "email": "emergencias@wayne-healthcare.gotham",
      "capacidad_camas": 50,
      "medicos_activos": 25,
      "enfermeras": 60,
      "emergencias_24h": true,
      "unidad_cuidados_intensivos": false,
      "quirofanos": 2,
      "especialidades": "Emergencias, Traumatología, Medicina General",
      "acepta_seguro_wayne": true,
      "activo": true,
      "fecha_apertura": "2005-01-10"
    }
  },
  {
    "model": "healthcare.hospital",
    "pk": 4,
    "fields": {
      "nombre": "Centro Cardiovascular Wayne",
      "tipo": "clinica",
      "direccion": "300 Heart Boulevard, Gotham South",
      "telefono": "(555) 100-4000",
      "email": "corazon@wayne-healthcare.gotham",
      "capacidad_camas": 80,
      "medicos_activos": 35,
      "enfermeras": 90,
      "emergencias_24h": true,
      "unidad_cuidados_intensivos": true,
      "quirofanos": 6,
      "especialidades": "Cardiología, Cirugía Cardiovascular, Rehabilitación Cardiaca",
      "acepta_seguro_wayne": true,
      "activo": true,
      "fecha_apertura": "1985-09-25"
    }
  },
  {
    "model": "healthcare.hospital",
    "pk": 5,
    "fields": {
      "nombre": "Hospital Infantil Wayne",
      "tipo": "hospital",
      "direccion": "150 Children Way, Gotham East",
      "telefono": "(555) 100-5000",
      "email": "ninos@wayne-healthcare.gotham",
      "capacidad_camas": 200,
      "medicos_activos": 60,
      "enfermeras": 180,
      "emergencias_24h": true,
      "unidad_cuidados_intensivos": true,
      "quirofanos": 5,
      "especialidades": "Pediatría, Neonatología, Oncología Pediátrica, Cirugía Pediátrica",
      "acepta_seguro_wayne": true,
      "activo": true,
      "fecha_apertura": "1995-11-12"
    }
  },
  {
    "model": "healthcare.serviciomedico",
    "pk": 1,
    "fields": {
      "nombre": "Consulta General",
      "categoria": "consulta",
      "descripcion": "Evaluación médica completa por médico general. Incluye revisión de signos vitales, historial médico y orientación.",
      "precio_sin_seguro": "150.00",
      "precio_con_seguro_wayne": "20.00",
      "duracion_minutos": 30,
      "requiere_cita_previa": true,
      "disponible_emergencias": false,
      "hospitales": [1, 3, 5]
    }
  },
  {
    "model": "healthcare.serviciomedico",
    "pk": 2,
    "fields": {
      "nombre": "Atención de Emergencias",
      "categoria": "emergencia",
      "descripcion": "Atención médica inmediata para emergencias 24/7. Incluye estabilización, diagnóstico de emergencia y tratamiento inicial.",
      "precio_sin_seguro": "2500.00",
      "precio_con_seguro_wayne": "100.00",
      "duracion_minutos": 120,
      "requiere_cita_previa": false,
      "disponible_emergencias": true,
      "hospitales": [1, 3]
    }
  },
  {
    "model": "healthcare.serviciomedico",
    "pk": 3,
    "fields": {
      "nombre": "Resonancia Magnética",
      "categoria": "diagnostico",
      "descripcion": "Estudio por imagen de alta resolución. Utilizado para diagnóstico de neurología, oncología, ortopedia.",
      "precio_sin_seguro": "1200.00",
      "precio_con_seguro_wayne": "200.00",
      "duracion_minutos": 45,
      "requiere_cita_previa": true,
      "disponible_emergencias": true,
      "hospitales": [1, 4]
    }
  },
  {
    "model": "healthcare.serviciomedico",
    "pk": 4,
    "fields": {
      "nombre": "Cirugía Cardiovascular",
      "categoria": "cirugia",
      "descripcion": "Procedimientos quirúrgicos del corazón y vasos sanguíneos. Realizado por cirujanos cardiovasculares certificados.",
      "precio_sin_seguro": "50000.00",
      "precio_con_seguro_wayne": "5000.00",
      "duracion_minutos": 240,
      "requiere_cita_previa": true,
      "disponible_emergencias": true,
      "hospitales": [1, 4]
    }
  },
  {
    "model": "healthcare.serviciomedico",
    "pk": 5,
    "fields": {
      "nombre": "Quimioterapia",
      "categoria": "tratamiento",
      "descripcion": "Tratamiento oncológico con medicamentos. Incluye monitoreo, manejo de efectos secundarios y apoyo nutricional.",
      "precio_sin_seguro": "8000.00",
      "precio_con_seguro_wayne": "800.00",
      "duracion_minutos": 180,
      "requiere_cita_previa": true,
      "disponible_emergencias": false,
      "hospitales": [2]
    }
  },
  {
    "model": "healthcare.doctor",
    "pk": 1,
    "fields": {
      "nombre_completo": "Sarah Mitchell",
      "especialidad": "cardiologia",
      "hospital_principal": 4,
      "anos_experiencia": 15,
      "certificaciones": "Board Certified Cardiology, Fellowship Interventional Cardiology",
      "rating": "4.95",
      "email": "dr.mitchell@wayne-healthcare.gotham",
      "telefono_consulta": "(555) 100-4001",
      "acepta_nuevos_pacientes": true,
      "horario_atencion": "Lunes a Viernes 8:00 - 16:00"
    }
  },
  {
    "model": "healthcare.doctor",
    "pk": 2,
    "fields": {
      "nombre_completo": "James Chen",
      "especialidad": "oncologia",
      "hospital_principal": 2,
      "anos_experiencia": 20,
      "certificaciones": "Medical Oncology, Hematology, Palliative Care",
      "rating": "4.88",
      "email": "dr.chen@wayne-healthcare.gotham",
      "telefono_consulta": "(555) 100-3001",
      "acepta_nuevos_pacientes": true,
      "horario_atencion": "Lunes a Jueves 9:00 - 17:00"
    }
  },
  {
    "model": "healthcare.doctor",
    "pk": 3,
    "fields": {
      "nombre_completo": "Maria Rodriguez",
      "especialidad": "pediatria",
      "hospital_principal": 5,
      "anos_experiencia": 12,
      "certificaciones": "Pediatrics, Pediatric Emergency Medicine",
      "rating": "4.92",
      "email": "dr.rodriguez@wayne-healthcare.gotham",
      "telefono_consulta": "(555) 100-5001",
      "acepta_nuevos_pacientes": true,
      "horario_atencion": "Lunes a Viernes 8:00 - 18:00, Sábados 9:00 - 13:00"
    }
  }
]
```

### Paso 5: URLs

**`healthcare/urls.py`**:

```python
from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Paso 6: Vistas

**`healthcare/views.py`**:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hospital, ServicioMedico, Doctor


@login_required
def home(request):
    """Página principal de Wayne Healthcare"""
    
    hospitales = Hospital.objects.filter(activo=True)
    total_camas = sum(h.capacidad_camas for h in hospitales)
    total_personal = sum(h.personal_total for h in hospitales)
    
    servicios = ServicioMedico.objects.all()[:6]
    doctores = Doctor.objects.filter(acepta_nuevos_pacientes=True)[:5]
    
    context = {
        'hospitales': hospitales,
        'total_camas': total_camas,
        'total_personal': total_personal,
        'servicios': servicios,
        'doctores': doctores,
    }
    
    return render(request, 'healthcare/home.html', context)
```

### Paso 7: Integrar

**`settings.py`**:
```python
INSTALLED_APPS = [
    # ... otras apps ...
    'healthcare',
]
```

**`urls.py` principal**:
```python
path('healthcare/', include('healthcare.urls')),
```

### Paso 8: Migraciones

```bash
python manage.py makemigrations healthcare
python manage.py migrate
python manage.py loaddata healthcare/fixtures/datos.json
python manage.py runserver
```

---

## Checklist

- [ ] Modelo `Hospital` creado
- [ ] Dataset con 5 hospitales
- [ ] Modelo `ServicioMedico` con precios
- [ ] Modelo `Doctor` con especialidades
- [ ] Template que muestre hospitales y servicios
- [ ] `'healthcare'` en `INSTALLED_APPS`
- [ ] URL `/healthcare/` configurada
- [ ] Datos cargados y funcionando

---

## Recursos

Mira ejemplos en:
- `foundation/` - App completa de Camilo
- `realestate/` - App de Perlaza
- `ventures/` - App de Juliana
