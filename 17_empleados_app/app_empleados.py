"""
-Alta de nuevos empleados
-Filtrar empleados: opcion por departamento o rango salarial.
Si se elige departamento, se muestra combo con departamentos y al
seleccionar uno muestra empleados. Si se elige rango salarial,
aparecen dos campos de textos (min y max) y un botón que al pulsarlo
muestra empleados
"""
import streamlit as st
import  pymongo as pm
import operaciones_mongodb as opmg

import importlib

importlib.reload(opmg)




# ============================================================
# CONFIGURACIÓN STREAMLIT
# ============================================================
st.set_page_config(
    page_title="Gestión de Empleados",
    page_icon="🎓",
    layout="wide"
)

st.title("🧑‍🔧 Gestión de Empleados")
st.write("Aplicación para gestionar los empleados de la base de datos Empresa.")
st.divider()


# ============================================================
# MENÚ
# ============================================================
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    ["Alta de empleado", "Filtar por departamento", "Filtar por rango salarial"]
)
    
    
# ========================================
#  ALTA NUEVOS EMPLEADOS
# ========================================

if opcion == "Alta de empleado":
    st.header("➕ Alta de empleado")
    with st.form("formulario_alta"):
        empleado = st.text_input("Empleado")
        edad = st.number_input("Edad",min_value=0.0, max_value=200.0, step=1.0)
        salario = st.number_input("Salario", min_value=0.0, max_value=100000.0, step=100.0)
        departamento = st.text_input("Departamento")
        guardar = st.form_submit_button("Guardar empleado")

    if guardar:
        if not empleado or not edad or not salario or not departamento:
            st.warning("Debes completar todos los campos de texto.")
        else:
            correcto, mensaje = opmg.alta_empleado(
                empleado.strip().upper(),
                int(edad),
                int(salario),
                departamento.strip().upper()
            )
            if correcto:
                st.success(mensaje)
            else:
                st.error(mensaje)

# ========================================
# FILTRO POR DEPARTAMENTO
# ========================================
elif opcion == "Filtar por departamento":
    st.header("🏢 Filtrar empleados por departamento")
    
    # 1. Obtenemos los departamentos desde MongoDB
    lista_departamentos = opmg.obtener_departamentos()
    
    if not lista_departamentos:
        st.info("No hay departamentos registrados en la base de datos.")
    else:
        # 2. Mostramos el combo (selectbox)
        depto_seleccionado = st.selectbox(
            "Selecciona un departamento:", 
            list(set((lista_departamentos)))
        )
        
        # 3. Al seleccionar uno, buscamos y mostramos los empleados automáticamente
        if depto_seleccionado:
            empleados = opmg.filtrar_por_departamento(depto_seleccionado)
            
            if empleados:
                st.subheader(f"Empleados en {depto_seleccionado} ({len(empleados)})")
                st.dataframe(empleados, use_container_width=True)
            else:
                st.warning("No se encontraron empleados en este departamento.")

# ========================================
# FILTRO POR RANGO SALARIAL
# ========================================
elif opcion == "Filtar por rango salarial":
    st.header("💰 Filtrar empleados por rango salarial")
    
    # Creamos dos columnas para que los campos min y max se vean alineados
    col1, col2 = st.columns(2)
    with col1:
        salario_min_txt = st.text_input("Salario mínimo")
    with col2:
        salario_max_txt = st.text_input("Salario máximo")
        
    buscar = st.button("Buscar empleados")
    
    if buscar:
        # 1. Validar que ambos campos estén rellenos
        if not salario_min_txt.strip() or not salario_max_txt.strip():
            st.warning("Debes introducir tanto el salario mínimo como el máximo.")
        else:
            try:
                # 2. Convertir los textos a números
                salario_min = int(salario_min_txt)
                salario_max = int(salario_max_txt)
                
                # 3. Validar lógica del rango
                if salario_min > salario_max:
                    st.error("El salario mínimo no puede ser mayor que el salario máximo.")
                else:
                    # 4. Consultar en MongoDB y mostrar resultados
                    empleados = opmg.filtrar_por_salario(salario_min, salario_max)
                    
                    if empleados:
                        st.subheader(f"Empleados encontrados ({len(empleados)})")
                        st.dataframe(empleados, use_container_width=True)
                    else:
                        st.info("No se encontraron empleados en ese rango salarial.")
                        
            except ValueError:
                st.error("Por favor, introduce valores numéricos válidos (sin letras ni símbolos).")
