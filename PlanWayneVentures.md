# Wayne Ventures — Plan de Desarrollo

> App Django de **Wayne Ventures** dentro del portal corporativo de Wayne Enterprises.
> Se integra como una división más del proyecto central. URL base: `/ventures/`

---

## Contexto del proyecto

### Posición dentro del portal

Wayne Ventures **no es un proyecto independiente**. Es una **app Django** que se integra al portal central de Wayne Enterprises (repositorio compartido del grupo). El portal central ya existe: tiene su propio `manage.py`, `settings.py`, `urls.py` y la app `core/` que muestra las 7 divisiones.

Tu trabajo es construir la app `ventures/` y conectarla al portal central siguiendo las instrucciones del README principal del repositorio.

> ⚠️ **Antes de integrar al proyecto central, hablar con Nicolás.**

### ¿Qué es Wayne Ventures?

Wayne Ventures es **una de las 7 divisiones** de Wayne Enterprises. Es el brazo de inversión estratégica y el radar global del grupo para detectar tecnologías disruptivas e integrarlas en el ecosistema corporativo del holding.

| Atributo | Detalle |
|---|---|
| **Nombre oficial** | Wayne Ventures |
| **Slogan** | *"Acelerando el futuro. Asegurando el mañana."* |
| **Sector** | Capital de Riesgo Corporativo (CVC) / Tecnología Profunda (Deep Tech) |
| **Mercado objetivo** | Startups tecnológicas (Seed a Serie B), gobiernos locales, sectores industriales del Grupo Wayne |
| **Presencia geográfica** | Global — nodos en Gotham City, Silicon Valley, Tel Aviv y Singapur |
| **Sede** | Wayne Tower, Nivel 90, Gotham City |
| **Contacto** | ventures@wayneenterprises.com |
| **URL en el portal** | `/ventures/` |

**Misión:**
> *"Impulsar el crecimiento sostenible de Wayne Enterprises mediante la inversión en talento externo y tecnología de vanguardia, facilitando la transición definitiva hacia una infraestructura basada en la nube."*

**Visión:**
> *"Ser el socio de inversión más influyente del mundo, validando las tecnologías que definirán el próximo siglo."*

---

## Stack tecnológico

Seguir el stack definido en el README principal del repositorio. No instalar versiones distintas.

| Capa | Tecnología |
|---|---|
| Backend | Django **6.0.3** / Python **3.13** |
| Frontend | HTML5 · CSS3 · JavaScript (Vanilla) |
| Base de datos | SQLite (local, **no subir `db.sqlite3` al repo**) |
| Fuentes | Google Fonts — `Cinzel` + `Rajdhani` ya disponibles en el portal base |

---

## Estructura de la app

La app de Wayne Ventures vive en la **carpeta `ventures/`** dentro de la raíz del proyecto central, al lado de `core/`. No tiene su propio `manage.py` ni `settings.py`: usa los del proyecto central.

```
Wayne-Enterprises/               ← raíz del repositorio compartido
│
├── core/                        ← NO tocar
├── wayne_enterprise/            ← NO tocar sin coordinar
│
├── ventures/                    ← TU app — todo tu trabajo va aquí
│   ├── migrations/
│   │   └── __init__.py
│   ├── templatetags/            ← filtros y tags de Django para el menú dinámico
│   │   ├── __init__.py
│   │   └── ventures_tags.py
│   ├── templates/
│   │   └── ventures/            ← subcarpeta obligatoria con el nombre de la app
│   │       ├── base.html        ← layout base con navbar y footer dinámicos
│   │       ├── home.html        ← homepage (requerido por el portal)
│   │       ├── about.html
│   │       ├── innovation.html
│   │       ├── pipeline.html
│   │       ├── portfolio_list.html
│   │       ├── portfolio_detail.html
│   │       ├── portfolio_cases.html
│   │       ├── team.html
│   │       ├── metrics.html
│   │       └── contact.html
│   ├── static/
│   │   └── ventures/            ← subcarpeta obligatoria con el nombre de la app
│   │       ├── css/
│   │       │   ├── base.css     ← variables CSS extendidas del portal
│   │       │   └── components.css
│   │       ├── js/
│   │       │   ├── main.js
│   │       │   └── charts.js
│   │       └── img/
│   │           ├── logo/
│   │           └── portfolio/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

> Las apps de modelos más complejos (portfolio, team, metrics, contact) se implementan **dentro de la app `ventures/`** o como sub-apps prefijadas (`ventures_portfolio`, etc.) — coordinar con Nicolás cuál de los dos enfoques usar antes de crear modelos.

---

## Integración al portal central

Seguir exactamente los pasos del README principal. Recordatorio de lo que hay que coordinar:

**Paso 1 — Agregar en `settings.py`** (coordinar con Nicolás):
```python
INSTALLED_APPS = [
    ...
    'core',
    'ventures',    # ← tu app
]
```

**Paso 2 — Agregar en `wayne_enterprise/urls.py`** (coordinar con Nicolás):
```python
path('ventures/', include('ventures.urls')),
```

**Paso 3 — Tu `ventures/urls.py` mínimo requerido:**
```python
from django.urls import path
from . import views

