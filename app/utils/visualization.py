import plotly.express as px
import pandas as pd


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