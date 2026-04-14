# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises con 7 divisiones de negocio. Cada compañero desarrolla una app que se integra automáticamente al portal central.

---

## 📊 Estado del Proyecto - Asignaciones

### Apps Django (Divisiones Corporativas)

| # | División | App | Responsable | Estado | Guía |
|---|----------|-----|-------------|--------|------|
| 1 | Wayne Technologies | `tech` | **Cuervo** | 🔴 Pendiente | [Guía](docs/guia_cuervo.md) |
| 2 | Wayne Industries | `industries` | **Diego Granja** | 🔴 Pendiente | [Guía](docs/guia_diego_granja.md) |
| 3 | Wayne Healthcare | `healthcare` | **Juan José** | 🔴 Pendiente | [Guía](docs/guia_juan_jose.md) |
| 4 | Wayne Real Estate | `realestate` | **Perlaza** | ✅ Activo | [Guía](docs/guia_perlaza.md) |
| 5 | Wayne Capital | `capital` | **Valeria** | 🔴 Pendiente | [Guía](docs/guia_valeria.md) |
| 6 | Wayne Foundation | `foundation` | **Camilo** | ✅ Activo | [Guía](docs/guia_camilo.md) |
| 7 | Wayne Ventures | `ventures` | **Juliana** | ✅ Activo | [Guía](docs/guia_juliana.md) |

### Sistemas ETL y Datasets

| ID | Responsable | Dataset | Tipo | Descripción | Guía |
|----|-------------|---------|------|-------------|------|
| 1 | **Cuervo** | Telemetría Tumbler | ETL | Datos de impacto, velocidad, consumo | [Guía](docs/guia_cuervo.md) |
| 2 | **Nicolás** | Contratos Defensa | ETL/XML | Licitaciones gobierno EE.UU. | [Guía](docs/guia_nicolas.md) |
| 3 | **Camilo** | Stock Market | ETL | Acciones WayneTech, series temporales | [Guía](docs/guia_camilo.md) |
| 4 | **Emerick** | Donaciones Fundación | ETL | Ayuda a orfanatos y hospitales | [Guía](docs/guia_emerick.md) |
| 5 | **Juan José** | Red Eléctrica Gotham | ETL | Datos de carga de Wayne Energy | [Guía](docs/guia_juan_jose.md) |
| 6 | **Juliana** | Satélites | ETL | Logs de comunicaciones WayneTech | [Guía](docs/guia_juliana.md) |
| 7 | **Valeria** | Desarrollo Urbano | ETL | Costos reconstrucción Gotham | [Guía](docs/guia_valeria.md) |
| 8 | **Dana** | Ciberseguridad | ML/ETL | Intentos de hackeo, clasificación ML | [Guía](docs/guia_dana.md) |
| 9 | **Perlaza** | Aerospace | ETL | Inventario aviones y drones | [Guía](docs/guia_perlaza.md) |
| 10 | **Diego Granja** | Patentes Nanotech | ETL | Propiedad intelectual Wayne | [Guía](docs/guia_diego_granja.md) |
| 11 | **Pérez** | RRHH Wayne Manor | RBAC | Personal y sistema de permisos | [Guía](docs/guia_perez.md) |
| 12 | **Drada** | Clean Energy | ETL | Monitoreo reactor fusión | [Guía](docs/guia_drada.md) |
| 13 | *(Sin asignar)* | Adquisiciones Startups | ETL | Historial de compras | [Guía](docs/guia_dataset_13.md) |
| 14 | *(Sin asignar)* | Wayne Shipping | ETL | Logística marítima | [Guía](docs/guia_dataset_14.md) |
| 15 | *(Sin asignar)* | Brother Eye AI | ML/ETL | Sistema de vigilancia | [Guía](docs/guia_dataset_15.md) |

**Progreso Total: ~55%**

---

## 🚀 Inicio Rápido: Clonar y Ejecutar

### Paso 1: Clonar el Repositorio

Abre **Git Bash** o **PowerShell** y ejecuta:

```bash
# Clonar el repositorio
git clone https://github.com/nicohr3366/Wayne-Enterprises.git

# Entrar a la carpeta
cd Wayne-Enterprises
```

