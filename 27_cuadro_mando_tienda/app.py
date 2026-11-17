# * Al seleccionar una tienda se mostrará:
# Una tabla con la información de dicha tienda. Y debajo de esa tabla:
#   - Total de facturación
#   - Total de gastos de personal
#   - Mes con mayor facturación

# * Al seleccionar un mes se mostrará:
# Una tabla con los datos de ese mes.
#   - Y debajo de esa tabla:
#       - Media de facturación de todas las tiendas
#       - Tienda con mayor gasto de personal
#
#  Utilizamos el archivo ventas_tienda.csv

import streamlit as st

# Título en la pantalla principal
st.title("Mi Aplicación Cuadro de Mandos ""Tiendas"" con Sidebar")

# Primer Combobox en el sidebar
opcion_1 = st.sidebar.selectbox(
    "Selecciona una categoría:",
    ["Electrónica", "Ropa", "Hogar"]
)

# Segundo Combobox en el sidebar
opcion_2 = st.sidebar.selectbox(
    "Selecciona un color:",
    ["Rojo", "Azul", "Verde"]
)

# Mostrar lo que el usuario eligió en la pantalla principal
st.write(f"Elegiste la categoría **{opcion_1}** de color **{opcion_2}**.")


