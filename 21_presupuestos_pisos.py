# A partir del fichero house.csv

# Se solicita un presupuesto y te muestra los datos
# de los pisos que puedas comprar ordenados de 
# mayor a menor precio

import pandas as pd

df=pd.read_csv("houses.csv", encoding="UTF-8")

print (df)

presupuesto=float(input("Introduce tu presupuesto: "))
print(df.query("price<=@presupuesto").sort_values(by=["price"],ascending=False))


