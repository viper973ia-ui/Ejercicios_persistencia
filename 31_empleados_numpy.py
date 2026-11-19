# A partir de la colección de empleados de la bd empresas DBMongo

# - Salario medio de todos los empleados
# - Edad mayor
# - Lista de departamentos

# *** SOLO UTILIZANOD NUMPY ***

import numpy as np
import pymongo as pm

# 1. Conexión a MongoDB (ajusta la URL si usas usuario/contraseña o servidor remoto)
cliente = pm.MongoClient("mongodb://localhost:27017/")
db = cliente["empresa"]
coleccion = db["empleados"]

# 2. Extraemos todos los documentos de la colección
empleados = list(coleccion.find())    

# Es una "lista de diccionarios" tipo:
# [{'_id': ObjectId('6af5ed84b1429d93966d99b9'), 'empleado': 'JUAN CARLOS', 'edad': 35, 'salario': 1200, 'departamento': 'VENTAS'},
# {'_id': ObjectId('6af5ed84b1429d93966d99ba'), 'empleado': 'MARCOS', 'edad': 39, 'salario': 1300, 'departamento': 'INFORMÁTICA'}

print (empleados)

if empleados:
    # Convertimos cada campo a un array de NumPy
    # Usamos .get() para evitar errores si algún documento no tiene el campo
    salarios = np.array(
        [emp.get("salario") for emp in empleados if emp.get("salario") is not None],
        dtype=float,
    )
    edades = np.array(
        [emp.get("edad") for emp in empleados if emp.get("edad") is not None],
        dtype=int,
    )
    departamentos = np.array(
        [
            emp.get("departamento")
            for emp in empleados
            if emp.get("departamento") is not None
        ]
    )

    print (salarios)
    print ("************************* (1)")
    print (edades)
    print ("************************* (2)")
    print (departamentos)
    print ("************************* (3)")

    # 3. Cálculos exclusivos con NumPy
    salario_medio = np.mean(salarios) if salarios.size > 0 else 0
    edad_mayor = np.max(edades) if edades.size > 0 else 0
    lista_departamentos = np.unique(departamentos).tolist()

    print ("A ==========================> Z")
    print ("lista_departamentos:", lista_departamentos)
    print ("A ==========================> Z")
    
    lista_departamentos_inversa = np.unique(departamentos)[::-1].tolist()
    print("-------------------------------------------------------------------------------------")
    print ("Z <========================== A")
    print ("lista_departamentos inversa:", lista_departamentos_inversa)
    print ("Z <========================== A")
    

    
    # 4. Mostrar resultados
    print(f"Salario medio: {salario_medio:.2f}")
    print(f"Edad mayor: {edad_mayor}")
    print(f"Lista de departamentos: {lista_departamentos}") # Sí, np.unique() siempre devuelve los elementos ordenados 
                                                            # de menor a mayor 
                                                            # (o alfabéticamente de la A a la Z si son textos).
else:
    print("La colección 'empleados' está vacía.")

# Cerrar conexión
cliente.close()
