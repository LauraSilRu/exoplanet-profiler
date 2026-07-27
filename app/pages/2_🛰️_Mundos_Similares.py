import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Mundos Similares", page_icon="🛰️", layout="wide")

st.title("🛰️ Mundos Similares")

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

st.markdown("### Selecciona un exoplaneta para encontrar otros mundos en su misma familia.")

planet_name = st.selectbox(
    "Selecciona un Exoplaneta de referencia:",
    options=sorted(df["planet_name"].dropna().tolist()),
    index=None,
    placeholder="Elige un planeta...",
)

if planet_name:
    selected_planet_cluster = df.loc[df["planet_name"] == planet_name, "cluster_label"].iloc[0]
    similar_planets_df = df[df["cluster_label"] == selected_planet_cluster].copy()

    st.write(f"El planeta **{planet_name}** pertenece a la **Familia {selected_planet_cluster}**.")
    st.write(f"Se han encontrado **{len(similar_planets_df)}** mundos en esta familia (incluyendo el seleccionado):")

    display_columns = [c for c in ["planet_name", "cluster_label", "family_label", "PC1", "PC2", "PC3", "PC4"] if c in similar_planets_df.columns]
    st.dataframe(similar_planets_df[display_columns])