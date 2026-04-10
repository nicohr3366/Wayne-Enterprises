# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises. Cada compañero desarrolla una app de división que se integra al portal central.

---

## Divisiones

| # | División | App | Responsable | Estado |
|---|----------|-----|-------------|--------|
| 1 | Wayne Technologies | `tech` | — | Pendiente |
| 2 | Wayne Industries | `industries` | — | Pendiente |
| 3 | Wayne Healthcare | `healthcare` | — | Pendiente |
| 4 | Wayne Real Estate | `realestate` | — | Pendiente |
| 5 | Wayne Capital | `capital` | — | Pendiente |
| 6 | Wayne Foundation | `foundation` | Nicolás | Activo |
| 7 | Wayne Ventures | `ventures` | — | Pendiente |

---

## Sistema de Autenticación

El portal tiene **usuarios con roles**:
- **Usuario**: Acceso básico
- **Administrador**: Puede gestionar otros usuarios

### URLs importantes
- `/accounts/registro/` — Crear cuenta
- `/accounts/login/` — Iniciar sesión
- `/accounts/dashboard/` — Panel de control
- `/accounts/logout/` — Cerrar sesión

Todas las apps de división requieren login.

---

## Guía Rápida Git

### Conceptos básicos

- **Repositorio**: Carpeta del proyecto con historial
- **Rama `main`**: Código oficial (no tocar directamente)
- **Tu rama**: Donde trabajas (`Nombre_Apellido`)
- **Commit**: Guardar cambios con mensaje descriptivo

### Flujo diario de trabajo

```bash
# 1. Activar entorno virtual (Windows)
venv\Scripts\activate

# 2. Bajar cambios del main antes de empezar
git pull origin main

# 3. Trabajar en tu código...

# 4. Ver cambios realizados
git status

# 5. Agregar cambios
git add .

# 6. Hacer commit
git commit -m "feat: descripción de cambios"

# 7. Subir a GitHub
git push origin tu-rama
```

### Configuración inicial (solo una vez)

```bash
# Instalar Git desde https://git-scm.com/downloads

# Configurar tu nombre
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Clonar el repositorio
git clone https://github.com/nicohr3366/Wayne-Enterprises.git

# Entrar a la carpeta
cd Wayne-Enterprises

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Preparar base de datos
python manage.py migrate

# Crear tu rama
git checkout -b Nombre_Apellido
```

---

## Cómo conectar tu app al portal

### Estructura requerida

```
tu_app/
├── migrations/
│   └── __init__.py
├── templates/
│   └── tu_app/              # Subcarpeta con nombre de tu app
│       └── home.html
├── static/
│   └── tu_app/
│       ├── css/
│       └── js/
├── __init__.py
├── urls.py                  # Debe tener app_name = 'tu_app'
├── views.py
└── ...
```

### Requisitos para urls.py

```python
from django.urls import path
from . import views

app_name = 'tu_app'  # IMPORTANTE: debe coincidir con tu app

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Proteger vistas con login

```python
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'tu_app/home.html')
```

### Pasos de integración

1. Copiar tu carpeta al proyecto (al lado de `core/`)
2. Agregar en `settings.py` → `INSTALLED_APPS`
3. Agregar en `urls.py` → `urlpatterns`
4. Crear migraciones: `python manage.py makemigrations tu_app`
5. Aplicar migraciones: `python manage.py migrate`
6. Probar: `python manage.py runserver`

---

## Hacer un Pull Request

1. Sube tus cambios: `git push origin tu-rama`
2. Ve al repo en GitHub
3. Clic en **"Compare & pull request"**
4. Escribe título descriptivo: `feat: agrego app [nombre]`
5. Describe los cambios
6. Clic en **"Create pull request"**
7. Nicolás revisa y acepta

---

## URLs reservadas

| División | URL |
|----------|-----|
| tech | `/tech/` |
| industries | `/industries/` |
| healthcare | `/healthcare/` |
| realestate | `/realestate/` |
| capital | `/capital/` |
| foundation | `/foundation/` |
| ventures | `/ventures/` |

---

## Errores comunes

| Error | Solución |
|-------|----------|
| "No module named 'django'" | Activar entorno: `venv\Scripts\activate` |
| "not a git repository" | Estar en la carpeta `Wayne-Enterprises` |
| "Table doesn't exist" | Ejecutar: `python manage.py migrate` |
| Template no encontrado | Revisar ruta: `templates/tu_app/home.html` |
| Tarjeta en "Próximamente" | Verificar `app_name` en `urls.py` y `INSTALLED_APPS` |
| Conflicto al hacer push | Hacer `git pull origin tu-rama` primero |

---

## Reglas del equipo

- Trabajar en tu propia rama, **nunca en `main`**
- Hacer `git pull origin main` antes de empezar cada día
- Commits con mensajes claros (`feat:`, `fix:`, `style:`)
- Avisar a Nicolás cuando el PR esté listo
- No modificar `core/` ni `accounts/` sin coordinar
- No subir `venv/` ni `db.sqlite3`

---

## Tecnologías

- Python 3.13 / Django 6.0.3
- SQLite
- HTML / CSS / JavaScript
- Git + GitHub

---

## Contacto

¿Problemas con Git o tu app? Avisa a Nicolás con captura de pantalla.
