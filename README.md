# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises con 7 divisiones de negocio.
Cada compañero desarrolla su dataset ETL dentro de la app de su división.

---

## 📋 Asignación: Quién trabaja dónde

| Compañero | Dataset | App Django | Carpeta de trabajo | Branch |
|---|---|---|---|---|
| **Nicolás** | Contratos Defensa ETL/XML | `apps/core/` | `apps/core/data/` | `main` |
| **Cuervo** | Telemetría Tumbler | `apps/tech/` | `apps/tech/data/` | `cuervo` |
| **Camilo** | Stock Market WayneTech | `apps/capital/` | `apps/capital/data/` | `Camilo_Piedrahita` |
| **Emerick / Drada** | Donaciones Fundación / Clean Energy | `apps/foundation/` | `apps/foundation/data/` | `Valeria-Drada` |
| **Juan José** | Red Eléctrica Gotham | `apps/industries/` | `apps/industries/data/` | `Juan_Jose_Arango` |
| **Juliana** | Satélites WayneTech | `apps/ventures/` | `apps/ventures/data/` | `WayneVentures_JulianaHoyos` |
| **Valeria** | Desarrollo Urbano Gotham | `apps/realestate/` | `apps/realestate/data/` | `Valeria` |
| **Danna** | Ciberseguridad ML/ETL | `apps/healthcare/` | `apps/healthcare/data/` | `Danna` |
| **Perlaza** | Aerospace / Inventario drones | `apps/realestate/` | `apps/realestate/data/` | `Perlaza_WayneRealEstate` |
| **Diego** | Patentes Nanotech | `apps/tech/` | `apps/tech/data/` | `Diego` |
| **Pérez** | RRHH Wayne Manor (RBAC) | `apps/accounts/` | `apps/accounts/data/` | `perez_Wayne-Manor` |

> **Regla:** Tu CSV/Excel **siempre** va en `apps/[tu_app]/data/`. Esa carpeta está en `.gitignore` — el archivo no se sube a GitHub, cada quien lo tiene localmente.

---

## 🗂️ Estructura del Proyecto

```
Wayne-Enterprises-2/
├── apps/
│   ├── accounts/              # Autenticación, roles (Pérez)
│   │   └── data/              # ← CSV de RRHH va aquí
│   ├── capital/               # Wayne Capital — finanzas (Camilo)
│   │   └── data/              # ← CSV de Stock Market va aquí
│   ├── core/                  # Portal principal + ETL Contratos Defensa (Nicolás)
│   │   ├── data/              # ← contratos.csv va aquí
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── load_contracts.py
│   │   ├── models.py          # modelo DefenseContract (51 campos)
│   │   ├── views.py           # dashboard, lista, detalle, exportar CSV
│   │   └── templates/core/
│   │       ├── contracts_dashboard.html
│   │       ├── contracts_list.html
│   │       └── contract_detail.html
│   ├── foundation/            # Wayne Foundation — donaciones (Emerick/Drada)
│   │   └── data/
│   ├── healthcare/            # Wayne Healthcare (Danna — Ciberseguridad)
│   │   └── data/
│   ├── industries/            # Wayne Industries — energía (Juan José)
│   │   └── data/
│   ├── realestate/            # Wayne Real Estate (Valeria / Perlaza)
│   │   └── data/
│   ├── tech/                  # Wayne Technologies (Cuervo / Diego)
│   │   └── data/
│   └── ventures/              # Wayne Ventures (Juliana)
│       └── data/
├── wayne_enterprise/          # Configuración principal Django
│   ├── settings.py
│   └── urls.py
├── manage.py
└── venv/                      # NO subir a Git
```

---

## ➕ Cómo agregar tu dataset (4 pasos)

Sigue exactamente este flujo. El ejemplo usa `capital` (Camilo / Stock Market) pero aplica a cualquier app.

### Paso 1 — Crea la carpeta `data/` y pon tu CSV ahí

```
apps/capital/data/stocks.csv      ← tu archivo aquí
apps/capital/data/.gitkeep        ← archivo vacío para que git vea la carpeta
```

El CSV **no se sube a GitHub** (está en `.gitignore`). El `.gitkeep` sí se sube para que la carpeta exista cuando alguien clone el repo.

### Paso 2 — Crea el modelo en `apps/[tu_app]/models.py`

```python
from django.db import models

class StockRecord(models.Model):
    ticker       = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    date         = models.DateField()
    open_price   = models.DecimalField(max_digits=12, decimal_places=4)
    close_price  = models.DecimalField(max_digits=12, decimal_places=4)
    volume       = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.ticker} — {self.date}"
```

Luego corre las migraciones:
```bash
python manage.py makemigrations capital
python manage.py migrate
```

### Paso 3 — Crea el management command para cargar datos

Crea esta estructura de carpetas:
```
apps/capital/management/__init__.py        ← archivo vacío
apps/capital/management/commands/__init__.py   ← archivo vacío
apps/capital/management/commands/load_stocks.py
```

Contenido de `load_stocks.py`:
```python
import csv
from django.core.management.base import BaseCommand
from apps.capital.models import StockRecord

class Command(BaseCommand):
    help = 'Carga registros de Stock Market desde CSV'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/capital/data/stocks.csv')

    def handle(self, *args, **options):
        registros = []
        with open(options['file'], encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registros.append(StockRecord(
                    ticker=row['TICKER'],
                    company_name=row['COMPANY'],
                    # ... mapear el resto de columnas de tu CSV
                ))
        StockRecord.objects.bulk_create(registros, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(registros)} registros cargados.'))
```

