import os
import time
from PIL import Image
# REMOVED: from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
import cv2
import numpy as np
import re
import hashlib
import shutil
import easyocr  # ✅ NEW FAST OCR MODEL

# Paths
RESERVATION_FOLDER = "/Users/mithunravi/Documents/Parking/reservation"
PROCESSED_FOLDER = os.path.join(RESERVATION_FOLDER, "processed")
OUTPUT_FILE = "/Users/mithunravi/Documents/Parking/reservation_extraction.txt"

# Clear processed folder at start
if os.path.exists(PROCESSED_FOLDER):
    shutil.rmtree(PROCESSED_FOLDER)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ✅ Load EasyOCR model (Fast + GPU supported)
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

# Device configuration (kept for structure, not used by EasyOCR)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Haar Cascade for number plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

def detect_plate_region(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 20))
    if len(plates) == 0:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    x, y, w, h = sorted(plates, key=lambda b: b[2]*b[3], reverse=True)[0]
    plate_img = img[y:y+h, x:x+w]
    return cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)

def upscale_image(img, scale=2):
    if img is None:
        return None
    h, w = img.shape[:2]
    if max(h, w) < 500:
        img = cv2.resize(img, (w*scale, h*scale), interpolation=cv2.INTER_CUBIC)
    return img

def format_plate_spacing(text):
    text = text.replace(" ", "")
    pattern = re.match(r"^([A-Z]{2})(\d{1,2})([A-Z]{1,3})(\d{3,4})$", text)
    if pattern:
        return " ".join(pattern.groups())
    else:
        return text

# ✅ UPDATED OCR PART ONLY — EVERYTHING ELSE SAME
def extract_text(image_path):
    img = detect_plate_region(image_path)
    if img is None:
        return None

    img = upscale_image(img)

    # Convert to numpy for EasyOCR
    img_np = np.array(img)

    try:
        results = reader.readtext(img_np, detail=0)
    except:
        return None

    if not results:
        return None

    text = " ".join(results)
    text = ''.join(ch for ch in text if ch.isalnum()).upper()
    text = text.strip()
    text = format_plate_spacing(text)
    return text

def save_text(text, file_path, existing_lines):
    if text not in existing_lines:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        existing_lines.add(text)

def get_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

print(f"👀 Watching folder: {RESERVATION_FOLDER}\n")

file_hashes = {}

# Load existing extracted lines to avoid duplicates
existing_lines = set()
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        existing_lines = set(line.strip() for line in f)

while True:
    try:
        # Only scan images directly in RESERVATION_FOLDER (exclude processed folder)
        files = sorted([
            f for f in os.listdir(RESERVATION_FOLDER)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
            and not os.path.exists(os.path.join(PROCESSED_FOLDER, f))
        ])

        for file_name in files:
            file_path = os.path.join(RESERVATION_FOLDER, file_name)
            current_hash = get_file_hash(file_path)
            if current_hash is None:
                continue
            if file_name in file_hashes and file_hashes[file_name] == current_hash:
                continue
            file_hashes[file_name] = current_hash

            try:
                text = extract_text(file_path)
                if text:
                    line = f"{file_name} - {text}"
                    print(f"✅ {line}")
                    save_text(line, OUTPUT_FILE, existing_lines)
                else:
                    print(f"⚠️ No text detected in {file_name}")

                # Move file to processed folder
                os.rename(file_path, os.path.join(PROCESSED_FOLDER, file_name))
                print(f"🗂 Moved {file_name} to processed folder")

            except Exception as e:
                print(f"❌ Error processing {file_name}: {e}")

        time.sleep(1)  # Slightly faster polling

    except KeyboardInterrupt:
        print("\n🛑 Exiting watcher.")
        break

def run_plate_extraction_for_violations():
    try:
        # your entire OCR logic that processes images in reservation folder
        print("🔍 Running violation OCR extraction...")
        process_reservation_images()   # <--- this should be your main OCR function
        print("✔️ Extraction complete.")
    except Exception as e:
        print(f"❌ OCR Error: {e}")
