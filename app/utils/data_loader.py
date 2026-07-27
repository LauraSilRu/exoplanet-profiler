import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def load_data():
    """Carga el dataset de clustering real si existe; si no, devuelve un mensaje claro."""
    base_path = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
    clustered_data_path = base_path / "clustered_exoplanets.csv"

    if not clustered_data_path.exists():
        st.session_state["is_mock"] = True
        st.session_state["data_status"] = "No se encontró el archivo de clustering procesado."
        return pd.DataFrame()

    df = pd.read_csv(clustered_data_path)

    if "pl_name" in df.columns:
        df = df.rename(columns={"pl_name": "planet_name"})

    if "Cluster_K4" in df.columns:
        df = df.rename(columns={"Cluster_K4": "cluster_label"})

    if "Familia_Planeta" in df.columns:
        df = df.rename(columns={"Familia_Planeta": "family_label"})

    st.session_state["is_mock"] = False
    st.session_state["data_status"] = "Datos de clustering cargados correctamente."

    if "df" not in st.session_state:
        st.session_state["df"] = df

    return df