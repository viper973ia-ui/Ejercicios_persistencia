import pymongo as pm

url="mongodb://localhost:27017"
serv=pm.MongoClient(url)

# Así tenemos la conexión de la url de mongodb

col_libros=serv.libreria.libros

#col_libros.insert_one({'isbn': '4444D', 'titulo': 'C++', 'paginas': 520, 'categoria': 'programacion', 'precio': 40.7})
col_libros.update_one({"isbn":"1111A"},{"$inc":{"precio":20}})

libros=serv.libreria.libros.find()

# con esto obtenemos un cursor para cada uno de los libros que recoge en
# totalidad de la base de datos libreria y en el la colección (tabla) libros
# que hemos configurado en MongoDb Compass

for lb in libros:
        print (lb)
serv.close
print("========================================")
#si queremos buscar con una propiedad (sin operadores que llevarian {})
libros=serv.libreria.libros.find({"categoria":"programacion"})

for lb in libros:
        print (lb)
serv.close