app_name = 'ventures'

urlpatterns = [
    path('', views.home, name='home'),  # ← requerido por el portal central
    path('about/', views.about, name='about'),
    path('innovation/', views.innovation, name='innovation'),
    path('portfolio/', views.portfolio_list, name='portfolio_list'),
    path('portfolio/cases/', views.portfolio_cases, name='portfolio_cases'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('team/', views.team, name='team'),
    path('metrics/', views.metrics, name='metrics'),
    path('pipeline/', views.pipeline, name='pipeline'),
    path('contact/', views.contact, name='contact'),
]
```

**Paso 4 — Migraciones:**
```bash
python manage.py makemigrations ventures
python manage.py migrate
```

---

## Reglas del equipo (del README principal)

- ✅ Trabajar siempre en **rama propia**, nunca directamente en `main`
- ✅ Commits con mensajes descriptivos de qué se hizo
- ✅ Hacer `git pull origin main` antes de empezar cada día
- ✅ Avisar a Nicolás cuando el PR esté listo para revisión
- ❌ **No modificar archivos de `core/`** sin avisar
- ❌ **No tocar `settings.py` ni `urls.py`** sin coordinarlo con Nicolás
- ❌ **No subir `venv/`** ni **`db.sqlite3`** al repositorio

---

## Identidad visual

### Principio de herencia + diferenciación

La app `ventures/` **hereda la identidad visual del portal** (`portal.css`) y la extiende con su propio acento diferenciador. No se reemplaza el sistema de diseño del portal: se amplía.

- **Dorado (`--gold: #D4AA50`)**: color heredado del portal. Presente en el logo compartido, bordes del sistema, elementos que conectan visualmente con Wayne Enterprises.
- **Cian (`--ventures-cyan: #00FFFF`)**: acento exclusivo de Wayne Ventures. Representa energía digital e innovación. Se usa en los elementos propios de esta división: CTAs principales, badges de estado activo, highlights de sección, glow de tarjetas del portafolio.

> La convivencia dorado/cian es intencional: el dorado ancla la app al universo Wayne; el cian la distingue como la división más tecnológica y ágil del grupo.

### Variables CSS — `ventures/static/ventures/css/base.css`

Este archivo **importa y extiende** las variables del portal. No redefinir las variables base del portal, solo agregar las propias de Ventures.

```css
/* Importar fuentes del portal (ya cargadas globalmente) */
/* Cinzel + Rajdhani se heredan del portal */

:root {
  /* ── Herencia del portal — NO modificar estos valores ── */
  /* Se listan como referencia. El valor real viene de portal.css */
  /* --gold:           #D4AA50  */
  /* --gold-dim:       #b8922e  */
  /* --gold-bright:    #e8c46a  */
  /* --gold-glow:      rgba(212,170,80,0.25) */
  /* --bat-black:      #050507  */
  /* --surface:        #0d0d14  */
  /* --surface-2:      #13131e  */
  /* --surface-3:      #1c1c28  */
  /* --border:         rgba(212,170,80,0.40) */
  /* --border-hover:   rgba(212,170,80,0.80) */
  /* --text-primary:   #f2eada  */
  /* --text-secondary: #b0a690  */
  /* --text-muted:     #7a7060  */

  /* ── Exclusivo Wayne Ventures ── */
  --ventures-cyan:       #00FFFF;
  --ventures-cyan-dim:   #00CCCC;
  --ventures-cyan-glow:  rgba(0, 255, 255, 0.18);
  --ventures-cyan-faint: rgba(0, 255, 255, 0.07);

  /* Bordes ventures: mezcla dorado-herencia + cian-propio según contexto */
  --ventures-border:       rgba(0, 255, 255, 0.25);
  --ventures-border-hover: rgba(0, 255, 255, 0.70);
}
```

### Tipografía

Heredar las fuentes ya cargadas por el portal. **No importar fuentes adicionales** sin coordinar con Nicolás.

| Uso | Fuente | Origen |
|---|---|---|
| Títulos / Display | `Cinzel`, serif | Heredada del portal |
| UI / Body / Nav | `Rajdhani`, sans-serif | Heredada del portal |
| Monospace / KPIs / Datos | `JetBrains Mono` | Nueva — agregar solo en el `<head>` del `base.html` de ventures |

```html
<!-- ventures/templates/ventures/base.html -->
<!-- Solo agregar JetBrains Mono, las demás ya están en el portal -->
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

### Logotipo en la app

- Usar el logotipo SVG de Wayne Enterprises (mismo que el portal)
- Aplicar el efecto `logoPulse` heredado del portal pero con glow **cian** en lugar de dorado:

```css
/* ventures/static/ventures/css/base.css */
.ventures-logo {
  animation: venturesLogoPulse 4s ease-in-out infinite;
}

@keyframes venturesLogoPulse {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(0,255,255,0.4)); }
  50%       { filter: drop-shadow(0 0 18px rgba(0,255,255,0.8)); }
}
```

### Animaciones disponibles (heredadas del portal)

Reutilizar las animaciones definidas en `portal.css`. No redefinirlas, solo usarlas con las mismas clases o `animation-name`:

| Animación | Efecto | Uso en Ventures |
|---|---|---|
| `fadeUp` | Aparece desde abajo | Hero tagline, títulos de sección |
| `fadeIn` | Aparece en opacidad | Stats bar, grids de cards |
| `logoPulse` | Glow pulsante | Logo en navbar (reemplazar por `venturesLogoPulse` con cian) |
| `blink` | Parpadeo suave | Status dot del navbar |
| `spotPulse` | Luz de ambiente | Spotlight en el hero |

Agregar en `ventures/static/ventures/css/base.css` solo las animaciones nuevas que necesite esta app.

### Estética general

Heredar del portal: fondo `--bat-black` · textura noise SVG · silhouette de ciudad · spotlight dorado. Diferenciar con: glow cian en cards del portafolio · badges cian para startups activas · línea separadora cian en headers de sección · contadores KPI en `JetBrains Mono` con color `--ventures-cyan`.

---

## Menú de navegación dinámico (Django)

**Principio**: todos los menús de la app deben construirse desde Django. Ningún enlace de navegación puede estar hardcodeado en el HTML. Esto permite activar, desactivar o reordenar secciones desde Django Admin sin tocar templates.

### Modelo `NavItem`

```python
# ventures/models.py

