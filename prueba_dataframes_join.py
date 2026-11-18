import polars as pl
df_departamentos=pl.DataFrame([
    {"id_departamento":1,"departamento":"ventas","responsable":"r1","presupuesto":30000},
    {"id_departamento":2,"departamento":"técnico","responsable":"r2","presupuesto":50000}
])
df_empleados=pl.DataFrame([
    {"id_empleado":111,"nombre":"e1","salario":1600,"id_departamento":1},
    {"id_empleado":222,"nombre":"e2","salario":1500,"id_departamento":2},
    {"id_empleado":333,"nombre":"e3","salario":1700,"id_departamento":2},
    {"id_empleado":444,"nombre":"e4","salario":1800,"id_departamento":1},
    {"id_empleado":555,"nombre":"e5","salario":1300,"id_departamento":1}
]) 

fusion=df_empleados.join(df_departamentos,on="id_departamento",how="inner")
print(fusion)