import numpy as np
from skimage.feature import graycomatrix, graycoprops


def extract_glcm_features(image, distances=None, angles=None, levels=256):
    """
    Extrait les caractéristiques de texture d'une image
    en utilisant la matrice GLCM.
    """

    if distances is None:
        distances = [1, 2, 3, 5]

    if angles is None:
        angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

    # Conversion RGB vers niveaux de gris
    if len(image.shape) == 3:
        gray = np.dot(
            image[..., :3],
            [0.299, 0.587, 0.114]
        ).astype(np.uint8)
    else:
        gray = image.astype(np.uint8)

    # Quantification des niveaux de gris
    gray = (gray.astype(np.uint16) * levels // 256).astype(np.uint8)

    # Calcul de la matrice GLCM
    glcm = graycomatrix(
        gray,
        distances=distances,
        angles=angles,
        levels=levels,
        symmetric=True,
        normed=True
    )

    # Extraction des propriétés
    features = {}

    properties = [
        "contrast",
        "dissimilarity",
        "homogeneity",
        "energy",
        "correlation",
        "ASM"
    ]

    for prop in properties:
        values = graycoprops(glcm, prop)
        features[prop] = float(np.mean(values))

    return features
