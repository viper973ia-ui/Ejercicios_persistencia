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

