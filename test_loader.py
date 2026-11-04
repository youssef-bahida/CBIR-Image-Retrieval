
import matplotlib.pyplot as plt

from modules.image_loader import load_image, get_image_paths


# Dossier des images de reference
folder = "Data/imgColor/ref"

# Recuperer les images
images = get_image_paths(folder)

print("Nombre d'images :", len(images))

# Charger la premiere image
if len(images) > 0:

    image = load_image(images[0])

    print("Image :", images[0].name)
    print("Dimensions :", image.shape)
    print("Type :", image.dtype)

    # Affichage
    plt.imshow(image)
    plt.title("Premiere image de reference")
    plt.axis("off")
    plt.show()

else:
    print("Aucune image trouvee.")

