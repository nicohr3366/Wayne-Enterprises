# Guía Individual: Perlaza - Wayne Real Estate

> **Responsable:** Perlaza  
> **División:** Wayne Real Estate (realestate)  
> **Estado:** ✅ ACTIVO - App completa y funcionando  
> **Rama Git:** `perlaza`

---

## Tu App Está Funcionando

La app `realestate` ya está completamente integrada al portal. Tu tarjeta en el home muestra **disponible** y los usuarios pueden entrar con login.

### URLs de tu App
- `/realestate/` - Página principal de Real Estate
- `/realestate/propiedades/` - Listado de propiedades

---

## Dataset para Mejorar

Tu app actualmente usa un modelo `Property`. Puedes mejorarla agregando **más propiedades** al dataset.

### Ejemplo de Dataset Adicional

Si quieres agregar más propiedades, crea: `realestate/fixtures/extra_datos.json`

```json
[
  {
    "model": "realestate.property",
    "pk": 6,
    "fields": {
      "nombre": "Torre Wayne Penthouse",
      "descripcion": "Penthouse de lujo en el edificio emblemático de Wayne Enterprises",
      "tipo": "residencial",
      "direccion": "100 Wayne Tower, Downtown Gotham",
      "precio": 25000000.00,
      "area_m2": 850,
      "habitaciones": 5,
      "banos": 6,
      "estacionamientos": 3,
      "disponible": true,
      "destacado": true,
      "fecha_listado": "2024-01-15"
    }
  },
  {
    "model": "realestate.property",
    "pk": 7,
    "fields": {
      "nombre": "Complejo Industrial Robinson",
      "descripcion": "Parque industrial con 5 galpones y oficinas administrativas",
      "tipo": "industrial",
      "direccion": "500 Robinson Industrial Park, Gotham Port",
      "precio": 8500000.00,
      "area_m2": 15000,
      "habitaciones": 0,
      "banos": 12,
      "estacionamientos": 50,
      "disponible": true,
      "destacado": false,
      "fecha_listado": "2024-02-20"
    }
  }
]
```

Cargar datos adicionales:
```bash
python manage.py loaddata realestate/fixtures/extra_datos.json
```

---

## Trabajo en tu Rama

### Tu Rama Git
Trabajas en la rama `perlaza`.

### Comandos Diarios
```bash
# Cambiar a tu rama
git checkout perlaza

# Bajar cambios del main
git pull origin main

# Ver cambios
git status

# Guardar cambios
git add .
git commit -m "feat: agrega [descripción]"
git push origin perlaza
```

---

## Mejoras Sugeridas

Como tu app ya funciona, puedes enfocarte en:

1. **Más Propiedades:** Agregar 10-15 propiedades al dataset
2. **Filtros:** Permitir filtrar por tipo (residencial/comercial/industrial)
3. **Búsqueda:** Campo de búsqueda por nombre o ubicación
4. **Galería:** Más imágenes por propiedad
5. **Mapa:** Integrar mapa de Gotham (simulado)

---

## Modelo Actual

Tu modelo actual en `realestate/models.py`:

```python
class Property(models.Model):
    TIPOS = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('industrial', 'Industrial'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPOS)
    direccion = models.CharField(max_length=300)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    area_m2 = models.PositiveIntegerField()
    habitaciones = models.PositiveIntegerField()
    banos = models.PositiveIntegerField()
    estacionamientos = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='realestate/', blank=True)
    fecha_listado = models.DateField(auto_now_add=True)
```

---

## Ayudar a Compañeros

Puedes ayudar a quienes aún no tienen su app:
- **Diego Granja** (Industries) - Estructura básica
- **Valeria** (Capital) - CSS y estilos
- **Juan José** (Healthcare) - Modelos de datos
- **Cuervo** (Tech) - Templates

---

## Checklist de Mejoras

- [ ] Agregar 5+ propiedades al dataset
- [ ] Mejorar filtros en la página
- [ ] Agregar campo de búsqueda
- [ ] Responsive design para móviles
- [ ] Subir mejoras a tu rama
