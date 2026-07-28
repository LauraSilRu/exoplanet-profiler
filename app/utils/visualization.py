import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_cluster_scatter_plot(df: pd.DataFrame):
    """Genera un gráfico de dispersión para los clusters usando PC1 y PC2."""
    if df.empty:
        return px.scatter(title="No hay datos disponibles")

    color_by = "cluster_label" if "cluster_label" in df.columns else None
    hover_data = ["planet_name"] if "planet_name" in df.columns else None
    title = "Distribución de Exoplanetas por Componentes Principales"
    if color_by:
        title += " y Familia"

    fig = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color=color_by,
        title=title,
        labels={
            "PC1": "Componente Principal 1",
            "PC2": "Componente Principal 2",
        },
        hover_data=hover_data,
    )
    fig.update_layout(legend_title_text="Familia")
    return fig

# -----------------------------------------------------------------------
# AGREGAR ESTO A app/utils/visualization.py
# Requiere agregar este import arriba junto a los otros:
#   import plotly.graph_objects as go
# (no reemplaza nada de lo que ya tenés, solo se agrega)
# -----------------------------------------------------------------------

def create_galaxy_view(df: pd.DataFrame, highlighted_planet: str | None = None):
    """Mapa 3D de exoplanetas usando PC1, PC2, PC3 como coordenadas espaciales.

    IMPORTANTE: esto NO son coordenadas astronómicas reales (no tenemos RA/Dec/
    distancia en el dataset). Es una proyección del espacio de las 3 primeras
    componentes principales usado para el clustering, presentada con estética
    de campo estelar. Se aclara explícitamente en el título del gráfico para
    no inducir a error al usuario final.
    """
    required_cols = {"PC1", "PC2", "PC3"}
    if df.empty or not required_cols.issubset(df.columns):
        fig = go.Figure()
        fig.update_layout(title="No hay datos suficientes para el mapa galáctico")
        return fig

    color_col = None
    for candidate in ("family_label", "cluster_label"):
        if candidate in df.columns:
            color_col = candidate
            break

    fig = go.Figure()

    if color_col:
        for label, group in df.groupby(color_col):
            fig.add_trace(
                go.Scatter3d(
                    x=group["PC1"],
                    y=group["PC2"],
                    z=group["PC3"],
                    mode="markers",
                    name=str(label),
                    marker=dict(size=3, opacity=0.6),
                    text=group.get("planet_name", ""),
                    hovertemplate="<b>%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>PC3: %{z:.2f}<extra></extra>",
                )
            )
    else:
        fig.add_trace(
            go.Scatter3d(
                x=df["PC1"],
                y=df["PC2"],
                z=df["PC3"],
                mode="markers",
                name="Exoplanetas",
                marker=dict(size=3, opacity=0.6, color="lightblue"),
                text=df.get("planet_name", ""),
                hovertemplate="<b>%{text}</b><extra></extra>",
            )
        )

    if highlighted_planet and "planet_name" in df.columns:
        row = df[df["planet_name"] == highlighted_planet]
        if not row.empty:
            fig.add_trace(
                go.Scatter3d(
                    x=row["PC1"],
                    y=row["PC2"],
                    z=row["PC3"],
                    mode="markers+text",
                    name="Seleccionado",
                    marker=dict(size=10, color="gold", symbol="diamond",
                                line=dict(width=2, color="white")),
                    text=row["planet_name"],
                    textposition="top center",
                    textfont=dict(color="white", size=13),
                )
            )

    fig.update_layout(
        title="Mapa Galáctico de Exoplanetas (espacio PCA — PC1/PC2/PC3, no coordenadas reales)",
        scene=dict(
            xaxis=dict(title="PC1", backgroundcolor="black",
                       gridcolor="rgba(255,255,255,0.15)", color="white"),
            yaxis=dict(title="PC2", backgroundcolor="black",
                       gridcolor="rgba(255,255,255,0.15)", color="white"),
            zaxis=dict(title="PC3", backgroundcolor="black",
                       gridcolor="rgba(255,255,255,0.15)", color="white"),
            bgcolor="black",
        ),
        paper_bgcolor="black",
        font=dict(color="white"),
        legend=dict(font=dict(color="white")),
        margin=dict(l=0, r=0, t=40, b=0),
        height=650,
    )
    return fig