class NavItem(models.Model):
    """
    Elemento del menú de navegación de Wayne Ventures.
    Administrable desde Django Admin sin modificar templates.
    """
    label = models.CharField(max_length=100, help_text="Texto visible en el menú")
    url_name = models.CharField(
        max_length=100,
        help_text="Nombre de URL con namespace. Ej: ventures:portfolio_list"
    )
    order = models.IntegerField(default=0, help_text="Orden de aparición (menor = primero)")
    is_active = models.BooleanField(default=True, help_text="Mostrar en el menú")
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        verbose_name = 'Nav Item'
        verbose_name_plural = 'Nav Items'

    def __str__(self):
        return f"{self.order}. {self.label}"

    def get_url(self):
        from django.urls import reverse
        try:
            return reverse(self.url_name)
        except Exception:
            return '#'
```

### Context processor para el menú

Para que el menú esté disponible en **todos los templates** de la app sin pasarlo manualmente en cada view, usar un context processor:

```python
# ventures/context_processors.py

from .models import NavItem

def ventures_nav(request):
    """
    Inyecta el menú de navegación activo en todos los templates de ventures.
    Registrar en settings.py > TEMPLATES > OPTIONS > context_processors.
    """
    return {
        'ventures_nav_items': NavItem.objects.filter(is_active=True)
    }
