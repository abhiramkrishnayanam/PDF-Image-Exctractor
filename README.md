# PDF-Image-Exctractor
Using PyMuPDF and OpenCV
![image](https://github.com/user-attachments/assets/51949232-f989-4b98-b827-49549f8b8289)

# 📄 PDF Image Extractor

A simple Streamlit-based web app that extracts image blocks from PDF files using computer vision techniques and allows users to download them individually or as a ZIP archive.

---

## 🧰 Tools / Libraries Used

- **Python** – Core programming language
- **[Streamlit](https://streamlit.io/)** – Framework for building web apps
- **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)** – Used for reading and rendering PDF pages
- **[OpenCV](https://opencv.org/)** – For image processing and contour detection
- **[NumPy](https://numpy.org/)** – Array manipulation
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** – Image handling and thumbnail creation
- **zipfile, os, tempfile** – File system and archive management

---

## 🔍 Step-by-Step Explanation of the Approach

1. **Upload PDF File**  
   The user uploads a PDF file through the app UI.

2. **PDF to Image Conversion**  
   Each page of the PDF is converted to a high-resolution image using `PyMuPDF` at 300 DPI.

3. **Image Block Detection**  
   - Convert the image to grayscale
   - Apply binary thresholding
   - Use `cv2.findContours()` to detect visual regions
   - Filter out small/noisy contours using size thresholds

4. **Image Extraction**  
   - Each valid image block is cropped from the page
   - Saved into an output folder

5. **Download Option**  
   - A ZIP archive of all extracted images is created
   - Users can download the full archive or individual images

6. **Image Display**  
   - Images are shown as thumbnails with optional individual download buttons

---

## ⚙️ Setup Instructions

### 🔧 Requirements

Install all necessary dependencies:

```bash
pip install -r requirements.txt

## 🧩 Challenges & Resolutions

| **Challenge**                                                              | **Resolution**                                                                                                                                                    |
|---------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Large images crowding the UI                                              | Used `PIL.Image.thumbnail()` to resize images for display                                                                                                        |
| Unwanted text/noise in output                                             | Applied size filters and contour-based image block extraction                                                                                                   |
| UI elements rendering out of order                                        | Ensured the ZIP download button is displayed before showing the images                                                                                          |
| Managing temporary files                                                  | Used Python’s `tempfile` module to handle temporary directories safely and cleanly                                                                              |
| Inability to detect embedded images if not truly image-type content       | Since many "images" in PDFs are actually vector graphics or drawn content, traditional image extraction fails. We addressed this by using high-resolution rendering (300 DPI) and contour detection to extract visual regions resembling images, even if not embedded as raster image objects. |

