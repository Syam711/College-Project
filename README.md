# 🖼️ Image Resolution Enhancement using EDSR

This project implements an image super-resolution system based on the **Enhanced Deep Super-Resolution (EDSR)** model. It allows users to upload low-resolution images and upscale them using deep learning, with support for predefined scaling factors (2x, 3x, 4x) or custom resolutions.

---

## ✅ Requirements

- Python **3.9 or higher**
- pip (Python package installer)

All required Python packages are listed in the `requirements.txt` file.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/edsr-image-enhancer.git
cd edsr-image-enhancer
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project Locally

### 1. Apply Migrations (if any)

```bash
python manage.py migrate
```

### 2. Run the Django Development Server

```bash
python manage.py runserver
```

Once the server is running, open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## 📷 How to Use

1. Open the web interface in your browser.
2. Upload a low-resolution image.
3. Choose a scale factor (2x, 3x, 4x) or enter a custom resolution.
4. Click "Start" to enhance the image.
5. Preview or download the high-resolution result.

---

## 📁 Project Structure (Simplified)

```
Image-Enhancer/
├── backend/
│   ├── models/                 # EDSR and utility models
│   ├── views.py                # Django views for processing
│   └── urls.py
├── templates/                  # HTML templates
├── static/                     # CSS
├── media/                      # Uploaded and processed images
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Customization & Extensibility

- You can enhance the model with:
  - Attention mechanisms (Channel/Spatial)
  - Multi-scale support
  - Post-processing: denoising, sharpening, contrast or color enhancements
- All enhancements can be optionally enabled in the backend logic.

---


## 🙋 Support

For questions, suggestions, or contributions, feel free to open an [issue](https://github.com/Syam711/Image-Enhancer/issues) or submit a pull request.
