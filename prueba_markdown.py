import streamlit as st

st.title("Ejemplo de tamaños de fuente en columnas")

# 1. Datos de ejemplo simulando tus alumnos
alumnos = [
    {"nombre": "Ana García", "curso": "1º ESO", "asistencia": "95%", "trabajo": "Sí", "nota": 9.5},
    {"nombre": "Luis Pérez", "curso": "1º ESO", "asistencia": "80%", "trabajo": "No", "nota": 6.0},
    {"nombre": "Marta Ruiz", "curso": "1º ESO", "asistencia": "100%", "trabajo": "Sí", "nota": 10.0},
     {"nombre": "Antonio Perez", "curso": "1º ESO", "asistencia": "90%", "trabajo": "Sí", "nota": 6.0},
]

# 2. Encabezados de la tabla
headers = st.columns(5)
headers[0].write("**Alumno**")
headers[1].write("**Curso**")
headers[2].write("**Asistencia**")
headers[3].write("**Trabajo**")
headers[4].write("**Nota**")

st.divider()

# 3. Mostrar cada alumno en sus 5 columnas
for i, alumno in enumerate(alumnos):
    columnas = st.columns(5)
    
    columnas[0].write(alumno["nombre"])
    columnas[1].write(alumno["curso"])
    columnas[2].write(alumno["asistencia"])
    columnas[3].write(alumno["trabajo"])
    
    # En la columna 4 aplicamos los distintos tamaños como ejemplo:
    if i == 0:
        # H3 (tamaño mediano-grande)
        columnas[4].markdown(f"### {alumno['nota']}")
    elif i == 1:
        # H1 (tamaño muy grande)
        columnas[4].markdown(f"## {alumno['nota']}")
    elif i == 2:
            # H1 (tamaño muy grande)
            columnas[4].markdown(f"# {alumno['nota']}")
    else:
        # Texto normal (para que compares la diferencia)
        columnas[4].write(alumno["nota"])