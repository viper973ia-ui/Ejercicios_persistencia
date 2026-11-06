import csv
import math

# Función para calcular la distancia euclidea entre dos puntos (x, y)
def distancia(punto1, punto2):
    # math.dist recibe dos estructuras (como tuplas o listas) y calcula la distancia directamente
    return math.dist(punto1, punto2)

# 1. Solicitar al usuario su posición actual
print("--- INTRODUCE TU POSICIÓN ---")
pos_usuario = (int(input("Tu posición x: ")), int(input("Tu posición y: ")))
print(f"Tu posición guardada es: {pos_usuario}\n")

# 2. Inicializar variables para encontrar el mínimo
distancia_corta = float('inf')  # Se inicializa con infinito para que cualquier distancia inicial sea menor
coordenada_tienda = None

# 3. Abrir el archivo CSV y buscar el punto más cercano
try:
    with open("coordenadas.csv", "r") as f:
        coord_reader = csv.reader(f)
        
        # Saltarse la cabecera si tu CSV la tiene (ej: x,y). 
        # Si tu CSV solo tiene números directos, comenta o borra la siguiente línea:
        next(coord_reader, None) 
        
        for fila in coord_reader:
            # Validar que la fila no esté vacía
            if not fila:
                continue
                
            # Convertir las coordenadas del CSV de texto (str) a números (int)
            punto_csv = (int(fila[0]), int(fila[1]))
            
            # Calcular la distancia entre la posición del usuario y el punto del CSV
            dist_actual = distancia(punto_csv, pos_usuario)
            
            # Si la distancia calculada es menor que la guardada, actualizamos
            if dist_actual < distancia_corta:
                distancia_corta = dist_actual
                coordenada_tienda = punto_csv

    # 4. Mostrar el resultado final si se encontraron tiendas
    if coordenada_tienda is not None:
        print("********** RESULTADO **********")
        print(f"La tienda más cercana a {pos_usuario} tiene las coordenadas {coordenada_tienda}")
        print(f"La distancia exacta es: {distancia_corta:.2f}")
    else:
        print("El archivo CSV estaba vacío o no contenía coordenadas válidas.")

except FileNotFoundError:
    print("Error: El fichero 'coordenadas.csv' no existe. Asegúrate de crearlo en la misma carpeta.")


#utiliando la función min 