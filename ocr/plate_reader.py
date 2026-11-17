import easyocr
import cv2
import re
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Sharpen
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    sharp = cv2.filter2D(gray, -1, kernel)

    # Threshold
    _, thresh = cv2.threshold(sharp, 150, 255, cv2.THRESH_BINARY)

    return thresh

def read_number_plate(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not loaded")
        return None

    processed = preprocess_image(image)

    results = reader.readtext(processed)

    best_text = None
    best_conf = 0

    for box, text, conf in results:
        cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())

        if len(cleaned) >= 6 and conf > best_conf:
            best_text = cleaned
            best_conf = conf

    if best_text:
        print("✅ Detected:", best_text)
        return best_text

    print("❌ Plate not detected")
    return None