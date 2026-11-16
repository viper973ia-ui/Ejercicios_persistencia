import mysql.connector
import pandas as pd

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mundo"
)

df=pd.read_sql("select * from paises",conexion)
print(df)
conexion.close()