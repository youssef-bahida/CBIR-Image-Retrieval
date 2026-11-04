
import matplotlib.pyplot as plt

from modules.image_loader import load_image
from modules.color_histogram import (
    calculate_histogram,
    normalize_histogram
)

# Charger une image
image = load_image("Data/imgColor/ref/01.jpg")

# Calculer les histogrammes
histograms = calculate_histogram(image)

# Normaliser les histogrammes
normalized = normalize_histogram(histograms)

# Afficher les informations
print("Nombre de canaux :", histograms.shape[0])
print("Nombre de bins :", histograms.shape[1])

print("\nHistogramme RGB :")
print(histograms)

print("\nHistogramme normalisé :")
print(normalized)

# Visualisation
colors = ["red", "green", "blue"]

for i in range(3):
    plt.plot(normalized[i], color=colors[i], label=colors[i].upper())

plt.title("Histogrammes RGB normalisés")
plt.xlabel("Intensité")
plt.ylabel("Fréquence normalisée")
plt.legend()
plt.grid()
plt.show()

