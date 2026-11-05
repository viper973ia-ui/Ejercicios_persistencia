"""
# ====   FORMA 1 de leer el fichero   ====
# ========================================
f=open("dias.txt","r")
linea=f.readline()
while linea!="":
    print(linea)
    linea=f.readline()
f.close()
print("=================================")
print("=======  FIN DEL FICHERO  =======")
print("=================================")

# con esto lee el fichero línea a línea

"""

# ====   FORMA 2 de leer el fichero   ====
# ========================================

with open("dias.txt","r") as f:
    linea=f.readline()
    while linea!="":
        print (linea)
        linea=f.readline()
with open("dias.txt","r") as f:
    lista_dias=f.readlines()
texto=" aaa   \n \t"
texto_limpio=texto.strip()
print(texto)
print(texto_limpio)

lista_limpia=list(map(lambda x:x.strip(),lista_dias))
                    
print(lista_limpia)

lista_limpia_compr_lista=[a.strip for a in lista_dias]

print(lista_limpia_compr_lista)
    
    
    