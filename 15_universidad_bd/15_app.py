""" Proyecto gestión de alumnos:

-Alta de alumnos: A través de una ventana, se solicitan los datos de un
nuevo alumno y se guardan en la base de datos. No se admiten dnis duplicados
si se proporciona un dni que ya existe, el alumno no se añade
y se avisa mediante un mensaje al usuario

-Busqueda de alumnos por curso. Se selecciona un curso en un combo
y debajo se muestra una tabla con los datos de todos los alumnos
de ese curso. En cada fila, aparecerá un botón para borrar a ese alumno

-Busqueda de alumno por dni. Se introduce el dni de un alumno
y se muestran todos sus datos, si no existe, mensaje de advertencia.  """


import streamlit as st
import operaciones_bd as op2

# ============================================================
# CONFIGURACIÓN STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Gestión de Alumnos",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Gestión de Alumnos")
st.write("Aplicación para gestionar los alumnos de la base de datos Universidad.")
st.divider()

# ============================================================
# MENÚ
# ============================================================
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    ["Alta de alumno", "Buscar por curso", "Buscar por DNI"]
)

# ============================================================
# ALTA DE ALUMNO
# ============================================================
if opcion == "Alta de alumno":
    st.header("➕ Alta de alumno")
    with st.form("formulario_alta"):
        dni = st.text_input("DNI")
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        curso = st.text_input("Curso")
        nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.5)
        guardar = st.form_submit_button("Guardar alumno")

    if guardar:
        if not dni or not nombre or not email or not curso:
            st.warning("Debes completar todos los campos de texto.")
        else:
            correcto, mensaje = op2.alta_alumno(
                dni.strip().upper(),
                nombre.strip(),
                email.strip(),
                curso.strip(),
                float(nota)
            )
            if correcto:
                st.success(mensaje)
            else:
                st.error(mensaje)

# ============================================================
# BÚSQUEDA POR CURSO
# ============================================================
elif opcion == "Buscar por curso":
    st.header("📚 Buscar alumnos por curso")
    cursos = op2.obtener_cursos()

    if not cursos:
        st.warning("No existen cursos en la base de datos.")
    else:
        curso = st.selectbox("Selecciona un curso:", cursos)
        alumnos = op2.buscar_por_curso(curso)

        if alumnos:
            st.success(f"Se han encontrado {len(alumnos)} alumnos.")

            # Cabecera con 6 columnas (índices 0 al 5)
            columnas = st.columns([2, 2, 3, 2, 1, 1])
            columnas[0].markdown("**DNI**")
            columnas[1].markdown("**Nombre**")
            columnas[2].markdown("**Email**")
            columnas[3].markdown("**Curso**")
            columnas[4].markdown("**Nota**")
            columnas[5].markdown("**Borrar**")
            st.divider()

            # Filas de alumnos usando solo listas/diccionarios nativos
            for alumno in alumnos:
                columnas = st.columns([2, 2, 3, 2, 1, 1])
                columnas[0].write(alumno["dni"])
                columnas[1].write(alumno["nombre"])
                columnas[2].write(alumno["email"])
                columnas[3].write(alumno["curso"])
                #columnas[4].write(alumno["nota"])
                columnas[4].markdown(
                                    f"<p style='font-size: 28px; font-weight: bold;'>{alumno['nota']}</p>",
                                    unsafe_allow_html=True 
                )

                with columnas[5]:
                    eliminar = st.button(
                        "🗑️",
                        key=f"borrar_{alumno['dni']}",
                        help="Eliminar alumno"
                    )
                    if eliminar:
                        borrado = op2.baja_alumno(alumno["dni"])
                        if borrado:
                            st.success("Alumno eliminado.")
                            st.rerun()
                        else:
                            st.error("No se ha podido eliminar.")
        else:
            st.info("No hay alumnos matriculados en este curso.")

# ============================================================
# BÚSQUEDA POR DNI
# ============================================================
elif opcion == "Buscar por DNI":
    st.header("🔎 Buscar alumno por DNI")
    dni_buscar = st.text_input("Introduce el DNI:")
    buscar = st.button("Buscar alumno", type="primary")

    if buscar:
        if not dni_buscar:
            st.warning("Introduce un DNI.")
        else:
            alumno = op2.buscar_por_dni(dni_buscar.strip().upper())
            if alumno:
                st.success("Alumno encontrado.")
                st.subheader(f"{alumno['nombre']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**DNI:** {alumno['dni']}")
                    st.write(f"**Nombre:** {alumno['nombre']}")
                    st.write(f"**Email:** {alumno['email']}")
                with col2:
                    st.write(f"**Curso:** {alumno['curso']}")
                    st.write(f"**Nota:** {alumno['nota']}")
            else:
                st.warning("No existe ningún alumno con ese DNI.")


