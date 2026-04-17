# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises con 7 divisiones de negocio. Cada compañero desarrolla una app que se integra automáticamente al portal central.

---

## 📊 Estado del Proyecto - Asignaciones

### Apps Django (Divisiones Corporativas)

| # | División | App | Responsable | Estado | Guía |
|---|----------|-----|-------------|--------|------|
| 1 | Wayne Technologies | `tech` | **Cuervo** | ✅ Activo |
| 2 | Wayne Industries | `industries` | **Diego Granja** | ✅ Activo |
| 3 | Wayne Healthcare | `healthcare` | **Juan José** | ✅ Activo |
| 4 | Wayne Real Estate | `realestate` | **Perlaza** | ✅ Activo |
| 5 | Wayne Capital | `capital` | **Valeria** | ✅ Activo |
| 6 | Wayne Foundation | `foundation` | **Camilo** | ✅ Activo |
| 7 | Wayne Ventures | `ventures` | **Juliana** | ✅ Activo |

### Sistemas ETL y Datasets

| ID | Responsable | Dataset | Tipo | Descripción | Guía |
|----|-------------|---------|------|-------------|------|
| 1 | **Cuervo** | Telemetría Tumbler | ETL | Datos de impacto, velocidad, consumo |
| 2 | **Nicolás** | Contratos Defensa | ETL/XML | Licitaciones gobierno EE.UU. |
| 3 | **Camilo** | Stock Market | ETL | Acciones WayneTech, series temporales |
| 4 | **Emerick** | Donaciones Fundación | ETL | Ayuda a orfanatos y hospitales |
| 5 | **Juan José** | Red Eléctrica Gotham | ETL | Datos de carga de Wayne Energy |
| 6 | **Juliana** | Satélites | ETL | Logs de comunicaciones WayneTech |
| 7 | **Valeria** | Desarrollo Urbano | ETL | Costos reconstrucción Gotham |
| 8 | **Dana** | Ciberseguridad | ML/ETL | Intentos de hackeo, clasificación ML |
| 9 | **Perlaza** | Aerospace | ETL | Inventario aviones y drones |
| 10 | **Diego Granja** | Patentes Nanotech | ETL | Propiedad intelectual Wayne |
| 11 | **Pérez** | RRHH Wayne Manor | RBAC | Personal y sistema de permisos |
| 12 | **Drada** | Clean Energy | ETL | Monitoreo reactor fusión |
| 13 | * | Adquisiciones Startups | ETL | Historial de compras |
| 14 | * | Wayne Shipping | ETL | Logística marítima |
| 15 | * | Brother Eye AI | ML/ETL | Sistema de vigilancia |

### Estructura de Carpetas del Proyecto

```
Wayne-Enterprises/
├── apps/                         # Apps Django del proyecto
│   ├── accounts/                  # Sistema de autenticación
│   ├── capital/                   # División 5: Capital
│   ├── core/                       # Portal principal y landing
│   ├── foundation/                 # División 6: Foundation
│   ├── healthcare/                 # División 3: Healthcare
│   ├── industries/                 # División 2: Industries
│   ├── realestate/                 # División 4: Real Estate
│   ├── tech/                       # División 1: Technologies
│   └── ventures/                   # División 7: Ventures
├── datasets/                      # Datasets y sistemas ETL
├── wayne_enterprise/              # Configuración principal Django
└── venv/                          # Entorno virtual (no subir a Git)
```

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