
import cv2
from pathlib import Path


# Formats d'images acceptes
IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff"
]


def load_image(image_path):
    """
    Charge une image et la convertit de BGR vers RGB.
    """

    image_path = str(image_path)

    # Lecture de l'image avec OpenCV
    image = cv2.imread(image_path)

    # Verification du chargement
    if image is None:
        raise ValueError(f"Impossible de lire : {image_path}")

    # Conversion BGR vers RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def get_image_paths(folder_path):
    """
    Recupere les chemins de toutes les images d'un dossier.
    """

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Dossier introuvable : {folder}")

    image_paths = []

    for file in folder.iterdir():

        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
            image_paths.append(file)

    return sorted(image_paths)

