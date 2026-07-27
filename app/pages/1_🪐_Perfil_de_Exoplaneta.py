import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Perfil de Exoplaneta", page_icon="🪐", layout="wide")

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

st.title("🪐 Perfil de Exoplaneta")
st.markdown("### Consulta el perfil de un exoplaneta específico.")

if "planet_name" not in df.columns:
    st.error("No se encontró la columna de identificador del planeta en los datos cargados.")
    st.stop()

planet_name = st.selectbox(
    "Selecciona un Exoplaneta",
    options=sorted(df["planet_name"].dropna().tolist()),
    index=None,
    placeholder="Elige un planeta...",
)

if planet_name:
    profile = df.loc[df["planet_name"] == planet_name].iloc[0].to_dict()
    st.json(profile)
