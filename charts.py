"""
charts.py
=========
Gráficos del Dashboard de Rendimiento Académico.

Todas las funciones reciben tablas ya calculadas por ``repository.py`` y
devuelven figuras de Plotly listas para ``st.plotly_chart``. Ninguna función
lee ficheros ni hace cálculos de negocio: solo dibujan.

Dependencias: plotly, pandas, numpy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --------------------------------------------------------------------------- #
# Paleta y estilo común
# --------------------------------------------------------------------------- #

AZUL: str = "#1f77b4"
AZUL_OSCURO: str = "#14507e"
AZUL_CLARO: str = "#7fb2d9"
VERDE: str = "#2e8b57"
ROJO: str = "#c0392b"
NARANJA: str = "#e08a1e"
GRIS: str = "#6b7280"
GRIS_CLARO: str = "#e5e7eb"

PALETA: list[str] = [
    AZUL,
    NARANJA,
    VERDE,
    ROJO,
    "#8e44ad",
    "#16a085",
    AZUL_CLARO,
    GRIS,
]

FUENTE: str = "Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
ALTURA_PREDETERMINADA: int = 420


def aplicar_estilo(
    figura: go.Figure,
    titulo: str = "",
    altura: int = ALTURA_PREDETERMINADA,
    y_titulo: str = "",
    x_titulo: str = "",
    rango_y: tuple[float, float] | None = None,
    mostrar_leyenda: bool = False,
) -> go.Figure:
    """Aplica el estilo visual común (tipografía, rejilla suave, márgenes)."""
    figura.update_layout(
        title=dict(
            text=titulo,
            x=0.5,
            xanchor="center",
            font=dict(size=20, color="#111827", family=FUENTE),
        ),
        height=altura,
        margin=dict(l=60, r=30, t=70, b=60),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family=FUENTE, size=13, color="#374151"),
        showlegend=mostrar_leyenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family=FUENTE),
    )
    figura.update_xaxes(
        title_text=x_titulo,
        showgrid=False,
        linecolor="#9ca3af",
        ticks="outside",
        tickcolor="#9ca3af",
    )
    figura.update_yaxes(
        title_text=y_titulo,
        showgrid=True,
        gridcolor=GRIS_CLARO,
        zeroline=False,
        linecolor="#9ca3af",
        ticks="outside",
        tickcolor="#9ca3af",
    )
    if rango_y is not None:
        figura.update_yaxes(range=list(rango_y))
    return figura


# --------------------------------------------------------------------------- #
# 1. Nota media por asignatura (gráfico principal)
# --------------------------------------------------------------------------- #

def grafico_nota_media_por_asignatura(tabla: pd.DataFrame) -> go.Figure:
    """Barras con la nota media de cada asignatura, escala fija 0-10.

    Parameters
    ----------
    tabla:
        Salida de ``repository.estadisticas_por_asignatura``.
    """
    figura = go.Figure()

    if tabla.empty:
        return aplicar_estilo(figura, "Nota media por asignatura", rango_y=(0, 10))

    figura.add_bar(
        x=tabla["asignatura"],
        y=tabla["nota_media"],
        marker_color=AZUL,
        marker_line_color=AZUL_OSCURO,
        marker_line_width=0.8,
        width=0.55,
        text=[f"{v:.2f}" for v in tabla["nota_media"]],
        textposition="outside",
        textfont=dict(size=13, color="#111827"),
        customdata=np.stack(
            [
                tabla["alumnos_evaluados"],
                tabla["nota_maxima"],
                tabla["porcentaje_aprobados"],
            ],
            axis=-1,
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Nota media: %{y:.2f}<br>"
            "Alumnos evaluados: %{customdata[0]}<br>"
            "Nota máxima: %{customdata[1]:.2f}<br>"
            "Aprobados: %{customdata[2]:.2f}%<extra></extra>"
        ),
    )

    return aplicar_estilo(
        figura,
        titulo="Nota media por asignatura",
        y_titulo="Nota media",
        rango_y=(0, 10),
        altura=460,
    )


# --------------------------------------------------------------------------- #
# 2. Evolución de las evaluaciones
# --------------------------------------------------------------------------- #

def grafico_evolucion_global(evolucion: pd.DataFrame) -> go.Figure:
    """Línea con la nota media global de cada evaluación."""
    figura = go.Figure()

    if evolucion.empty:
        return aplicar_estilo(figura, "Evolución de la nota media", rango_y=(0, 10))

    figura.add_trace(
        go.Scatter(
            x=evolucion["evaluacion"],
            y=evolucion["nota_media"],
            mode="lines+markers+text",
            name="Nota media",
            line=dict(color=AZUL, width=3),
            marker=dict(size=11, color=AZUL, line=dict(color="white", width=2)),
            text=[f"{v:.2f}" for v in evolucion["nota_media"]],
            textposition="top center",
            textfont=dict(size=12, color="#111827"),
            hovertemplate=(
                "Evaluación %{x}<br>"
                "Nota media: %{y:.2f}<extra></extra>"
            ),
        )
    )

    figura.update_xaxes(dtick=1, tickformat="d")

    return aplicar_estilo(
        figura,
        titulo="Evolución de la nota media por evaluación",
        x_titulo="Evaluación",
        y_titulo="Nota media",
        rango_y=(0, 10),
    )


def grafico_evolucion_por_asignatura(evolucion: pd.DataFrame) -> go.Figure:
    """Una línea por asignatura con su nota media en cada evaluación."""
    figura = go.Figure()

    if evolucion.empty:
        return aplicar_estilo(
            figura, "Evolución por asignatura", rango_y=(0, 10), mostrar_leyenda=True
        )

    for indice, (asignatura, grupo) in enumerate(
        evolucion.groupby("asignatura", sort=True)
    ):
        grupo = grupo.sort_values("evaluacion")
        color = PALETA[indice % len(PALETA)]
        figura.add_trace(
            go.Scatter(
                x=grupo["evaluacion"],
                y=grupo["nota_media"],
                mode="lines+markers",
                name=str(asignatura),
                line=dict(color=color, width=2.5),
                marker=dict(size=9, color=color, line=dict(color="white", width=1.5)),
                hovertemplate=(
                    f"<b>{asignatura}</b><br>"
                    "Evaluación %{x}<br>"
                    "Nota media: %{y:.2f}<extra></extra>"
                ),
            )
        )

    figura.update_xaxes(dtick=1, tickformat="d")

    return aplicar_estilo(
        figura,
        titulo="Evolución de la nota media por asignatura",
        x_titulo="Evaluación",
        y_titulo="Nota media",
        rango_y=(0, 10),
        mostrar_leyenda=True,
    )


def grafico_aprobados_por_evaluacion(evolucion: pd.DataFrame) -> go.Figure:
    """Barras con el porcentaje de aprobados en cada evaluación."""
    figura = go.Figure()

    if evolucion.empty:
        return aplicar_estilo(figura, "Aprobados por evaluación", rango_y=(0, 105))

    figura.add_bar(
        x=evolucion["evaluacion"],
        y=evolucion["porcentaje_aprobados"],
        marker_color=VERDE,
        width=0.5,
        text=[f"{v:.1f}%" for v in evolucion["porcentaje_aprobados"]],
        textposition="outside",
        hovertemplate="Evaluación %{x}<br>Aprobados: %{y:.2f}%<extra></extra>",
    )
    figura.update_xaxes(dtick=1, tickformat="d")

    return aplicar_estilo(
        figura,
        titulo="Porcentaje de aprobados por evaluación",
        x_titulo="Evaluación",
        y_titulo="% aprobados",
        rango_y=(0, 105),
    )


# --------------------------------------------------------------------------- #
# 3. Distribución de notas
# --------------------------------------------------------------------------- #

def grafico_distribucion(datos: pd.DataFrame, intervalos: int = 10) -> go.Figure:
    """Histograma de todas las notas, con la línea de aprobado marcada."""
    figura = go.Figure()

    if datos.empty:
        return aplicar_estilo(figura, "Distribución de notas")

    figura.add_trace(
        go.Histogram(
            x=datos["nota"],
            xbins=dict(start=0, end=10, size=10 / intervalos),
            marker_color=AZUL,
            marker_line_color="white",
            marker_line_width=1,
            hovertemplate="Nota %{x}<br>Frecuencia: %{y}<extra></extra>",
        )
    )

    figura.add_vline(
        x=5,
        line_dash="dash",
        line_color=ROJO,
        annotation_text="Aprobado (5)",
        annotation_position="top",
        annotation_font=dict(color=ROJO, size=12),
    )

    return aplicar_estilo(
        figura,
        titulo="Distribución de notas",
        x_titulo="Nota",
        y_titulo="Número de calificaciones",
        rango_y=None,
    )


def grafico_boxplot(datos: pd.DataFrame) -> go.Figure:
    """Diagrama de caja de las notas por asignatura."""
    figura = go.Figure()

    if datos.empty:
        return aplicar_estilo(figura, "Distribución por asignatura", rango_y=(0, 10))

    for indice, (asignatura, grupo) in enumerate(
        datos.groupby("asignatura", sort=True)
    ):
        color = PALETA[indice % len(PALETA)]
        figura.add_trace(
            go.Box(
                y=grupo["nota"],
                name=str(asignatura),
                marker_color=color,
                line_color=color,
                boxpoints="all",
                jitter=0.35,
                pointpos=0,
                marker=dict(size=7, opacity=0.75),
                hovertemplate=(
                    f"<b>{asignatura}</b><br>Nota: %{{y:.2f}}<extra></extra>"
                ),
            )
        )

    return aplicar_estilo(
        figura,
        titulo="Distribución de notas por asignatura",
        y_titulo="Nota",
        rango_y=(0, 10),
        mostrar_leyenda=False,
    )


def grafico_estado(datos: pd.DataFrame) -> go.Figure:
    """Gráfico circular con el reparto de aprobados y suspensos."""
    figura = go.Figure()

    if datos.empty:
        return aplicar_estilo(figura, "Aprobados y suspensos")

    conteo = datos["aprobado"].value_counts()
    aprobados = int(conteo.get(True, 0))
    suspensos = int(conteo.get(False, 0))

    figura.add_trace(
        go.Pie(
            labels=["Aprobado", "Suspenso"],
            values=[aprobados, suspensos],
            hole=0.55,
            marker=dict(colors=[VERDE, ROJO], line=dict(color="white", width=2)),
            textinfo="label+percent",
            textfont=dict(size=13),
            hovertemplate="%{label}: %{value} notas (%{percent})<extra></extra>",
        )
    )

    figura.update_layout(
        annotations=[
            dict(
                text=f"{aprobados + suspensos}<br><span style='font-size:12px'>notas</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=20, color="#111827"),
            )
        ]
    )

    return aplicar_estilo(figura, "Aprobados y suspensos", altura=380)


# --------------------------------------------------------------------------- #
# 4. Comparativas por grupo, curso y alumnos
# --------------------------------------------------------------------------- #

def grafico_por_grupo(tabla: pd.DataFrame) -> go.Figure:
    """Barras con la nota media de cada grupo."""
    figura = go.Figure()

    if tabla.empty:
        return aplicar_estilo(figura, "Nota media por grupo", rango_y=(0, 10))

    figura.add_bar(
        x=tabla["grupo"],
        y=tabla["nota_media"],
        marker_color=AZUL_CLARO,
        marker_line_color=AZUL_OSCURO,
        marker_line_width=0.8,
        width=0.5,
        text=[f"{v:.2f}" for v in tabla["nota_media"]],
        textposition="outside",
        customdata=tabla["alumnos"],
        hovertemplate=(
            "<b>Grupo %{x}</b><br>"
            "Nota media: %{y:.2f}<br>"
            "Alumnos: %{customdata}<extra></extra>"
        ),
    )

    return aplicar_estilo(
        figura,
        titulo="Nota media por grupo",
        y_titulo="Nota media",
        rango_y=(0, 10),
        altura=380,
    )


def grafico_por_curso(tabla: pd.DataFrame) -> go.Figure:
    """Barras con la nota media de cada curso."""
    figura = go.Figure()

    if tabla.empty:
        return aplicar_estilo(figura, "Nota media por curso", rango_y=(0, 10))

    figura.add_bar(
        x=tabla["curso"],
        y=tabla["nota_media"],
        marker_color=NARANJA,
        width=0.5,
        text=[f"{v:.2f}" for v in tabla["nota_media"]],
        textposition="outside",
        customdata=tabla["alumnos"],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Nota media: %{y:.2f}<br>"
            "Alumnos: %{customdata}<extra></extra>"
        ),
    )

    return aplicar_estilo(
        figura,
        titulo="Nota media por curso",
        y_titulo="Nota media",
        rango_y=(0, 10),
        altura=380,
    )


def grafico_ranking_alumnos(tabla: pd.DataFrame, limite: int = 10) -> go.Figure:
    """Barras horizontales con los alumnos de mejor nota media."""
    figura = go.Figure()

    if tabla.empty:
        return aplicar_estilo(figura, "Ranking de alumnos", rango_y=(0, 10))

    datos = tabla.head(limite).sort_values("nota_media")
    colores = [
        VERDE if valor >= 7 else (NARANJA if valor >= 5 else ROJO)
        for valor in datos["nota_media"]
    ]

    figura.add_bar(
        x=datos["nota_media"],
        y=datos["nombre"],
        orientation="h",
        marker_color=colores,
        text=[f"{v:.2f}" for v in datos["nota_media"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Nota media: %{x:.2f}<extra></extra>",
    )

    figura.update_yaxes(showgrid=False)
    figura.update_xaxes(range=[0, 10], showgrid=True, gridcolor=GRIS_CLARO)

    return aplicar_estilo(
        figura,
        titulo="Ranking de alumnos por nota media",
        x_titulo="Nota media",
        altura=max(320, 40 * len(datos) + 120),
    )


def grafico_edad_nota(tabla: pd.DataFrame) -> go.Figure:
    """Dispersión edad del alumno frente a su nota media."""
    figura = go.Figure()

    if tabla.empty or "edad" not in tabla.columns:
        return aplicar_estilo(figura, "Edad y rendimiento", rango_y=(0, 10))

    datos = tabla.dropna(subset=["edad"])
    if datos.empty:
        return aplicar_estilo(figura, "Edad y rendimiento", rango_y=(0, 10))

    figura.add_trace(
        go.Scatter(
            x=datos["edad"],
            y=datos["nota_media"],
            mode="markers+text",
            text=datos["nombre"],
            textposition="top center",
            textfont=dict(size=10, color=GRIS),
            marker=dict(
                size=13,
                color=datos["nota_media"],
                colorscale=[[0, ROJO], [0.5, NARANJA], [1, VERDE]],
                cmin=0,
                cmax=10,
                line=dict(color="white", width=1.5),
                showscale=False,
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Edad: %{x}<br>"
                "Nota media: %{y:.2f}<extra></extra>"
            ),
        )
    )

    return aplicar_estilo(
        figura,
        titulo="Relación entre edad y nota media",
        x_titulo="Edad",
        y_titulo="Nota media",
        rango_y=(0, 10),
    )


def grafico_aprobados_por_asignatura(tabla: pd.DataFrame) -> go.Figure:
    """Barras con el porcentaje de aprobados de cada asignatura."""
    figura = go.Figure()

    if tabla.empty:
        return aplicar_estilo(figura, "% de aprobados por asignatura", rango_y=(0, 105))

    colores = [
        VERDE if valor >= 90 else (NARANJA if valor >= 75 else ROJO)
        for valor in tabla["porcentaje_aprobados"]
    ]

    figura.add_bar(
        x=tabla["asignatura"],
        y=tabla["porcentaje_aprobados"],
        marker_color=colores,
        width=0.55,
        text=[f"{v:.1f}%" for v in tabla["porcentaje_aprobados"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Aprobados: %{y:.2f}%<extra></extra>",
    )

    return aplicar_estilo(
        figura,
        titulo="Porcentaje de aprobados por asignatura",
        y_titulo="% aprobados",
        rango_y=(0, 118),
        altura=390,
    )
