import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# CONFIGURACION
st.set_page_config(
    page_title="Wayne Healthcare · Cybersecurity",
    page_icon="🦇",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    padding: 22px 0 18px; border-bottom: 1px solid rgba(56,189,248,0.2); margin-bottom: 28px;
  }
  .wayne-title { font-family: 'Cinzel', serif; font-size: 22px; font-weight: 900; color: #f8fafc; letter-spacing: .12em; }
  .wayne-subtitle { font-size: 11px; color: #64748b; letter-spacing: .25em; text-transform: uppercase; margin-top: 4px; }
  .wayne-badge { background: rgba(56,189,248,.1); border: 1px solid rgba(56,189,248,.35); color: #38bdf8; padding: 5px 14px; border-radius: 4px; font-size: 10px; letter-spacing: .2em; text-transform: uppercase; }
  .gold-line { height: 1px; background: linear-gradient(90deg,#f59e0b,transparent); margin: 6px 0 0; width: 80px; }
  .kpi-card { background: rgba(7,18,36,0.95); border: 1px solid rgba(56,189,248,0.15); border-radius: 10px; padding: 20px 22px; text-align: center; position: relative; overflow: hidden; }
  .kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
  .kpi-blue::before   { background: linear-gradient(90deg,#38bdf8,transparent); }
  .kpi-red::before    { background: linear-gradient(90deg,#f87171,transparent); }
  .kpi-orange::before { background: linear-gradient(90deg,#f59e0b,transparent); }
  .kpi-green::before  { background: linear-gradient(90deg,#22c55e,transparent); }
  .kpi-number { font-family: 'Cinzel', serif; font-size: 34px; font-weight: 900; line-height: 1.1; margin: 8px 0 4px; }
  .kpi-label  { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #64748b; }
  .kpi-icon   { font-size: 20px; margin-bottom: 4px; }
  .chart-wrapper { background: rgba(7,18,36,0.95); border: 1px solid rgba(56,189,248,0.12); border-radius: 10px; padding: 20px; margin-bottom: 16px; }
  .chart-title { font-size: 10px; letter-spacing: .18em; text-transform: uppercase; color: #475569; padding-bottom: 10px; margin-bottom: 16px; border-bottom: 1px solid rgba(56,189,248,0.1); font-family: 'Cinzel', serif; }
</style>
""", unsafe_allow_html=True)

# CARGA DEL CSV
# Path relativo: este script esta en healthcare/dashboard/
# el CSV esta en healthcare/data/cybersecurity.csv
CSV_PATH = Path(__file__).parent.parent / "data" / "cybersecurity.csv"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df_raw = cargar_datos()
except FileNotFoundError:
    st.error(f"CSV no encontrado en: {CSV_PATH}")
    st.info("Ejecuta el comando desde la raiz del proyecto Django.")
    st.stop()

# HEADER
st.markdown("""
<div class="wayne-header">
  <div>
    <div class="wayne-title">🦇 Wayne Healthcare</div>
    <div class="wayne-subtitle">Cybersecurity Division · Intelligence Dashboard</div>
    <div class="gold-line"></div>
  </div>
  <div class="wayne-badge">Security Core · Live</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR FILTROS
with st.sidebar:
    st.markdown("### 🔍 Filtros")
    st.markdown("---")
    sel_sev  = st.selectbox("Severidad",      ["Todas"] + sorted(df_raw["Severidad"].dropna().unique().tolist()))
    sel_stat = st.selectbox("Estado",         ["Todos"] + sorted(df_raw["Estado"].dropna().unique().tolist()))
    sel_tipo = st.selectbox("Tipo de evento", ["Todos"] + sorted(df_raw["Tipo_Evento"].dropna().unique().tolist()))
    sel_prot = st.selectbox("Protocolo",      ["Todos"] + sorted(df_raw["Protocolo"].dropna().unique().tolist()))
    buscar   = st.text_input("Buscar (ID / sistema / analista)", "")
    st.markdown("---")
    if st.button("🔄 Recargar datos"):
        st.cache_data.clear()
        st.rerun()

# APLICAR FILTROS
df = df_raw.copy()
if sel_sev  != "Todas": df = df[df["Severidad"]   == sel_sev]
if sel_stat != "Todos":  df = df[df["Estado"]      == sel_stat]
if sel_tipo != "Todos":  df = df[df["Tipo_Evento"] == sel_tipo]
if sel_prot != "Todos":  df = df[df["Protocolo"]   == sel_prot]
if buscar:
    mask = (
        df["ID_Evento"].str.contains(buscar, case=False, na=False) |
        df["Sistema_Afectado"].str.contains(buscar, case=False, na=False) |
        df["Analista_IA"].str.contains(buscar, case=False, na=False)
    )
    df = df[mask]

# KPIs
total     = len(df)
criticas  = len(df[df["Severidad"] == "CRITICA"])
altas     = len(df[df["Severidad"] == "ALTA"])
resueltos = len(df[df["Estado"]    == "RESUELTO"])

col1, col2, col3, col4 = st.columns(4)
kpis = [
    (col1, "kpi-blue",   "🖥",  "#38bdf8", total,     "Total eventos"),
    (col2, "kpi-red",    "⚠️", "#f87171", criticas,  "Amenazas criticas"),
    (col3, "kpi-orange", "🔒", "#f59e0b", altas,     "Alta severidad"),
    (col4, "kpi-green",  "✔️", "#22c55e", resueltos, "Resueltos"),
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
COLORES = ["#f87171","#f59e0b","#38bdf8","#22c55e","#a78bfa",
           "#ec4899","#14b8a6","#8b5cf6","#f97316","#06b6d4"]

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Rajdhani, sans-serif", color="#94a3b8"),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1", size=11)),
)

# FUNCIONES DE GRAFICAS
def grafica_donut(serie, titulo):
    """Donut chart para variables categoricas como Severidad y Estado"""
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
    """Barra horizontal para top N valores de una columna"""
    conteo = serie.value_counts().nlargest(top).reset_index()
    conteo.columns = ["categoria", "total"]
    conteo = conteo.sort_values("total", ascending=True)
    fig = px.bar(conteo, x="total", y="categoria", orientation="h",
                 color="total", color_continuous_scale=["#0c2a4a", "#38bdf8"])
    fig.update_layout(**BASE_LAYOUT, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor="rgba(96,165,250,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", color="#94a3b8")
    st.markdown(f'<div class="chart-wrapper"><div class="chart-title">{titulo}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def grafica_linea():
    """Linea temporal: eventos agrupados por dia usando columna Timestamp"""
    df_ts = df.copy()
    df_ts["Timestamp"] = pd.to_datetime(df_ts["Timestamp"])
    df_ts["Fecha"]     = df_ts["Timestamp"].dt.date
    por_dia = df_ts.groupby("Fecha").size().reset_index(name="Eventos")
    fig = px.line(por_dia, x="Fecha", y="Eventos", color_discrete_sequence=["#38bdf8"])
    fig.update_traces(line_width=1.8, mode="lines+markers",
                      marker_color="#f59e0b", marker_size=4)
    fig.update_layout(**BASE_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(96,165,250,0.08)", color="#64748b")
    fig.update_yaxes(gridcolor="rgba(96,165,250,0.08)", color="#64748b")
    st.markdown('<div class="chart-wrapper"><div class="chart-title">Eventos por dia</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RENDERIZAR GRAFICAS
c1, c2 = st.columns(2)
with c1:
    grafica_donut(df["Severidad"], "Distribucion por severidad")
with c2:
    grafica_donut(df["Estado"],    "Estado de los incidentes")

grafica_barras(df["Tipo_Evento"],      "Top 10 tipos de amenaza")
grafica_barras(df["Sistema_Afectado"], "Top 10 sistemas afectados")

grafica_linea()

c3, c4 = st.columns(2)
with c3:
    grafica_donut(df["Protocolo"],   "Distribucion por protocolo")
with c4:
    grafica_donut(df["Analista_IA"], "Carga por analista IA")

# TABLA DETALLE
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-wrapper"><div class="chart-title">Registro detallado de eventos</div>', unsafe_allow_html=True)

cols_tabla = ["ID_Evento", "Timestamp", "Tipo_Evento", "Severidad",
              "Sistema_Afectado", "Estado", "Analista_IA", "Falso_Positivo"]

st.dataframe(
    df[cols_tabla].reset_index(drop=True),
    use_container_width=True,
    height=380,
)
st.caption(f"Mostrando {len(df):,} de {len(df_raw):,} registros")
st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="text-align:center; padding:28px 0 10px; font-family:'Cinzel',serif;
     font-size:10px; letter-spacing:.18em; color:#1e3a5f; text-transform:uppercase;">
  2024 Wayne Healthcare - Cybersecurity Division - Gotham City
</div>
""", unsafe_allow_html=True)