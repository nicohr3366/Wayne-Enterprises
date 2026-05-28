import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from apps.realestate.etl.transform import load_data

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wayne Real Estate // Urban Analytics",
    page_icon="🦇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── THEME CONSTANTS ────────────────────────────────────────────────────────────
COLOR_MAP = {
    "Completado":                "#4ade80",
    "En Revisión":               "#fbbf24",
    "Suspendido":                "#fb923c",
    "Cancelado":                 "#f87171",
    "En Curso":                  "#818cf8",
    "En Licitación":             "#38bdf8",
    "Emergencia — Prioridad S":  "#e879f9",
}

def hex_to_rgba(hex_color: str, alpha: float = 0.5) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

BG_DEEP    = "#060608"
BG_CARD    = "#0d0d12"
GOLD       = "#c9a84c"
GOLD_DIM   = "#7a5e28"
TEXT       = "#e8e0cc"
TEXT_MUTED = "#6b6455"

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
html, body { background: #060608; }

.stApp {
    background-color: #060608;
    background-image:
        repeating-linear-gradient(0deg,  transparent, transparent 2px,  rgba(201,168,76,0.012) 2px,  rgba(201,168,76,0.012) 4px),
        repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(201,168,76,0.018) 80px, rgba(201,168,76,0.018) 81px);
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px, transparent 3px,
        rgba(0,0,0,0.07) 3px, rgba(0,0,0,0.07) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

*, p, li, span, div {
    font-family: 'Rajdhani', sans-serif;
    color: #e8e0cc;
}

h1, h2, h3, h4 {
    font-family: 'Cinzel', serif !important;
    color: #c9a84c !important;
    letter-spacing: 0.06em;
}

section[data-testid="stSidebar"] {
    background-color: #0d0d12 !important;
    border-right: 1px solid rgba(201,168,76,0.2);
}

section[data-testid="stSidebar"] * {
    color: #6b6455;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
}

.stPlotlyChart { background: transparent !important; }

[data-testid="stDataFrame"] {
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 4px;
}

[data-baseweb="select"] {
    background: #0d0d12 !important;
    border-color: rgba(201,168,76,0.3) !important;
}

hr { border-color: rgba(201,168,76,0.15) !important; margin: 24px 0; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #060608; }
::-webkit-scrollbar-thumb { background: #7a5e28; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ──────────────────────────────────────────────────────────────────
df_full = load_data()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:

    BAT_LOGO_B64 = "PHN2ZyB2aWV3Qm94PSIwIDAgNDggNDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0yNCAzOEMyNCAzOCA0IDMyIDQgMThDNCAxNCA4IDEwIDEyIDEyQzE0IDEzIDE0IDE2IDE0IDE2QzE0IDE2IDE3IDEyIDI0IDEyQzMxIDEyIDM0IDE2IDM0IDE2QzM0IDE2IDM0IDEzIDM2IDEyQzQwIDEwIDQ0IDE0IDQ0IDE4QzQ0IDMyIDI0IDM4IDI0IDM4WiIgZmlsbD0iI0M5QTg0QyIgb3BhY2l0eT0iMC45Ii8+CjxwYXRoIGQ9Ik0yNCAzNkMyNCAzNiA4IDMwIDggMTlDMTIgMjAgMTQgMTYgMTQgMTZDMTQgMTYgMTcgMjIgMjQgMjJDMzEgMjIgMzQgMTYgMzQgMTZDMzQgMTYgMzYgMjAgNDAgMTlDNDAgMzAgMjQgMzYgMjQgMzZaIiBmaWxsPSIjMDUwNTA3Ii8+CjxwYXRoIGQ9Ik0yNCAyNkwyMiAyMkgyNkwyNCAyNloiIGZpbGw9IiNDOUE4NEMiIG9wYWNpdHk9IjAuNSIvPgo8L3N2Zz4="

    st.markdown(
        f'<div style="text-align:center; padding:28px 0 24px;">'
        f'<div style="display:flex; align-items:center; justify-content:center; gap:12px;">'
        f'<img src="data:image/svg+xml;base64,{BAT_LOGO_B64}" width="44" height="44" style="display:block;"/>'
        f'<div style="text-align:left;">'
        f'<div style="font-family:Cinzel,serif; color:#c9a84c; font-size:13px; font-weight:900; letter-spacing:0.12em; line-height:1.25;">WAYNE<br>REAL ESTATE</div>'
        f'<div style="font-family:Share Tech Mono,monospace; color:#7a5e28; font-size:9px; letter-spacing:0.25em; margin-top:3px;">DIVISIÓN CORPORATIVA · 04</div>'
        f'</div>'
        f'</div>'
        f'<div style="width:80%; height:1px; background:linear-gradient(90deg,transparent,#c9a84c,transparent); opacity:0.35; margin:16px auto 0;"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="color:#7a5e28; letter-spacing:0.25em; font-size:10px; margin-bottom:12px; font-family:Share Tech Mono,monospace;">── FILTERS</div>',
        unsafe_allow_html=True,
    )

    estados_disponibles = sorted(df_full["estado"].dropna().unique().tolist())
    estados_sel = st.multiselect(
        "Estado",
        options=estados_disponibles,
        default=estados_disponibles,
        label_visibility="collapsed",
    )

    col_dist = None
    distritos_sel = []
    if "district" in df_full.columns or "distrito" in df_full.columns:
        col_dist = "district" if "district" in df_full.columns else "distrito"
        distritos = sorted(df_full[col_dist].dropna().unique().tolist())
        distritos_sel = st.multiselect(
            "Distrito",
            options=distritos,
            default=distritos,
            label_visibility="collapsed",
        )

    st.markdown("---")
    st.markdown("""
    <div style="font-family:Share Tech Mono,monospace; color:#3a342a; font-size:10px; line-height:1.9;">
        SYS // GOTHAM-GRID-04<br>
        LAT 40.7128° N · LNG 74.0060° W<br>
        ACCESS — ALPHA CLEARANCE<br>
        OPERATOR — B. WAYNE
    </div>
    """, unsafe_allow_html=True)


# ── APPLY FILTERS ──────────────────────────────────────────────────────────────
df = df_full[df_full["estado"].isin(estados_sel)]
if col_dist and distritos_sel:
    df = df[df[col_dist].isin(distritos_sel)]

total = len(df)


# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="font-family:Share Tech Mono,monospace; color:#7a5e28; font-size:10px; letter-spacing:0.4em; margin-bottom:12px;">// WAYNE ENTERPRISES · DIVISIÓN CORPORATIVA 04 · ACCESO RESTRINGIDO</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="font-family:Cinzel,serif; color:#c9a84c; font-size:13px; font-weight:400; letter-spacing:0.5em; margin-bottom:6px; opacity:0.7;">WAYNE ENTERPRISES</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="font-family:Cinzel,serif; color:#c9a84c; font-size:46px; font-weight:900; line-height:1.0; letter-spacing:0.06em;">WAYNE REAL ESTATE</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="font-family:Rajdhani,sans-serif; color:#e8e0cc; font-size:20px; font-weight:300; letter-spacing:0.25em; opacity:0.6; margin-top:4px; margin-bottom:4px;">URBAN PROJECTS ANALYTICS</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div style="display:flex; align-items:center; gap:14px; margin-top:16px; margin-bottom:8px;">'
    f'<div style="width:48px; height:1px; background:#c9a84c; opacity:0.5;"></div>'
    f'<div style="font-family:Share Tech Mono,monospace; color:#6b6455; font-size:11px; letter-spacing:0.2em;">{total} REGISTROS · GOTHAM CITY INFRASTRUCTURE DIVISION</div>'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown("---")


# ── METRIC CARDS ───────────────────────────────────────────────────────────────
status_counts = df["estado"].value_counts()
n = len(status_counts)
cols = st.columns(min(4, n))

for i, (estado, cantidad) in enumerate(status_counts.items()):
    color = COLOR_MAP.get(estado, GOLD)
    with cols[i % 4]:
        st.markdown(
            f'<div style="background:#0d0d12; border:1px solid rgba(201,168,76,0.15); border-left:3px solid {color}; padding:24px 20px 18px; margin-bottom:16px; position:relative; overflow:hidden;">'
            f'<div style="font-family:Share Tech Mono,monospace; color:#6b6455; font-size:10px; letter-spacing:0.25em; text-transform:uppercase; margin-bottom:12px;">{estado}</div>'
            f'<div style="font-family:Cinzel,serif; color:{color}; font-size:42px; font-weight:700; line-height:1;">{cantidad}</div>'
            f'<div style="position:absolute; bottom:6px; right:10px; font-size:30px; opacity:0.04; color:{color}; font-family:Cinzel,serif;">{cantidad}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── SECTION LABEL ──────────────────────────────────────────────────────────────
st.markdown(
    '<div style="font-family:Share Tech Mono,monospace; font-size:10px; color:#7a5e28; letter-spacing:0.35em; margin:8px 0 16px;">── PROJECT DISTRIBUTION</div>',
    unsafe_allow_html=True,
)

col_pie, col_bar = st.columns([1, 1], gap="large")

# ── DONUT CHART ────────────────────────────────────────────────────────────────
with col_pie:
    fig_donut = go.Figure(go.Pie(
        values=status_counts.values,
        labels=status_counts.index,
        hole=0.52,
        marker=dict(
            colors=[COLOR_MAP.get(s, GOLD) for s in status_counts.index],
            line=dict(color=BG_DEEP, width=4),
        ),
        textinfo="label+percent",
        textfont=dict(family="Share Tech Mono", size=12, color=TEXT),
        textposition="outside",
        pull=[0.02] * n,
        hovertemplate="<b>%{label}</b><br>%{value} proyectos<br>%{percent}<extra></extra>",
    ))

    fig_donut.add_annotation(
        text=f"{total}<br><span style='font-size:9px'>TOTAL</span>",
        x=0.5, y=0.5,
        font=dict(family="Cinzel", size=22, color=GOLD),
        showarrow=False,
        align="center",
    )

    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=TEXT,
        height=420,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
    )

    st.plotly_chart(fig_donut, use_container_width=True)

# ── BAR CHART ──────────────────────────────────────────────────────────────────
with col_bar:
    fig_bar = go.Figure()

    for estado, cantidad in status_counts.items():
        color = COLOR_MAP.get(estado, GOLD)
        fig_bar.add_trace(go.Bar(
            y=[estado],
            x=[cantidad],
            orientation="h",
            marker=dict(
                color=hex_to_rgba(color, 0.5),
                line=dict(color=color, width=1),
            ),
            text=str(cantidad),
            textposition="outside",
            textfont=dict(family="Cinzel", size=13, color=color),
            hovertemplate=f"<b>{estado}</b>: {cantidad}<extra></extra>",
            name=estado,
            showlegend=False,
        ))

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(t=20, b=20, l=0, r=60),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(201,168,76,0.08)",
            zeroline=False,
            tickfont=dict(family="Share Tech Mono", size=11, color=TEXT_MUTED),
            showline=True,
            linecolor="rgba(201,168,76,0.2)",
        ),
        yaxis=dict(
            tickfont=dict(family="Share Tech Mono", size=11, color=TEXT_MUTED),
            showgrid=False,
            showline=False,
        ),
        bargap=0.35,
    )

    st.plotly_chart(fig_bar, use_container_width=True)


# ── TABLE ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="font-family:Share Tech Mono,monospace; font-size:10px; color:#7a5e28; letter-spacing:0.35em; margin:8px 0 16px;">── PROJECT REGISTRY</div>',
    unsafe_allow_html=True,
)

