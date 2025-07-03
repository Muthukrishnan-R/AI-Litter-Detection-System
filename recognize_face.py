import os
import json
from deepface import DeepFace
from scipy.spatial.distance import cosine

# Load cached embeddings
cache_file = "face_embeddings_cache.json"
with open(cache_file, "r") as f:
    embeddings_cache = json.load(f)

def recognize_face(input_img):
    if not os.path.exists(input_img):
        print(f"❌ Error: File '{input_img}' not found! Make sure the image exists.")
        return None

    try:
        # Generate embedding for the new face
        input_embedding = DeepFace.represent(input_img, model_name="Facenet")[0]['embedding']
        
        best_match = None
        best_score = float("inf")  # Lower distance = better match

        # Compare with cached embeddings
        for img_path, cached_embedding in embeddings_cache.items():
            dist = cosine(input_embedding, cached_embedding)  # Cosine similarity
            
            if dist < best_score:  # Keep track of the best match
                best_score = dist
                best_match = img_path

        # Set a threshold for a valid match (adjust as needed)
        if best_match and best_score < 0.4:  
            print(f"✅ Match Found: {best_match}, Distance: {best_score}")
            return best_match
        else:
            print("❌ No match found in the database.")
            return None

    except Exception as e:
        print(f"Error in recognition: {e}")
        return None

# Example usage
input_image_path = "new_face.jpg"

# Check if file exists before running
if os.path.exists(input_image_path):
    recognize_face(input_image_path)
else:
    print("⚠️ new_face.jpg not found! Please provide an image.")