### Paso 2: Verificar tu Rama (Importante)

Cada persona tiene su propia rama. **Nunca trabajes en `main`**.

#### Ver ramas disponibles:
```bash
# Ver ramas remotas (las que están en GitHub)
git branch -r
```

Deberías ver algo como:
```
  origin/main
  origin/camilo
  origin/cuervo
  origin/diego_granja
  origin/juan_jose
  origin/juliana
  origin/perlaza
  origin/valeria
```

#### Cambiar a tu rama:
```bash
# Para Cuervo
git checkout cuervo

# Para Diego Granja
git checkout diego_granja

# Para Juan José
git checkout juan_jose

# Para Valeria
git checkout valeria

# Para Camilo, Perlaza, Juliana (ya tienen apps funcionando)
git checkout camilo
```

#### Si NO tienes tu rama creada:
```bash
# Crear tu rama desde main
git checkout main
git pull origin main
git checkout -b Nombre_Apellido

# Subir tu rama a GitHub
git push -u origin Nombre_Apellido
```

---

## 🗄️ Configuración de Base de Datos (XAMPP)

### 1. Instalar XAMPP

1. Descarga **XAMPP** desde: https://www.apachefriends.org
2. Ejecuta el instalador
3. **IMPORTANTE:** Solo instala **MySQL** (desmarca Apache si no lo necesitas)
4. Completa la instalación

### 2. Iniciar MySQL

1. Abre **XAMPP Control Panel** (busca en el menú inicio)
2. En la fila **MySQL**, clic en **Start**
3. Espera que diga **Running** en verde
4. Clic en **Admin** (se abre phpMyAdmin en el navegador)

### 3. Crear Base de Datos

1. En phpMyAdmin, clic en **Nueva** (menú izquierdo)
2. **Nombre:** `wayne_enterprise`
3. **Collation:** `utf8mb4_general_ci`
4. Clic en **Crear**

### 4. Verificar Configuración

El archivo `settings.py` ya está configurado. Solo verifica que MySQL esté corriendo.

### 5. Crear Tablas

```bash
# En la terminal de VS Code (estando en Wayne-Enterprises/)
python manage.py migrate
```

**Verifica en phpMyAdmin**: Debes ver tablas creadas como `auth_user`, `django_session`, etc.

---

## 💻 Instalación del Proyecto

### 1. Crear Entorno Virtual

```bash
# En la carpeta Wayne-Enterprises/
python -m venv venv
```

### 2. Activar Entorno (Windows)

```bash
venv\Scripts\activate
```

> Verás `(venv)` al inicio de la línea de comandos

### 3. Instalar Dependencias

```bash
python -m pip install django PyMySQL
```

### 4. Configurar PyMySQL

El archivo `wayne_enterprise/__init__.py` ya tiene:

```python
import pymysql
pymysql.version_info = (2, 2, 4, "final", 0)
pymysql.install_as_MySQLdb()
```

### 5. Crear Superusuario (Opcional pero recomendado)

```bash
python manage.py createsuperuser
```

- **Username:** `admin`
- **Email:** tu@email.com
- **Password:** tu contraseña

### 6. Iniciar Servidor

```bash
python manage.py runserver
```

Abre en navegador: `http://127.0.0.1:8000`

---

## 🗂️ Dataset y ETL: Explicación para Principiantes

### ¿Qué es un Dataset? (Fácil)

Imagina que estás creando una **agenda de contactos**. El **dataset** es simplemente la **lista de contactos de ejemplo** que pones para probar que tu agenda funciona.

**Ejemplo del mundo real:**
- 📱 App de contactos → Dataset: "Juan Pérez, tel: 555-0100"
- 🏥 App de hospitales → Dataset: "Hospital General, 100 camas"
- 🏢 App de empresas → Dataset: "Wayne Tech, 500 empleados"

**En este proyecto, cada persona tiene:**
1. **Una App Django** (su división de Wayne Enterprises)
2. **Un Dataset ETL** (sistema de procesamiento de datos)

---

### Tipos de Trabajo

#### Tipo A: Apps Django (Divisiones 1-7)
Crear una aplicación web que se integra al portal.

