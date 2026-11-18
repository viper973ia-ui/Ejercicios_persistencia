"""
app.py
======
Dashboard de Rendimiento Académico — aplicación Streamlit.

Ejecución
---------
    streamlit run app.py

Estructura del proyecto
-----------------------
    app.py          Interfaz: filtros, tarjetas KPI, pestañas y tablas.
    repository.py   Carga de datos, limpieza, filtros y todos los cálculos.
    charts.py       Gráficos de Plotly.
    Alumnos.csv     Catálogo de alumnos (id, nombre, edad, curso, grupo).
    Notas.csv       Calificaciones (id_nota, id_alumno, asignatura, evaluación, nota).

La aplicación no calcula nada por su cuenta: pide los datos a ``repository``
y los dibujos a ``charts``.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

import charts
import repository_dashboard as repo

# --------------------------------------------------------------------------- #
# Configuración de la página
# --------------------------------------------------------------------------- #

st.set_page_config(
    page_title="Dashboard de rendimiento académico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ESTILOS = """
<style>
    .block-container {padding-top: 2.2rem; padding-bottom: 2rem; max-width: 1500px;}
    h1, h2, h3 {font-family: Inter, "Segoe UI", Roboto, sans-serif; color: #111827;}
    h1 {font-size: 2.1rem !important; font-weight: 700 !important; margin-bottom: .2rem;}
    h2 {font-size: 1.45rem !important; font-weight: 600 !important; margin-top: 1.6rem;}
    h3 {font-size: 1.15rem !important; font-weight: 600 !important;}
    [data-testid="stMetricLabel"] p {font-size: .85rem !important; color: #4b5563;}
    [data-testid="stMetricValue"] {font-size: 1.9rem !important; color: #111827;}
    [data-testid="stSidebar"] {background-color: #fafafa; border-right: 1px solid #e5e7eb;}
    [data-testid="stSidebar"] h2 {font-size: 1.3rem !important; margin-top: .4rem;}
    div[data-testid="stDataFrame"] {border: 1px solid #e5e7eb; border-radius: 8px;}
    .subtitulo {color: #6b7280; font-size: .95rem; margin-bottom: 1.2rem;}
    .pie {color: #9ca3af; font-size: .8rem; margin-top: 2.5rem;
          border-top: 1px solid #e5e7eb; padding-top: .8rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 1.6rem;}
    .stTabs [data-baseweb="tab"] {font-size: .95rem; padding-left: 0; padding-right: 0;}
</style>
"""
st.markdown(ESTILOS, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Carga de datos (cacheada)
# --------------------------------------------------------------------------- #

@st.cache_data(show_spinner="Cargando datos académicos…")
def cargar(archivo_alumnos: bytes | None, archivo_notas: bytes | None):
    """Carga los CSV (por defecto los del proyecto) y construye el dataset."""
    from io import BytesIO

    alumnos_origen = BytesIO(archivo_alumnos) if archivo_alumnos else None
    notas_origen = BytesIO(archivo_notas) if archivo_notas else None
    return repo.cargar_datos(alumnos_origen, notas_origen)


# --------------------------------------------------------------------------- #
# Barra lateral: filtros y descargas
# --------------------------------------------------------------------------- #

with st.sidebar:
    st.markdown("## Filtros")

    with st.expander("Cargar otros ficheros CSV", expanded=False):
        subida_alumnos = st.file_uploader("Alumnos.csv", type="csv", key="up_alumnos")
        subida_notas = st.file_uploader("Notas.csv", type="csv", key="up_notas")
        st.caption(
            "Si no subes nada se usan los CSV incluidos en la carpeta del proyecto."
        )

bytes_alumnos = subida_alumnos.getvalue() if subida_alumnos else None
bytes_notas = subida_notas.getvalue() if subida_notas else None

try:
    alumnos, notas, datos = cargar(bytes_alumnos, bytes_notas)
except Exception as error:  # pragma: no cover - error de fichero corrupto
    st.error(f"No se han podido leer los datos: {error}")
    st.stop()

opciones = repo.obtener_opciones(datos)

with st.sidebar:
    curso = st.selectbox("Curso", [repo.TODOS, *opciones["curso"]], index=0)
    asignatura = st.selectbox(
        "Asignatura", [repo.TODOS, *opciones["asignatura"]], index=0
    )
    grupo = st.selectbox("Grupo", [repo.TODOS, *opciones["grupo"]], index=0)
    evaluacion = st.selectbox(
        "Evaluación", [repo.TODOS, *opciones["evaluacion"]], index=0
    )

    st.divider()
    st.caption(
        f"**{len(datos)}** calificaciones · **{datos['id_alumno'].nunique()}** alumnos · "
        f"**{datos['asignatura'].nunique()}** asignaturas"
    )

filtrado = repo.aplicar_filtros(datos, curso, asignatura, grupo, evaluacion)

with st.sidebar:
    st.download_button(
        "⬇️ Descargar datos filtrados (CSV)",
        data=repo.exportar_csv(filtrado),
        file_name="datos_filtrados.csv",
        mime="text/csv",
        width="stretch",
        disabled=filtrado.empty,
    )


# --------------------------------------------------------------------------- #
# Cabecera y KPIs
# --------------------------------------------------------------------------- #

st.markdown("# 📊 Dashboard de rendimiento académico")
st.markdown(
    '<div class="subtitulo">Análisis de calificaciones por asignatura, evaluación, '
    "curso y grupo.</div>",
    unsafe_allow_html=True,
)

if filtrado.empty:
    st.warning(
        "No hay calificaciones que cumplan los filtros seleccionados. "
        "Prueba a ampliar la selección."
    )
    st.stop()

kpis = repo.calcular_kpis(filtrado)

columnas_kpi = st.columns(5)
columnas_kpi[0].metric("Alumnos evaluados", f"{kpis['alumnos_evaluados']}")
columnas_kpi[1].metric("Nota media", repo.formatear_nota(kpis["nota_media"]))
columnas_kpi[2].metric("Nota máxima", repo.formatear_nota(kpis["nota_maxima"]))
columnas_kpi[3].metric("Nota mínima", repo.formatear_nota(kpis["nota_minima"]))
columnas_kpi[4].metric(
    "Aprobados", repo.formatear_porcentaje(kpis["porcentaje_aprobados"])
)

st.write("")

# Tablas calculadas una sola vez
tabla_asignaturas = repo.estadisticas_por_asignatura(filtrado)
tabla_alumnos = repo.rendimiento_por_alumno(filtrado)
tabla_evolucion = repo.evolucion_por_evaluacion(filtrado)
tabla_evolucion_asignatura = repo.evolucion_por_asignatura(filtrado)
tabla_grupos = repo.estadisticas_por_grupo(filtrado)
tabla_cursos = repo.estadisticas_por_curso(filtrado)

pestana_asignaturas, pestana_evolucion, pestana_distribucion = st.tabs(
    ["Notas por asignatura", "Evolución de evaluaciones", "Distribución de notas"]
)


# --------------------------------------------------------------------------- #
# Pestaña 1 — Notas por asignatura
# --------------------------------------------------------------------------- #

with pestana_asignaturas:
    st.markdown("## Estadísticas por asignatura")
    st.dataframe(
        repo.preparar_tabla_para_mostrar(tabla_asignaturas),
        width="stretch",
        hide_index=True,
        column_config={
            "asignatura": st.column_config.TextColumn("asignatura", width="medium"),
            "alumnos_evaluados": st.column_config.NumberColumn(
                "alumnos_evaluados", format="%d"
            ),
            "nota_media": st.column_config.NumberColumn("nota_media", format="%.2f"),
            "nota_maxima": st.column_config.NumberColumn("nota_maxima", format="%.2f"),
            "nota_minima": st.column_config.NumberColumn("nota_minima", format="%.2f"),
            "porcentaje_aprobados": st.column_config.NumberColumn(
                "porcentaje_aprobados", format="%.2f"
            ),
        },
    )

    st.plotly_chart(
        charts.grafico_nota_media_por_asignatura(tabla_asignaturas),
        width="stretch",
        config={"displayModeBar": False},
    )

    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        st.plotly_chart(
            charts.grafico_aprobados_por_asignatura(tabla_asignaturas),
            width="stretch",
            config={"displayModeBar": False},
        )
    with columna_derecha:
        st.plotly_chart(
            charts.grafico_por_grupo(tabla_grupos),
            width="stretch",
            config={"displayModeBar": False},
        )

    st.markdown("## Rendimiento por alumno")
    st.dataframe(
        repo.preparar_tabla_para_mostrar(tabla_alumnos),
        width="stretch",
        hide_index=True,
        column_config={
            "id_alumno": st.column_config.NumberColumn("id_alumno", format="%d"),
            "nombre": st.column_config.TextColumn("nombre", width="medium"),
            "curso": st.column_config.TextColumn("curso"),
            "grupo": st.column_config.TextColumn("grupo"),
            "nota_media": st.column_config.NumberColumn("nota_media", format="%.2f"),
            "asignaturas_evaluadas": st.column_config.NumberColumn(
                "asignaturas_evaluadas", format="%d"
            ),
            "asignaturas_aprobadas": st.column_config.NumberColumn(
                "asignaturas_aprobadas", format="%d"
            ),
        },
    )

    columna_izquierda, columna_derecha = st.columns([3, 2])
    with columna_izquierda:
        st.plotly_chart(
            charts.grafico_ranking_alumnos(tabla_alumnos),
            width="stretch",
            config={"displayModeBar": False},
        )
    with columna_derecha:
        st.plotly_chart(
            charts.grafico_por_curso(tabla_cursos),
            width="stretch",
            config={"displayModeBar": False},
        )


# --------------------------------------------------------------------------- #
# Pestaña 2 — Evolución de evaluaciones
# --------------------------------------------------------------------------- #

with pestana_evolucion:
    st.markdown("## Evolución de las evaluaciones")

    if len(tabla_evolucion) < 2:
        st.info(
            "Selecciona más de una evaluación en el filtro lateral para comparar "
            "la evolución entre convocatorias."
        )

    st.plotly_chart(
        charts.grafico_evolucion_global(tabla_evolucion),
        width="stretch",
        config={"displayModeBar": False},
    )

    st.plotly_chart(
        charts.grafico_evolucion_por_asignatura(tabla_evolucion_asignatura),
        width="stretch",
        config={"displayModeBar": False},
    )

    columna_izquierda, columna_derecha = st.columns(2)
    with columna_izquierda:
        st.plotly_chart(
            charts.grafico_aprobados_por_evaluacion(tabla_evolucion),
            width="stretch",
            config={"displayModeBar": False},
        )
    with columna_derecha:
        st.markdown("### Detalle por evaluación")
        st.dataframe(
            repo.preparar_tabla_para_mostrar(tabla_evolucion),
            width="stretch",
            hide_index=True,
            column_config={
                "evaluacion": st.column_config.NumberColumn("evaluacion", format="%d"),
                "nota_media": st.column_config.NumberColumn(
                    "nota_media", format="%.2f"
                ),
                "nota_maxima": st.column_config.NumberColumn(
                    "nota_maxima", format="%.2f"
                ),
                "nota_minima": st.column_config.NumberColumn(
                    "nota_minima", format="%.2f"
                ),
                "porcentaje_aprobados": st.column_config.NumberColumn(
                    "porcentaje_aprobados", format="%.2f"
                ),
                "num_notas": st.column_config.NumberColumn("num_notas", format="%d"),
            },
        )


# --------------------------------------------------------------------------- #
# Pestaña 3 — Distribución de notas
# --------------------------------------------------------------------------- #

with pestana_distribucion:
    st.markdown("## Distribución de notas")

    resumen = repo.resumen_distribucion(filtrado)
    columnas_resumen = st.columns(5)
    columnas_resumen[0].metric("Media", repo.formatear_nota(resumen["media"]))
    columnas_resumen[1].metric("Mediana", repo.formatear_nota(resumen["mediana"]))
    columnas_resumen[2].metric("Desviación típica", repo.formatear_nota(resumen["desviacion"]))
    columnas_resumen[3].metric("Percentil 25", repo.formatear_nota(resumen["p25"]))
    columnas_resumen[4].metric("Percentil 75", repo.formatear_nota(resumen["p75"]))

    st.write("")

    columna_izquierda, columna_derecha = st.columns([3, 2])
    with columna_izquierda:
        st.plotly_chart(
            charts.grafico_distribucion(filtrado),
            width="stretch",
            config={"displayModeBar": False},
        )
    with columna_derecha:
        st.plotly_chart(
            charts.grafico_estado(filtrado),
            width="stretch",
            config={"displayModeBar": False},
        )

    st.plotly_chart(
        charts.grafico_boxplot(filtrado),
        width="stretch",
        config={"displayModeBar": False},
    )

    columna_izquierda, columna_derecha = st.columns([2, 3])
    with columna_izquierda:
        st.markdown("### Notas por intervalo")
        st.dataframe(
            repo.tabla_distribucion(filtrado),
            width="stretch",
            hide_index=True,
            column_config={
                "desde": st.column_config.NumberColumn("desde", format="%.1f"),
                "hasta": st.column_config.NumberColumn("hasta", format="%.1f"),
                "num_notas": st.column_config.NumberColumn("num_notas", format="%d"),
                "porcentaje": st.column_config.NumberColumn(
                    "porcentaje", format="%.2f"
                ),
            },
        )
    with columna_derecha:
        st.plotly_chart(
            charts.grafico_edad_nota(tabla_alumnos.merge(
                alumnos[["id_alumno", "edad"]], on="id_alumno", how="left"
            )),
            width="stretch",
            config={"displayModeBar": False},
        )


# --------------------------------------------------------------------------- #
# Pie de página
# --------------------------------------------------------------------------- #

st.markdown(
    f'<div class="pie">Fuente: <code>Alumnos.csv</code> y <code>Notas.csv</code> · '
    f"{len(filtrado)} calificaciones mostradas de {len(datos)} · "
    "Nota de aprobado: 5,0 · Escala 0-10</div>",
    unsafe_allow_html=True,
)
