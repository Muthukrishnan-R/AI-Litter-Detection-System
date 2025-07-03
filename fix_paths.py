import os
from app import app, db
from models import PastDetection

def fix_existing_image_paths():
    with app.app_context():
        # Fetch all PastDetection entries
        detections = PastDetection.query.all()
        
        # Iterate through each entry
        for detection in detections:
            # Convert backslashes to forward slashes
            detection.image_path = detection.image_path.replace("\\", "/")
            
            # Extract the relative path from the `static` folder
            static_folder = os.path.join(app.root_path, 'static').replace("\\", "/")
            if static_folder in detection.image_path:
                detection.image_path = detection.image_path.replace(static_folder + "/", "")
        
        # Commit changes to the database
        db.session.commit()
        print("Database entries updated successfully!")

if __name__ == "__main__":
    fix_existing_image_paths()