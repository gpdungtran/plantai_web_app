# feedback.py - lưu đánh giá người dùng
import os
import json
from datetime import datetime

def save_feedback(username, image_bytes, prediction, is_correct, location):
    """
    print("save_feedback")    
    folder = "data/records"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"{folder}/{username}_{timestamp}.jpg"
    json_filename = f"{folder}/{username}_{timestamp}.json"

    with open(img_filename, "wb") as f:
        f.write(image_bytes)

    record = {
        "user": username,
        "time": timestamp,
        "prediction": prediction,
        "correct": is_correct,
        "location": location,
        "image_path": img_filename
    }
    with open(json_filename, "w") as f:
        json.dump(record, f, indent=2)

    """
