"""
Realiza un progrma para la organizacion de una libreria
un libro tiene tres propiedades: titulo, autor y precio.

Cuando se inicie el programa, se va a mostrar un menu:
1-Nuevo libro
2-Mostrar todos
3-Buscar por titulo
4-Libros por precio maximo
5-Salir

1-Se piden los datos del nuevo libro y se guardan
2-Se muestran los titulos de todos los libros
3-Se le pide el titulo y se muestran todos sus datos
4-Se le pide el precio maximo y se muestran los titulos de los libros cuyo precio sea igual o inferior al introducido
Despues de ejecutar cualquiera de las anteriores opciones, se muestra de nuevo el menu.
Asi hasta que elija la opcion 5 que sale del programa
"""
import streamlit as st 
libros=[]
tab_nuevo,tab_todos,tab_buscar,tab_precios=st.tabs(["Nuevo libro","Mostrar todos","Buscar por título","Libros por precio máximo"])
with tab_nuevo:
    titulo=st.text_input("Introduce Título: ")
    autor=st.text_input("Introduce Autor: ")
    precio=st.number_input("Introduce Precio: ")
    if st.button("Guardar libro"):
        libros.append({"titulo": titulo, "autor": autor, "precio": precio})
        libs=list(filter(lambda lib:lib["titulo"].lower()==titulo.lower(),libros))
with tab_buscar:
    titulo=st.text_input("Introduce el título del libro a buscar: ")
    if st.button("Buscar"):
        if libs:
            st.success(f"Título:{libs[0]["titulo"]},Autor:{libs[0]["autor"]}, Precio: {libs[0]["precio"]}")
    else:
        st.error("Libro no encontrado")



def titulos():
    print("Títulos de los libros:")
    for lib in libros:
        print(f"Título: {lib["titulo"]} precio:{lib["precio"]}")
def buscar_titulo(titulo):   
    encontrado=False    
    for i in libros:
        if titulo.lower() == i["titulo"].lower():
            print("Se ha encontrado tu libro")
            print(f"Título: {i['titulo']} Autor: {i['autor']} Precio: {i['precio']}")
            encontrado= True
            break
    if not encontrado:
        print("Libro no encontrado")
    return encontrado
def nuevo_libro():
	titulo = input("Título: ")
	autor = input("Autor: ")
	try:
		precio = float(input("Precio: "))
	except ValueError:
		print("Precio no válido. No se agregó el libro.")
		return
	if not buscar_titulo(titulo):
		libros.append({"titulo": titulo, "autor": autor, "precio": precio})
		print("Libro agregado.")
	else:
		print("Libro repetido, no se agregó")
def libros_por_precio_maximo(max_precio):  
    titulos = [n["titulo"] for n in libros if n["precio"]<=max_precio]    
    if len(titulos)>0:
        print(f"Libros con precio <= {max_precio}:")
        for j in titulos:
            print(j)  
    else:
        print("No hay libros con ese precio o inferior.")
opcion="0"    
while opcion!="5":
	mostrar_menu()
	opcion=input("Elige una opción: ")
	if opcion == "1":
		nuevo_libro()
	elif opcion == "2":
		titulos()
	elif opcion == "3":
		buscar=input("Introduce el titulo del libro que quieres buscar: ")
		buscar_titulo(buscar)
	elif opcion == "4":
		try:
			max_precio = float(input("Precio máximo: "))
			libros_por_precio_maximo(max_precio)
		except ValueError:
			print("Precio no válido.")
	elif opcion == "5":
		print("Saliendo del programa...")
	else:
		print("Opción no válida. Intenta de nuevo.") 

