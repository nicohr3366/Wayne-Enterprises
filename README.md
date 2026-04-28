# Wayne Enterprises — Portal Corporativo

Portal modular Django para el conglomerado Wayne Enterprises con 7 divisiones de negocio. Cada compañero desarrolla una app que se integra automáticamente al portal central.

---

## 📊 Sistemas ETL y Datasets

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
Wayne-Enterprises-2/
├── apps/                          # Apps Django del proyecto
│   ├── accounts/                  # Autenticación y roles
│   ├── capital/                   # División 5: Wayne Capital
│   ├── core/                      # Portal principal y landing
│   ├── foundation/                # División 6: Wayne Foundation
│   ├── healthcare/                # División 3: Wayne Healthcare
│   ├── industries/                # División 2: Wayne Industries
│   ├── realestate/                # División 4: Wayne Real Estate
│   ├── tech/                      # División 1: Wayne Technologies
│   └── ventures/                  # División 7: Wayne Ventures
├── wayne_enterprise/              # Configuración principal Django
├── manage.py
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

## 🗄️ Configuración de Base de Datos (MariaDB 10.6+)

> **IMPORTANTE:** Django 4.2+ requiere **MariaDB 10.6 o superior**. XAMPP trae MariaDB 10.4 que **NO es compatible** y causará error al migrar. Sigue los pasos de abajo.

### 1. Instalar MariaDB 10.6

1. Descarga **MariaDB 10.6** desde: https://mariadb.org/download/?t=mariadb&p=mariadb&r=10.6
2. Selecciona **Windows** → **MSI Package (x86_64)**
3. Ejecuta el instalador
4. En la pantalla **"Modify password for root user"**:
   - **Desmarca** la casilla (sin contraseña, más simple)
   - O deja una contraseña que recuerdes y actualiza `settings.py`
5. En la pantalla **"Database settings"**:
   - Puerto: `3306`
   - Deja todo por defecto y haz clic en **Next**
   - Si dice "puerto en uso", apaga MySQL en XAMPP primero y vuelve a intentar

> Si ya tienes XAMPP corriendo con MySQL, **detén MySQL en XAMPP** antes de instalar MariaDB 10.6 para evitar conflicto de puertos.

### 2. Crear la Base de Datos

Abre **PowerShell** y ejecuta:

```powershell
& "C:\Program Files\MariaDB 10.6\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS wayne_enterprise CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Verificar Configuración

El archivo `settings.py` ya está configurado para conectarse a `localhost:3306` sin contraseña. Solo verifica que el servicio **MariaDB** esté corriendo (aparece en Servicios de Windows o arranca automáticamente al instalar).

### 4. Crear Tablas

```bash
# En la terminal de VS Code (estando en Wayne-Enterprises/)
python manage.py migrate
```

**Verifica**: Debes ver una lista de migraciones aplicadas sin errores.

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