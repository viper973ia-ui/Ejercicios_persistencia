import csv
import math

# Función para calcular la distancia euclidea entre dos puntos (x, y)
def distancia(punto1, punto2):
    return math.dist(punto1, punto2)

# 1. Solicitar al usuario su posición actual
print("--- INTRODUCE TU POSICIÓN ---")
pos_usuario = (int(input("Tu posición x: ")), int(input("Tu posición y: ")))
print(f"Tu posición guardada es: {pos_usuario}\n")

# 2. Abrir el archivo CSV y buscar el punto más cercano
try:
    with open("coordenadas.csv", "r") as f:
        coord_reader = csv.reader(f)
        
        # Saltarse la cabecera si tu CSV la tiene (ej: x,y)
        next(coord_reader, None)
        
        # Creamos una lista con todos los puntos válidos convertidos a enteros
        puntos = [
            (int(fila[0]), int(fila[1])) 
            for fila in coord_reader 
            if fila
        ]
        
    # 3. Utilizar la función min() para encontrar la coordenada más cercana
    if puntos:
        # min() evalúa cada punto de la lista usando nuestra función distancia como 'key'
        coordenada_tienda = min(puntos, key=lambda punto: distancia(punto, pos_usuario))
        distancia_corta = distancia(coordenada_tienda, pos_usuario)
        
        # 4. Mostrar el resultado final
        print("********** RESULTADO **********")
        print(f"La tienda más cercana a {pos_usuario} tiene las coordenadas {coordenada_tienda}")
        print(f"La distancia exacta es: {distancia_corta:.2f}")
    else:
        print("El archivo CSV estaba vacío o no contenía coordenadas válidas.")

except FileNotFoundError:
    print("Error: El fichero 'coordenadas.csv' no existe. Asegúrate de crearlo en la misma carpeta.")
