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
  return df["gastos_personal"].max()


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
max_gasto_general = mayor_gasto_personal(df)

print("\n--- Resultados ---")
if total_ventas is not None:
  print(f"Ventas totales de '{tienda_buscada}': {total_ventas}")
  print(f"Mes con mayor facturación de '{tienda_buscada}': {mejor_mes}")
else:
  print(f"No se encontraron datos para la tienda '{tienda_buscada}'.")
  
# Nombre de la tienda más antigua  


print(f"Mayor gasto de personal entre todas las tiendas: {max_gasto_general}")

tienda_antigua, año_apertura = df.loc[
    df["año_apertura"].idxmin(), ["nombre_tienda", "año_apertura"]
]
print("La tienda más antigua es:"
    *df.loc[df["año_apertura"].idxmin(), ["nombre_tienda", "año_apertura"]],
    sep=" - ",
)


""" # Solución del profesor
# import pandas as pd
dt=pd.read_csv("ventas_tiendas.csv")
""" #tienda=input("Introduce el nombre de la tienda: ")


""" dtquery=dt.query("nombre_tienda==@tienda")
#dtquery=dt[dt["nombre_tienda"]==tienda]
print(f"La facturación total de la tienda {tienda}  es {dtquery["facturacion"].sum()}") """ """

#mostrar mayor gasto de personal de todas las empresas
dfgrupo=dt.groupby("nombre_tienda").agg(gastos_personal=("gastos_personal","sum"))
print(dfgrupo["gastos_personal"].max())

print(dt.groupby("nombre_tienda")["gastos_personal"].sum().max()) 

tienda=input("Introduce el nombre de la tienda: ")

dtquery=dt.query("nombre_tienda==@tienda")
print(dtquery)

print("El mes con mayor facturación es: ",  dtquery
      .sort_values(by="facturacion",ascending=False) #ordena de mayor a menor
      .iloc[0] #se queda con el primer registro del dataframe ordenado de MAYOR a menor
      .to_dict()["mes"]) #convierte en un diccionario y extrae la propiedad deseada 

# Nombre de la tienda más antigua

dtquery_antiguedad=(dt.groupby("nombre_tienda")["año_apertura"].min())
print ("La tienda más antigua es:", dtquery_antiguedad) """