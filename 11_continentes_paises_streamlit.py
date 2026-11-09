import streamlit as st
import json

# Configuración de la página en modo ancho
st.set_page_config(layout="wide")

# Ruta del archivo JSON
dir_fichero = r"C:\Curso Python Tarde\proyectos_persistencia\countries.json"

with open(dir_fichero, "r", encoding="UTF-8") as f:
    datos = json.load(f)

# Extraer y ordenar regiones para el filtro
lista_regiones = list(set(pais["region"] for pais in datos if "region" in pais))
lista_regiones.sort()
opciones_filtro = ["Todos"] + lista_regiones

# --- INTERFAZ DE STREAMLIT ---
st.title("🌍 Explorador de Países")

# Selector de región
region_seleccionada = st.selectbox("Filtrar por Región/Continente:", opciones_filtro)

# Filtrar datos
if region_seleccionada == "Todos":
    paises_a_mostrar = datos
else:
    paises_a_mostrar = [p for p in datos if p.get("region") == region_seleccionada]

st.write(f"Mostrando **{len(paises_a_mostrar)}** países:")
st.markdown("---")

# Mostrar los países en columnas por fila (4 países por fila)
columnas_por_fila = 4

for i in range(0, len(paises_a_mostrar), columnas_por_fila):
    cols = st.columns(columnas_por_fila)
    
    for j in range(columnas_por_fila):
        if i + j < len(paises_a_mostrar):
            pais = paises_a_mostrar[i + j]
            
            with cols[j]:
                with st.container(border=True):
                    # 1. NAME (Nombre del país arriba del todo)
                    st.subheader(pais.get("name", "Desconocido"))
                    
                    # 2. POPULATION (Población en el medio)
                    poblacion_formateada = f"{pais.get('population', 0):,}".replace(",", ".")
                    st.write(f"👥 **Población:** {poblacion_formateada}")
                    
                    # 3. FLAGS (Bandera abajo)
                    url_bandera = pais.get("flags", {}).get("png", "")
                    if url_bandera:
                        st.image(url_bandera, use_container_width=True)
