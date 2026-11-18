import streamlit as st 
import polars as pl

st.set_page_config(
    page_title="Análisis académico",
    layout="wide"
) 

# ---- SIDEBAR ------
st.sidebar.header("Filtros")

def limpiar_asignatura():
    st.session_state["select_asignatura"] = None

def limpiar_curso():
    st.session_state["select_curso"] = None
    
def limpiar_grupo():
    st.session_state["select_grupo"] = None

def limpiar_evaluacion():
    st.session_state["select_evaluacion"] = None



#def limpiar_filtros_para_grafico():
#    st.session_state["select_curso"] = None
#    st.session_state["select_asignatura"] = None

# Desplegables existentes
opcion_1 = st.sidebar.selectbox(
    "Curso:",
    ["1º ESO", "2º ESO", "3º ESO"],  # Lista provisional (o usa [] si la quieres vacía)
    index=None,
    placeholder="Elige un curso...",
    key="select_curso",
    on_change=limpiar_curso
)

opcion_2 = st.sidebar.selectbox(
    "Asignatura:",
    ["Matemáticas", "Lengua", "Historia"],  # Lista provisional
    index=None,
    placeholder="Elige asignatura...",
    key="select_asignatura",
    on_change=limpiar_asignatura
)

opcion_3 = st.sidebar.selectbox(
    "Grupo:",
    ["Grupo A", "Grupo B", "Grupo C"],  # Lista provisional
    index=None,
    placeholder="Elige un grupo...",
    key="select_grupo",
    on_change=limpiar_grupo
)

opcion_4 = st.sidebar.selectbox(
    "Evaluación:",
    ["1ª Evaluación", "2ª Evaluación", "3ª Evaluación"],  # Lista provisional
    index=None,
    placeholder="Elige una evaluación...",
    key="select_evaluacion",
    on_change=limpiar_evaluacion
)

st.sidebar.divider()   # Crea una línea debajo de los selectbox

# --- ÁREA PRINCIPAL CONDICIONAL ---

st.info("👈 Selecciona un curso, una asignatura, un grupo y una evaluación en el panel lateral.")

st.title("📊 Dashboard de rendimiento académico")

if opcion_1:
    st.title(f"Resultados del curso: {opcion_1}")
else:
    st.title("Resultados (selecciona un curso)")

st.subheader("Análisis de calificaciones por asignatura, evaluación, curso y grupo")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Alumnos evaluados", f"12")
col2.metric("Nota media", f"7.58")
col3.metric("Nota máxima", f"9.50")
col4.metric("Nota mínima", f"4.50")
col5.metric("Aprobados", f"97.9%")