```

Registrar en `settings.py` (coordinar con Nicolás):
```python
TEMPLATES = [{
    ...
    'OPTIONS': {
        'context_processors': [
            ...
            'ventures.context_processors.ventures_nav',  # ← agregar
        ],
    },
}]
```

### Template del navbar (`ventures/templates/ventures/base.html`)

```html
<!-- Navbar dinámico — los links vienen de la base de datos vía context processor -->
<header>
  <div class="wrapper">
    <div class="logo-group">
      <img class="bat-logo ventures-logo" src="{% static 'ventures/img/logo/wayne-ventures-logo.svg' %}" alt="Wayne Ventures">
      <div class="logo-text">
        <h1>Wayne Ventures</h1>
        <span>A Wayne Enterprises Company</span>
      </div>
    </div>

    <nav class="ventures-nav" aria-label="Navegación principal">
      <ul class="nav-list">
        {% for item in ventures_nav_items %}
          <li class="nav-item">
            <a href="{{ item.get_url }}"
               class="nav-link {% if request.resolver_match.url_name == item.url_name.split(':')[-1] %}nav-link--active{% endif %}"
               {% if item.open_in_new_tab %}target="_blank" rel="noopener"{% endif %}>
              {{ item.label }}
            </a>
          </li>
        {% endfor %}
      </ul>

      <!-- Botón de regreso al portal central -->
      <a href="{% url 'core:home' %}" class="portal-back-link">
        ← Portal Wayne
      </a>

      <!-- Burger para mobile -->
      <button class="nav-burger" aria-label="Abrir menú" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>
</header>
```

### Datos iniciales del menú

Al crear el fixture `fixtures/initial_data.json`, incluir los NavItems con este orden y URL names:

| order | label | url_name |
|---|---|---|
| 1 | Portfolio | `ventures:portfolio_list` |
| 2 | Servicios | `ventures:innovation` |
| 3 | Pipeline | `ventures:pipeline` |
| 4 | Equipo | `ventures:team` |
| 5 | Métricas | `ventures:metrics` |
| 6 | Contacto | `ventures:contact` |

El link "Sobre Nosotros" puede ir en el footer en lugar del navbar principal para no saturarlo.

### Footer dinámico

El footer también obtiene sus links del mismo modelo `NavItem`. En el template del footer, filtrar por una categoría o simplemente reutilizar `ventures_nav_items`. Si se necesita una sección de footer diferente al navbar, agregar un campo `show_in_footer = models.BooleanField(default=False)` al modelo.

---

## Componentes CSS — Coherencia con `portal.css`

Todos los componentes de `ventures/` deben verse como extensiones naturales del portal, no como un sitio aparte. Usar las mismas clases base donde sea posible y solo agregar modificadores con prefijo `ventures-`.

### Cards del portafolio

Inspiradas en `.division-card` del portal. Misma estructura visual: borde dorado base, línea inferior animada al hover, número decorativo en fondo, glow de fondo en hover — pero la línea inferior y el glow de hover son **cian** en lugar de dorado.

```css
/* ventures/static/ventures/css/components.css */

.startup-card {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);           /* dorado heredado */
  padding: 28px 28px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: block;
}

.startup-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--ventures-cyan-faint) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.startup-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, var(--ventures-cyan), transparent);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.startup-card:hover {
  border-color: var(--ventures-border-hover);
  background: var(--surface-2);
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 0 20px var(--ventures-cyan-glow);
}

.startup-card:hover::before { opacity: 1; }
.startup-card:hover::after  { transform: scaleX(1); }
```

### Badges de estado

Coherentes con `.badge-live` / `.badge-soon` del portal. Agregar variantes para las etapas de inversión:

```css
.badge-seed {
  background: rgba(0,255,255,0.12);
  border: 1px solid rgba(0,255,255,0.40);
  color: var(--ventures-cyan);
}

