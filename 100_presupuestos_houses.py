# Generar un programa que introduciendo un presupuesto
# te muestra que casas te puedes permitir

import csv
import math 

presupuesto=int(input("Introducce tu presupuesto: "))
with open("houses.csv", "r") as f:
        fila=csv.DictReader(f)
        for casas in fila:
            if int(casas["price"]) <= presupuesto:
                print (casas)
        