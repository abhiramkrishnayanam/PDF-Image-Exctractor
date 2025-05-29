import streamlit as st
import tempfile
import os
import zipfile
from PIL import Image
from pdf_image_extractor import extract_image_blocks

st.set_page_config(page_title="PDF Image Region Extractor", layout="wide")

st.title("📄 Extract Image Blocks from PDF")

uploaded_pdf = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_pdf:
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, uploaded_pdf.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        output_folder = os.path.join(temp_dir, "detected_new_images")

        with st.spinner("🔍 Processing PDF to extract image blocks..."):
            count = extract_image_blocks(pdf_path, output_folder)

        if count == 0:
            st.warning("⚠️ No image blocks were detected.")
        else:
            st.success(f"✅ {count} image block(s) extracted!")

            # Display images in a grid
            image_files = sorted(os.listdir(output_folder))
            cols = st.columns(4)
            for idx, img_file in enumerate(image_files):
                col = cols[idx % 4]
                img_path = os.path.join(output_folder, img_file)
                with col:
                    st.image(img_path, caption=img_file, width=120)
                    with open(img_path, "rb") as img_bin:
                        st.download_button(
                            label="⬇️ Download",
                            data=img_bin,
                            file_name=img_file,
                            mime="image/jpeg",
                            key=f"download_{img_file}"
                        )

            # Create ZIP
            zip_path = os.path.join(temp_dir, "detected_new_images.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for img_file in image_files:
                    file_path = os.path.join(output_folder, img_file)
                    zipf.write(file_path, arcname=img_file)

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download All as ZIP",
                    data=f,
                    file_name="detected_new_images.zip",
                    mime="application/zip"
                )
