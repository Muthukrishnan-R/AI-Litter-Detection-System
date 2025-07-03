import os
import json
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from main import detection
from models import db, PastDetection
from flask_migrate import Migrate  # Import Flask-Migrate

UPLOAD_FOLDER = os.path.join('static/assets', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///detections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "Litter"
# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)


# Hardcoded login credentials (change as needed)
ADMIN_CREDENTIALS = {
    "admin": "password123"
}

# Load precomputed face embeddings at startup
cache_file = "face_embeddings_cache.json"
if os.path.exists(cache_file):
    with open(cache_file, "r") as f:
        embeddings_cache = json.load(f)
else:
    embeddings_cache = {}  # Empty cache if file doesn't exist

@app.route("/")
def index():
    if "user" not in session:  # Check if user is logged in
        return redirect(url_for("login"))  # Redirect to login page if not logged in
    
    img_filepath = session.get('uploaded_img_filepath', None)
    prediction = session.get('prediction', None)

    # Only remove image-related session keys
    session.pop('uploaded_img_filepath', None)
    session.pop('prediction', None)

    return render_template('index.html', image=img_filepath, flag=bool(img_filepath), prediction=prediction)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()  # Default to empty string
        password = request.form.get("password", "").strip()

        print(f"Entered Username: {username}")  # Debugging
        print(f"Entered Password: {password}")  # Debugging

        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session["user"] = username  # Store user in session
            return redirect(url_for("home"))
        else:
            print("Invalid login attempt!")  # Debugging
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        img = request.files.get("image")
        if img and allowed_file(img.filename):
            img_filename = secure_filename(img.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
            img.save(img_path)

            # Run detection
            prediction_text = detection(img_path, embeddings_cache)

            # Extract license plate and suspect name from the prediction
            license_plate = "Unknown"
            suspect_name = "Unknown"
            if "Reg No:" in prediction_text:
                license_plate = prediction_text.split("Reg No: ")[1].split(",")[0]
            if "Person:" in prediction_text:
                suspect_name = prediction_text.split("Person: ")[1]

            # Save to database
            new_detection = PastDetection(
                image_path=img_path,
                license_plate=license_plate,
                suspect_name=suspect_name
            )
            db.session.add(new_detection)
            db.session.commit()

            session['uploaded_img_filepath'] = img_path
            session['prediction'] = prediction_text

        return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/past_detections")
def past_detections():
    detections = PastDetection.query.order_by(PastDetection.timestamp.desc()).all()
    return render_template("past_detections.html", detections=detections)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
