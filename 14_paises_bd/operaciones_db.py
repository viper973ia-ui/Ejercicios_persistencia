import mysql.connector as con
def crear_conexion():
    return con.connect(host="localhost",
    user="root",
    password="root",
    port=3306,
    database="mundo"   
)
    
def borrar_tablas():
    db=crear_conexion()
    cursor=db.cursor()
    cursor.execute("delete from continentes")
    cursor.execute("delete from paises")
    db.commit()
    db.close()

def crear_continentes(continentes):   #["Asia","Americas",....]
    # Conectamos a la base de datos    
    db = crear_conexion()
    cursor = db.cursor()
    
    # Preparamos la consulta SQL. 
    # Asumo que tu tabla tiene una columna llamada 'nombre' (o similar)
    sql = "INSERT INTO continentes (continente) VALUES(%s)"
    
    # Transformamos la lista de strings en una lista de tuplas, 
    # ya que mysql-connector requiere este formato: [("Asia",), ("Americas",), ...]
    datos = [(c,) for c in continentes]
    
    try:
        # Insertamos todos los registros de un solo golpe
        cursor.executemany(sql, datos)
        db.commit()
        print(f"Se han insertado {cursor.rowcount} continentes correctamente.")
    except con.Error as e:
        print(f"Error al insertar continentes: {e}")
        db.rollback()
    finally:
        # Aseguramos el cierre de la conexión
        cursor.close()
        db.close()
def devolver_continentes():
    sql="select * from continentes"
    db = crear_conexion()
    cursor=db.cursor(dictionary=True)
    cursor = db.cursor()
    cursor.execute(sql)
    resultado=cursor.fetchall()    # se entrega una lista de tuplas por defecto.
    db.close()                     # En este caso nos da un diccionario
    return resultado
def crear_paises(paises):  # [{"pais":"pais1,","poblacion":333,"bandera":"http:....,"idContinente":2},.....]
     # Conectamos a la base de datos    
         db = crear_conexion()
         cursor = db.cursor()
         
         # Preparamos la consulta SQL. 
         # Asumo que tu tabla tiene una columna llamada 'nombre' (o similar)
         sql = "INSERT INTO paises (pais,poblacion,bandera,idContinente) VALUES(%s,%s,%s,%s)"
         
         # Transformamos la lista de strings en una lista de tuplas, 
         # ya que mysql-connector requiere este formato: [("Asia",), ("Americas",), ...]
         #lista_tuplas = [(p["pais"],p["poblacion"],p["bandera"],p["idContinente"]) for p in paises]
         lista_tuplas=[tuple(p.values()) for p in paises ]
    
         
         try:
             # Insertamos todos los registros de un solo golpe
             cursor.executemany(sql, list(lista_tuplas))
             db.commit()
             print(f"Se han insertado {cursor.rowcount} continentes correctamente.")
         except con.Error as e:
             print(f"Error al insertar continentes: {e}")
             db.rollback()
         finally:
             # Aseguramos el cierre de la conexión
             cursor.close()
             db.close()
             
def paises_por_continente(id_continente):
    sql="select * from paises where idContinente=%s"
    db = crear_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql)
    resultado=cursor.fetchall()
    db.close()
    return resultado
    