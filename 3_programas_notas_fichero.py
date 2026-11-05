#Al iniciar el programa se debe mostrar el siguiente menu:
#1.- Añadir notas
#2.- Mostrar notas extremas
#3.- Total de aprobados
#4.- Nota media
#5.- Mostrar todas
#6.- Salir


#El usuario elije una opción (1 al 6) y el programa le muestra o le pide
#los datos necesarios para llevar a cabo la acción. Después,
#vuelve a salir el menú y así hasta que elija la opción de salir.
#las notas se guardan en un fichero



indice=0
salir=False
opcion=1



while opcion != 6:
    try:
        print("=====================================")
        print("          MENÚ DE NOTAS              ")
        print("=====================================")
        print("1.- Añadir notas")
        print("2.- Mostrar notas extremas")
        print("3.- Total de aprobados")
        print("4.- Nota media")
        print("5.- Mostrar todas")
        print("6.- Salir")
        opcion=int(input("Elije opción (1 - 6); "))
        match opcion:
            case 1:
                num=int(input("Escribe una nota a la lista; "))
                f=open("notas.txt","a")
                f.write(str(num)+"\n")
                f.close()
            case 2:
                f=open("notas.txt","r")
                cad=f.readlines()
                print(cad)
                f.close() 
                lista_limpia = list(map(lambda x: int(x.rstrip()), cad))
                print("La máxima nota es ", max(lista_limpia))
                print("La mínima nota es ", min(lista_limpia))
            case 3:
                aprobados=0
                f=open("notas.txt","r")
                cad=f.readline()
                print(cad)
                while str(cad)!="":
                    if int(cad)>=5:
                        print(cad)
                        aprobados+=1
                        cad=f.readline()    
                print (f"El total de aprobados es de {aprobados}")
            case 4:
                contar=0
                notas=0
                f=open("notas.txt","r")
                cad=f.readline()
                while str(cad)!="":
                    notas=notas+int(cad)
                    contar=contar+1
                    cad=f.readline() 
                if (contar==0):
                    print("No hay notas para calcular la media")
                else:
                    print (f"La nota media es de {notas/contar}")
            case 5:
                f=open("notas.txt","r")
                cad=f.readlines()
                lista_limpia = list(map(lambda x: int(x.rstrip()), cad))
                print(lista_limpia)
            case 6:
                print("fin del programa")
                salir=True
                exit
            case _:
                print("Opción no válido")
    except ValueError:
        print("No es un valor numérico, vuelve a intentar")   
