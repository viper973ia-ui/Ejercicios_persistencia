import pandas as pd
import streamlit as st

# Configuración básica de la página
st.set_page_config(page_title="Análisis de Tiendas", page_icon="🏪")
st.title("📊 Consulta de Ventas por Tienda")


# Cargar el archivo CSV con caché para mejorar el rendimiento
@st.cache_data
def cargar_datos():
  return pd.read_csv("ventas_tienda.csv")


df = cargar_datos()


# --- Funciones de análisis ---
def ventas_totales_tienda(df, tienda):
  df_filtrado = df[df["nombre_tienda"].str.lower() == tienda.lower()]
  if df_filtrado.empty:
    return None
  return df_filtrado["facturacion"].sum()


def mayor_gasto_personal(df):
  return df["gastos_personal"].max()


def mes_mayor_facturacion(df, tienda):
  df_filtrado = df[df["nombre_tienda"].str.lower() == tienda.lower()]
  if df_filtrado.empty:
    return None
  indice_max = df_filtrado["facturacion"].idxmax()
  return df_filtrado.loc[indice_max, "mes"]


# --- Dato general en la parte superior ---
max_gasto_general = mayor_gasto_personal(df)
st.metric(
    label="💰 Mayor gasto de personal registrado (todas las tiendas)",
    value=f"{max_gasto_general:,.2f}",
)

st.divider()

# --- Interacción con el usuario ---
tienda_buscada = st.text_input(
    "Introduce el nombre de la tienda a buscar:", placeholder="Ej. Tienda Norte"
).strip()

if tienda_buscada:
  total_ventas = ventas_totales_tienda(df, tienda_buscada)
  mejor_mes = mes_mayor_facturacion(df, tienda_buscada)

  if total_ventas is not None:
    st.subheader(f"Resultados para: {tienda_buscada.title()}")

    # Mostrar resultados en dos columnas visuales
    col1, col2 = st.columns(2)
    col1.metric("Ventas Totales", f"{total_ventas:,.2f}")
    col2.metric("Mes de Mayor Facturación", str(mejor_mes))
  else:
    st.error(f"No se encontraron datos para la tienda '{tienda_buscada}'.")
