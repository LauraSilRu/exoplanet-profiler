import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Perfil de Exoplaneta", page_icon="🪐", layout="wide")

# ── Cabecera ─────────────────────────────────────────────────────────────────
st.title("🪐 Perfil de Exoplaneta")
st.markdown(
    "Selecciona cualquier exoplaneta del catálogo para ver a qué **familia de mundos** pertenece "
    "y su posición en el espacio de componentes principales."
)

# ── Advertencia ética ────────────────────────────────────────────────────────
st.warning(
    "⚠️ **Nota metodológica:** Las familias descubiertas son agrupaciones estadísticas, no "
    "categorías taxonómicas oficiales. Representan patrones matemáticos encontrados en los datos "
    "y deben interpretarse como hipótesis de trabajo, no como clasificaciones astronómicas definitivas.",
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

if "planet_name" not in df.columns:
    st.error("No se encontró la columna de identificador del planeta en los datos cargados.")
    st.stop()

# ── Información de familias ───────────────────────────────────────────────────
FAMILY_INFO = {
    0: ("🔴 Gigante Gaseoso",      "#FF6F61",
        "Planetas de gran masa y radio. Orbitan generalmente a distancias amplias de su estrella. "
        "PC1 elevado refleja su gran escala orbital."),
    1: ("🔵 Sub-Neptuno / Neptuno Frío", "#4FC3F7",
        "Planetas de tamaño intermedio, más fríos, con órbitas cortas a medias. "
        "PC2 negativo indica estrellas más compactas y frías."),
    2: ("⭐ Anomalía Extrema",     "#F0C75E",
        "Un único planeta con valores extremos en escala orbital y gradiente térmico. "
        "Sus coordenadas PCA lo alejan significativamente del resto del catálogo."),
    3: ("🟢 Rocoso / Super-Tierra", "#66BB6A",
        "La familia más abundante (50.4%). Planetas compactos, de menor radio y masa, "
        "con órbitas cortas alrededor de estrellas enanas. PC1 bajo y PC2 positivo."),
}

PC_EXPLANATIONS = {
    "PC1": ("Escala orbital", "44.0%",
            "Captura principalmente el semieje mayor (`pl_orbsmax`, loading 0.81) y el período orbital "
            "(`pl_orbper`, loading 0.38). Un valor alto indica planeta muy alejado de su estrella."),
    "PC2": ("Gradiente térmico-estelar", "30.2%",
            "Captura la gravedad superficial estelar (`st_logg`, loading 0.45) y el radio estelar "
            "(`st_rad`, loading -0.41). Diferencia estrellas compactas/frías de las gigantes/calientes."),
    "PC3": ("Excentricidad orbital", "9.6%",
            "Dominada por `pl_orbeccen` (loading 0.95). Distingue planetas en órbitas muy elípticas "
            "de los que siguen trayectorias casi circulares."),
    "PC4": ("Metalicidad estelar", "6.4%",
            "Captura `st_met` (loading 0.81). Refleja la abundancia de elementos pesados en la estrella, "
            "lo que influye en la composición de sus planetas."),
}

# ── Selector ─────────────────────────────────────────────────────────────────
st.markdown("---")
planet_name = st.selectbox(
    "🔍 Selecciona un Exoplaneta",
    options=sorted(df["planet_name"].dropna().tolist()),
    index=None,
    placeholder="Escribe o elige un planeta...",
)

# ── Tarjeta de perfil ────────────────────────────────────────────────────────
if planet_name:
    profile = df.loc[df["planet_name"] == planet_name].iloc[0].to_dict()
    cluster = int(profile.get("cluster_label", -1))
    family_name, family_color, family_desc = FAMILY_INFO.get(
        cluster, ("Familia desconocida", "#999999", "Sin descripción disponible.")
    )

    # Banner de familia
    st.markdown(f"""
    <div style="background:{family_color}22; border-left: 5px solid {family_color};
         padding: 18px 20px; border-radius: 10px; margin: 16px 0">
        <h2 style="color:{family_color}; margin:0 0 6px 0">{family_name}</h2>
        <p style="margin:0; color:#ccc; font-size:0.95em">{family_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas PCA
    st.markdown("### 📐 Coordenadas en el espacio PCA")
    st.caption(
        "Estas coordenadas no son posiciones astronómicas reales. Representan la posición del planeta "
        "en el espacio matemático reducido por PCA a partir de sus 12 características físicas y orbitales."
    )

    cols = st.columns(4)
    for col, (pc_key, (pc_name, pc_var, pc_desc)) in zip(cols, PC_EXPLANATIONS.items()):
        val = profile.get(pc_key, None)
        val_str = f"{val:.3f}" if val is not None else "N/D"
        col.metric(
            label=f"{pc_key} — {pc_name}",
            value=val_str,
            help=f"Varianza explicada: {pc_var}\n\n{pc_desc}"
        )

    # Guía de interpretación de PCA
    with st.expander("ℹ️ ¿Qué significan estas coordenadas?"):
        for pc_key, (pc_name, pc_var, pc_desc) in PC_EXPLANATIONS.items():
            st.markdown(f"**{pc_key} — {pc_name}** *(explica el {pc_var} de la varianza)*")
            st.markdown(f"> {pc_desc}")
            st.markdown("")
