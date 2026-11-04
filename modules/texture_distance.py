import numpy as np


def compare_texture_features(features1, features2):
    """
    Calcule la distance euclidienne entre deux
    ensembles de caractéristiques GLCM.
    """

    keys = [
        "contrast",
        "dissimilarity",
        "homogeneity",
        "energy",
        "correlation",
        "ASM"
    ]

    vector1 = np.array([features1[key] for key in keys])
    vector2 = np.array([features2[key] for key in keys])

    # Normalisation pour éviter la domination
    # des caractéristiques ayant de grandes valeurs
    scale = np.maximum(np.abs(vector1), np.abs(vector2))
    scale[scale == 0] = 1

    vector1 = vector1 / scale
    vector2 = vector2 / scale

    return float(np.linalg.norm(vector1 - vector2))
