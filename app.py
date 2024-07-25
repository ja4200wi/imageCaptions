from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
api_key = os.getenv('HUGGINGFACE_API_KEY')
server_api_key = os.getenv('FRONTEND_API_KEY')

if not api_key or not server_api_key:
    raise ValueError("Missing API key environment variables")

def image_to_model(image_bytes):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'Authorization' not in request.headers:
        return jsonify({"error": "Missing API key"}), 403

    request_api_key = request.headers['Authorization'].split(" ")[1]
    if request_api_key != server_api_key:
        return jsonify({"error": "Invalid API key"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image_bytes = file.read()
        description = image_to_model(image_bytes)
        return jsonify({"description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
