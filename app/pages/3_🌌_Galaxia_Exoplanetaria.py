"""
Página: Galaxia Exoplanetaria
------------------------------
Mapa 3D de exoplanetas (espacio PCA) con buscador que sugiere nombres
a medida que el usuario escribe. No requiere librerías externas: Streamlit
re-ejecuta el script en cada tecla, así que el filtrado es en vivo con
Python puro.

"""

import streamlit as st
from utils.data_loader import load_data, get_planet_names
from utils.visualization import create_galaxy_view

st.set_page_config(page_title="Galaxia Exoplanetaria", page_icon="🌌", layout="wide")

st.title("🌌 Galaxia Exoplanetaria")
st.caption(
    "Explorá los exoplanetas ubicados en el espacio de sus 3 primeras "
    "componentes principales (PC1, PC2, PC3). Esta vista **no representa "
    "coordenadas astronómicas reales**: es una proyección del mismo espacio "
    "de características usado para el clustering, con estética de campo estelar."
)

df = load_data()

if df.empty:
    st.warning(st.session_state.get("data_status", "No hay datos disponibles."))
    st.stop()

planet_names = get_planet_names(df)

if "galaxy_selected_planet" not in st.session_state:
    st.session_state["galaxy_selected_planet"] = None

# --- Buscador con sugerencias en vivo ---
search_term = st.text_input(
    "🔎 Buscar exoplaneta",
    placeholder="Escribí el nombre del planeta (ej. Kepler-22 b)...",
    key="galaxy_search_input",
)

if search_term:
    matches = [name for name in planet_names if search_term.lower() in name.lower()][:8]

    if matches:
        st.caption(f"{len(matches)} coincidencia(s) — hacé clic para ubicarlo en el mapa:")
        cols = st.columns(len(matches))
        for col, name in zip(cols, matches):
            if col.button(name, use_container_width=True, key=f"suggestion_{name}"):
                st.session_state["galaxy_selected_planet"] = name
    else:
        st.info("No se encontraron planetas con ese nombre.")

selected = st.session_state["galaxy_selected_planet"]

# --- Layout: mapa + panel de detalle ---
if selected:
    col_map, col_info = st.columns([3, 1])

    with col_info:
        st.metric("Planeta seleccionado", selected)
        row = df[df["planet_name"] == selected]
        if not row.empty:
            if "family_label" in df.columns:
                st.write(f"**Familia:** {row['family_label'].values[0]}")
            if "cluster_label" in df.columns:
                st.write(f"**Cluster:** {row['cluster_label'].values[0]}")
        if st.button("✖️ Limpiar selección"):
            st.session_state["galaxy_selected_planet"] = None
            st.rerun()

    with col_map:
        st.plotly_chart(create_galaxy_view(df, highlighted_planet=selected), use_container_width=True)
else:
    st.plotly_chart(create_galaxy_view(df), use_container_width=True)
