#A partir del documento alumnos.json realizar:

# - calcular la nota media global
# - mostrar nota más alta de cada curso
# - Total de alumnos de cada curso


import pandas as pd

df=pd.read_json("alumnos.json", encoding="UTF-8")

print(df)


print(f"1.- La nota media global es: {df["nota"].mean():.2f}")

grupo=df.groupby("curso").agg(nota_mas_alta=("nota","max"))
print(f"2.- La nota mas alta de cada curso es: ", grupo.sort_values(by=["nota_mas_alta"]))

grupo=df.groupby("curso").agg(total_alumnos=("nombre","count"))
print(f"El total de alumnos de cada curso es: ", grupo.sort_values(by=["total_alumnos"]))