column_cfg = {
    "estado": st.column_config.TextColumn("STATUS", width="medium"),
}

if "project_id" in df.columns:
    column_cfg["project_id"] = st.column_config.TextColumn("ID", width="small")
if "project_name" in df.columns:
    column_cfg["project_name"] = st.column_config.TextColumn("PROJECT NAME", width="large")
if "district" in df.columns:
    column_cfg["district"] = st.column_config.TextColumn("DISTRICT", width="medium")
elif "distrito" in df.columns:
    column_cfg["distrito"] = st.column_config.TextColumn("DISTRICT", width="medium")

st.dataframe(
    df,
    use_container_width=True,
    height=420,
    column_config=column_cfg,
    hide_index=True,
)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:56px; padding-top:20px; border-top:1px solid rgba(201,168,76,0.1); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
    <div style="font-family:Cinzel,serif; color:#2a241c; font-size:11px; letter-spacing:0.15em;">
        WAYNE REAL ESTATE · DIVISIÓN CORPORATIVA
    </div>
    <div style="font-family:Share Tech Mono,monospace; color:#2a241c; font-size:10px; letter-spacing:0.15em;">
        © WAYNE ENTERPRISES · GOTHAM CITY · CLEARANCE: ALPHA
    </div>
</div>
""", unsafe_allow_html=True)