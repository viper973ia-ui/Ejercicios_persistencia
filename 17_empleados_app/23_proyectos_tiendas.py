# Sobre el archivo ventas, realizar:

# A partir de nombre de tienda, mostrar sus ventas totales

# Mostrar el mayor gasto de personal de tiendas

# A partir del nombre de tienda, mes en la que esta
# obtuvo mayor facturación

import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv("ventas_tienda.csv")


# 1. A partir de nombre de tienda, mostrar sus ventas totales (facturación total)
def ventas_totales_tienda(df, tienda):
  df_filtrado = df[df["nombre_tienda"].str.lower() == tienda.lower()]
  if df_filtrado.empty:
    return None
  return df_filtrado["facturacion"].sum()


# 2. Mostrar el mayor gasto de personal de tiendas
def mayor_gasto_personal(df):
  indice_max = df["gastos_personal"].idxmax()
  tienda = df.loc[indice_max, "nombre_tienda"]
  gasto = df.loc[indice_max, "gastos_personal"]
  return tienda, gasto

# 3. A partir del nombre de tienda, mes en el que esta obtuvo mayor facturación
def mes_mayor_facturacion(df, tienda):
  df_filtrado = df[df["nombre_tienda"].str.lower() == tienda.lower()]
  if df_filtrado.empty:
    return None
  indice_max = df_filtrado["facturacion"].idxmax()
  return df_filtrado.loc[indice_max, "mes"]


# --- Interacción con el usuario ---
tienda_buscada = input("Introduce el nombre de la tienda a buscar: ").strip()

total_ventas = ventas_totales_tienda(df, tienda_buscada)
mejor_mes = mes_mayor_facturacion(df, tienda_buscada)
tienda_max, max_gasto_general = mayor_gasto_personal(df)

print("\n--- Resultados ---")
if total_ventas is not None:
  print(f"Ventas totales de '{tienda_buscada}': {total_ventas}")
  print(f"Mes con mayor facturación de '{tienda_buscada}': {mejor_mes}")
else:
  print(f"No se encontraron datos para la tienda '{tienda_buscada}'.")

print(
    f"Mayor gasto de personal entre todas las tiendas: {max_gasto_general} (en"
    f" {tienda_max})"
)
