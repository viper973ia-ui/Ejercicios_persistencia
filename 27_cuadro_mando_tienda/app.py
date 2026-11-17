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
import matplotlib.pyplot as plt
import tiendas_repositorio as tr

st.set_page_config(page_title="Cuadro de Mando Tiendas", layout="wide")

# --- SIDEBAR ---
st.sidebar.header("Filtros")

# Callbacks para limpiar los otros filtros cuando se selecciona uno
def limpiar_mes():
    st.session_state["select_mes"] = None

def limpiar_tienda():
    st.session_state["select_tienda"] = None

def limpiar_filtros_para_grafico():
    st.session_state["select_tienda"] = None
    st.session_state["select_mes"] = None

# Desplegables existentes
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

st.sidebar.divider()

# Botón en el sidebar actualizado
boton_grafico = st.sidebar.button(
    "Ver Gráfico de gastos totales por tienda", 
    on_click=limpiar_filtros_para_grafico,
    use_container_width=True
)

# --- ÁREA PRINCIPAL CONDICIONAL ---
if opcion_1 is not None:
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

# Bloque condicional cuando se pulsa el botón del gráfico
elif boton_grafico:
    st.markdown(
    "<h1 style='text-align: center;'>Distribución de gastos totales por tienda</h1>", 
    unsafe_allow_html=True
    ) 
    
    # 1. Leemos el CSV y agrupamos por tienda sumando la facturación
    df_total = (
        pl.read_csv("ventas_tienda.csv")
        .group_by("nombre_tienda")
        .agg(pl.col("gastos_personal").sum())
        .sort("gastos_personal", descending=True)
    )
    st.write(df_total)
    # 2. Extraemos las columnas como listas de Python para Matplotlib
    tiendas = df_total["nombre_tienda"].to_list()
    ventas = df_total["gastos_personal"].to_list()

    # 3. Generamos el gráfico de tarta
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        ventas,
        labels=tiendas,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Porcentaje de gastos por tienda")

    # 4. Mostramos el gráfico centrado
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    with col_centro:
        st.pyplot(fig)

else:
    st.info("👈 Selecciona una tienda, un mes o pulsa el botón del gráfico en el panel lateral.")

