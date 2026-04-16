# Guía Individual: Juliana - Wayne Ventures

> **Responsable:** Juliana  
> **División:** Wayne Ventures (ventures)  
> **Estado:** ✅ ACTIVO - App completa y funcionando  
> **Rama Git:** `juliana`

---

## Tu App Está Funcionando

La app `ventures` ya está completamente integrada al portal. Tu tarjeta muestra **disponible** y los usuarios pueden navegar tu sección.

### URLs de tu App
- `/ventures/` - Página principal de Ventures

### Características Actuales
- Sistema de navegación dinámica
- Estadísticas de startups
- Secciones: Portfolio, Startups, Pitch

---

## Dataset para Mejorar

Tu app usa navegación dinámica. Puedes mejorar agregando **más items de navegación** o **empresas del portfolio**.

### Agregar Items de Navegación

En `ventures/fixtures/navitems.json`:

```json
[
  {
    "model": "ventures.navitem",
    "pk": 6,
    "fields": {
      "label": "Nuevo Servicio",
      "url": "/ventures/nuevo/",
      "icon": "icon-star",
      "order": 6,
      "active": true
    }
  }
]
```

Cargar:
```bash
python manage.py loaddata ventures/fixtures/navitems.json
```

---

## Trabajo en tu Rama

### Tu Rama Git
Trabajas en la rama `juliana`.

### Comandos Diarios
```bash
# Cambiar a tu rama
git checkout juliana

# Bajar cambios del main
git pull origin main

# Guardar cambios
git add .
git commit -m "feat: descripción del cambio"
git push origin juliana
```

---

## Mejoras Sugeridas

1. **Modelo Startup:** Crear modelo para empresas incubadas
2. **Portfolio:** Mostrar empresas reales del portfolio
3. **Formulario de Pitch:** Formulario para emprendedores
4. **Estadísticas:** Gráficos de inversión y retornos
5. **Blog:** Noticias de startups

### Modelo Startup Sugerido

```python
# ventures/models.py

class Startup(models.Model):
    ETAPAS = [
        ('idea', 'Idea'),
        ('mvp', 'MVP'),
        ('seed', 'Seed'),
        ('serie_a', 'Serie A'),
        ('serie_b', 'Serie B+'),
        ('exit', 'Exit'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fundadores = models.CharField(max_length=500)
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    inversion_wayne = models.DecimalField(max_digits=12, decimal_places=2)
    valuation = models.DecimalField(max_digits=12, decimal_places=2)
    empleados = models.PositiveIntegerField()
    website = models.URLField()
    activa = models.BooleanField(default=True)
    fecha_fundacion = models.DateField()
    
    def __str__(self):
        return self.nombre
```

### Dataset de Startups

```json
[
  {
    "model": "ventures.startup",
    "pk": 1,
    "fields": {
      "nombre": "Gotham Tech Labs",
      "descripcion": "Startup de IA para seguridad urbana",
      "fundadores": "Bruce Chen, Sarah Smith",
      "etapa": "serie_a",
      "inversion_wayne": 5000000.00,
      "valuation": 50000000.00,
      "empleados": 45,
      "website": "https://gothamtech.io",
      "activa": true,
      "fecha_fundacion": "2021-03-15"
    }
  },
  {
    "model": "ventures.startup",
    "pk": 2,
    "fields": {
      "nombre": "CleanGotham",
      "descripcion": "Soluciones de energía limpia para la ciudad",
      "fundadores": "Maria Rodriguez",
      "etapa": "seed",
      "inversion_wayne": 1200000.00,
      "valuation": 8000000.00,
      "empleados": 12,
      "website": "https://cleangotham.com",
      "activa": true,
      "fecha_fundacion": "2023-01-10"
    }
  }
]
```

---

## Ayudar a Compañeros

Puedes ayudar a:
- **Valeria** (Capital) - Sistema de navegación
- **Cuervo** (Tech) - Estructura de modelos
- **Diego Granja** (Industries) - CSS y diseño

---

## Checklist de Mejoras

- [ ] Crear modelo Startup
- [ ] Dataset con 5+ startups
- [ ] Mostrar startups en template
- [ ] Formulario de contacto para pitches
- [ ] Estadísticas de portfolio
- [ ] Subir mejoras a rama juliana
