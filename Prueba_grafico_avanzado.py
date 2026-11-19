import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng(7)
mujeres = rng.normal(164, 6.5, 500)
hombres = rng.normal(177, 7.0, 500)
bins = np.arange(140, 205, 2.5)
fig, ax = plt.subplots(figsize=(7, 4))
for datos, nombre, color in [(mujeres, "Mujeres", "#E07B39"),
(hombres, "Hombres", "#3776AB")]:
    ax.hist(datos, bins=bins, density=True, alpha=0.55, 
    color=color,
    edgecolor="white", label=nombre)
    ax.axvline(datos.mean(), color=color, linestyle="--", 
    linewidth=2)
ax.set_xlabel("Altura (cm)")
ax.set_ylabel("Densidad")
ax.set_title("Distribución de alturas por grupo")
ax.legend()
plt.show()