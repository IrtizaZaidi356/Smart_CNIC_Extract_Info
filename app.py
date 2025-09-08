import streamlit as st
import cv2
import numpy as np
import json
from backend.utils.cnic_extractor import extract_cnic_info

st.set_page_config(page_title="CNIC Extractor", page_icon="🧾", layout="centered")

st.title("🧾 Smart CNIC Extractor")

uploaded_file = st.file_uploader("Please upload the front side of your CNIC to extract details.", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert file → OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    with st.spinner("Extracting CNIC details..."):
        try:
            data = extract_cnic_info(image)
            st.success(data["message"])

            st.subheader("📋 Extracted CNIC Info")
            st.json(data["data"])

            # Download JSON
            json_str = json.dumps(data["data"], indent=2)
            st.download_button(
                label="⬇️ Download Extracted Info (JSON)",
                data=json_str,
                file_name="cnic_info.json",
                mime="application/json"
            )

        except ValueError as e:
            st.error(str(e))
        except Exception as ex:
            st.error(f"❌ Unexpected error: {str(ex)}")





