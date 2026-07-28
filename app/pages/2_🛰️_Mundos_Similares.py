import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Mundos Similares", page_icon="🛰️", layout="wide")

st.title("🛰️ Mundos Similares")
st.markdown(
    "Selecciona un exoplaneta de referencia y descubre todos los mundos que pertenecen a "
    "su misma **familia de mundos**, visualizados en el espacio PCA."
)

# ── Advertencia ética ────────────────────────────────────────────────────────
st.warning(
    "⚠️ **Nota metodológica:** Los planetas de una misma familia comparten un perfil estadístico "
    "similar en el espacio PCA. Esto no implica semejanza física garantizada ni proximidad "
    "astronómica real. Son agrupaciones matemáticas, no categorías taxonómicas oficiales.",
    icon="⚠️",
)

# ── Carga de datos ───────────────────────────────────────────────────────────
if "df" not in st.session_state or st.session_state.df.empty:
    data_path = Path(__file__).resolve().parent.parent / ".." / "data" / "processed" / "clustered_exoplanets.csv"
    if data_path.exists():
        df = pd.read_csv(data_path)
        if "pl_name" in df.columns:
            df = df.rename(columns={"pl_name": "planet_name"})
        if "Cluster_K4" in df.columns:
            df = df.rename(columns={"Cluster_K4": "cluster_label"})
        if "Familia_Planeta" in df.columns:
            df = df.rename(columns={"Familia_Planeta": "family_label"})
        st.session_state.df = df
    else:
        st.warning("No se encontraron datos procesados. Revisa que exista el archivo clustered_exoplanets.csv.")
        st.stop()
else:
    df = st.session_state.df

if "cluster_label" not in df.columns:
    st.error("Los datos cargados no contienen información de clusters ('cluster_label').")
    st.info("Esta funcionalidad requiere que el notebook de clustering genere la columna correspondiente.")
    st.stop()

# ── Información de familias ───────────────────────────────────────────────────
FAMILY_INFO = {
    0: ("🔴 Gigantes Gaseosos",         "#FF6F61"),
    1: ("🔵 Sub-Neptunos / Neptunos Fríos", "#4FC3F7"),
    2: ("⭐ Anomalía Extrema",           "#F0C75E"),
    3: ("🟢 Rocosos / Super-Tierras",    "#66BB6A"),
}

# ── Selector ─────────────────────────────────────────────────────────────────
st.markdown("---")
planet_name = st.selectbox(
    "🔍 Selecciona un Exoplaneta de referencia:",
    options=sorted(df["planet_name"].dropna().tolist()),
    index=None,
    placeholder="Escribe o elige un planeta...",
)

if planet_name:
    selected_cluster = int(df.loc[df["planet_name"] == planet_name, "cluster_label"].iloc[0])
    similar_df = df[df["cluster_label"] == selected_cluster].copy()
    family_name, family_color = FAMILY_INFO.get(selected_cluster, ("Familia desconocida", "#999999"))

    # ── Banner ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{family_color}22; border-left: 5px solid {family_color};
         padding: 14px 20px; border-radius: 10px; margin: 16px 0">
        <h3 style="color:{family_color}; margin:0 0 4px 0">{family_name}</h3>
        <p style="margin:0; color:#ccc; font-size:0.9em">
            <b>{planet_name}</b> pertenece a esta familia junto con otros
            <b>{len(similar_df) - 1}</b> mundos ({len(similar_df)} en total, {len(similar_df)/len(df)*100:.1f}% del catálogo).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Gráfico scatter destacado ─────────────────────────────────────────────
    st.markdown("### 🗺️ Posición en el espacio PCA (PC1 vs PC2)")
    st.caption(
        "Los puntos de color representan todos los planetas de la misma familia. "
        "La ⭐ dorada es el planeta que seleccionaste."
    )

    fig = go.Figure()

    # Todos los planetas de la familia (fondo)
    others = similar_df[similar_df["planet_name"] != planet_name]
    fig.add_trace(go.Scatter(
        x=others["PC1"], y=others["PC2"],
        mode="markers",
        marker=dict(size=7, color=family_color, opacity=0.55,
                    line=dict(width=0.5, color="white")),
        text=others["planet_name"],
        hovertemplate="<b>%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>",
        name=f"Familia: {family_name}",
    ))

    # El planeta seleccionado (destacado)
    sel_row = df[df["planet_name"] == planet_name]
    fig.add_trace(go.Scatter(
        x=sel_row["PC1"], y=sel_row["PC2"],
        mode="markers+text",
        marker=dict(size=16, color="gold", symbol="star",
                    line=dict(width=1.5, color="white")),
        text=[planet_name],
        textposition="top center",
        textfont=dict(color="white", size=12),
        hovertemplate=f"<b>{planet_name}</b><br>PC1: %{{x:.2f}}<br>PC2: %{{y:.2f}}<extra></extra>",
        name="Seleccionado",
    ))

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#111B3A",
        font=dict(color="white"),
        xaxis=dict(title="PC1 — Escala orbital (44.0%)",
                   gridcolor="rgba(255,255,255,0.1)", color="white"),
        yaxis=dict(title="PC2 — Gradiente térmico-estelar (30.2%)",
                   gridcolor="rgba(255,255,255,0.1)", color="white"),
        legend=dict(font=dict(color="white")),
        height=480,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Tabla de mundos similares ─────────────────────────────────────────────
    st.markdown("### 📋 Todos los mundos de esta familia")
    display_cols = [c for c in ["planet_name", "cluster_label", "family_label", "PC1", "PC2", "PC3", "PC4"] if c in similar_df.columns]
    st.dataframe(similar_df[display_cols], use_container_width=True)