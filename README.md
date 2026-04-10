# Wayne Enterprises — Portal Corporativo


## ¿De qué va este proyecto?

Estamos construyendo un portal corporativo para Wayne Enterprises. Cada uno del grupo desarrolla su propia
app de Django para una división de la empresa, y todas se conectan
al portal central que está en este repositorio.

La página principal muestra las 7 divisiones. Cuando alguien conecta
su app, la tarjeta de esa división se activa automáticamente.


## Cómo conectar tu app al portal

### Lo que tu carpeta DEBE traer

Antes de integrar revisa que tenga esto:

```
tu_app/
├── migrations/
│   └── __init__.py        ← si no existe, créalo
├── templates/
│   └── tu_app/            ← subcarpeta con el nombre de tu app
│       └── home.html
├── static/
│   └── tu_app/
│       ├── css/
│       └── js/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

Tu `urls.py` debe tener mínimo esto:
```python
from django.urls import path
from . import views

app_name = 'nombre_de_tu_app'

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Pasos para integrar (Primero hablas conmigo antes de esto)

**1.** Copia tu carpeta en la raíz del proyecto, al lado de `core/`.

**2.** Agrega tu app en `wayne_enterprise/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'core',
    'tu_app',    # ← aquí
]
```

**3.** Agrega la URL en `wayne_enterprise/urls.py`:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tu_app/', include('tu_app.urls')),  # ← aquí
]
```

**4.** Migrar y probar:
```bash
python manage.py makemigrations tu_app
python manage.py migrate
python manage.py runserver
```

### URLs reservadas por división

| App | URL |
|-----|-----|
| tech | `/tech/` |
| industries | `/industries/` |
| healthcare | `/healthcare/` |
| realestate | `/realestate/` |
| capital | `/capital/` |
| foundation | `/foundation/` |
| ventures | `/ventures/` |

-

## Reglas del equipo

- ✅ Cada uno trabaja en su propia rama, nunca directamente en `main`
- ✅ Hacer commits con mensajes que expliquen qué se hizo
- ✅ Hacer `git pull origin main` antes de empezar cada día
- ✅ Avisar a Nicolás cuando el PR esté listo
- ❌ No modificar archivos de `core/` sin avisar
- ❌ No tocar `settings.py` ni `urls.py` sin coordinarlo
- ❌ No subir la carpeta `venv/` ni el archivo `db.sqlite3`

---

## Estructura del proyecto

```
Wayne-Enterprises/
│
├── core/                        # Portal principal — NO tocar
│   ├── static/core/
│   │   ├── css/portal.css
│   │   └── js/portal.js
│   ├── templates/core/home.html
│   ├── views.py
│   └── urls.py
│
├── wayne_enterprise/            # Configuración global de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Tecnologías

- Python 3.13 / Django 6.0.3
- HTML5 / CSS3 / JavaScript
- Google Fonts (Cinzel, Rajdhani)
- SQLite — base de datos local
- Git + GitHub — control de versiones
