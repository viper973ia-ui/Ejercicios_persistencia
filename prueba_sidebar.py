import streamlit as st 

with st.sidebar:
    st.write("Menú navegación")
    st.text_input("Dato:")
    if st.button("pulsar"):
        st.write("ha pulsado")


