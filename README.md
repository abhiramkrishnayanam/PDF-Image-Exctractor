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

## 🧭 Step-by-step Explanation of the Approach

### 1. 📥 Uploading the PDF
- The user uploads a PDF file containing pages with potentially image-like content.
- Streamlit handles the file upload and temporarily saves the file for processing.

### 2. 🧠 PDF Processing and Image Detection
- We use **PyMuPDF (`fitz`)** to render each page of the PDF at high resolution (300 DPI).
- This rendering converts all visible content — including non-image visuals like vector graphics — into pixel data.
- Each rendered page is converted into a NumPy array and processed using **OpenCV**.

### 3. 🔍 Preprocessing with OpenCV
- Convert the image to **grayscale**.
- Apply **binary thresholding** (with `cv2.threshold`) to enhance contrast.
- Detect **contours** (connected components) in the thresholded image which may represent image blocks.
- Apply filters based on **width and height** to eliminate noise or small non-image elements.

### 4. 🖼️ Extracting Image Regions
- For each valid contour, the bounding box is used to crop the image from the original page.
- These cropped regions are saved as individual image files in an output folder.

### 5. 🧳 Packaging for Download
- After processing, all extracted images are compressed into a `.zip` file.
- A download button is provided to let the user download all extracted images at once.

### 6. 🌐 UI Display
- To avoid clutter, each extracted image is **resized using PIL’s `.thumbnail()`** method.
- Images are displayed in a grid layout using Streamlit’s column-based structure.
- Each displayed image includes a **download button**, allowing selective downloads if desired.

### 7. 🧹 Cleanup
- Temporary directories and files are managed using Python’s `tempfile` module.
- This ensures no clutter is left behind after the session ends.

---

## ⚙️ Setup Instructions

### 🔧 Requirements

Install all necessary dependencies:

```bash
pip install -r requirements.txt
```
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


