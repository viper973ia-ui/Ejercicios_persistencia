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

import polars as pl

# 1. Escanear el archivo CSV (Modo Lazy: no carga todo en memoria todavía)
lazy_df = pl.scan_csv("ventas_tienda.csv")

def lista_tiendas():
    lista_tiendas=(
        lazy_df
        .select(pl.col("nombre_tienda").drop_nulls().unique().sort())
        .collect()
        .to_series()
        .to_list()
    )
    return lista_tiendas

def lista_mes():
    lazy_df = pl.scan_csv("ventas_tienda.csv", encoding="utf8-lossy")
    meses_unicos = (
        lazy_df
        .select(pl.col("mes").drop_nulls().unique(maintain_order=True))
        .collect()
        .to_series()
        .to_list()
    )
    return meses_unicos

# Nueva función para filtrar la información de la tienda seleccionada
def datos_por_tienda(tienda):
    lazy_df = pl.scan_csv("ventas_tienda.csv", encoding="utf8-lossy")
    return (
        lazy_df
        .filter(pl.col("nombre_tienda") == tienda)
        .drop("nombre_tienda")  # <-- Elimina esta columna del resultado
        .collect()
    )

def datos_por_mes(mes):
    lazy_df = pl.scan_csv("ventas_tienda.csv", encoding="utf8-lossy")
    return (
        lazy_df
        .filter(pl.col("mes") == mes)
        .drop("mes")  # Ocultamos la columna "mes" porque ya va en el título
        .collect()
    )