import csv

# **************  UTILIZANDO el READER  ******************

with open ("empleados.csv","r") as f:
    next(f) #se salta la primera línea
    datos=csv.reader(f,delimiter=",")   # De esta manera podemos definir el delimitador que se
                                        # va a usar en el fichero CSV ("," es por defecto)
    print("1.-  ***********")
    for row in datos:                   
        print(row)
    print ("===============")

# *************  UTILIZANDO el DICTREADER ****************
with open ("empleados.csv","r") as f:
    datos=csv.DictReader(f)             # De esta manera podemos definir el delimitador que se
    print("2.-  ***********")           # va a usar en el fichero CSV ("," es por defecto)
    for row in datos:                  
        print(row)
    print ("===============")

# *************  UTILIZANDO LISTAS con READER ****************

with open("empleados.csv","r") as f:
    print("3.-  ***********")
    datos=list(csv.reader(f))
    print(datos)
    print ("===============")


# *************  UTILIZANDO LISTAS con DICTREADER   ****************    
with open("empleados.csv","r") as f:
    print("4.-  ***********")
    datos=list(csv.DictReader(f))
    print(datos)
    print ("===============")
    
    

#solicita la introducción de un departamento y te muestra
#los nombres de las personas de ese departamento

consulta_departamento=input("Introducir un departamento: ").lower()

with open ("empleados.csv","r") as f:
    datos=csv.DictReader(f)             # De esta manera podemos definir el delimitador que se
    print("CONSULTA.-  ***********")     # va a usar en el fichero CSV ("," es por defecto)
    for emp in datos:                   
        if emp["departamento"].lower()==consulta_departamento:
            print(emp["empleado"])
    print ("===============")
    
#nombre del empleado con mayor salario

with open ("empleados.csv","r") as f:
    print("***********   CONSULTA Empleado + SALARIO  ***********")
    datos=list(csv.DictReader(f))
    empleado_top = max(datos, key=lambda x: float(x["salario"]))
    print(f"Empleado: {empleado_top['empleado']} | Salario: {empleado_top['salario']}")
    print ("=====================================================")