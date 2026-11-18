"""
app.py
====
Dashboard de Rendimiento Académico — versión simplificada.

Ejecución
----
    streamlit run app.py

Estructura del proyecto
----
    app.py          Interfaz: filtros, tarjetas KPI, pestañas y tablas.
    repository.py   Carga de datos, limpieza, filtros y cálculos.
    charts.py       Gráficos de Plotly.
    Alumnos.csv     Catálogo de alumnos (id, nombre, edad, curso, grupo).
    Notas.csv       Calificaciones (id_nota, id_alumno, asignatura, evaluación, nota).
"""

import streamlit as st
import charts
import repository2 as repo

# ---- Configuración de la página ---- #

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


# ---- Carga de datos (cacheada) ---- #

@st.cache_data(show_spinner="Cargando datos académicos…")
def cargar():
    return repo.cargar_datos()


try:
    alumnos, notas, datos = cargar()
except Exception as error:
    st.error(f"No se han podido leer los datos: {error}")
    st.stop()


# ---- Barra lateral: solo filtros ---- #

opciones = repo.obtener_opciones(datos)

with st.sidebar:
    st.markdown("## Filtros")
    curso     = st.selectbox("Curso",      [repo.TODOS, *opciones["curso"]],      index=0)
    asignatura = st.selectbox("Asignatura", [repo.TODOS, *opciones["asignatura"]], index=0)
    grupo      = st.selectbox("Grupo",      [repo.TODOS, *opciones["grupo"]],      index=0)
    evaluacion = st.selectbox("Evaluación", [repo.TODOS, *opciones["evaluacion"]], index=0)

    st.divider()
    st.caption(
        f"**{len(datos)}** calificaciones · **{datos['id_alumno'].nunique()}** alumnos · "
        f"**{datos['asignatura'].nunique()}** asignaturas"
    )

filtrado = repo.aplicar_filtros(datos, curso, asignatura, grupo, evaluacion)


# ---- Cabecera y KPIs ---- #

st.markdown("# 📊 Dashboard de rendimiento académico")
st.markdown(
    '<div class="subtitulo">Análisis de calificaciones por asignatura, evaluación, '
    "curso y grupo.</div>",
    unsafe_allow_html=True,
)

if filtrado.empty:
    st.warning("No hay calificaciones que cumplan los filtros seleccionados. Prueba a ampliar la selección.")
    st.stop()

kpis = repo.calcular_kpis(filtrado)

col = st.columns(5)
col[0].metric("Alumnos evaluados", f"{kpis['alumnos_evaluados']}")
col[1].metric("Nota media",        repo.formatear_nota(kpis["nota_media"]))
col[2].metric("Nota máxima",       repo.formatear_nota(kpis["nota_maxima"]))
col[3].metric("Nota mínima",       repo.formatear_nota(kpis["nota_minima"]))
col[4].metric("Aprobados",         repo.formatear_porcentaje(kpis["porcentaje_aprobados"]))

st.write("")

# Tablas calculadas una sola vez
t_asignaturas        = repo.estadisticas_por_asignatura(filtrado)
t_alumnos            = repo.rendimiento_por_alumno(filtrado)
t_evolucion          = repo.evolucion_por_evaluacion(filtrado)
t_evolucion_asig     = repo.evolucion_por_asignatura(filtrado)
t_grupos             = repo.estadisticas_por_grupo(filtrado)
t_cursos             = repo.estadisticas_por_curso(filtrado)

tab1, tab2, tab3 = st.tabs(
    ["Notas por asignatura", "Evolución de evaluaciones", "Distribución de notas"]
)


# ---- Pestaña 1 — Notas por asignatura ---- #

