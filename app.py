import streamlit as st
import tempfile
import os
import zipfile
from PIL import Image
from pdf_image_extractor import extract_image_blocks

st.set_page_config(page_title="PDF Image Extractor", layout="wide")
st.title("📄 PDF Image Region Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        output_folder = os.path.join(tmpdir, "extracted_images")
        os.makedirs(output_folder, exist_ok=True)

        extract_image_blocks(pdf_path, output_folder)

        # 📦 ZIP all extracted images
        zip_path = os.path.join(tmpdir, "images.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)

        # 📥 ZIP download comes first
        with open(zip_path, "rb") as zf:
            st.download_button(
                label="📦 Download All Images as ZIP",
                data=zf,
                file_name="extracted_images.zip",
                mime="application/zip"
            )

        st.markdown("---")
        st.subheader("📸 Extracted Image Previews")

        image_files = sorted([
            f for f in os.listdir(output_folder) if f.lower().endswith((".jpg", ".png"))
        ])

        cols = st.columns(4)
        for i, image_file in enumerate(image_files):
            image_path = os.path.join(output_folder, image_file)
            img = Image.open(image_path)

            # Resize image for thumbnail preview
            thumbnail_size = (150, 150)
            img.thumbnail(thumbnail_size)

            with cols[i % 4]:
                st.image(img, caption=image_file, use_column_width=False)
                with open(image_path, "rb") as img_file:
                    st.download_button(
                        label="⬇ Download",
                        data=img_file,
                        file_name=image_file,
                        mime="image/jpeg"
                    )
