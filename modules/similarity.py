def calculate_similarity(color_distance, texture_distance,
                         color_weight=0.5, texture_weight=0.5):

    total_weight = color_weight + texture_weight

    if total_weight == 0:
        raise ValueError("La somme des poids ne peut pas être nulle.")

    score = (
        color_weight * color_distance
        + texture_weight * texture_distance
    ) / total_weight

    return float(score)


def rank_images(query_image, reference_images,
                query_color_hist, query_texture,
                color_weight=0.5, texture_weight=0.5):

    from modules.color_histogram import calculate_histogram, normalize_histogram
    from modules.color_distance import compare_histograms
    from modules.texture_glcm import extract_glcm_features
    from modules.texture_distance import compare_texture_features
    from modules.image_loader import load_image

    results = []

    for image_path in reference_images:

        image = load_image(image_path)

        # Caractéristiques couleur
        hist = normalize_histogram(calculate_histogram(image))

        # Caractéristiques texture
        texture = extract_glcm_features(image)

        # Distances
        color_dist = compare_histograms(query_color_hist, hist)

        texture_dist = compare_texture_features(
            query_texture,
            texture
        )

        # Score global
        score = calculate_similarity(
            color_dist,
            texture_dist,
            color_weight,
            texture_weight
        )

        results.append({
            "image": str(image_path),
            "color_distance": color_dist,
            "texture_distance": texture_dist,
            "similarity_score": score
        })

    # Plus petit score = plus grande similarité
    results.sort(key=lambda item: item["similarity_score"])

    return results
