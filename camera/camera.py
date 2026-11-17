import cv2
import os
from datetime import datetime
import time

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return None

    # Let camera warm up (important!)
    time.sleep(2)

    # Capture multiple frames to stabilize focus
    for _ in range(10):
        ret, frame = cap.read()

    if not ret:
        print("❌ Failed to capture image")
        cap.release()
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vehicle_{timestamp}.jpg"

    save_path = os.path.join("static", "images", "captures", filename)

    # Save high quality image
    cv2.imwrite(save_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])

    cap.release()

    print(f"✅ High quality image saved: {save_path}")
    return save_path