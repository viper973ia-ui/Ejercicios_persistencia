import polars as pl
df=pl.scan_csv("houses.csv")     # hace una carga según necesidad (Lazy) 
                                 # planifica la consulta sin cargar el
                                 # archivo todavía.
                                 
                                 # read_csv ejecuta los datos al instante
                                 # en memoria (Eager)

print(df)
filtro=df.filter(pl.col("rooms")>2)
print(filtro.collect())
print(filtro.select(pl.col("price").mean()).collect())

# Estilo scan_ndjson
{"curso":"Java","horario":"tardes","duracion":120}
{"curso":"Java","horario":"mañanas","duracion":80}
{"curso":"PHP","horario":"tardes","duracion":150}
{"curso":"Python","horario":"tardes","duracion":60} 

df1=pl.scan_ndjson("academia.json")

print (df1)

