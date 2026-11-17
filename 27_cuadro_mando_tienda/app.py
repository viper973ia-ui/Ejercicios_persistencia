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
import polars as pl
import tiendas_repositorio as tr

st.set_page_config(page_title="Cuadro de Mando Tiendas", layout="wide")

# --- SIDEBAR ---
st.sidebar.header("Filtros")

# 1. Creamos funciones pequeñas (callbacks) para limpiar el otro desplegable al elegir uno
def limpiar_mes():
    st.session_state["select_mes"] = None

def limpiar_tienda():
    st.session_state["select_tienda"] = None

# 2. Ambos empiezan vacíos (index=None) y se limpian mutuamente al cambiar
opcion_1 = st.sidebar.selectbox(
    "Selecciona una tienda:",
    tr.lista_tiendas(),
    index=None,
    placeholder="Elige una tienda...",
    key="select_tienda",
    on_change=limpiar_mes
)

opcion_2 = st.sidebar.selectbox(
    "Selecciona un mes:",
    tr.lista_mes(),
    index=None,
    placeholder="Elige un mes...",
    key="select_mes",
    on_change=limpiar_tienda
)

# --- ÁREA PRINCIPAL CONDICIONAL ---
if opcion_1 is not None:
    # SOLO se muestra si elegiste una tienda
    st.title(f"Resultados de la tienda: {opcion_1}")
    df_tienda = tr.datos_por_tienda(opcion_1)
    st.dataframe(df_tienda, use_container_width=True, hide_index=True)

    total_facturacion = df_tienda["facturacion"].sum()
    total_gastos = df_tienda["gastos_personal"].sum()
    mes_top = (
        df_tienda
        .sort("facturacion", descending=True)
        .select("mes")
        .item(0, 0)
    )

    st.subheader("Resumen de la tienda")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de facturación", f"{total_facturacion:,.0f} €")
    col2.metric("Total de gastos de personal", f"{total_gastos:,.0f} €")
    col3.metric("Mes con mayor facturación", mes_top)

elif opcion_2 is not None:
    # SOLO se muestra si elegiste un mes
    st.title(f"Resultados del mes: {opcion_2}")
    df_mes = tr.datos_por_mes(opcion_2)
    st.dataframe(df_mes, use_container_width=True, hide_index=True)

    media_facturacion = df_mes["facturacion"].mean()
    tienda_mayor_gasto = (
        df_mes
        .sort("gastos_personal", descending=True)
        .select("nombre_tienda")
        .item(0, 0)
    )

    st.subheader("Resumen del mes")
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Media de facturación (todas las tiendas)", f"{media_facturacion:,.2f} €")
    col_m2.metric("Tienda con mayor gasto de personal", tienda_mayor_gasto)

else:
    # Mensaje inicial cuando ninguno de los dos está seleccionado
    st.info("👈 Selecciona una tienda o un mes en el panel lateral para ver sus resultados.")