```
Ejemplo: Real Estate de Perlaza
├── Modelo Property (edificios)
├── Template HTML (página web)
└── Dataset JSON (edificios de ejemplo)
```

#### Tipo B: Sistemas ETL (IDs 1-12)
Crear scripts que procesan datos de diferentes fuentes.

```
Ejemplo: Dataset de Emerick (Donaciones)
├── CSV con donaciones
├── Script extract.py (lee datos)
├── Script transform.py (limpia)
├── Script load.py (guarda resultado)
└── Reporte HTML (resultado final)
```

---

### Paso a Paso: Crear tu Dataset (Muy Fácil)

#### Opción 1: Dataset JSON para Django (Apps de División)

**Paso 1:** Crear carpeta
```bash
mkdir tu_app/fixtures
```

**Paso 2:** Crear archivo de datos
Archivo: `tu_app/fixtures/datos.json`

```json
[
  {
    "model": "tu_app.nombre_modelo",
    "pk": 1,
    "fields": {
      "nombre": "Edificio Ejemplo",
      "precio": 100000
    }
  }
]
```

**Paso 3:** Cargar en Django
```bash
python manage.py loaddata tu_app/fixtures/datos.json
```

**Paso 4:** Ver en navegador
Abrir `http://127.0.0.1:8000/tu-app/` y verás tus datos.

#### Opción 2: Sistema ETL (Para IDs 1-12)

**Paso 1:** Crear estructura
```bash
mkdir tu_nombre_etl
cd tu_nombre_etl
mkdir data scripts output
```

**Paso 2:** Crear datos fuente
Archivo: `data/mis_datos.csv`
```csv
id,nombre,valor
1,Item A,100
2,Item B,200
```

**Paso 3:** Crear script Python
Archivo: `scripts/mi_script.py`
```python
import csv

# LEER datos
with open('data/mis_datos.csv') as f:
    datos = list(csv.DictReader(f))

# PROCESAR datos
for d in datos:
    d['valor_doble'] = int(d['valor']) * 2

# GUARDAR resultado
with open('output/resultado.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['id','nombre','valor_doble'])
    writer.writeheader()
    writer.writerows(datos)

print("¡Listo! Ver resultado.csv")
```

**Paso 4:** Ejecutar
```bash
python scripts/mi_script.py
```

---

### Dataset por Persona

| ID | Persona | Dataset | Formato | Dificultad |
|----|---------|---------|---------|------------|
| 1 | Cuervo | Telemetría Tumbler | CSV + ETL | Media |
| 2 | Nicolás | Contratos Defensa | JSON/XML | Media |
| 3 | Camilo | Stock Market | JSON + Charts | Media |
| 4 | Emerick | Donaciones | CSV + ETL | Fácil |
| 5 | Juan José | Red Eléctrica | CSV + Tiempo | Media |
| 6 | Juliana | Satélites | Logs CSV | Media |
| 7 | Valeria | Desarrollo Urbano | CSV + Costos | Fácil |
| 8 | Dana | Ciberseguridad | CSV + ML | Alta |
| 9 | Perlaza | Aerospace | JSON | Fácil |
| 10 | Diego Granja | Patentes | JSON + Fechas | Fácil |
| 11 | Pérez | RRHH | CSV + RBAC | Media |
| 12 | Drada | Clean Energy | CSV + Alertas | Media |

---

### Dataset por División (Apps Django)

| División | Qué incluir | Ejemplos | Mínimo Requerido |
|----------|-------------|----------|------------------|
| **Tech** | Proyectos tecnológicos | IA, robótica, defensa | 5 proyectos |
| **Industries** | Productos manufacturados | Motores, baterías, maquinaria | 5 productos |
| **Healthcare** | Hospitales, servicios médicos | Centros, doctores, tratamientos | 5 hospitales/servicios |
| **Real Estate** | Propiedades | Edificios, apartamentos, oficinas | 5 propiedades |
| **Capital** | Fondos de inversión | Portafolios, inversiones | 5 fondos |
| **Foundation** | Proyectos sociales | Becas, ayuda comunitaria | 5 proyectos |
| **Ventures** | Startups incubadas | Empresas, pitch decks | 5 startups |