with tab1:
    st.markdown("## Estadísticas por asignatura")
    st.dataframe(
        repo.preparar_tabla(t_asignaturas),
        use_container_width=True,
        hide_index=True,
        column_config={
            "nota_media":           st.column_config.NumberColumn(format="%.2f"),
            "nota_maxima":          st.column_config.NumberColumn(format="%.2f"),
            "nota_minima":          st.column_config.NumberColumn(format="%.2f"),
            "porcentaje_aprobados": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    st.plotly_chart(charts.grafico_nota_media_por_asignatura(t_asignaturas),
                    use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.grafico_aprobados_por_asignatura(t_asignaturas),
                        use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(charts.grafico_por_grupo(t_grupos),
                        use_container_width=True, config={"displayModeBar": False})

    st.markdown("## Rendimiento por alumno")
    st.dataframe(
        repo.preparar_tabla(t_alumnos),
        use_container_width=True,
        hide_index=True,
        column_config={
            "nota_media": st.column_config.NumberColumn(format="%.2f"),
        },
    )

    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(charts.grafico_ranking_alumnos(t_alumnos),
                        use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(charts.grafico_por_curso(t_cursos),
                        use_container_width=True, config={"displayModeBar": False})


# ---- Pestaña 2 — Evolución de evaluaciones ---- #

with tab2:
    st.markdown("## Evolución de las evaluaciones")

    if len(t_evolucion) < 2:
        st.info("Selecciona más de una evaluación para comparar la evolución.")

    st.plotly_chart(charts.grafico_evolucion_global(t_evolucion),
                    use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(charts.grafico_evolucion_por_asignatura(t_evolucion_asig),
                    use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(charts.grafico_aprobados_por_evaluacion(t_evolucion),
                        use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown("### Detalle por evaluación")
        st.dataframe(
            repo.preparar_tabla(t_evolucion),
            use_container_width=True,
            hide_index=True,
            column_config={
                "nota_media":           st.column_config.NumberColumn(format="%.2f"),
                "nota_maxima":          st.column_config.NumberColumn(format="%.2f"),
                "nota_minima":          st.column_config.NumberColumn(format="%.2f"),
                "porcentaje_aprobados": st.column_config.NumberColumn(format="%.2f"),
            },
        )


# ---- Pestaña 3 — Distribución de notas ---- #

with tab3:
    st.markdown("## Distribución de notas")

    res = repo.resumen_distribucion(filtrado)
    col = st.columns(5)
    col[0].metric("Media",            repo.formatear_nota(res["media"]))
    col[1].metric("Mediana",          repo.formatear_nota(res["mediana"]))
    col[2].metric("Desviación típica",repo.formatear_nota(res["desviacion"]))
    col[3].metric("Percentil 25",     repo.formatear_nota(res["p25"]))
    col[4].metric("Percentil 75",     repo.formatear_nota(res["p75"]))

    st.write("")

    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(charts.grafico_distribucion(filtrado),
                        use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(charts.grafico_estado(filtrado),
                        use_container_width=True, config={"displayModeBar": False})

    st.plotly_chart(charts.grafico_boxplot(filtrado),
                    use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns([2, 3])
    with c1:
        st.markdown("### Notas por intervalo")
        st.dataframe(
            repo.tabla_distribucion(filtrado),
            use_container_width=True,
            hide_index=True,
            column_config={
                "desde":    st.column_config.NumberColumn(format="%.1f"),
                "hasta":    st.column_config.NumberColumn(format="%.1f"),
                "porcentaje": st.column_config.NumberColumn(format="%.2f"),
            },
        )
    with c2:
        t_edad = t_alumnos.merge(alumnos[["id_alumno", "edad"]], on="id_alumno", how="left")
        st.plotly_chart(charts.grafico_edad_nota(t_edad),
                        use_container_width=True, config={"displayModeBar": False})


# ---- Pie de página ---- #

st.markdown(
    f'<div class="pie">Fuente: <code>Alumnos.csv</code> y <code>Notas.csv</code> · '
    f"{len(filtrado)} calificaciones mostradas de {len(datos)} · "
    "Nota de aprobado: 5,0 · Escala 0-10</div>",
    unsafe_allow_html=True,
)
