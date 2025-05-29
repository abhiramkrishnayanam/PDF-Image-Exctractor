import streamlit as st
import tempfile
import os
import zipfile
from PIL import Image
from pdf_image_extractor import extract_image_blocks  # Custom image extraction module

# Page configuration
st.set_page_config(page_title="PDF Image Extractor", layout="wide")
st.title("📄 PDF Image Region Extractor")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Create a temporary directory to handle the uploaded PDF and outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded PDF to temporary path
        pdf_path = os.path.join(tmpdir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Folder to store extracted image regions
        output_folder = os.path.join(tmpdir, "extracted_images")
        os.makedirs(output_folder, exist_ok=True)

        # Extract image regions using your backend function
        extract_image_blocks(pdf_path, output_folder)

        # Create a ZIP file with all extracted images
        zip_path = os.path.join(tmpdir, "images.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        # Download button for the ZIP file
        with open(zip_path, "rb") as zf:
            st.download_button(
                label="📦 Download All Images as ZIP",
                data=zf,
                file_name="extracted_images.zip",
                mime="application/zip"
            )

        st.markdown("---")
        st.subheader("📸 Extracted Image Previews")

        # Sort and filter image files
        image_files = sorted([
            f for f in os.listdir(output_folder) if f.lower().endswith((".jpg", ".png"))
        ])

        # Display thumbnails in a grid layout (4 columns)
        cols = st.columns(4)
        for i, image_file in enumerate(image_files):
            image_path = os.path.join(output_folder, image_file)
            img = Image.open(image_path)

            # Resize image for display
            thumbnail_size = (150, 150)
            img.thumbnail(thumbnail_size)

            # Show image preview and individual download button
            with cols[i % 4]:
                st.image(img, caption=image_file, use_column_width=False)
                with open(image_path, "rb") as img_file:
                    st.download_button(
                        label="⬇ Download",
                        data=img_file,
                        file_name=image_file,
                        mime="image/jpeg"
                    )