---

### Verificar que tu Dataset Funciona

#### Para Apps Django:
1. Ejecutar `python manage.py loaddata tu_app/fixtures/datos.json`
2. Abrir `http://127.0.0.1:8000/tu-app/`
3. Debes ver los datos mostrados en la página

#### Para ETL:
1. Ejecutar tu script: `python scripts/tu_script.py`
2. Verificar que se creó el archivo en `output/`
3. Abrir el resultado (CSV, JSON o HTML) y verificar datos

---

### Errores Comunes en Datasets

| Error | Causa | Solución |
|-------|-------|----------|
| "No module named..." | No activaste el entorno virtual | `venv\Scripts\activate` |
| "Table doesn't exist" | No hiciste migraciones | `python manage.py migrate` |
| JSON no carga | Comillas mal puestas | Validar en jsonlint.com |
| CSV no lee | Codificación incorrecta | Guardar como UTF-8 |
| Datos no aparecen | No ejecutaste el script | Revisar que `output/` tenga archivos |

---

## 🔄 Flujo de Trabajo Git (Muy Importante)

### Configuración Inicial (Solo una vez)

```bash
# Configurar tu identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Verificar tu rama
git branch

# Si estás en main, cambia a tu rama
git checkout tu_rama
```

### Trabajo Diario (Cada vez que empiezas)

```bash
# 1. Asegúrate de estar en tu rama
git branch
# Debe decir: * tu_rama

# 2. Bajar cambios del main antes de empezar
git pull origin main

# 3. Ver qué archivos cambiaste
git status

# 4. Revisar cambios específicos
git diff nombre_archivo

# 5. Agregar cambios al área de preparación
git add nombre_archivo
# O agregar todos los cambios:
git add .

# 6. Guardar cambios (commit)
git commit -m "feat: descripción de lo que hiciste"

# 7. Subir a GitHub
git push origin tu_rama
```

### Mensajes de Commit

Usa prefijos para organizar tus cambios:

```bash
# Nueva funcionalidad
git commit -m "feat: agrega modelo Producto para industries"

# Corrección de errores
git commit -m "fix: corrige error en template de login"

# Mejoras visuales
git commit -m "style: mejora CSS de tarjetas de productos"

# Documentación
git commit -m "docs: actualiza instrucciones en README"

# Datos
git commit -m "data: agrega 10 productos al dataset"
```

### Resolver Conflictos

Si al hacer `git pull origin main` ves conflictos:

1. Abre los archivos marcados con conflictos
2. Busca `<<<<<<< HEAD` y `>>>>>>> main`
3. Decide qué código quedarse
4. Elimina las marcas
5. Guarda y commitea:
   ```bash
   git add .
   git commit -m "fix: resuelve conflictos de merge"
   ```

---

## 🏗️ Cómo Crear tu App de División

### Estructura Requerida

Tu app debe tener esta estructura EXACTA:

```
tu_app/                              # Nombre en minúsculas
├── migrations/
│   ├── __init__.py                   # Vacío o con "# Migrations"
│   └── 0001_initial.py              # Se crea automáticamente
├── templates/
│   └── tu_app/                       # Carpeta con nombre de tu app
│       └── home.html                # Template principal
├── static/
│   └── tu_app/                       # CSS y JS de tu app
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── fixtures/                         # Dataset JSON
│   └── datos.json
├── __init__.py                     # Vacío o con comentario
├── admin.py                         # Opcional
├── apps.py                          # Configuración de app
├── models.py                        # Tu modelo de datos
├── urls.py                          # URLs de tu app
├── views.py                         # Lógica de vistas
└── tests.py                         # Opcional
```

### Archivo urls.py (MUY IMPORTANTE)

Sin esto, tu tarjeta aparece en "Próximamente":

```python
from django.urls import path
from . import views

# ESTA LÍNEA ES OBLIGATORIA
app_name = 'tu_app'

urlpatterns = [
    path('', views.home, name='home'),
]
```

### Archivo views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # Esto protege con login
def home(request):
    return render(request, 'tu_app/home.html')
