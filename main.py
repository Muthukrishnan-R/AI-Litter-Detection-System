from inference import get_model
import supervision as sv
import cv2
import pytesseract
from dotenv import load_dotenv
import os
import numpy as np
import re
import json
from scipy.spatial.distance import cosine
from twilio.rest import Client

from faker import Faker
from deepface import DeepFace

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load environment variables
load_dotenv()
roboflow_api_key = os.getenv("ROBOFLOW_API_KEY")
account_sid = os.getenv("SID")
auth_token = os.getenv("TOKEN")
faces_db_path = "D:/Litter - Copy/faces_db"  # Forward slashes
cache_file = "face_embeddings_cache.json"  # Cached embeddings file

# Validate environment variables
if not all([roboflow_api_key, account_sid, auth_token]):
    raise EnvironmentError("Missing required environment variables: ROBOFLOW_API_KEY, SID, or TOKEN.")

# Load the model
model = get_model('vehicle-littering-detection/5', api_key=roboflow_api_key)
fake = Faker('en_IN')

# Load cached face embeddings
if os.path.exists(cache_file):
    with open(cache_file, "r") as f:
        embeddings_cache = json.load(f)
else:
    embeddings_cache = {}

def detect_faces(image):
    """Detects faces in an image using OpenCV Haar cascade."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def recognize_face(face_crop, embeddings_cache):
    try:
        # Generate embedding for the new face
        input_embedding = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=False)[0]['embedding']
        
        best_match = None
        min_distance = float("inf")

        # Compare with cached embeddings
        for img_path, cached_embedding in embeddings_cache.items():
            dist = cosine(input_embedding, cached_embedding)  # Cosine similarity
            
            if dist < min_distance:
                min_distance = dist
                best_match = img_path.split(os.sep)[-2]  # Extract person name from path

        # Set a threshold for valid match
        return best_match if min_distance < 0.4 else "Unknown"

    except Exception as e:
        print(f"Error in face recognition: {e}")
        return "Unknown"

def detection(img_path, embeddings_cache):
    """Processes an image to detect vehicle littering and recognize persons."""
    image = cv2.imread(img_path)
    results = model.infer(image)[0]

    # Load detections into the supervision API
    detections = sv.Detections.from_inference(results)
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

    classes = detections.data['class_name']
    recognized_person = "Unknown"

    if all(item in classes for item in ["license", "waste"]):
        print(" Detection started")
        license_index = np.where(classes == 'license')[0][0]
        x, y, w, h = list(map(int, detections.xyxy[license_index]))
        plate_region = image[y:h, x:w]

        plate_text = pytesseract.image_to_string(plate_region, config='--psm 8')
        plain_text = re.sub(r'[^a-zA-Z0-9]', '', plate_text)
        print(f" Detected License Plate: {plain_text}")

        # Detect and recognize faces
        faces = detect_faces(image)
        best_face = None
        best_face_name = "Unknown"

        for (fx, fy, fw, fh) in faces:
            face_crop = image[fy:fy+fh, fx:fx+fw]
            person_name = recognize_face(face_crop, embeddings_cache)
            if person_name != "Unknown":
                best_face = (fx, fy, fw, fh)
                best_face_name = person_name
                break  # Stop at the first valid match

        # Draw bounding box only for the best match
        if best_face:
            fx, fy, fw, fh = best_face
            cv2.rectangle(annotated_image, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
            cv2.putText(annotated_image, best_face_name, (fx, fy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imwrite(img_path, annotated_image)

        # Send alert if a license plate is found
        if plain_text:
            getAlertapi("+917397529410", plain_text, best_face_name)
            return f" Vehicle Littering Detected. Reg No: {plain_text}, Person: {best_face_name}"
        else:
            return " License plate text could not be detected."

    return "No vehicle littering detected..!"

def generate_message():
    """Generates a fake location for alerts."""
    return fake.address()

def getAlertapi(number, plain_text, person_name):
    """Sends an SMS alert when littering is detected."""
    try:
        client = Client(account_sid, auth_token)
        location = generate_message()
        body = f" Alert!!! Vehicle no: {plain_text} is littering at Location: {location}. Suspect: {person_name}"
        message = client.messages.create(from_='+15674014325', body=body, to=number)
        print(" Message sent successfully. SID:", message.sid)
        return True
    except Exception as e:
        print(" Error while sending the message:", e)
        return False