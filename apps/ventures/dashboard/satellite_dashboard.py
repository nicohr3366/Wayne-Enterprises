import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Wayne Ventures · Satellite Monitoring", page_icon="📡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
  .stApp { background: #030d1a; }
  .block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }
  html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; color: #cbd5e1; }
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
  .wayne-header { display: flex; align-items: center; justify-content: space-between; padding: 22px 0 18px; border-bottom: 1px solid rgba(212,170,80,0.2); margin-bottom: 28px; }
  .wayne-title { font-family: 'Cinzel', serif; font-size: 22px; font-weight: 900; color: #f8fafc; letter-spacing: .12em; }
  .wayne-subtitle { font-size: 11px; color: #64748b; letter-spacing: .25em; text-transform: uppercase; margin-top: 4px; }
  .wayne-badge { background: rgba(212,170,80,.1); border: 1px solid rgba(212,170,80,.35); color: #D4AA50; padding: 5px 14px; border-radius: 4px; font-size: 10px; letter-spacing: .2em; text-transform: uppercase; }
  .gold-line { height: 1px; background: linear-gradient(90deg,#D4AA50,transparent); margin: 6px 0 0; width: 80px; }
  .kpi-card { background: rgba(7,18,36,0.95); border: 1px solid rgba(212,170,80,0.15); border-radius: 10px; padding: 20px 22px; text-align: center; position: relative; overflow: hidden; }
  .kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background: linear-gradient(90deg,#D4AA50,transparent); }
  .kpi-number { font-family: 'Cinzel', serif; font-size: 34px; font-weight: 900; line-height: 1.1; margin: 8px 0 4px; }
  .kpi-label  { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #64748b; }
  .kpi-icon   { font-size: 20px; margin-bottom: 4px; }
  .chart-wrapper { background: rgba(7,18,36,0.95); border: 1px solid rgba(212,170,80,0.12); border-radius: 10px; padding: 20px; margin-bottom: 16px; }
  .chart-title { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #7a7060; padding-bottom: 10px; margin-bottom: 16px; border-bottom: 1px solid rgba(212,170,80,0.1); font-family: 'Cinzel', serif; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos_csv():
    csv_path = Path(__file__).parent.parent / "data" / "WayneTech_Satellite_ErrorLogs.csv"
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        return df
    except FileNotFoundError:
        st.error(f"CSV no encontrado en: {csv_path}")
        return pd.DataFrame()

df_raw = cargar_datos_csv()
if df_raw.empty:
    st.error("No hay datos en el CSV")
    st.stop()

# Detectar columnas del CSV
severity_col = 'Severidad' if 'Severidad' in df_raw.columns else 'severity'
sat_col = 'Satélite' if 'Satélite' in df_raw.columns else 'satellite_name'
subsys_col = 'Subsistema' if 'Subsistema' in df_raw.columns else 'subsystem'
resolved_col = 'Resuelto' if 'Resuelto' in df_raw.columns else 'resolved'
log_col = 'Log ID' if 'Log ID' in df_raw.columns else 'log_id'
err_col = 'Código Error' if 'Código Error' in df_raw.columns else 'error_code'
ts_col = 'Fecha/Hora' if 'Fecha/Hora' in df_raw.columns else 'timestamp'
snr_col = 'SNR (dB)' if 'SNR (dB)' in df_raw.columns else 'snr_db'
elev_col = 'Ángulo Elevación (°)' if 'Ángulo Elevación (°)' in df_raw.columns else 'elevation_angle_deg'

with st.sidebar:
    st.markdown("### 🔍 Filtros")
    st.markdown("---")
    sel_sev = st.selectbox("Severidad", ["Todas"] + sorted(df_raw[severity_col].dropna().unique().tolist()))
    sel_sat = st.selectbox("Satélite", ["Todos"] + sorted(df_raw[sat_col].dropna().unique().tolist()))
    sel_sub = st.selectbox("Subsistema", ["Todos"] + sorted(df_raw[subsys_col].dropna().unique().tolist()))
    sel_res = st.selectbox("Estado", ["Todos", "Resuelto", "No Resuelto"])
    buscar = st.text_input("Buscar (Log ID / Error Code)", "")
    st.markdown("---")
    if st.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()

df = df_raw.copy()
if sel_sev != "Todas":
    df = df[df[severity_col] == sel_sev]
if sel_sat != "Todos":
    df = df[df[sat_col] == sel_sat]
if sel_sub != "Todos":
    df = df[df[subsys_col] == sel_sub]
if sel_res == "Resuelto":
    df = df[df[resolved_col] == "Sí"]
elif sel_res == "No Resuelto":
    df = df[df[resolved_col] == "No"]
if buscar:
    mask = (
        df[log_col].astype(str).str.contains(buscar, case=False, na=False) |
        df[err_col].astype(str).str.contains(buscar, case=False, na=False)
    )
    df = df[mask]

total = len(df)
criticos = len(df[df[severity_col] == "CRITICAL"])
altos = len(df[df[severity_col] == "HIGH"])
resueltos = len(df[df[resolved_col] == "Sí"])

col1, col2, col3, col4 = st.columns(4)
for col, icon, color, valor, label in zip([col1, col2, col3, col4], 
                                           ["📡", "⚠️", "🔴", "✔️"], 
                                           ["#D4AA50", "#ff6b6b", "#ffd93d", "#51cf66"],
                                           [total, criticos, altos, resueltos],
                                           ["Total Logs", "Críticos", "Alta Severidad", "Resueltos"]):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-icon">{icon}</div>
          <div class="kpi-number" style="color:{color}">{valor:,}</div>
          <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

COLORES = ["#ff6b6b", "#ffd93d", "#51cf66", "#74c0fc", "#D4AA50", "#ec4899", "#14b8a6", "#8b5cf6", "#f97316", "#06b6d4"]
BASE_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Rajdhani, sans-serif", color="#94a3b8"), margin=dict(l=10, r=10, t=10, b=10), legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1", size=11)))

def grafica_donut(serie, titulo):
    conteo = serie.value_counts().reset_index()
    conteo.columns = ["categoria", "total"]
    fig = px.pie(conteo, names="categoria", values="total", hole=0.55, color_discrete_sequence=COLORES)
    fig.update_layout(**BASE_LAYOUT)
    fig.update_traces(textfont_color="#cbd5e1", textfont_size=11)
    st.markdown(f'<div class="chart-wrapper"><div class="chart-title">{titulo}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_barras(serie, titulo, top=10):
    conteo = serie.value_counts().nlargest(top).reset_index()
    conteo.columns = ["categoria", "total"]
    conteo = conteo.sort_values("total", ascending=True)
    fig = px.bar(conteo, x="total", y="categoria", orientation="h", color="total", color_continuous_scale=["#0c2a4a", "#D4AA50"])
    fig.update_layout(**BASE_LAYOUT, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", color="#94a3b8")
    st.markdown(f'<div class="chart-wrapper"><div class="chart-title">{titulo}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_linea():
    df_ts = df.copy()
    df_ts[ts_col] = pd.to_datetime(df_ts[ts_col])
    df_ts["fecha"] = df_ts[ts_col].dt.date
    por_dia = df_ts.groupby("fecha").size().reset_index(name="Eventos")
    fig = px.line(por_dia, x="fecha", y="Eventos", color_discrete_sequence=["#D4AA50"])
    fig.update_traces(line_width=2.5, mode="lines+markers", marker_color="#ffd93d", marker_size=5)
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    st.markdown('<div class="chart-wrapper"><div class="chart-title">Eventos por día</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_scatter():
    df_scatter = df.dropna(subset=[snr_col, elev_col, severity_col]).copy()
    if len(df_scatter) == 0:
        st.info("No hay datos disponibles")
        return
    severity_colors = {"CRITICAL": "#ff6b6b", "HIGH": "#ffd93d", "MEDIUM": "#74c0fc", "LOW": "#51cf66"}
    fig = px.scatter(df_scatter, x=snr_col, y=elev_col, color=severity_col, color_discrete_map=severity_colors, hover_data=[log_col, sat_col, subsys_col])
    fig.update_layout(**BASE_LAYOUT, hovermode="closest")
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    st.markdown('<div class="chart-wrapper"><div class="chart-title">SNR vs Ángulo Elevación (color = severidad)</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 📊 Análisis Principal")
c1, c2 = st.columns(2)
with c1:
    grafica_donut(df[severity_col], "Distribución por Severidad")
with c2:
    grafica_donut(df[resolved_col], "Estado de los Logs")

grafica_barras(df[subsys_col], "Top 10 Subsistemas Problemáticos", 10)
grafica_barras(df[sat_col], "Top 10 Satélites Más Activos", 10)
grafica_linea()
grafica_scatter()

st.markdown("### 📋 Detalle de Logs")
cols_mostrar = [log_col, ts_col, sat_col, err_col, severity_col, subsys_col, resolved_col, snr_col]
cols_existentes = [c for c in cols_mostrar if c in df.columns]
df_tabla = df[cols_existentes].copy()
df_tabla.columns = ["Log ID", "Timestamp", "Satélite", "Error Code", "Severidad", "Subsistema", "Resuelto", "SNR (dB)"]
st.dataframe(df_tabla, use_container_width=True, height=400)

st.markdown("### 📈 Estadísticas")
col1, col2, col3, col4 = st.columns(4)
with col1:
    snr_mean = pd.to_numeric(df[snr_col], errors='coerce').mean()
    st.metric("SNR Promedio", f"{snr_mean:.2f} dB")
with col2:
    st.metric("Total Eventos", f"{len(df):,}")
with col3:
    tasa = (len(df[df[resolved_col] == "Sí"])/len(df)*100) if len(df) > 0 else 0
    st.metric("Tasa Resolución", f"{tasa:.1f}%")
with col4:
    st.metric("Satélites Únicos", f"{df[sat_col].nunique()}")

# ESTILOS WAYNE ENTERPRISES
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
  .stApp { background: #030d1a; }
  .block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }
  html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; color: #cbd5e1; }
  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
  .wayne-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 0 18px; border-bottom: 1px solid rgba(212,170,80,0.2); margin-bottom: 28px;
  }
  .wayne-title { font-family: 'Cinzel', serif; font-size: 22px; font-weight: 900; color: #f8fafc; letter-spacing: .12em; }
  .wayne-subtitle { font-size: 11px; color: #64748b; letter-spacing: .25em; text-transform: uppercase; margin-top: 4px; }
  .wayne-badge { background: rgba(212,170,80,.1); border: 1px solid rgba(212,170,80,.35); color: #D4AA50; padding: 5px 14px; border-radius: 4px; font-size: 10px; letter-spacing: .2em; text-transform: uppercase; }
  .gold-line { height: 1px; background: linear-gradient(90deg,#D4AA50,transparent); margin: 6px 0 0; width: 80px; }
  .kpi-card { background: rgba(7,18,36,0.95); border: 1px solid rgba(212,170,80,0.15); border-radius: 10px; padding: 20px 22px; text-align: center; position: relative; overflow: hidden; }
  .kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
  .kpi-gold::before  { background: linear-gradient(90deg,#D4AA50,transparent); }
  .kpi-red::before    { background: linear-gradient(90deg,#ff6b6b,transparent); }
  .kpi-orange::before { background: linear-gradient(90deg,#ffd93d,transparent); }
  .kpi-green::before  { background: linear-gradient(90deg,#51cf66,transparent); }
  .kpi-number { font-family: 'Cinzel', serif; font-size: 34px; font-weight: 900; line-height: 1.1; margin: 8px 0 4px; }
  .kpi-label  { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #64748b; }
  .kpi-icon   { font-size: 20px; margin-bottom: 4px; }
  .chart-wrapper { background: rgba(7,18,36,0.95); border: 1px solid rgba(212,170,80,0.12); border-radius: 10px; padding: 20px; margin-bottom: 16px; }
  .chart-title { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #7a7060; padding-bottom: 10px; margin-bottom: 16px; border-bottom: 1px solid rgba(212,170,80,0.1); font-family: 'Cinzel', serif; }
</style>
""", unsafe_allow_html=True)

# CARGA DE DATOS DESDE CSV
@st.cache_data
def cargar_datos_csv():
    """Carga datos desde el CSV"""
    csv_path = Path(__file__).parent.parent / "data" / "WayneTech_Satellite_ErrorLogs.csv"
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        return df
    except FileNotFoundError:
        st.error(f"CSV no encontrado en: {csv_path}")
        st.info("Verifica que el archivo exista en apps/ventures/data/")
        return pd.DataFrame()

try:
    df_raw = cargar_datos_csv()
    if df_raw.empty:
        st.error("No hay datos en el CSV")
        st.stop()
except Exception as e:
    st.error(f"Error cargando datos: {str(e)}")
    st.stop()

# Detectar columnas del CSV
severity_col = 'Severidad' if 'Severidad' in df_raw.columns else 'severity'
sat_col = 'Satélite' if 'Satélite' in df_raw.columns else 'satellite_name'
subsys_col = 'Subsistema' if 'Subsistema' in df_raw.columns else 'subsystem'
resolved_col = 'Resuelto' if 'Resuelto' in df_raw.columns else 'resolved'
log_col = 'Log ID' if 'Log ID' in df_raw.columns else 'log_id'
err_col = 'Código Error' if 'Código Error' in df_raw.columns else 'error_code'
ts_col = 'Fecha/Hora' if 'Fecha/Hora' in df_raw.columns else 'timestamp'
snr_col = 'SNR (dB)' if 'SNR (dB)' in df_raw.columns else 'snr_db'
elev_col = 'Ángulo Elevación (°)' if 'Ángulo Elevación (°)' in df_raw.columns else 'elevation_angle_deg'

# HEADER
st.markdown("""
<div class="wayne-header">
  <div>
    <div class="wayne-title">📡 Wayne Ventures Satellite Monitoring</div>
    <div class="wayne-subtitle">Orbital Error Tracking · Live Dashboard</div>
    <div class="gold-line"></div>
  </div>
  <div class="wayne-badge">Satellite Core · Live</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR FILTROS
with st.sidebar:
    st.markdown("### 🔍 Filtros")
    st.markdown("---")
    
    sel_sev = st.selectbox("Severidad", ["Todas"] + sorted(df_raw[severity_col].dropna().unique().tolist()), key="sel_sev")
    sel_sat = st.selectbox("Satélite", ["Todos"] + sorted(df_raw[sat_col].dropna().unique().tolist()), key="sel_sat")
    sel_sub = st.selectbox("Subsistema", ["Todos"] + sorted(df_raw[subsys_col].dropna().unique().tolist()), key="sel_sub")
    sel_res = st.selectbox("Estado", ["Todos", "Resuelto", "No Resuelto"], key="sel_res")
    
    buscar = st.text_input("Buscar (Log ID / Error Code)", "", key="search_input")
    st.markdown("---")
    if st.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()

# APLICAR FILTROS
df = df_raw.copy()
if sel_sev != "Todas":
    df = df[df[severity_col] == sel_sev]
if sel_sat != "Todos":
    df = df[df[sat_col] == sel_sat]
if sel_sub != "Todos":
    df = df[df[subsys_col] == sel_sub]
if sel_res == "Resuelto":
    df = df[df[resolved_col] == "Sí"]
elif sel_res == "No Resuelto":
    df = df[df[resolved_col] == "No"]
if buscar:
    mask = (
        df[log_col].str.contains(buscar, case=False, na=False) |
        df[err_col].str.contains(buscar, case=False, na=False)
    )
    df = df[mask]

# KPIs
total = len(df)
criticos = len(df[df[severity_col] == "CRITICAL"])
altos = len(df[df[severity_col] == "HIGH"])
resueltos = len(df[df[resolved_col] == "Sí"])

col1, col2, col3, col4 = st.columns(4)
kpis = [
    (col1, "kpi-gold", "📡", "#D4AA50", total, "Total Logs"),
    (col2, "kpi-red", "⚠️", "#ff6b6b", criticos, "Críticos"),
    (col3, "kpi-orange", "🔴", "#ffd93d", altos, "Alta Severidad"),
    (col4, "kpi-green", "✔️", "#51cf66", resueltos, "Resueltos"),
]
for col, cls, icon, color, valor, label in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-icon">{icon}</div>
          <div class="kpi-number" style="color:{color}">{valor:,}</div>
          <div class="kpi-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# PALETA DE COLORES
COLORES = ["#ff6b6b", "#ffd93d", "#51cf66", "#74c0fc", "#D4AA50",
           "#ec4899", "#14b8a6", "#8b5cf6", "#f97316", "#06b6d4"]

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Rajdhani, sans-serif", color="#94a3b8"),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1", size=11)),
)

# FUNCIONES DE GRAFICAS

def grafica_donut(serie, titulo):
    """Donut chart para variables categóricas"""
    conteo = serie.value_counts().reset_index()
    conteo.columns = ["categoria", "total"]
    fig = px.pie(conteo, names="categoria", values="total", hole=0.55,
                 color_discrete_sequence=COLORES)
    fig.update_layout(**BASE_LAYOUT)
    fig.update_traces(textfont_color="#cbd5e1", textfont_size=11)
    st.markdown(f'<div class="chart-wrapper"><div class="chart-title">{titulo}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_barras(serie, titulo, top=10):
    """Barra horizontal para top N valores"""
    conteo = serie.value_counts().nlargest(top).reset_index()
    conteo.columns = ["categoria", "total"]
    conteo = conteo.sort_values("total", ascending=True)
    fig = px.bar(conteo, x="total", y="categoria", orientation="h",
                 color="total", color_continuous_scale=["#0c2a4a", "#D4AA50"])
    fig.update_layout(**BASE_LAYOUT, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", color="#94a3b8")
    st.markdown(f'<div class="chart-wrapper"><div class="chart-title">{titulo}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_linea():
    """Línea temporal: eventos agrupados por día"""
    df_ts = df.copy()
    df_ts["timestamp"] = pd.to_datetime(df_ts["timestamp"])
    df_ts["fecha"] = df_ts["timestamp"].dt.date
    por_dia = df_ts.groupby("fecha").size().reset_index(name="Eventos")
    fig = px.line(por_dia, x="fecha", y="Eventos", color_discrete_sequence=["#D4AA50"])
    fig.update_traces(line_width=2.5, mode="lines+markers",
                      marker_color="#ffd93d", marker_size=5)
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b")
    st.markdown('<div class="chart-wrapper"><div class="chart-title">Eventos por día</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_scatter_snr_ber():
    """Scatter: SNR vs Bit Error Rate con color por Severidad"""
    df_scatter = df.dropna(subset=['snr_db', 'elevation_angle_deg', 'severity']).copy()
    if len(df_scatter) == 0:
        st.info("No hay datos disponibles para esta gráfica")
        return
    
    severity_colors = {
        "CRITICAL": "#ff6b6b",
        "HIGH": "#ffd93d",
        "MEDIUM": "#74c0fc",
        "LOW": "#51cf66"
    }
    
    fig = px.scatter(df_scatter, x="snr_db", y="elevation_angle_deg", 
                     color="severity", size="event_duration_ms",
                     color_discrete_map=severity_colors,
                     hover_data=["log_id", "satellite_name", "subsystem"])
    fig.update_layout(**BASE_LAYOUT, hovermode="closest")
    fig.update_xaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b", title="SNR (dB)")
    fig.update_yaxes(gridcolor="rgba(212,170,80,0.08)", color="#64748b", title="Ángulo Elevación (°)")
    st.markdown('<div class="chart-wrapper"><div class="chart-title">SNR vs Ángulo Elevación (tamaño = duración evento)</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RENDERIZAR GRAFICAS

st.markdown("### 📊 Análisis Principal")

# Fila 1: Donuts de Severidad y Estado
c1, c2 = st.columns(2)
with c1:
    grafica_donut(df["severity"], "Distribución por Severidad")
with c2:
    df["estado_texto"] = df["resolved"].apply(lambda x: "Resuelto" if x == 1 else "No Resuelto")
    grafica_donut(df["estado_texto"], "Estado de los Logs")

# Fila 2: Barras
grafica_barras(df["subsystem"], "Top 10 Subsistemas Problemáticos", 10)
grafica_barras(df["satellite_name"], "Top 10 Satélites Más Activos", 10)

# Fila 3: Línea temporal
grafica_linea()

# Fila 4: Scatter SNR vs Elevation
grafica_scatter_snr_ber()

# TABLA DETALLE
st.markdown("### 📋 Detalle de Logs (filtrados)")

# Preparar columnas para mostrar
cols_mostrar = ["log_id", "timestamp", "satellite_name", "error_code", 
                "severity", "subsystem", "resolved", "snr_db", "event_duration_ms"]
cols_existentes = [c for c in cols_mostrar if c in df.columns]

df_tabla = df[cols_existentes].copy()
df_tabla["resolved"] = df_tabla["resolved"].apply(lambda x: "✔️ Sí" if x == 1 else "❌ No")
df_tabla.columns = ["Log ID", "Timestamp", "Satélite", "Error Code", 
                    "Severidad", "Subsistema", "Resuelto", "SNR (dB)", "Duración (ms)"]

st.dataframe(df_tabla, use_container_width=True, height=400)

# ESTADÍSTICAS ADICIONALES
st.markdown("### 📈 Estadísticas Rápidas")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("SNR Promedio", f"{df['snr_db'].mean():.2f} dB")
with col2:
    st.metric("Duración Promedio", f"{df['event_duration_ms'].mean():.0f} ms")
with col3:
    if len(df) > 0:
        tasa = (len(df[df['resolved']==1])/len(df)*100)
    else:
        tasa = 0
    st.metric("Tasa Resolución", f"{tasa:.1f}%")
with col4:
    st.metric("Reintentos Promedio", f"{df['retry_count'].mean():.1f}")