```

### Integrar al Portal

1. **Editar `settings.py`:**
   ```python
   INSTALLED_APPS = [
       # ... otras apps ...
       'tu_app',
   ]
   ```

2. **Editar `urls.py` principal:**
   ```python
   path('tu-url/', include('tu_app.urls')),
   ```

3. **Crear migraciones:**
   ```bash
   python manage.py makemigrations tu_app
   python manage.py migrate
   ```

---

## 📚 Guías Individuales

Cada persona tiene una guía detallada en `/docs/`:

| Persona | Archivo | Estado |
|---------|---------|--------|
| **Camilo** | [guia_camilo.md](docs/guia_camilo.md) | App Foundation completa |
| **Cuervo** | [guia_cuervo.md](docs/guia_cuervo.md) | Crear app desde cero |
| **Dana** | [guia_dana.md](docs/guia_dana.md) | Dataset Ciberseguridad |
| **Diego Granja** | [guia_diego_granja.md](docs/guia_diego_granja.md) | Crear app desde cero |
| **Drada** | [guia_drada.md](docs/guia_drada.md) | Dataset Clean Energy |
| **Emerick** | [guia_emerick.md](docs/guia_emerick.md) | Dataset Donaciones |
| **Juan José** | [guia_juan_jose.md](docs/guia_juan_jose.md) | Crear app desde cero |
| **Juliana** | [guia_juliana.md](docs/guia_juliana.md) | App Ventures completa |
| **Nicolás** | [guia_nicolas.md](docs/guia_nicolas.md) | Dataset Contratos Defensa |
| **Pérez** | [guia_perez.md](docs/guia_perez.md) | Dataset RRHH |
| **Perlaza** | [guia_perlaza.md](docs/guia_perlaza.md) | App Real Estate completa |
| **Valeria** | [guia_valeria.md](docs/guia_valeria.md) | Crear app desde cero |
| **Dataset 13** | [guia_dataset_13.md](docs/guia_dataset_13.md) | Adquisiciones Startups |
| **Dataset 14** | [guia_dataset_14.md](docs/guia_dataset_14.md) | Wayne Shipping |
| **Dataset 15** | [guia_dataset_15.md](docs/guia_dataset_15.md) | Brother Eye AI |

**¿No tienes tu guía?** Crea el archivo `docs/guia_tu_nombre.md` basándote en los ejemplos existentes.

---

## 🌐 URLs del Sistema

### Autenticación (No requieren login)
- `/accounts/login/` — Iniciar sesión
- `/accounts/registro/` — Crear cuenta
- `/` — Portal principal

### Protegidas (Requieren login)
- `/accounts/dashboard/` — Panel de control
- `/accounts/logout/` — Cerrar sesión
- `/admin/` — Panel Django Admin (superusuarios)

### Divisiones (Requieren login)
| URL | División |
|-----|----------|
| `/tech/` | Wayne Technologies |
| `/industries/` | Wayne Industries |
| `/healthcare/` | Wayne Healthcare |
| `/realestate/` | Wayne Real Estate |
| `/capital/` | Wayne Capital |
| `/foundation/` | Wayne Foundation |
| `/ventures/` | Wayne Ventures |

---

## ❌ Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| "No module named 'django'" | Entorno no activado | `venv\Scripts\activate` |
| "Access denied for user 'root'" | MySQL no iniciado en XAMPP | Abrir XAMPP → clic en Start en MySQL |
| "Table doesn't exist" | Migraciones no aplicadas | `python manage.py migrate` |
| "Tarjeta en Próximamente" | Falta `app_name` en `urls.py` | Agregar `app_name = 'tu_app'` |
| "No module named 'tu_app'" | No está en `INSTALLED_APPS` | Agregar `'tu_app'` en `settings.py` |
| "Cannot use ImageField" | Pillow no instalado | `python -m pip install Pillow` |
| "tarjeta no se activa" | URL no incluida | Agregar `path('url/', include('tu_app.urls'))` |
| "datos no se cargan" | JSON mal formado | Validar JSON en jsonlint.com |

---

## 🚫 Reglas del Equipo (Obligatorias)

1. ✅ **Trabajar en tu rama**, nunca en `main`
2. ✅ **Hacer `git pull origin main`** antes de empezar cada día
3. ✅ **Crear tu dataset** con al menos 5 registros
4. ✅ **Probar tu app** antes de hacer commit (¿funciona en navegador?)
5. ✅ **Usar mensajes claros** en commits
6. ❌ **NO modificar** `core/`, `accounts/` sin coordinar con Nicolás
7. ❌ **NO subir** carpetas: `venv/`, `__pycache__/`, archivos de base de datos
8. ❌ **NO usar** `git add .` sin revisar primero `git status`

---

## 🔄 Hacer Pull Request (Entrega)

Cuando tu app esté lista (modelo + template + dataset):

1. **Sube tu rama:**
   ```bash
   git push origin tu_rama
   ```

2. **Ve a GitHub** en navegador: `github.com/nicohr3366/Wayne-Enterprises`

3. **Clic en "Compare & pull request"** (aparece automáticamente)

4. **Título del PR:**
   ```
   feat: agrega app [nombre] con dataset de X registros
   ```

5. **Descripción del PR:**
   ```markdown
   ## Qué incluye esta PR
   
   - ✅ Modelo [Nombre] creado
   - ✅ Template `home.html` con estilos
   - ✅ Dataset con X registros en `fixtures/datos.json`
   - ✅ URLs configuradas
   - ✅ App integrada al portal
   
   ## Cómo probar
   1. `python manage.py migrate`
   2. `python manage.py loaddata tu_app/fixtures/datos.json`
   3. Abrir `/tu-url/` en navegador
   
   ## Screenshots
   [Adjuntar capturas de pantalla]
   ```

6. **Clic en "Create pull request"**

7. **Avisar a Nicolás** por WhatsApp/Teams

8. Nicolás revisa y fusiona a `main`

---

## 📞 Contacto y Ayuda

### Problemas Técnicos
- **Nicolás** - Git, Django, configuración, conflictos

### Ayuda con tu App
- **Camilo** - Foundation (app completa, ejemplo de estructura)
- **Juliana** - Ventures (sistema de navegación)
- **Perlaza** - Real Estate (modelos y templates)

### Dudas de Dataset
- Ver ejemplos en las guías individuales de `/docs/`
- Usar apps existentes como referencia: `foundation/`, `realestate/`, `ventures/`

---

## 🛠️ Comandos de Referencia

```bash
# Servidor Django
python manage.py runserver