.badge-active {
  background: rgba(58,170,98,0.18);
  border: 1px solid rgba(58,170,98,0.45);
  color: #4dcc7a;  /* mismo verde que badge-live del portal */
}

.badge-exited {
  background: rgba(180,60,60,0.15);
  border: 1px solid rgba(180,60,60,0.35);
  color: #d47070;  /* mismo rojo que badge-soon del portal */
}
```

### Stats bar de KPIs

Mismo patrón que `.stats-bar` / `.stat-item` del portal:

```css
.ventures-stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid var(--border);
  background: var(--surface);
  margin: 48px 0;
}

.ventures-stat-item {
  padding: 26px 28px;
  border-right: 1px solid var(--border);
}

.ventures-stat-item:last-child { border-right: none; }

/* Valor en cian (diferenciador de Ventures) vs dorado del portal */
.ventures-stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 30px;
  font-weight: 600;
  color: var(--ventures-cyan);
  letter-spacing: 0.05em;
  line-height: 1;
  margin-bottom: 8px;
  text-shadow: 0 0 20px var(--ventures-cyan-glow);
}

.ventures-stat-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.3em;
  color: var(--text-secondary);
  text-transform: uppercase;
  font-family: 'Rajdhani', sans-serif;
}
```

### Separadores de sección

En el portal se usa `.gold-line` (gradiente dorado). En Ventures usar la misma clase pero con una variante cian:

```css
.ventures-section-line {
  width: 100px;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--ventures-cyan), transparent);
  margin: 28px auto;
}
```

### Botones CTA

```css
/* Primario: fondo cian, texto negro */
.btn-ventures-primary {
  background: var(--ventures-cyan);
  color: #050507;  /* --bat-black */
  font-family: 'Rajdhani', sans-serif;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 12px 28px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 13px;
}

.btn-ventures-primary:hover {
  background: var(--ventures-cyan-dim);
  box-shadow: 0 0 20px var(--ventures-cyan-glow);
}

/* Secundario: outline cian */
.btn-ventures-secondary {
  background: transparent;
  color: var(--ventures-cyan);
  border: 1px solid var(--ventures-border);
  font-family: 'Rajdhani', sans-serif;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  padding: 11px 28px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 13px;
}

.btn-ventures-secondary:hover {
  border-color: var(--ventures-cyan);
  background: var(--ventures-cyan-faint);
  box-shadow: 0 0 16px var(--ventures-cyan-glow);
}
```

---

## Secciones del sitio

### 1. Homepage (`/ventures/`)

Vista requerida por el portal central: `views.home`. Es la primera página que activa la tarjeta de Wayne Ventures en el portal.

- Tagline principal (fuente `Cinzel`, `clamp(34px, 5vw, 60px)`): *"Acelerando el futuro."* con `<em>` en cian: *"Asegurando el mañana."*
- Subtítulo (fuente `Rajdhani`): Wayne Ventures como brazo de inversión estratégica
- CTA doble: `btn-ventures-primary` → **"Explorar Portafolio"** + `btn-ventures-secondary` → **"Presentar mi Proyecto"**
- Badge: *"A Wayne Enterprises Company"* — misma fuente y estilo que `.hero-eyebrow` del portal
- Fondo: heredar `body::before` (noise texture) + `.city-bg` + `.spotlight` del portal
- `ventures-stats-bar` con las 4 cifras canónicas animadas con `fadeIn`

---

### 2. Sobre Wayne Ventures (`/ventures/about/`)

- Narrativa fundacional con layout de dos columnas
- Mapa visual de las 7 divisiones con Wayne Ventures destacada (tarjeta con borde cian, las demás con borde dorado heredado)
- Misión y Visión con `section-line` cian como separador
- Presencia geográfica: 4 nodos (Gotham City · Silicon Valley · Tel Aviv · Singapur)
- Sinergias con Wayne Shipping y Wayne Technologies
- RSE: relación con Wayne Foundation, Tech for Good, descarbonización

---

### 3. Servicios / Tesis de Inversión (`/ventures/innovation/`)

- Los 4 productos en cards con estilo `startup-card` adaptado
- Propuesta de valor en 3 puntos con iconos SVG en cian
- Tecnologías de foco con badges `badge-seed`
- *Project Oracle Cloud* como tarjeta destacada con `featured` flag

---

### 4. Portafolio (`/ventures/portfolio/` y `/ventures/portfolio/<slug>/`)

**Modelos Django:**

```python
# ventures/models.py

