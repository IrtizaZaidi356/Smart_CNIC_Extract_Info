import easyocr
import numpy as np
import re
import cv2
from scipy.spatial import distance
from collections import OrderedDict
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize OCR with Urdu + English
reader = easyocr.Reader(['en', 'ur'])

# Normalized coordinates for each field (Smart CNIC layout)
field_coords = {
    'Name': [[0.28, 0.27], [0.42, 0.27], [0.42, 0.32], [0.28, 0.32]],
    'Father Name': [[0.29, 0.45], [0.5, 0.45], [0.5, 0.51], [0.29, 0.51]],
    'Country of Stay': [[0.32, 0.63], [0.6, 0.63], [0.6, 0.67], [0.32, 0.67]],
    'Gender': [[0.66, 0.86], [0.75, 0.86], [0.75, 0.91], [0.66, 0.91]],
    'Identity Number': [[0.36, 0.13], [0.7, 0.13], [0.7, 0.18], [0.36, 0.18]],
    'Date of Birth': [[0.53, 0.75], [0.64, 0.75], [0.64, 0.8], [0.53, 0.8]],
    'Date of Issue': [[0.28, 0.85], [0.4, 0.85], [0.4, 0.91], [0.28, 0.91]],
    'Date of Expiry': [[0.53, 0.86], [0.65, 0.86], [0.65, 0.91], [0.53, 0.91]],
}

def normalize(img, result):
    h, w = img.shape[:2]
    return [([[pt[0]/w, pt[1]/h] for pt in bbox], text) for bbox, text, _ in result]

def calculate_distance(box1, box2):
    return sum(distance.euclidean(pt1, pt2) for pt1, pt2 in zip(box1, box2))

def extract_cnic_info(image):
    result = reader.readtext(image)
    raw_text_blocks = [t for _, t, _ in result]
    text_combined = " ".join(raw_text_blocks).lower()

    # Urdu presence detection
    urdu_regex = re.compile(r'[\u0600-\u06FF]')
    contains_urdu = any(urdu_regex.search(t) for t in raw_text_blocks)

    # CNIC number pattern
    cnic_match = re.search(r'\d{5}-\d{7}-\d{1}', text_combined)

    # English keyword presence
    english_keywords = ['republic', 'identity', 'card', 'pakistan', 'nadra']
    contains_english = any(kw in text_combined for kw in english_keywords)

    # Decision block
    if cnic_match:
        if contains_urdu and not contains_english:
            raise ValueError("⚠️ Your CNIC is valid but in the Urdu format. Please upload the latest Smart CNIC (English version).")
    elif not contains_english:
        raise ValueError("❌ Your ID Card is invalid. Only Pakistani Smart CNICs are accepted.")
    else:
        raise ValueError("⚠️ Your CNIC image is unclear. Please upload a high-quality image of your Smart CNIC.")


    # Begin Smart CNIC field extraction
    norm_results = normalize(image, result)
    temp_output = {}

    for field, template_box in field_coords.items():
        min_distance = float('inf')
        best_text = ""
        for ocr_box, ocr_text in norm_results:
            dist = calculate_distance(template_box, ocr_box)
            if dist < min_distance:
                min_distance = dist
                best_text = ocr_text.strip()
        temp_output[field] = best_text if best_text and len(best_text) >= 2 else ""

    temp_output['Country of Stay'] = "Pakistan"

    all_text = " ".join(raw_text_blocks)
    if not re.match(r'\d{5}-\d{7}-\d{1}', temp_output['Identity Number']):
        match_id = re.search(r'\d{5}-\d{7}-\d{1}', all_text)
        temp_output['Identity Number'] = match_id.group(0) if match_id else ""

    if temp_output['Gender'].lower() not in ['m', 'male', 'f', 'female']:
        g_match = re.search(r'\b(Male|Female|M|F)\b', all_text, re.IGNORECASE)
        if g_match:
            g = g_match.group(0).lower()
            temp_output['Gender'] = 'M' if 'm' in g else 'F'
        else:
            temp_output['Gender'] = ""

    # Date extraction
    dates = re.findall(r'\d{2}[-/.]\d{2}[-/.]\d{4}', all_text)
    temp_output['Date of Birth'] = ""
    temp_output['Date of Issue'] = ""
    temp_output['Date of Expiry'] = ""
    if dates:
        if len(dates) >= 3:
            temp_output['Date of Birth'] = dates[0]
            temp_output['Date of Issue'] = dates[1]
            temp_output['Date of Expiry'] = dates[2]
        elif len(dates) == 2:
            temp_output['Date of Birth'] = dates[0]
            temp_output['Date of Issue'] = dates[1]
        elif len(dates) == 1:
            temp_output['Date of Birth'] = dates[0]

    # Final cleanup
    cleaned_output = {}
    for field, value in temp_output.items():
        if not isinstance(value, str):
            cleaned_value = ""
        else:
            cleaned_value = (
                value.replace("Date ol Birth", "")
                     .replace("Dale", "")
                     .replace("Date ol [ 4piry", "")
                     .replace("Date of IssUE", "")
                     .strip()
            )
            if field in ['Date of Birth', 'Date of Issue', 'Date of Expiry']:
                if not re.match(r'\d{2}[-/.]\d{2}[-/.]\d{4}', cleaned_value):
                    cleaned_value = ""
            if field == 'Name' and cleaned_value.lower() == 'name':
                cleaned_value = ""
        cleaned_output[field] = cleaned_value

    # Maintain order
    ordered_output = OrderedDict()
    for key in [
        "Identity Number", "Name", "Father Name", "Country of Stay",
        "Gender", "Date of Birth", "Date of Issue", "Date of Expiry"
    ]:
        ordered_output[key] = cleaned_output.get(key, "")

    return {
        "message": "✅ Your CNIC has been successfully uploaded and processed.",
        "data": ordered_output
    }