# Base de datos
python manage.py makemigrations        # Crear migraciones
python manage.py makemigrations app    # Crear migraciones de app específica
python manage.py migrate                # Aplicar migraciones

# Datos
python manage.py loaddata app/fixtures/datos.json

# Superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Ver URLs
python manage.py show_urls

# Git - Ver estado
git status                    # Ver cambios
git log --oneline -10          # Ver últimos 10 commits
git branch                    # Ver rama actual
```

---

## 📖 Recursos de Aprendizaje

### Para Principiantes
- [Tutorial Django Oficial](https://docs.djangoproject.com/es/4.2/intro/tutorial01/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Markdown Guía](https://www.markdownguide.org/basic-syntax/)
- [JSON Validator](https://jsonlint.com/) - Para validar tu dataset

### Documentación de Apps Completas
- Ver código de `foundation/` - App completa de Camilo
- Ver código de `realestate/` - App completa de Perlaza
- Ver código de `ventures/` - App completa de Juliana

---

## 📝 Notas para la Próxima Clase

### Antes de la clase cada persona debe tener:
- [ ] Rama personal creada en GitHub
- [ ] App creada con estructura básica (carpetas)
- [ ] Modelo definido en `models.py`
- [ ] Dataset JSON con 5+ registros
- [ ] Template básico `home.html`

### En clase se trabajará:
- [ ] Integración de apps al portal
- [ ] Revisión de datasets
- [ ] Pruebas en conjunto
- [ ] Preparación de presentación final

---

*Wayne Enterprises — Proyecto de Arquitectura de Computadores*  
*2026*  
*Equipo: Cuervo, Diego Granja, Juan José, Perlaza, Valeria, Camilo, Juliana, Nicolás*