class Sector(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Startup(models.Model):
    STAGE_CHOICES = [
        ('seed', 'Seed'),
        ('serie_a', 'Serie A'),
        ('serie_b', 'Serie B'),
        ('growth', 'Growth'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('exited', 'Exited'),
        ('acquired', 'Acquired'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=300)
    description = models.TextField()
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    investment_year = models.IntegerField()
    logo = models.ImageField(upload_to='portfolio/logos/')
    website_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-investment_year']

    def __str__(self):
        return self.name
```

Cards con clase `startup-card`. Badge de estado: `badge-active`, `badge-exited`, `badge-acquired`. Total de startups de muestra coherente con el KPI oficial: **45+**.

---

### 5. Casos de Éxito (`/ventures/portfolio/cases/`)

- 3–5 casos con estructura: Contexto → Desafío → Solución → Resultado
- Sinergias mencionadas: Wayne Shipping (IoT/tracking) y Wayne Technologies (cloud/serverless)
- Referencia al KPI de 12 proyectos escalados este semestre
- Cards con línea inferior cian y quote en `Cinzel` itálica

---

### 6. Equipo Directivo (`/ventures/team/`)

**Director de División:** Lucius Fox Jr. — VP de Estrategia Tecnológica

**Roles clave:**
- VP de Scouting Global
- Head of Cloud Engineering (líder del Cloud Sandbox Program)
- Portfolio Success Manager

```python
# ventures/models.py

class ExecutiveLevel(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    level = models.ForeignKey(ExecutiveLevel, on_delete=models.SET_NULL, null=True)
    linkedin_url = models.URLField(blank=True)
    reports_to_group = models.BooleanField(
        default=False,
        help_text="True si reporta directamente al C-Level de Wayne Enterprises"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['level__order', 'order']

    def __str__(self):
        return f"{self.name} — {self.role}"
```

Cards de equipo con estilo `.division-card` heredado del portal, con foto circular enmarcada en cian para el Director.

---

### 7. KPIs & Métricas (`/ventures/metrics/`)

**Cifras canónicas — no modificar:**

| KPI | Valor |
|---|---|
| Capital invertido | **+$250M USD** |
| Startups activas | **45+** |
| Proyectos escalados este semestre | **12** |
| Presencia geográfica | **8 países** |

```python
# ventures/models.py

class KPI(models.Model):
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"
```

Mostrar en `ventures-stats-bar`. Valores en `JetBrains Mono` con color `--ventures-cyan`. Animar con `IntersectionObserver` + JS: los contadores se activan al entrar en el viewport, usando `fadeIn` heredado del portal.

---

### 8. Pipeline de Proyectos (`/ventures/pipeline/`)

Visualización kanban con etapas: Exploración → Due Diligence → Incubación → Escalado → Portfolio. Cada columna con cabecera en `Cinzel`, borde cian en la columna activa. Referencia a *Project Oracle Cloud* como proyecto estrella con `badge-seed`. Estática en Fase 1, dinámica con modelo `PipelineProject` en fases posteriores.

---

### 9. Contacto Institucional (`/ventures/contact/`)

**CTA en `Cinzel`:** *"¿Tienes una idea que pueda cambiar el mundo?"* → botón `btn-ventures-primary`: **"Presentar mi Proyecto"**

- Email: `ventures@wayneenterprises.com`
- Dirección: Wayne Tower, Nivel 90, Gotham City

```python
# ventures/models.py

class ContactInquiry(models.Model):
    INQUIRY_TYPE = [
        ('startup', 'Startup — Busco inversión/incubación'),
        ('investor', 'Inversor — Quiero co-invertir'),
        ('alliance', 'Alianza estratégica'),
        ('other', 'Otro'),
    ]
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Consulta de contacto'
        verbose_name_plural = 'Consultas de contacto'
```

---

## Navbar y Footer — Detalles de implementación dinámica

### Navbar

El navbar se construye completamente desde el modelo `NavItem`. Comportamiento:

- **Sticky**: `position: sticky; top: 0; z-index: 100` con `backdrop-filter: blur` al hacer scroll
- **Active state**: comparar `request.resolver_match.url_name` con el `url_name` del item para resaltar la sección activa con color `--ventures-cyan`
- **Mobile burger**: toggle de clase `nav-open` en el `<nav>` vía JavaScript. El menú mobile se despliega con animación `fadeIn`
- **Link al portal**: siempre visible, con estilo `.portal-back-link` (color `--text-muted`, hover `--gold`)

### Footer

El footer también es dinámico. Además de los links de navegación del modelo `NavItem` (filtrados por `show_in_footer=True` si se añade ese campo), incluye:

- Slogan oficial en `Cinzel`: *"Acelerando el futuro. Asegurando el mañana."*
- Email y dirección como texto estático (estos datos son fijos de marca, no requieren modelo)
- Línea separadora con `.gold-line` heredada del portal
- Copyright con `--text-muted` y `font-family: Rajdhani`

---

## Fases de implementación

### Fase 1 — Fundamentos y Homepage
- Crear la carpeta `ventures/` con la estructura mínima
- Crear modelo `NavItem` y su context processor
- Poblar `NavItem` con los 6 items del menú via fixture o creación manual
- Implementar `base.html` con navbar dinámico y footer
- Importar variables de `portal.css` y definir las variables `--ventures-*` en `base.css`
- Hero: tagline en `Cinzel`, slogan oficial, CTA doble, stats bar cian, fondo heredado del portal
- Página `about.html` con misión, visión y mapa de divisiones
- **Coordinar con Nicolás** la integración en `settings.py` y `urls.py`

**Entregable**: App integrada al portal con navbar dinámico funcional y homepage estilizada.

---

### Fase 2 — Portfolio, Servicios y Tesis de Inversión
- Modelos `Sector` y `Startup` + migraciones + Django Admin
- 10–15 startups ficticias de muestra (coherentes con el total de 45+)
- Listado con filtros + detalle por startup con `startup-card`
- Página `innovation.html` con los 4 productos oficiales
- Casos de éxito con sinergias Wayne Shipping / Wayne Technologies

**Entregable**: Portafolio dinámico administrable + servicios completos.

---

### Fase 3 — Equipo y KPIs
- Modelos `ExecutiveLevel` y `TeamMember` + poblar con Lucius Fox Jr. y roles clave
- Modelo `KPI` + poblar con las 4 cifras canónicas
- Dashboard con `ventures-stats-bar` y contadores animados JS
- Registrar todos los modelos en Django Admin con `list_display` útil

**Entregable**: Equipo y métricas funcionales con datos correctos.

---

### Fase 4 — Pipeline y Contacto
- Página Pipeline (kanban) con referencia a *Project Oracle Cloud*
- Modelo `ContactInquiry` + formulario + vista POST con CSRF + Django Admin
- CTA "Presentar mi Proyecto" operativo
- Email y dirección visibles en footer y página de contacto

**Entregable**: Flujo de contacto funcional con datos oficiales.

---

### Fase 5 — Pulido y coherencia de marca
- Auditoría responsive (mobile, tablet, desktop) — coherente con las media queries de `portal.css`
- Consistencia visual: dorado heredado + cian ventures, sin excepciones ni colores ajenos
- Verificar que las animaciones `fadeUp` / `fadeIn` del portal funcionen en los templates de ventures
- Meta tags SEO y Open Graph
- Accesibilidad: contraste cian (`#00FFFF`) sobre negro (`#050507`) es AAA — verificar con herramienta
- Verificar link "← Portal Wayne" en navbar funcional en todas las páginas

**Entregable**: App production-ready, coherente con el portal corporativo.

---

## URLs del sitio

Todas las URLs de esta app arrancan desde `/ventures/` (URL reservada en el README del portal).

| URL | Vista | Descripción |
|---|---|---|
| `/ventures/` | `ventures.views.home` | Homepage / Hero — requerido por el portal |
| `/ventures/about/` | `ventures.views.about` | Sobre Wayne Ventures + RSE |
| `/ventures/innovation/` | `ventures.views.innovation` | Tesis de inversión y servicios |
| `/ventures/portfolio/` | `ventures.views.portfolio_list` | Listado del portafolio |
| `/ventures/portfolio/cases/` | `ventures.views.portfolio_cases` | Casos de éxito |
| `/ventures/portfolio/<slug>/` | `ventures.views.portfolio_detail` | Detalle de startup |
| `/ventures/team/` | `ventures.views.team` | Equipo directivo |
| `/ventures/metrics/` | `ventures.views.metrics` | Dashboard de KPIs |
| `/ventures/pipeline/` | `ventures.views.pipeline` | Pipeline de proyectos |
| `/ventures/contact/` | `ventures.views.contact` | Contacto institucional |

---

## Reglas canónicas de contenido y desarrollo

| # | Regla |
|---|---|
| 1 | **Paleta**: dorado `--gold #D4AA50` heredado del portal + cian `--ventures-cyan #00FFFF` exclusivo de Ventures. Sin otros colores. |
| 2 | **Tipografía**: `Cinzel` en títulos y `Rajdhani` en UI, heredadas del portal. `JetBrains Mono` solo para datos/KPIs. |
| 3 | **Variables CSS**: no redefinir variables del portal. Solo añadir las `--ventures-*` en `base.css`. |
| 4 | **Animaciones**: reutilizar `fadeUp`, `fadeIn`, `blink` del portal. Añadir solo `venturesLogoPulse`. No duplicar keyframes. |
| 5 | **Menú dinámico**: todos los links de navbar y footer vienen del modelo `NavItem`. Ningún link hardcodeado en HTML. |
| 6 | **Slogan**: *"Acelerando el futuro. Asegurando el mañana."* — no modificar. |
| 7 | **Cifras**: +$250M USD · 45+ startups · 12 proyectos escalados · 8 países. No inventar variantes. |
| 8 | **Director**: **Lucius Fox Jr.**, VP de Estrategia Tecnológica. No cambiar. |
| 9 | **Contacto**: `ventures@wayneenterprises.com` · Wayne Tower, Nivel 90, Gotham City. |
| 10 | **Productos**: exactamente los 4 definidos. No añadir ni renombrar sin actualizar este plan. |
| 11 | **Admin como CMS**: todo contenido dinámico (NavItems, startups, KPIs, equipo) administrable desde `/admin/`. |
| 12 | **Django version**: 6.0.3 / Python 3.13. No usar versiones distintas a las del portal. |
| 13 | **Rama Git**: trabajar siempre en rama propia. Nunca hacer commits directamente en `main`. |

---

## Contexto corporativo — Las 7 divisiones de Wayne Enterprises

Esta narrativa debe estar presente en la sección About y en el footer de la app.

| División | Enfoque | Sinergia con Ventures |
|---|---|---|
| **Wayne Ventures** ← *esta app* | Inversión CVC · Incubación · IA · ML · IoT · Cloud | — |
| Wayne Technologies | I+D tecnológico avanzado | Herramientas serverless para migración cloud |
| Wayne Shipping | Logística y flota global | Startups IoT para tracking en tiempo real |
| Wayne Biotech | Biotecnología y ciencias de la vida | Pipeline HealthTech |
| Wayne Manufacturing | Industria avanzada | Descarbonización por IA |
| Wayne Financial | Servicios financieros | — |
| Wayne Foundation | RSE y filantropía | Pilotos HealthTech en clínicas de Gotham City |

Wayne Ventures no opera de forma aislada: es el **motor de innovación y laboratorio de experimentación ágil** de todo el ecosistema. Sus inversiones impactan directamente a las otras 6 divisiones.

---

*Plan de desarrollo de la app `ventures/`. Fuente de verdad de contenido: este documento. Para reglas de integración al portal: seguir el README principal del repositorio.*
