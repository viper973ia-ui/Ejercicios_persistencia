# Generar un programa que introduciendo un presupuesto
# te muestra que casas te puedes permitir

import csv,streamlit as st

def posibles(presupuesto):
   with open("houses.csv", "r") as f:
       todos=csv.DictReader(f)
       return [h for h in todos if int(h["price"])<=presupuesto]
       

pres= st.text_input("Dime tu presupuesto: ")

if st.button ("Calcular"):
    st.table(posibles(int(pres)))
    
#  Otra forma más corta


presupuesto = st.number_input("Dime tu presupuesto: ")
with open("houses.csv", "r") as f:
    disponibles=list(filter(lambda p:float(p["price"])<=presupuesto,csv.DictReader(f)))
    st.table(disponibles)