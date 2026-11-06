#realizar una nueva versión del ejercicio 38_buscar_cursos
#lo más reducida posible
import datetime as dt
import streamlit as st
import json
dir_fichero="C:\Curso Python Tarde\Ejercicios_persistencia_(profesor)"
with open(dir_fichero,"r",encoding="UTF-8") as f:
    datos=json.load(f)
cursos=datos["cursos"]
#Nombre del curso con la nota media más alta
#Nombre del curso que finalizó antes
def media(numeros):
    if numeros:
        return sum(numeros)/len(numeros)
    else:
        return 0
def convertir_a_fecha(texto):
    return dt.datetime.strptime(texto,"%d/%m/%Y")
def curso_antes():
    curso=min(cursos,key=lambda c:convertir_a_fecha(c["fecha_fin"]))
    
    return f"El curso más antiguo es {curso["denominacion"]}"
    
def curso_media_mayor():
    curso=max(cursos,key=lambda c:media(c["calificaciones"]))
    
    return f"El curso con la media más alta es {curso["denominacion"]}"
    
#llamadas a las funciones
st.write(curso_antes())
st.write(curso_media_mayor()) 
