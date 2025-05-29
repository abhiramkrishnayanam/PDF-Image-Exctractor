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

## 🧩 Challenges & Resolutions

**Challenge:** Large images crowding the UI  
**Resolution:** Used `PIL.Image.thumbnail()` to resize images for a cleaner display.

**Challenge:** Unwanted text or noise appearing in the extracted output  
**Resolution:** Applied size filters and contour-based image block extraction to isolate likely image regions.

**Challenge:** UI elements like buttons and images rendering out of order  
**Resolution:** Structured the Streamlit layout to ensure the ZIP download button appears before the image gallery.

**Challenge:** Managing temporary files safely and efficiently  
**Resolution:** Utilized Python’s `tempfile` module to handle temporary directories cleanly without leaving residual files.

**Challenge:** Inability to detect embedded images when they aren’t actual raster images  
**Resolution:** Many images in PDFs are not true embedded image files but vector graphics or drawn content. We resolved this by rendering each PDF page at 300 DPI and using OpenCV contour detection to extract image-like regions based on their visual appearance.