Ejecutar:
```bash
python manage.py load_stocks
```

### Paso 4 — Crea las vistas y templates

En `apps/capital/views.py`:
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StockRecord

@login_required
def home(request):
    return render(request, 'capital/home.html', {})

@login_required
def stocks_dashboard(request):
    records = StockRecord.objects.all()
    return render(request, 'capital/stocks_dashboard.html', {'records': records})
```

En `apps/capital/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stocks/', views.stocks_dashboard, name='stocks_dashboard'),
]
```

---

## 🔑 Sistema de Roles

El sistema tiene 9 roles jerárquicos. El admin puede asignarlos en `/accounts/admin/roles/`.

| Rol | Código | Descripción |
|---|---|---|
| Administrador | `admin` | Acceso total al sistema |
| Ejecutivo C-Suite | `executive` | CEO, COO, CFO, CIO, CTO, CISO |
| Director de División | `division_manager` | Líderes de cada división |
| Gerente de Tecnología | `tech_manager` | TI, DevOps, Platform Engineering |
| Analista de Seguridad | `security_analyst` | CISO área, cumplimiento CMMC/NIST |
| Analista FinOps | `finops_analyst` | Control de costos cloud |
| Gerente PMO | `pmo_manager` | Gestión de proyectos |
| Gerente de RRHH | `hr_manager` | Talento y capacitación |
| Usuario | `usuario` | Acceso básico al portal |

Para restringir una vista a un rol mínimo:
```python
from apps.accounts.views import rol_requerido

@rol_requerido('division_manager')
def vista_confidencial(request):
    ...
```

---

## 🗄️ Configuración de Base de Datos (MariaDB 10.6+)

> **IMPORTANTE:** Django 6.0 requiere **MariaDB 10.6 o superior**. XAMPP trae MariaDB 10.4 que **NO es compatible**.

### 1. Instalar MariaDB 10.6

1. Descarga **MariaDB 10.6** desde: https://mariadb.org/download/
2. Selecciona **Windows → MSI Package (x86_64)**
3. Durante la instalación: sin contraseña para root (más simple)
4. Puerto: `3306`. Si XAMPP está corriendo, apaga MySQL primero.

### 2. Crear la Base de Datos

```powershell
& "C:\Program Files\MariaDB 10.6\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS wayne_enterprise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Crear Tablas

```bash
python manage.py migrate
```

---

## 💻 Instalación del Proyecto

```bash
# 1. Clonar
git clone https://github.com/nicohr3366/Wayne-Enterprises.git
cd Wayne-Enterprises

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Dependencias
pip install django PyMySQL

# 4. Migraciones
python manage.py migrate

# 5. Superusuario (opcional)
python manage.py createsuperuser

# 6. Servidor
python manage.py runserver
```

Abre: `http://127.0.0.1:8000`

---

## 🔄 Flujo de Trabajo Git

### Configuración inicial (solo una vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Cambiar a tu rama

```bash
# Ver en qué rama estás
git branch

# Cambiar a tu rama (reemplaza con tu nombre)
git checkout Camilo_Piedrahita

# Si tu rama NO existe todavía, créala desde main
git checkout main
git pull origin main
git checkout -b Tu_Nombre
git push -u origin Tu_Nombre
```

### Trabajo diario

```bash
# 1. Bajar cambios nuevos de main
git pull origin main

# 2. Trabajar en tu app...

# 3. Ver qué cambiaste
git status

# 4. Agregar tus archivos (SOLO los tuyos, no los de otros)
git add apps/capital/
git add apps/capital/templates/

# 5. Commit
git commit -m "feat: agrega modelo StockRecord y dashboard"

# 6. Subir tu rama
git push origin Camilo_Piedrahita
```

### Mensajes de commit

```bash
git commit -m "feat: agrega modelo para dataset stock market"
git commit -m "fix: corrige error en template de capital"
git commit -m "style: mejora CSS del dashboard"
git commit -m "data: agrega script de carga ETL"
git commit -m "docs: actualiza README con instrucciones de capital"
```

### Para integrar tu trabajo a main (Pull Request)

1. Sube tu rama: `git push origin Tu_Nombre`
2. Ve a GitHub → **Pull Requests** → **New Pull Request**
3. Base: `main` ← Compare: `Tu_Nombre`
4. Describe qué hiciste y pide revisión

---

## 📊 Estado del Proyecto

| App | Modelo | ETL | Vistas | Template | Responsable |
|---|---|---|---|---|---|
| `core` | ✅ DefenseContract | ✅ load_contracts | ✅ dashboard + lista + detalle | ✅ | Nicolás |
| `accounts` | ✅ UserProfile (9 roles) | — | ✅ login/registro/roles | ✅ | Nicolás |
| `realestate` | ✅ Property | — | 🔲 | 🔲 | Valeria / Perlaza |
| `ventures` | ✅ NavItem | — | 🔲 | 🔲 | Juliana |
| `capital` | 🔲 | 🔲 | 🔲 | 🔲 | Camilo |
| `tech` | 🔲 | 🔲 | 🔲 | 🔲 | Cuervo / Diego |
| `industries` | 🔲 | 🔲 | 🔲 | 🔲 | Juan José |
| `healthcare` | 🔲 | 🔲 | 🔲 | 🔲 | Danna |
| `foundation` | 🔲 | 🔲 | 🔲 | 🔲 | Emerick / Drada |

✅ = implementado · 🔲 = pendiente

que panda haga ET y streamlit el L de ETL
