<<<<<<< HEAD
# Wayne Industries - Sistema en Java

## Descripción
Sistema de gestión empresarial desarrollado en Java usando Programación Orientada a Objetos.

## Funcionalidades
- Crear departamentos
- Agregar empleados
- Listar departamentos
- Ver empleados por departamento
- Eliminar empleados
- Mostrar toda la empresa

## Cómo ejecutar

1. Compilar:
javac *.java

2. Ejecutar:
java Main

## Autor
Proyecto académico - Wayne Industries
=======
# Wayne Enterprises — Portal Corporativo

## LEE ESTO ANTES DE HACER CUALQUIER COSA

El proyecto cambió de nombre. Si ya tenías el proyecto clonado antes,
**no sigas trabajando en esa carpeta**, porque apunta a un repositorio
viejo que ya no se usa. Sigue la guía desde el principio con el nuevo enlace.

**Nombre nuevo del repositorio:** `Wayne-Enterprises`  
**Enlace nuevo:**
```
https://github.com/nicohr3366/Wayne-Enterprises
```

---

## ¿De qué va este proyecto?

Estamos construyendo un portal corporativo para Wayne Enterprises. Cada uno del grupo desarrolla su propia
app de Django para una división de la empresa, y todas se conectan
al portal central que está en este repositorio.

La página principal muestra las 7 divisiones. Cuando alguien conecta
su app, la tarjeta de esa división se activa automáticamente.

---

## Divisiones del proyecto

| # | División | Carpeta de la app | Responsable |
|---|----------|-------------------|-------------|
| 1 | Wayne Technologies | `tech` | — |
| 2 | Wayne Industries | `industries` | — |
| 3 | Wayne Healthcare | `healthcare` | — |
| 4 | Wayne Real Estate | `realestate` | — |
| 5 | Wayne Capital | `capital` | — |
| 6 | Wayne Foundation | `foundation` | — |
| 7 | Wayne Ventures | `ventures` | — |

---

## Conceptos de Git que necesitas entender

Antes de empezar a trabajar es importante entender cómo funciona
Git y GitHub porque lo vamos a usar todo el tiempo.

### ¿Qué es Git?

Git es un programa que guarda el historial de cambios de tu proyecto.
Imagínalo como un "control Z" infinito que además te permite trabajar
en equipo sin pisarte con los demás.

### ¿Qué es GitHub?

GitHub es una página web donde subimos ese historial para que todos
lo puedan ver y descargar. Es como Google Drive pero para código.

### ¿Qué es un repositorio (repo)?

Es la carpeta del proyecto guardada en GitHub con todo su historial.
Cuando "clonas" un repo, te descargas esa carpeta completa a tu PC.

### ¿Qué es una rama (branch)?

Imagina que el proyecto es un árbol. La rama principal se llama `main`
y tiene el código oficial que funciona. Cada compañero crea su propia
rama para trabajar sin afectar el `main`.

```
main  ←── código oficial del portal (NO tocar directamente)
 │
 ├── WayneVentures_JulianaHoyos  ←── rama de Juliana
 ├── Juan_Jose_Arango             ←── rama de Juan José
 ├── Valeria                      ←── rama de Valeria
 └── tu_rama                      ←── la tuya
```

Cuando tu trabajo esté listo, haces un **Pull Request** para pedir
que tus cambios se mezclen al `main`. Nicolás revisa y acepta.

### ¿Qué es un commit?

Es como una foto del estado actual de tu código. Cada vez que avanzas
algo importante, haces un commit con un mensaje que describe qué cambiaste.

### ¿Qué es push y pull?

- **push** → subir tus commits de tu PC a GitHub
- **pull** → bajar los cambios de GitHub a tu PC

---

## SITUACIÓN A — Ya tenía el proyecto clonado (proyecto viejo)

Si ya tenías el repo clonado antes con el nombre anterior, sigue
estos pasos para actualizarte al nuevo sin perder tu trabajo.

**Paso 1 — Abre la terminal dentro de la carpeta del proyecto viejo**

En VS Code: `Terminal → New Terminal`

**Paso 2 — Cambia la URL del repositorio al nuevo**

```bash
git remote set-url origin https://github.com/nicohr3366/Wayne-Enterprises.git
```

Esto le dice a Git que de ahora en adelante suba y baje del nuevo repo.

**Paso 3 — Baja los últimos cambios del main**

```bash
git fetch origin
git checkout main
git pull origin main
```

**Paso 4 — Ve a tu rama**

```bash
git checkout nombre-de-tu-rama
```

Por ejemplo si tu rama se llama `Valeria`:
```bash
git checkout Valeria
```

**Paso 5 — Actualiza tu rama con los cambios del main**

```bash
git merge main
```

Si aparece un mensaje de conflictos, avísale a Nicolás antes de
seguir para resolverlo juntos.

**Paso 6 — Sube tu rama actualizada**

```bash
git push origin nombre-de-tu-rama
```

---

## SITUACIÓN B — Nunca he clonado el proyecto (empezando desde cero)

### Paso 1 — Instalar Git

Si no tienes Git instalado, descárgalo de:
```
https://git-scm.com/downloads
```
Instálalo con todas las opciones que trae por defecto.

### Paso 2 — Configurar Git con tu nombre (solo la primera vez)

Abre la terminal y escribe esto con tus datos reales:
```bash
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu@email.com"
```

Esto hace que tus commits queden registrados con tu nombre.

### Paso 3 — Clonar el repositorio

