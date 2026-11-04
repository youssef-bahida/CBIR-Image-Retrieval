
import streamlit as st
import io
import zipfile

from pathlib import Path

from modules.image_loader import load_image, get_image_paths
from modules.color_histogram import calculate_histogram, normalize_histogram
from modules.texture_glcm import extract_glcm_features
from modules.similarity import rank_images


# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CBIR - Image Retrieval",
    page_icon="🖼️",
    layout="wide"
)


# =====================================================
# 2. CREATE PROJECT ZIP
# =====================================================

def create_project_zip():

    project_path = Path(__file__).resolve().parent
    zip_buffer = io.BytesIO()

    excluded_dirs = {
        "venv",
        ".venv",
        ".git",
        "__pycache__",
        ".pytest_cache"
    }

    excluded_files = {
        "secrets.toml"
    }

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for file_path in project_path.rglob("*"):

            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(project_path)

            if any(part in excluded_dirs for part in relative_path.parts):
                continue

            if file_path.name in excluded_files:
                continue

            if file_path.suffix == ".pyc":
                continue

            zip_file.write(file_path, relative_path)

    zip_buffer.seek(0)

    return zip_buffer.getvalue()


# =====================================================
# 3. SIMILARITY PERCENTAGE
# =====================================================

def calculate_similarity_percentage(score):

    similarity = (1 / (1 + max(0, score))) * 100

    return round(similarity, 2)


# =====================================================
# 4. HEADER
# =====================================================

st.title("🖼️ CBIR - Content-Based Image Retrieval")

st.caption(
    "Recherche et classement d'images par caractéristiques "
    "de couleur et de texture."
)

# Download project
project_zip = create_project_zip()

st.download_button(
    label="📦 Télécharger tout le projet (ZIP)",
    data=project_zip,
    file_name="TP-2-IRIC.zip",
    mime="application/zip",
    type="primary",
    use_container_width=True
)

st.divider()


# =====================================================
# 5. DATASET SELECTION
# =====================================================

col_dataset, col_query = st.columns([1, 2])

with col_dataset:

    st.subheader("Base de données")

    dataset = st.selectbox(
        "Choisir le dataset",
        ["imgColor", "imgTexture"]
    )

    base_folder = Path("Data") / dataset

    ref_folder = base_folder / "ref"
    test_folder = base_folder / "test"


# =====================================================
# 6. CHECK DATASET
# =====================================================

if not ref_folder.exists() or not test_folder.exists():

    st.error("Les dossiers ref et test sont introuvables.")
    st.stop()

reference_images = get_image_paths(ref_folder)
query_images = get_image_paths(test_folder)

if not reference_images or not query_images:

    st.warning("Aucune image trouvée dans les dossiers.")
    st.stop()


# =====================================================
# 7. QUERY IMAGE
# =====================================================

with col_query:

    st.subheader("Image requête")

    query_names = [path.name for path in query_images]

    selected_name = st.selectbox(
        "Sélectionner une image à rechercher",
        query_names
    )

    query_path = next(
        path for path in query_images
        if path.name == selected_name
    )

    query_image = load_image(query_path)

    st.image(
        query_image,
        caption=f"Image sélectionnée : {selected_name}",
        width=180
    )


st.divider()


# =====================================================
# 8. SEARCH PARAMETERS
# =====================================================

st.subheader("⚙️ Paramètres de recherche")

col1, col2, col3 = st.columns(3)

with col1:

    color_weight = st.slider(
        "🎨 Importance de la couleur",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )

with col2:

    texture_weight = st.slider(
        "🧩 Importance de la texture",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )

with col3:

    columns_per_row = st.selectbox(
        "Images par ligne",
        [3, 4, 5, 6],
        index=1
    )


# =====================================================
# 9. SEARCH ENGINE
# =====================================================

if st.button(
    "🔍 Rechercher les images similaires",
    type="primary",
    use_container_width=True
):

    if color_weight + texture_weight == 0:

        st.error("Choisissez au moins un poids non nul.")

        st.stop()

    with st.spinner("Analyse des images en cours..."):

        # Query color features
        query_color_hist = normalize_histogram(
            calculate_histogram(query_image)
        )

        # Query texture features
        query_texture = extract_glcm_features(query_image)

        # Compare reference images
        results = rank_images(
            query_image,
            reference_images,
            query_color_hist,
            query_texture,
            color_weight,
            texture_weight
        )

    # Save results in session
    st.session_state["results"] = results
    st.session_state["query_name"] = selected_name
    st.session_state["dataset"] = dataset


# =====================================================
# 10. DISPLAY RESULTS
# =====================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()

    st.subheader("📊 Résultats de recherche")

    st.success(
        f"{len(results)} images analysées pour "
        f"la requête : {st.session_state['query_name']}"
    )

    # Compact horizontal grid
    for start in range(0, len(results), columns_per_row):

        cols = st.columns(columns_per_row)

        for col_index, col in enumerate(cols):

            result_index = start + col_index

            if result_index >= len(results):
                break

            result = results[result_index]

            result_image = load_image(result["image"])

            similarity_percent = calculate_similarity_percentage(
                result["similarity_score"]
            )

            with col:

                st.image(
                    result_image,
                    use_container_width=True
                )

                st.markdown(
                    f"**#{result_index + 1} — "
                    f"{Path(result['image']).name}**"
                )

                # Similarity percentage
                st.metric(
                    label="Taux de similarité",
                    value=f"{similarity_percent:.2f}%"
                )

                # Technical score
                st.caption(
                    f"Score technique : "
                    f"{result['similarity_score']:.4f}"
                )

                # Detailed distances
                with st.expander("Détails"):

                    st.write(
                        f"🎨 Distance couleur : "
                        f"{result['color_distance']:.4f}"
                    )

                    st.write(
                        f"🧩 Distance texture : "
                        f"{result['texture_distance']:.4f}"
                    )

    st.divider()

    st.caption(
        "Classement : le score technique le plus faible "
        "correspond à l'image la plus similaire."
    )

    st.info(
        "Le taux de similarité est un indicateur calculé à partir "
        "du score technique. Il ne représente pas une probabilité "
        "ou une mesure absolue de ressemblance."
    )


# =====================================================
# 11. FOOTER
# =====================================================

st.divider()

st.caption(
    "TP-2-IRIC | Content-Based Image Retrieval | "
    "Python • OpenCV • GLCM • Streamlit"
)

