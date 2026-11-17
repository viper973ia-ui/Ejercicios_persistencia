import streamlit as st 

saludo=""

with st.sidebar:
    st.write("Menú navegación")
    st.text_input("Dato:")
    if st.button("pulsar"):
        saludo="Estoy en navegación"
        #st.write("ha pulsado")
    st.write(saludo)  # Lo escribe en la zona de Menú navegación y Dato (dentro del sidebar)

st.write(saludo)      # Aquí lo escribe en la otra zona del sidebar

