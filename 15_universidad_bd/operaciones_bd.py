import mysql.connector as con
from mysql.connector import Error


# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================

def conectar():
    try:
        return con.connect(host="localhost",
            user="root",
            password="root",
            port=3306,
            database="universidad")

    except Error as error:
        print(f"Error de conexión: {error}")
        return None

# ============================================================
# ALTA DE ALUMNO
# ============================================================

def alta_alumno(dni, nombre, email, curso, nota):

    conexion = conectar()

    if conexion is None:
        return False, "No se ha podido conectar con la base de datos."

    cursor = conexion.cursor()

    try:
        # Comprobar primero si existe el DNI

        sql = """
            SELECT dni
            FROM alumnos
            WHERE dni = %s
        """

        cursor.execute(sql, (dni,))

        if cursor.fetchone():

            return False, "Ya existe un alumno con ese DNI."

        # Insertar alumno

        sql = """
            INSERT INTO alumnos
            (dni, nombre, email, curso, nota)
            VALUES (%s, %s, %s, %s, %s)
        """

        datos = (
            dni,
            nombre,
            email,
            curso,
            nota
        )

        cursor.execute(sql, datos)

        conexion.commit()

        return True, "Alumno añadido correctamente."

    except Error as error:

        return False, f"Error: {error}"

    finally:

        cursor.close()
        conexion.close()


# ============================================================
# BUSCAR ALUMNOS POR CURSO
# ============================================================

def buscar_por_curso(curso):

    conexion = conectar()

    if conexion is None:
        return []

    cursor = conexion.cursor(dictionary=True)

    try:

        sql = """
            SELECT dni, nombre, email, curso, nota
            FROM alumnos
            WHERE curso = %s
            ORDER BY nombre
        """

        cursor.execute(sql, (curso,))

        return cursor.fetchall()

    except Error as error:

        print(f"Error: {error}")
        return []

    finally:

        cursor.close()
        conexion.close()


# ============================================================
# BUSCAR ALUMNO POR DNI
# ============================================================

def buscar_por_dni(dni):

    conexion = conectar()

    if conexion is None:
        return None

    cursor = conexion.cursor(dictionary=True)

    try:

        sql = """
            SELECT dni, nombre, email, curso, nota
            FROM alumnos
            WHERE dni = %s
        """

        cursor.execute(sql, (dni,))

        return cursor.fetchone()

    except Error as error:

        print(f"Error: {error}")
        return None

    finally:

        cursor.close()
        conexion.close()


# ============================================================
# BAJA DE ALUMNO
# ============================================================

def baja_alumno(dni):

    conexion = conectar()

    if conexion is None:
        return False

    cursor = conexion.cursor()

    try:

        sql = """
            DELETE FROM alumnos
            WHERE dni = %s
        """

        cursor.execute(sql, (dni,))

        conexion.commit()

        return cursor.rowcount > 0

    except Error as error:

        print(f"Error: {error}")
        return False

    finally:

        cursor.close()
        conexion.close()


# ============================================================
# OBTENER TODOS LOS CURSOS
# ============================================================

def obtener_cursos():

    conexion = conectar()

    if conexion is None:
        return []

    cursor = conexion.cursor()

    try:

        sql = """
            SELECT DISTINCT curso
            FROM alumnos
            ORDER BY curso
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        return [fila[0] for fila in resultados]

    except Error as error:

        print(f"Error: {error}")
        return []

    finally:

        cursor.close()

# ============================================================
# ACTUALIZAR ALUMNO
# ============================================================

def actualizar_alumno(dni, nombre, email, curso, nota):
    conexion = None
    try:
        conexion = conectar()  # Reemplaza 'conectar()' por el nombre exacto de tu función de conexión
        cursor = conexion.cursor()
        sql = """
            UPDATE alumnos
            SET nombre = %s, email = %s, curso = %s, nota = %s
            WHERE dni = %s
        """
        cursor.execute(sql, (nombre, email, curso, nota, dni))
        conexion.commit()

        if cursor.rowcount > 0:
            return True, "Alumno actualizado correctamente."
        else:
            return False, "No se realizaron cambios o no existe el alumno."
    except Exception as e:
        return False, f"Error al actualizar: {e}"
    finally:
        if conexion:
            conexion.close()
