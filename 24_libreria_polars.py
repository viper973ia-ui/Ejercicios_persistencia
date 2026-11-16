import polars as pl

"""

    ¿Porqué Polars?
    1.- Estilo y métodos + modernos
    2.- Más eficiente
"""
datos = [ 
    {"nombre": "Ana", "edad": 25, "salario": 25000, "departamento": "ventas"}, 
    {"nombre": "Luis", "edad": 32, "salario": 32000,"departamento": "Informática"}, 
    {"nombre": "Marta", "edad": 28, "salario": 28000,"departamento": "Informática"}, 
    {"nombre": "Pedro", "edad": 41, "salario": 41000,"departamento": "ventas"} 
] 
df = pl.DataFrame(datos) 
print(df) 

# Acceso a filas y columnas
print(df["edad"]) # Es una serie
print(df["edad"].to_list())    #columna en lista de valores
print(df.row(0))
print(df.row(1))

print(df.row(0,named=True))    #diccionario con los datos de la fila
#Transformación en diccionarios
print(df.to_dicts())           #convierte todo el dataframe en una lista de diccionarios

#Filtrado
print("El filtro de salario > 30.000 es: ",df.filter(pl.col("salario")>30000))

print(df.filter((pl.col("salario")>30000) | (pl.col("edad")<50)))

#ordenación
print(df.sort(by="edad", descending=False))
print(df.sort("salario", descending=True).row(0))
print(df.sort("salario", descending=True).row(0)[0])

print(df.sort(by="edad", descending=False).row(-1))
print(df.sort(by="edad", descending=False).row(-1)[-1])

# funciones para cálculos min(), max(), mean(), count(), unique()

print("Salario más alto", df["salario"].max())
print("Salario más bajo", df["salario"].min())

print(df["departamento"].unique().to_list())   #para evitar duplicados

#selección

resultado=df.select(pl.col("salario").mean().alias("salario medio"),pl.col("edad").mean().alias("edad media"))
print(resultado)

# Agrupaciones en un dataframe

print(df.group_by("departamento").agg(pl.col("salario").mean().alias("salario medio"), pl.col("nombre").count().alias("total empleados")))


# Recorrido de un dataframe

for element in df.iter_rows():             # como tuplas
    print (element)

for element in df.iter_rows(named=True):   # como diccionarios
    print (element)
    

# Sobre rendimiento en lectura de archivos