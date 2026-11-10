"""
    Utilizando los archivos de funciones definidos, hará lo siguiente
    -Borrará las tablas de base de datos
    -Recuperar continentes y paises del JSON
    -Prepará los datos obtenidos, para poder enviarlos a las funciones
    de la base de datos
    -Llamará a las funciones para guardar continentes y guardar paises
        

"""


# 1. Borrado de las tablas de datoss
import operaciones_db as ap
ap.borrar_tablas()

# 2. Recuperar continentes y paises del JSON
import operaciones_json as opjson
continentes=opjson.continentes()
continentes_bd=ap.devolver_continentes()  # [Como lista de continetes]
print("****************************")
print(continentes)
print("****************************")
print (continentes_bd)
print("****************************")
ap.crear_continentes(opjson.continentes())

paises=opjson.paises()
print (paises)
print("*****************")
#ap.crear_paises(paises)

def obtener_idcontinente(continente):
   return [c["idContinente"] for c in continentes_bd if c["continente"]== continente[0]]    
paises_para_bd=[{"pais":p["name"],"poblacion":p["population"],"bandera":p["flags"]["png"],"idContinente":obtener_idcontinente(p["region"])} for p in paises]
ap.crear_paises(paises_para_bd)
# 3.