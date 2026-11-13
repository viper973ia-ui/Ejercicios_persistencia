import pymongo as py  # <-- ESTA LÍNEA ES LA QUE FALTA O NO ESTÁ GUARDADA


from pymongo import MongoClient
from bson.objectid import ObjectId

URL = "mongodb://localhost:27017/"

def alta_empleado(empleado, edad, salario, departamento):
    # Se abre aquí y se cierra sola al terminar el bloque 'with'
    with MongoClient(URL) as serv:
        db = serv["empresa"]
        col_empleados = db["empleados"]
        col_empleados.insert_one({
            "empleado": empleado,
            "edad": edad,
            "salario": salario,
            "departamento": departamento
        })
    return True, "Empleado guardado"

def obtener_departamentos():
    """Devuelve una lista ordenada de los departamentos únicos en la base de datos."""
    try:
        with MongoClient(URL) as serv:
            db = serv["empresa"]
            col_empleados = db["empleados"]
            departamentos = col_empleados.distinct("departamento")
            return sorted(list(set(departamentos)))
    except Exception as e:
        print(f"Error al obtener departamentos: {e}")
        return []

def filtrar_por_departamento(departamento):
    """Devuelve una lista de empleados que pertenecen al departamento indicado."""
    try:
        with MongoClient(URL) as serv:
            db = serv["empresa"]
            col_empleados = db["empleados"]
            empleados = list(col_empleados.find({"departamento": departamento}, {"_id": 0}))
            return empleados
    except Exception as e:
        print(f"Error al filtrar empleados: {e}")
        return []
    
def filtrar_por_salario(salario_min, salario_max):
    """Devuelve una lista de empleados cuyo salario está entre salario_min y salario_max."""
    try:
        with MongoClient(URL) as serv:
            db = serv["empresa"]
            col_empleados = db["empleados"]
            
            filtro = {
                "salario": {
                    "$gte": salario_min,
                    "$lte": salario_max
                }
            }
            empleados = list(col_empleados.find(filtro, {"_id": 0}))
            return empleados
    except Exception as e:
        print(f"Error al filtrar por salario: {e}")
        return []

from bson.objectid import ObjectId

def obtener_todos_empleados():
    try:
        with MongoClient(URL) as serv:
            db = serv["empresa"]
            col_empleados = db["empleados"]
            
            empleados = list(col_empleados.find())
            for emp in empleados:
                emp["_id"] = str(emp["_id"])
            return empleados
    except Exception as e:
        print(f"Error al obtener todos los empleados: {e}")
        return []

def actualizar_empleados(lista_empleados):
    try:
        with MongoClient(URL) as serv:
            db = serv["empresa"]
            col_empleados = db["empleados"]
            
            for emp in lista_empleados:
                id_empleado = ObjectId(emp["_id"])
                datos_actualizar = {k: v for k, v in emp.items() if k != "_id"}
                col_empleados.update_one(
                    {"_id": id_empleado},
                    {"$set": datos_actualizar}
                )
            return True, "Los datos de los empleados se han actualizado correctamente."
    except Exception as e:
        print(f"Error al actualizar los empleados: {e}")
        return False, f"Error al actualizar los empleados: {e}"
