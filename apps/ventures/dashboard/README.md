# 📡 Wayne Ventures Satellite Dashboard

Dashboard de monitoreo de satélites con dos visualizaciones:
1. **Django Dashboard** (Chart.js) - Puerto 8000
2. **Streamlit Dashboard** (Plotly) - Puerto 8501

## 🚀 Cómo Ejecutar

### Opción 1: Ejecutar ambas terminales (RECOMENDADO)

**Terminal 1 - Django:**
```bash
cd "c:\Users\juhor\Desktop\Programacion\Electiva de Programacion\Corte 2\waynetech-landing"
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```
Acceso: http://127.0.0.1:8000/ventures/satellites/

**Terminal 2 - Streamlit:**
```bash
cd "c:\Users\juhor\Desktop\Programacion\Electiva de Programacion\Corte 2\waynetech-landing"
.\.venv\Scripts\Activate.ps1
streamlit run apps/ventures/dashboard/satellite_dashboard.py
```
Acceso: http://127.0.0.1:8501

---

## 📊 Características del Dashboard Streamlit

### 5 Gráficas Principales:

1. **Donut - Severidad**: Distribución porcentual de logs por nivel (CRITICAL, HIGH, MEDIUM, LOW)
2. **Donut - Estado**: Proporción de logs resueltos vs no resueltos
3. **Barras - Top 10 Subsistemas**: Subsistemas con más errores
4. **Barras - Top 10 Satélites**: Satélites más problemáticos
5. **Línea Temporal**: Evolución de eventos por día
6. **Scatter - SNR vs Elevación**: Relación entre señal y ángulo con color por severidad

### Panel Lateral:
- Filtro por **Severidad**
- Filtro por **Satélite**
- Filtro por **Subsistema**
- Filtro por **Estado** (Resuelto/No Resuelto)
- **Búsqueda** por Log ID o Error Code
- Botón **Recargar datos**

### Tabla Detalle:
- Muestra todos los logs filtrados
- Columnas: Log ID, Timestamp, Satélite, Error Code, Severidad, Subsistema, Estado, SNR, Duración

### Estadísticas:
- SNR Promedio (dB)
- Duración Promedio (ms)
- Tasa de Resolución (%)
- Reintentos Promedio

---

## 🎨 Tema Visual

Ambos dashboards mantienen la identidad de **Wayne Enterprises**:
- Colores: Oro (#D4AA50), Negro (#050507), Rojo (#ff6b6b), Verde (#51cf66)
- Fuentes: Cinzel (títulos), Rajdhani (cuerpo)
- Diseño: Dark mode con bordes dorados

---

## 📝 Notas Técnicas

- El dashboard Streamlit lee directamente de la BD SQLite (db.sqlite3)
- No requiere sincronización manual de datos
- Los cambios en Django se reflejan inmediatamente al recargar en Streamlit
- Las gráficas son interactivas (hover, zoom, download)

---

## ⚠️ Troubleshooting

**Error: "ModuleNotFoundError: No module named 'streamlit'"**
→ Ejecuta: `pip install streamlit plotly`

**Error: "404 Not Found" en SQLite**
→ Verifica que db.sqlite3 existe en la raíz del proyecto

**Streamlit no carga datos**
→ Asegúrate de haber ejecutado: `python manage.py runserver` antes (para que la BD esté activa)

**Puerto 8501 ocupado**
→ Streamlit puede usar otro puerto: `streamlit run app.py --server.port 8502`
