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

# ── Cabecera ─────────────────────────────────────────────────────────────────
st.title("🌌 Galaxia Exoplanetaria")
st.markdown(
    "Explora los **675 exoplanetas** del catálogo en un mapa 3D interactivo. "
    "Puedes rotar, hacer zoom y buscar cualquier planeta por su nombre."
)

# ── Advertencia ética ────────────────────────────────────────────────────────
st.warning(
    "⚠️ **Nota metodológica:** Las familias descubiertas son agrupaciones estadísticas, no "
    "categorías taxonómicas oficiales. Representan patrones matemáticos encontrados en los datos "
    "y deben interpretarse como hipótesis de trabajo, no como clasificaciones astronómicas definitivas.",
    icon="⚠️",
)

# ── Guía de uso ───────────────────────────────────────────────────────────────
with st.expander("ℹ️ ¿Qué estoy viendo aquí?", expanded=False):
    st.markdown("""
    Este mapa utiliza las **3 primeras componentes principales (PC1, PC2, PC3)** como ejes espaciales.
    Cada punto es un exoplaneta, coloreado por su familia:

    | Color | Familia | Planetas |
    |:---:|:---|---:|
    | 🔴 | Gigantes Gaseosos | 74 |
    | 🔵 | Sub-Neptunos | 260 |
    | ⭐ | Anomalía Extrema | 1 |
    | 🟢 | Rocosos / Super-Tierras | 340 |

    **Importante:** Los ejes **no son coordenadas astronómicas reales** (RA/Dec/distancia).
    Son una proyección matemática del espacio de características usada para el clustering.

    | Eje | Interpretación | Varianza |
    |:---|:---|---:|
    | PC1 | Escala orbital (`pl_orbsmax`, `pl_orbper`) | 44.0% |
    | PC2 | Gradiente térmico-estelar (`st_logg`, `st_rad`) | 30.2% |
    | PC3 | Excentricidad orbital (`pl_orbeccen`) | 9.6% |
    """)

# ── Carga de datos ───────────────────────────────────────────────────────────
df = load_data()

if df.empty:
    st.warning(st.session_state.get("data_status", "No hay datos disponibles."))
    st.stop()

planet_names = get_planet_names(df)

if "galaxy_selected_planet" not in st.session_state:
    st.session_state["galaxy_selected_planet"] = None

# ── Mapa 3D primero (sin selección) ──────────────────────────────────────────
st.markdown("### 🗺️ Mapa 3D del espacio PCA")
st.caption(
    "Rota el mapa arrastrando · Zoom con la rueda · Pasa el ratón sobre un punto para ver el nombre del planeta."
)

# Renderizar el mapa antes del buscador
selected = st.session_state["galaxy_selected_planet"]

if selected:
    col_map, col_info = st.columns([3, 1])

    with col_info:
        st.markdown("#### Planeta seleccionado")
        st.metric("🪐", selected)
        row = df[df["planet_name"] == selected]
        if not row.empty:
            if "family_label" in df.columns:
                st.write(f"**Familia:** {row['family_label'].values[0]}")
            if "cluster_label" in df.columns:
                cluster_val = int(row['cluster_label'].values[0])
                FAMILY_NAMES = {0: "🔴 Gigante Gaseoso", 1: "🔵 Sub-Neptuno",
                                2: "⭐ Anomalía", 3: "🟢 Rocoso / Super-Tierra"}
                st.write(f"**Tipo:** {FAMILY_NAMES.get(cluster_val, str(cluster_val))}")
            st.write(f"**PC1:** {row['PC1'].values[0]:.3f}")
            st.write(f"**PC2:** {row['PC2'].values[0]:.3f}")
            st.write(f"**PC3:** {row['PC3'].values[0]:.3f}")
        if st.button("✖️ Limpiar selección"):
            st.session_state["galaxy_selected_planet"] = None
            st.rerun()

    with col_map:
        st.plotly_chart(create_galaxy_view(df, highlighted_planet=selected), use_container_width=True)
else:
    st.plotly_chart(create_galaxy_view(df), use_container_width=True)

# ── Buscador con sugerencias (después del mapa) ───────────────────────────────
st.markdown("---")
st.markdown("### 🔎 Buscar y ubicar un exoplaneta")
st.caption("Escribe el nombre del planeta para obtener sugerencias. Al hacer clic en uno, se destacará en el mapa (recarga la página).")

search_term = st.text_input(
    "Nombre del planeta",
    placeholder="Ej: Kepler-22 b, 51 Peg b, TRAPPIST-1 b...",
    key="galaxy_search_input",
    label_visibility="collapsed",
)

if search_term:
    matches = [name for name in planet_names if search_term.lower() in name.lower()][:8]

    if matches:
        st.caption(f"{len(matches)} coincidencia(s) — haz clic para ubicarlo en el mapa:")
        cols = st.columns(min(len(matches), 4))
        for col, name in zip(cols, matches):
            if col.button(name, use_container_width=True, key=f"suggestion_{name}"):
                st.session_state["galaxy_selected_planet"] = name
                st.rerun()
    else:
        st.info("No se encontraron planetas con ese nombre.")
