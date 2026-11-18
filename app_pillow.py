import streamlit as st
from PIL import Image

st.title("Mi Dashboard de Ejemplo 📊")
st.sidebar.header("Menú de navegación")

try:
  imagen = Image.open("logo.png")
  st.image(imagen, caption="Logo de la empresa", use_container_width=True)
except FileNotFoundError:
  st.warning("No se encontró la imagen 'logo.png'. Revisa la ruta.")

st.metric(label="Ventas Totales", value="$25,400", delta="+12%")
