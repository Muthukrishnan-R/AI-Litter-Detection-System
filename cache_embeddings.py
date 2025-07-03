import os
import json
from deepface import DeepFace

# Define paths
faces_db = "faces_db"
cache_file = "face_embeddings_cache.json"

# Dictionary to store embeddings
embeddings_cache = {}

# Loop through each person's folder
for person in os.listdir(faces_db):
    person_path = os.path.join(faces_db, person)
    if os.path.isdir(person_path):  # Ensure it's a folder
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            try:
                # Generate embedding
                embedding = DeepFace.represent(img_path, model_name="Facenet")[0]['embedding']
                embeddings_cache[img_path] = embedding  # Store in dictionary
                print(f"Processed {img_path}")
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

# Save embeddings to JSON
with open(cache_file, "w") as f:
    json.dump(embeddings_cache, f)

print("Face embeddings cached successfully!")
