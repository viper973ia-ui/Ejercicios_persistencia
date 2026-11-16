# Sobre el archivo ventas_tiendas.csv, realizar:

# A partir de nombre de tienda, mostrar sus ventas totales

# Mostrar la tienda con mayor gasto de personal
# (nombre de tienda e importe gasto de personal)

# A partir del nombre de tienda, mes en la que esta
# obtuvo mayor facturación

import polars as pl

# Cargar el archivo CSV (nota el plural en 'ventas_tiendas.csv')
df = pl.read_csv("ventas_tienda.csv")

# Pedir el nombre de la tienda al usuario
tienda = input("Introduce el nombre de la tienda: ").strip()

# Filtrar los datos de esa tienda (ignorando mayúsculas/minúsculas)
df_tienda = df.filter(
    pl.col("nombre_tienda").str.to_lowercase() == tienda.lower()
)

print("\n--- Resultados ---")

if df_tienda.is_empty():
  print(f"No se encontró la tienda '{tienda}'.")
else:
  # 1. Ventas totales de la tienda buscada
  print (df_tienda)
  ventas_totales = df_tienda["facturacion"].sum()
  print(f"Ventas totales de {tienda}: {ventas_totales}")

    # 3. Mes en el que obtuvo mayor facturación y su importe
  fila_mejor_mes = df_tienda.sort("facturacion", descending=True).row(
      0, named=True)
  print(
      f"Mes de mayor facturación de {tienda}: {fila_mejor_mes['mes']}"
      f" ({fila_mejor_mes['facturacion']})"
  )


# 2. Tienda con mayor gasto de personal acumulado (nombre e importe total)
fila_max_gasto = (
                df.group_by("nombre_tienda")
                .agg(pl.col("gastos_personal").sum())
                .sort("gastos_personal", descending=True)
                .row(0, named=True)
)

print(
    f"Tienda con mayor gasto de personal: {fila_max_gasto['nombre_tienda']}"
    f" ({fila_max_gasto['gastos_personal']})"
)
