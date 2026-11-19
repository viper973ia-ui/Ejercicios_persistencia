import numpy as np

datos=np.array([10,2,11,8,20])
datos2=np.array([[4,8,-1],[5,3,11]])

print (datos[0])  # 10
print (datos2[1][1]) # 3

print(datos2[datos2>0])

for fila in datos2:
        for celda in fila:
                print(celda)
                
a1=np.array([200,120,30])
a2=np.array([130,50,85])
suma=np.add(a1,a2)
print(suma)

unir=np.concatenate((a1,a2))
print(unir)