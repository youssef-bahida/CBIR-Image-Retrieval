
import cv2
import numpy as np


def calculate_histogram(image, bins=256):
    """
    Calcule les histogrammes des trois canaux RGB.
    """

    histograms = []

    # Parcourir les trois canaux : Rouge, Vert, Bleu
    for channel in range(3):

        histogram = cv2.calcHist(
            [image],
            [channel],
            None,
            [bins],
            [0, 256]
        )

        histograms.append(histogram.flatten())

    return np.array(histograms)


def normalize_histogram(histograms):
    """
    Normalise les histogrammes pour faciliter
    la comparaison entre différentes images.
    """

    normalized = []

    for histogram in histograms:

        total = np.sum(histogram)

        if total > 0:
            histogram = histogram / total

        normalized.append(histogram)

    return np.array(normalized)

