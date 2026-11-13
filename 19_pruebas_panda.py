import pandas as pd

lista_reproduccion=[
    {"titulo":"canción inventada","duracion":3.20,"valoracion":4},
    {"titulo":"Bohemian Rapsody","duracion":5.40,"valoracion":10},
    {"titulo":"Green summer","duracion":4.10,"valoracion":7}
] 

# Creación de un DataFrame I

df=pd.DataFrame(lista_reproduccion)
print(df)

print("********************")
df=pd.DataFrame(lista_reproduccion)
df.index=df["titulo"]
print(df)
print("con índice = ''titulo''")


# Creación de un DataFrame II

lista_empleados=[{
  "_id": {
    "$oid": "6af5ed84b1429d93966d99b9"
  },
  "empleado": "JUAN CARLOS",
  "edad": 35,
  "salario": 1200,
  "departamento": "VENTAS"
},
{
  "_id": {
    "$oid": "6af5ed84b1429d93966d99ba"
  },
  "empleado": "MARCOS",
  "edad": 39,
  "salario": 1300,
  "departamento": "INFORMÁTICA"
},
{
  "_id": {
    "$oid": "6af5ed84b1429d93966d99bb"
  },
  "empleado": "RAQUEL",
  "edad": 28,
  "salario": 1100,
  "departamento": "VENTAS"
},
{
  "_id": {
    "$oid": "6af5ed84b1429d93966d99bc"
  },
  "empleado": "MARÍA",
  "edad": 45,
  "salario": 1700,
  "departamento": "INFORMÁTICA"
},
{
  "_id": {
    "$oid": "6af5f1e0a7be2b72c8327b99"
  },
  "empleado": "ANA",
  "edad": 33,
  "salario": 1600,
  "departamento": "INFORMÁTICA"
},
{
  "_id": {
    "$oid": "6af5f1e0a7be2b72c8327b9a"
  },
  "empleado": "RAQUEL",
  "edad": 45,
  "salario": 2000,
  "departamento": "RRHH"
},
{
  "_id": {
    "$oid": "6af5f1e0a7be2b72c8327b9b"
  },
  "empleado": "MARTÍN",
  "edad": 29,
  "salario": 1900,
  "departamento": "RRHH"
},
{
  "_id": {
    "$oid": "6af60dcb30ccf0a1400359a7"
  },
  "empleado": "EMPLEADO8",
  "edad": 52,
  "salario": 2700,
  "departamento": "INGENIERIA"
}]


print("//////////////////////////////////////////////////////////////////////////////")
print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
df=pd.DataFrame(lista_empleados)
print(df)


df=pd.read_csv("empleados.csv", encoding="UTF-8")
print (df)
print(df.columns)
print(df.values)

for v in df.values:
    print(v[0])

# salario medio

print(f"El salario medio: {df['salario'].mean():.2f}")
print(f"salario medio de informática: {df.query('departamento == \"informática\"')['salario'].mean():.2f}")

# Quiero agruparlos por departamento y con la columna salario medio y edad máxima de cada departamento

grupo=df.groupby("departamento").agg(salario_medio=("salario","mean"),edad_maxima=("edad","max"))
print(grupo)
