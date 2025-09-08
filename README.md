# 🧾 CNIC Extractor (Smart CNIC OCR)

This project extracts details from **Pakistani Smart CNIC (Computerized National Identity Card)** using **OCR (Optical Character Recognition)**.  
It is built with **Python, EasyOCR, OpenCV, and Streamlit**, and can be deployed easily on **Streamlit Cloud** using GitHub.  

---

## Smart CNIC Extract Information APP Link:
  - https://smartcnicextractinfo.streamlit.app/

---

## 🚀 Features
- 📤 Upload Smart CNIC image (JPEG/PNG)  
- 🔍 Extracts important fields automatically:  
  - Identity Number  
  - Name  
  - Father Name  
  - Country of Stay  
  - Gender  
  - Date of Birth  
  - Date of Issue  
  - Date of Expiry  
- 📝 Shows extracted data in JSON format  
- ⬇️ Option to download extracted info as JSON file  
- ❌ Error handling for invalid / low-quality / Urdu-only CNICs  

---

## 🏗 Project Structure

  - app.py # Main Streamlit app
  - backend
    - utils
      - cnic_extractor.py # CNIC OCR & extraction logic
  - requirements.txt # Dependencies

---

## 📦 Requirements

### Requirements.txt contains:

  - streamlit
  - easyocr
  - opencv-python-headless
  - numpy
  - scipy

---

## 📸 Demo (UI Flow):

   - Upload CNIC Image
   - Extracted Info
   - Download JSON


<img width="1910" height="953" alt="smart_cnic_front_side" src="https://github.com/user-attachments/assets/4f934d5c-4df7-46c3-b287-acb964f55f55" />

--- 

## 🔒 Notes:

   - Works only with Smart CNIC (English format), not old Urdu-only CNICs.
   - Image must be clear and high-quality for best OCR results.
   - Uses EasyOCR (English + Urdu) but forces validation for Smart CNIC English layout.

---

## 👨‍💻 Author:

   - Developed by: **SYED IRTIZA ABBAS ZAIDI**
   - For learning & OCR-based automation projects.
