# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises. Cada compañero desarrolla una app de división que se integra al portal central.

---

## Divisiones

| # | División | App | Responsable | Estado |
|---|----------|-----|-------------|--------|
| 1 | Wayne Technologies | `tech` | — | Pendiente |
| 2 | Wayne Industries | `industries` | — | Pendiente |
| 3 | Wayne Healthcare | `healthcare` | — | Pendiente |
| 4 | Wayne Real Estate | `realestate` | — | Activo |
| 5 | Wayne Capital | `capital` | — | Pendiente |
| 6 | Wayne Foundation | `foundation` | Nicolás | Activo |
| 7 | Wayne Ventures | `ventures` | Juliana | Activo |

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
- `/accounts/admin/roles/` — Gestión de roles (admin)

Todas las apps de división requieren login.

---

## Configuración Inicial

```bash
# 1. Clonar el repositorio
git clone https://github.com/nicohr3366/Wayne-Enterprises.git
cd Wayne-Enterprises

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno (Windows)
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Preparar base de datos
python manage.py migrate

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

---

## Flujo de Trabajo Git

### Configuración inicial (solo una vez)

```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Crear tu rama de trabajo
git checkout -b Nombre_Apellido
```

### Trabajo diario

```bash
# 1. Activar entorno
venv\Scripts\activate

# 2. Bajar cambios del main antes de empezar
git pull origin main

# 3. Ver cambios realizados
git status

# 4. Agregar cambios
git add .

# 5. Hacer commit
git commit -m "feat: descripción de cambios"

# 6. Subir a GitHub
git push origin tu-rama
```

---

## Cómo conectar tu app al portal

### Estructura requerida

```
tu_app/
├── migrations/
│   └── __init__.py
├── templates/
│   └── tu_app/
│       └── home.html
├── static/
│   └── tu_app/
│       ├── css/
│       └── js/
├── __init__.py
├── urls.py          # Debe tener app_name = 'tu_app'
├── views.py
└── ...
```

### Requisitos para urls.py

```python
from django.urls import path
from . import views

app_name = 'tu_app'  # IMPORTANTE

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

## URLs Reservadas

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

## Errores Comunes

| Error | Solución |
|-------|----------|
| "No module named 'django'" | Activar entorno: `venv\Scripts\activate` |
| "not a git repository" | Estar en la carpeta `Wayne-Enterprises` |
| "Table doesn't exist" | Ejecutar: `python manage.py migrate` |
| Template no encontrado | Revisar ruta: `templates/tu_app/home.html` |
| Tarjeta en "Próximamente" | Verificar `app_name` en `urls.py` y `INSTALLED_APPS` |

---

## Reglas del Equipo

- Trabajar en tu propia rama, **nunca en `main`**
- Hacer `git pull origin main` antes de empezar cada día
- Commits con mensajes claros (`feat:`, `fix:`, `style:`)
- Avisar a Nicolás cuando el PR esté listo
- No modificar `core/` ni `accounts/` sin coordinar
- No subir `venv/` ni `db.sqlite3`

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

## Tecnologías

- Python 3.13 / Django 6.0.3
- SQLite
- HTML / CSS / JavaScript
- Git + GitHub

---

## Contacto

¿Problemas con Git o tu app? Avisa a Nicolás con captura de pantalla.
