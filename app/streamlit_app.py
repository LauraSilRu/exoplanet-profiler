import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualization import create_cluster_scatter_plot

st.set_page_config(
    page_title="ExoProfiler",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("🌌 ExoProfiler: Explorador de Familias")
st.markdown("### Visualiza las familias de mundos descubiertas a través de clustering.")

# Carga los datos
with st.spinner("Cargando datos de clustering..."):
    df = load_data()

# Estado de datos
if df.empty:
    st.warning("No hay datos de clustering disponibles todavía.")
    st.info("Asegúrate de haber generado el archivo data/processed/clustered_exoplanets.csv desde el notebook de análisis.")
    st.stop()

st.success(st.session_state.get("data_status", "Datos cargados."))

st.sidebar.header("Filtros")
if "cluster_label" in df.columns:
    cluster_options = sorted(df["cluster_label"].dropna().astype(int).unique().tolist())
    selected_cluster = st.sidebar.multiselect("Familias a mostrar", cluster_options, default=cluster_options)
    if selected_cluster:
        df = df[df["cluster_label"].isin(selected_cluster)]

col1, col2, col3 = st.columns(3)
col1.metric("Planetas cargados", len(df))
col2.metric("Familias detectadas", df["cluster_label"].nunique() if "cluster_label" in df.columns else "N/D")
col3.metric("Fuente", "clustered_exoplanets.csv")

fig = create_cluster_scatter_plot(df)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver tabla de datos"):
    st.dataframe(df[[c for c in ["planet_name", "cluster_label", "family_label", "PC1", "PC2", "PC3", "PC4"] if c in df.columns]].head(200))