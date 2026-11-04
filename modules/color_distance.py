import cv2
import numpy as np


def compare_histograms(hist1, hist2):
    """
    Compare deux histogrammes RGB avec la distance de Bhattacharyya.
    Retourne une distance moyenne entre 0 et 1.
    """

    distances = []

    for channel in range(3):
        h1 = hist1[channel].astype(np.float32)
        h2 = hist2[channel].astype(np.float32)

        distance = cv2.compareHist(
            h1,
            h2,
            cv2.HISTCMP_BHATTACHARYYA
        )

        distances.append(distance)

    return float(np.mean(distances))
