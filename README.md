
# 🖼️ TP-2-IRIC — Content-Based Image Retrieval

A Content-Based Image Retrieval (CBIR) application developed with Python, OpenCV, GLCM and Streamlit.

## 🚀 Features

- Image query selection
- RGB color histogram extraction
- Color similarity using Bhattacharyya distance
- Texture analysis using GLCM
- Contrast, Dissimilarity, Homogeneity, Energy, Correlation and ASM
- Combined color and texture similarity ranking
- Similarity percentage indicator
- Compact horizontal image results grid
- Complete project ZIP download

## 🛠️ Technologies

- Python
- Streamlit
- OpenCV
- NumPy
- Scikit-image
- Pillow

## 📁 Project Structure

```text
TP-2-IRIC/
├── Data/
│   ├── imgColor/
│   │   ├── ref/
│   │   └── test/
│   └── imgTexture/
│       ├── ref/
│       └── test/
├── modules/
│   ├── image_loader.py
│   ├── color_histogram.py
│   ├── color_distance.py
│   ├── texture_glcm.py
│   ├── texture_distance.py
│   └── similarity.py
├── results/
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/youssef-bahida/TP-2-IRIC.git
cd TP-2-IRIC
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 📊 Similarity Calculation

The application combines color and texture distances.

A lower technical distance indicates a more similar image.

The displayed percentage is an indicative transformation:

Similarity (%) = 100 / (1 + distance)

It is not a statistical probability.

## 👨‍💻 Author

**Youssef Bahida**

GitHub: https://github.com/youssef-bahida

