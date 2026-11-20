
#1. Consumo total semanal
#2. Consumo medio diario
#3. Dias con mayor y menor consumo
#4. Dias con consumo superior a la media

#6. Días con consumo un 20% inferior a la media
#7. Coste total, sabiendo que de lunes a viernes el coste del Kw es 0,02 y en fin de semana del 0,018


#
##5. Porcentaje de consumo cada día

import numpy as np

consumos = np.array([1250, 1380, 980, 1450, 1520, 1100, 1600])
dias = np.array(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])

# 1. Consumo total semanal
total_semanal = np.sum(consumos)
print(f"1. Consumo total semanal: {total_semanal} kW")

# 2. Consumo medio diario
media_diaria = np.mean(consumos)
print(f"2. Consumo medio diario: {media_diaria:.2f} kW")

# 3. Días con mayor y menor consumo
dia_mayor = dias[np.argmax(consumos)]
dia_menor = dias[np.argmin(consumos)]
print("=========================================")
print ("dia_mayor:",dia_mayor)
print ("dia_menor:",dia_menor)
print("=========================================")
print(f"3. Mayor consumo: {dia_mayor} ({np.max(consumos)} kW) | Menor consumo: {dia_menor} ({np.min(consumos)} kW)")

# 4. Días con consumo superior a la media
dias_sup_media = dias[consumos > media_diaria]
print(f"4. Días superiores a la media: {dias_sup_media.tolist()}")

# 5. Porcentaje de consumo cada día
porcentajes = (consumos / total_semanal) * 100
print("5. Porcentaje de consumo por día:")
for dia, pct in zip(dias, porcentajes):
    print(f"   - {dia}: {pct:.2f}%")

# Como calcular la suma de porcentajes para comprobar que es el 100%
print ("?????????????????????????????????????????????????????????")
suma_porcentajes = sum(porcentajes)
print(f"Suma total de porcentajes: {suma_porcentajes:.2f}%")
print ("=========================================================")


# 5. Porcentaje de consumo cada día (tabulado en consola)
porcentajes = (consumos / total_semanal) * 100

# ****   OTRA FORMA VISUAL DE PORCENTAJES   ***

print("5. Porcentaje de consumo por día:")
print("-" * 35)
for dia, pct in zip(dias, porcentajes):
    # {dia:<12} reserva 12 espacios alineados a la izquierda
    # {pct:>6.2f} reserva 6 espacios alineados a la derecha con 2 decimales
    print(f"   - {dia:<12} {pct:>6.2f}%")
print("-" * 35)
print(f"   {'Total:':<14} {np.sum(porcentajes):>6.2f}%")

# 6. Días con consumo un 20% inferior a la media (menor al 80% de la media)
limite_inferior = media_diaria * 0.80
dias_inf_20 = dias[consumos < limite_inferior]
print(f"6. Días con consumo >20% inferior a la media (< {limite_inferior:.2f} kW): {dias_inf_20.tolist()}")

# 7. Coste total (Lunes-Viernes: 0,02 | Fin de semana: 0,018)
tarifas = np.array([0.02, 0.02, 0.02, 0.02, 0.02, 0.018, 0.018])
coste_total = np.sum(consumos * tarifas)
print(f"7. Coste total semanal: {coste_total:.2f} €")


##8. Mostrar consumo de cada día
