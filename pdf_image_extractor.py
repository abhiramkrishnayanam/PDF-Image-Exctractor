import fitz  # PyMuPDF
import cv2
import numpy as np
import os

def extract_image_blocks(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    pdf_file = fitz.open(pdf_path)
    total_images = 0

    for page_number in range(len(pdf_file)):
        pix = pdf_file[page_number].get_pixmap(dpi=300)
        img_data = pix.samples
        img_size = (pix.height, pix.width, pix.n)
        img_np = np.frombuffer(img_data, dtype=np.uint8).reshape(img_size)

        if pix.n == 4:
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
        else:
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_count = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 50 and h > 50:
                roi = img_cv[y:y+h, x:x+w]
                save_path = os.path.join(output_folder, f"page{page_number+1}_img{img_count+1}.jpg")
                cv2.imwrite(save_path, roi)
                img_count += 1
                total_images += 1

    return total_images
