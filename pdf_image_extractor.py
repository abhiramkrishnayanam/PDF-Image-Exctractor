import fitz  # PyMuPDF for reading and rendering PDFs
import cv2  # OpenCV for image processing
import numpy as np  # For numerical operations on image arrays
import os  # For file and directory operations


def extract_image_blocks(pdf_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file using PyMuPDF
    pdf_file = fitz.open(pdf_path)
    total_images = 0  # Counter for total images extracted

    # Iterate through each page of the PDF
    for page_number in range(len(pdf_file)):
        # Render the page to an image with high resolution (300 DPI)
        pix = pdf_file[page_number].get_pixmap(dpi=300)
        img_data = pix.samples
        img_size = (pix.height, pix.width, pix.n)  # Image shape (height, width, channels)

        # Convert raw image data to NumPy array
        img_np = np.frombuffer(img_data, dtype=np.uint8).reshape(img_size)

        # Convert image to BGR format based on channel count
        if pix.n == 4:
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
        else:
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Convert the image to grayscale for thresholding
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply binary inverse threshold to highlight dark regions
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        # Detect external contours (potential image blocks)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img_count = 0  # Counter for images per page

        # Loop through all detected contours
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)  # Get bounding box of the contour

            # Filter out small regions to avoid noise (minimum 50x50 pixels)
            if w > 50 and h > 50:
                # Crop the region of interest from the original image
                roi = img_cv[y:y + h, x:x + w]

                # Construct file name and save the image as JPG
                save_path = os.path.join(output_folder, f"page{page_number + 1}_img{img_count + 1}.jpg")
                cv2.imwrite(save_path, roi)

                img_count += 1
                total_images += 1

    # Return the total number of images saved
    return total_images