Esto descarga el proyecto completo a tu PC:
```bash
git clone https://github.com/nicohr3366/Wayne-Enterprises.git
```

Se crea una carpeta llamada `Wayne-Enterprises`. Entra a ella:
```bash
cd Wayne-Enterprises
```

### Paso 4 — Crear el entorno virtual

El entorno virtual es una burbuja donde se instalan las librerías
del proyecto sin afectar el resto de tu computador. Es obligatorio
crearlo siempre al empezar un proyecto de Python.

```bash
python -m venv venv
```

### Paso 5 — Activar el entorno virtual

Cada vez que vayas a trabajar debes activarlo primero:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

Sabes que está activo cuando ves `(venv)` al inicio de la línea
en la terminal.

### Paso 6 — Instalar las dependencias (Recordar leer bien lo que esta en el archivo.txt)

```bash
pip install -r requirements.txt
```

Esto instala Django y todo lo necesario para correr el proyecto.

### Paso 7 — Preparar la base de datos

```bash
python manage.py migrate
```

### Paso 8 — Crear tu propia rama

Nunca trabajes directamente en `main`. Crea tu rama con tu nombre
(sin espacios, usa guion bajo):

```bash
git checkout -b Nombre_Apellido
```

Por ejemplo:
```bash
git checkout -b Maria_Lopez
```

### Paso 9 — Verificar que todo funciona

```bash
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` — debe aparecer el portal Wayne Enterprises.

---

## Flujo de trabajo diario

Este es el orden que hay que seguir cada vez que te sientas a trabajar:

**1. Activar el entorno virtual (siempre primero)**
```bash
# Windows
venv\Scripts\activate
```

**2. Bajar cambios del main antes de empezar**

Esto asegura que trabajas con la versión más actualizada:
```bash
git pull origin main
```

**3. Trabajar en tu código...**

Haz los cambios, crea archivos, lo que necesites.

**4. Ver qué archivos cambiaste**
```bash
git status
```

Muestra en rojo los archivos modificados que aún no guardaste en Git.

**5. Agregar los cambios**
```bash
git add .
```

El punto significa "agregar todo lo que cambié".

**6. Hacer el commit con un mensaje claro**
```bash
git commit -m "descripcion de lo que hice"
```

Ejemplos de buenos mensajes:
```bash
git commit -m "feat: agrego modelo de productos"
git commit -m "fix: corrijo error en la vista principal"
git commit -m "style: ajusto colores del navbar"
```

**7. Subir tus cambios a GitHub**
```bash
git push origin nombre-de-tu-rama
```

---

## Cómo traer los cambios de un compañero a tu rama

Cuando yo acepte el Pull Request de alguien, esos cambios
quedan en `main`. Para traerlos a tu rama y estar actualizado:

```bash
git fetch origin
git merge origin/main
```

### ¿Qué pasa si hay un conflicto?

Un conflicto ocurre cuando tú y otro compañero modificaron el
mismo archivo en el mismo lugar y Git no sabe cuál versión dejar.

Git marca los archivos en conflicto así:
```
<<<<<<< HEAD
tu versión del código
=======
la versión del main
>>>>>>> origin/main
```

Tienes que borrar esas marcas y dejar la versión correcta.  
**Si no entiendes cómo resolverlo, avisame al privado antes de seguir.**

Después de resolver:
```bash
git add .
git commit -m "fix: resuelvo conflicto con main"
git push origin nombre-de-tu-rama
```

---

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

---

## Cómo hacer un Pull Request

Cuando ya terminaste tu trabajo y lo subiste a tu rama en GitHub:

**Paso 1 — Entra al repo en GitHub**
```
https://github.com/nicohr3366/Wayne-Enterprises
```

**Paso 2 — Busca el botón "Compare & pull request"**

Aparece en amarillo/verde cuando GitHub detecta que subiste
cambios recientes a tu rama.

**Paso 3 — Escribe un título y descripción**

Ejemplo:
- Título: `feat: agrego app Wayne Ventures`
- Descripción: qué hiciste, qué modelos tiene, cómo se prueba

**Paso 4 — Clic en "Create pull request"**

Nicolás recibe la notificación, revisa y acepta o pide cambios.

**Paso 5 — Después de que acepten tu PR**

Actualiza tu rama local con lo nuevo del main:
```bash
git checkout main
git pull origin main
git checkout nombre-de-tu-rama
git merge main
```

---

## Errores comunes y sus soluciones

**"fatal: not a git repository"**  
→ No estás dentro de la carpeta del proyecto.
Usa `cd Wayne-Enterprises` primero.

**"error: failed to push some refs"**  
→ Alguien subió cambios antes. Haz primero:
```bash
git pull origin nombre-de-tu-rama
```
Y luego intenta el push de nuevo.

**"No module named 'django'"**  
→ Olvidaste activar el entorno virtual.
Actívalo con `venv\Scripts\activate`.

**"No module named 'tu_app'"**  
→ No registraste la app en `INSTALLED_APPS` del `settings.py`.

**"TemplateDoesNotExist"**  
→ El template no está en `templates/tu_app/home.html`.
Revisa que la ruta sea exactamente así.

**"Table doesn't exist"**  
→ Olvidaste correr `python manage.py migrate`.

**La tarjeta del portal sigue en "Próximamente"**  
→ El nombre en `INSTALLED_APPS` no coincide con el `app_name`
en tu `apps.py`. Deben ser exactamente iguales.

---

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
>>>>>>> 9aa5b9054f289fbc2ceaf862767be2ae4b7354b0
