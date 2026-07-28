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

# ── Cabecera ────────────────────────────────────────────────────────────────
st.title("🌌 ExoProfiler: Explorador de Familias de Exoplanetas")
st.markdown(
    "Descubrimiento inteligente de **4 familias de mundos** a partir de "
    "datos reales del NASA Exoplanet Archive, usando PCA + K-Means."
)

# ── Advertencia ética ───────────────────────────────────────────────────────
st.warning(
    "⚠️ **Nota metodológica:** Las familias descubiertas son agrupaciones "
    "estadísticas, no categorías taxonómicas oficiales. Representan patrones "
    "matemáticos encontrados en los datos y deben interpretarse como hipótesis "
    "de trabajo, no como clasificaciones astronómicas definitivas.",
    icon="⚠️",
)

# ── Guía de uso ─────────────────────────────────────────────────────────────
with st.expander("📖 ¿Cómo usar esta app?", expanded=False):
    st.markdown("""
    Esta aplicación te permite explorar los **675 exoplanetas** analizados por el modelo de clustering.
    Usa el menú de la izquierda para navegar entre las tres secciones:

    | Sección | ¿Qué encontrarás? |
    |:---|:---|
    | 🪐 **Perfil de Exoplaneta** | Consulta la familia y coordenadas PCA de cualquier planeta por su nombre |
    | 🛰️ **Mundos Similares** | Encuentra todos los planetas que pertenecen a la misma familia que el tuyo |
    | 🌌 **Galaxia Exoplanetaria** | Mapa 3D interactivo del espacio PCA — busca y ubica cualquier planeta |

    **En esta página** puedes ver la distribución global de todas las familias en el plano PC1-PC2,
    y filtrarlas desde el panel lateral.
    """)

# ── Carga de datos ──────────────────────────────────────────────────────────
with st.spinner("Cargando datos de clustering..."):
    df = load_data()

if df.empty:
    st.warning("No hay datos de clustering disponibles todavía.")
    st.info("Asegúrate de haber generado el archivo data/processed/clustered_exoplanets.csv desde el notebook de análisis.")
    st.stop()

st.success(st.session_state.get("data_status", "Datos cargados."))

# ── Nombres de familias ──────────────────────────────────────────────────────
FAMILY_NAMES = {
    0: "🔴 Gigantes Gaseosos",
    1: "🔵 Sub-Neptunos",
    2: "⭐ Anomalía Extrema",
    3: "🟢 Rocosos / Super-Tierras",
}

# ── Sidebar con nombres reales ───────────────────────────────────────────────
st.sidebar.header("Filtros")
if "cluster_label" in df.columns:
    df["familia_nombre"] = df["cluster_label"].map(FAMILY_NAMES).fillna("Desconocido")
    all_families = [FAMILY_NAMES[k] for k in sorted(FAMILY_NAMES.keys()) if k in df["cluster_label"].unique()]
    selected_families = st.sidebar.multiselect("Familias a mostrar", all_families, default=all_families)
    if selected_families:
        df = df[df["familia_nombre"].isin(selected_families)]

# ── Métricas ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("🪐 Planetas mostrados", len(df))
col2.metric("🏷️ Familias activas", df["cluster_label"].nunique() if "cluster_label" in df.columns else "N/D")
col3.metric("📡 Fuente de datos", "NASA Exoplanet Archive")

# ── Gráfico principal ────────────────────────────────────────────────────────
st.markdown("### Distribución de Familias en el espacio PCA")
st.caption(
    "Cada punto es un exoplaneta. Los ejes representan las dos primeras componentes principales: "
    "**PC1 (escala orbital, 44%)** en horizontal y **PC2 (gradiente térmico-estelar, 30.2%)** en vertical. "
    "Juntos capturan el **74.2% de la varianza** del dataset."
)
fig = create_cluster_scatter_plot(df)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Ver tabla de datos"):
    st.dataframe(
        df[[c for c in ["planet_name", "cluster_label", "family_label", "PC1", "PC2", "PC3", "PC4"] if c in df.columns]].head(200)
    )