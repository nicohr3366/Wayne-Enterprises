# Guía Individual: Camilo - Wayne Foundation

> **Responsable:** Camilo  
> **División:** Wayne Foundation (foundation)  
> **Estado:** ✅ Activo - App completa y funcionando  
> **Rama Git:** `camilo` o `Camilo_Apellido`

---

## ¿Qué es Wayne Foundation?

Wayne Foundation es la división de responsabilidad social y filantropía del conglomerado. Gestiona:
- Programas de ayuda comunitaria
- Becas educativas
- Proyectos de desarrollo social
- Donaciones y patrocinios

---

## Tu App Actual

Tu app `foundation` ya está **completa y funcionando** en el portal.

### Estructura de tu App
```
foundation/
├── migrations/
│   └── __init__.py
├── templates/foundation/
│   └── home.html          ← Tu página principal
├── static/foundation/
│   └── css/               ← Estilos de Foundation
├── __init__.py
├── urls.py                ← URLs de tu app
├── views.py               ← Lógica de vistas
└── apps.py
```

### URLs de tu App
- `/foundation/` - Página principal de Foundation
- Requiere login (protegida)

---

## Dataset Sugerido para Foundation

Tu app debería tener datos de ejemplo sobre proyectos filantrópicos.

### Ejemplo de Dataset (JSON)

Crear archivo: `foundation/fixtures/datos.json`

```json
[
  {
    "model": "foundation.proyecto",
    "pk": 1,
    "fields": {
      "nombre": "Becas Educativas Gotham",
      "descripcion": "Programa de becas para estudiantes de bajos recursos en Gotham City",
      "categoria": "educacion",
      "presupuesto": 5000000.00,
      "fecha_inicio": "2024-01-15",
      "activo": true,
      "beneficiarios": 250
    }
  },
  {
    "model": "foundation.proyecto",
    "pk": 2,
    "fields": {
      "nombre": "Centro de Rehabilitación Arkham",
      "descripcion": "Centro de apoyo psicológico y rehabilitación para ex-pacientes",
      "categoria": "salud",
      "presupuesto": 3200000.00,
      "fecha_inicio": "2023-08-20",
      "activo": true,
      "beneficiarios": 150
    }
  },
  {
    "model": "foundation.proyecto",
    "pk": 3,
    "fields": {
      "nombre": "Comedores Comunitarios",
      "descripcion": "Red de comedores que sirven 10,000 comidas diarias",
      "categoria": "alimentacion",
      "presupuesto": 1800000.00,
      "fecha_inicio": "2023-03-10",
      "activo": true,
      "beneficiarios": 10000
    }
  },
  {
    "model": "foundation.proyecto",
    "pk": 4,
    "fields": {
      "nombre": "Tech Gotham",
      "descripcion": "Programa de enseñanza de programación para jóvenes",
      "categoria": "tecnologia",
      "presupuesto": 2200000.00,
      "fecha_inicio": "2024-06-01",
      "activo": true,
      "beneficiarios": 500
    }
  },
  {
    "model": "foundation.proyecto",
    "pk": 5,
    "fields": {
      "nombre": "Refugios de Invierno",
      "descripcion": "Alojamiento temporal durante temporada de frío",
      "categoria": "vivienda",
      "presupuesto": 4100000.00,
      "fecha_inicio": "2023-11-01",
      "activo": true,
      "beneficiarios": 800
    }
  }
]
```

### Categorías para Foundation
- `educacion` - Becas y programas educativos
- `salud` - Centros médicos y rehabilitación
- `alimentacion` - Comedores y bancos de alimentos
- `vivienda` - Refugios y vivienda temporal
- `tecnologia` - Capacitación tech
- `arte` - Patrocinio cultural
- `medio_ambiente` - Proyectos ecológicos

---

## Modelo Sugerido (models.py)

Si quieres agregar un modelo para tu dataset:

```python
from django.db import models

class Proyecto(models.Model):
    CATEGORIAS = [
        ('educacion', 'Educación'),
        ('salud', 'Salud'),
        ('alimentacion', 'Alimentación'),
        ('vivienda', 'Vivienda'),
        ('tecnologia', 'Tecnología'),
        ('arte', 'Arte y Cultura'),
        ('medio_ambiente', 'Medio Ambiente'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    presupuesto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_inicio = models.DateField()
    activo = models.BooleanField(default=True)
    beneficiarios = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='foundation/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Proyecto Foundation"
        verbose_name_plural = "Proyectos Foundation"
```

### Crear y aplicar migraciones:
```bash
python manage.py makemigrations foundation
python manage.py migrate
```

---

## Trabajo en tu Rama

### Tu Rama Git
Debes tener una rama llamada `camilo` o `Camilo_Apellido`.

### Comandos Diarios
```bash
# 1. Cambiar a tu rama
git checkout camilo

# 2. Bajar cambios del main
git pull origin main

# 3. Ver qué cambiaste
git status

# 4. Agregar cambios
git add .

# 5. Commit con mensaje claro
git commit -m "feat: agrega dataset de proyectos foundation"

# 6. Subir a GitHub
git push origin camilo
```

---

## Checklist de Entrega

- [ ] Dataset con al menos 5 proyectos de Foundation
- [ ] Modelo Proyecto creado (opcional pero recomendado)
- [ ] Datos mostrándose en el template home.html
- [ ] CSS responsivo para móviles
- [ ] Commit y push a tu rama
- [ ] Pull Request listo para revisión

---

## Ayuda a tus Compañeros

Como tu app ya está funcionando, puedes ayudar a:
- **Cuervo** (Tech) - Con la estructura básica
- **Diego Granja** (Industries) - Con modelos y datasets
- **Valeria** (Capital) - Con estilos CSS

---

## Contacto

¿Preguntas? Contacta a:
- **Nicolás** - Coordinación general
- **Perlaza/Juliana** - Ya tienen apps activas también

---

## Recursos Útiles

- Template base: `templates/base.html` (extends)
- Colores corporativos: Dorado `#C9A84C`, Negro `#050507`
- Ejemplo: Ver `realestate` o `ventures` para referencia
