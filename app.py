# app.py
import os
from flask import Flask, render_template, request, jsonify
import requests
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.debug = True

UPLOAD_FOLDER = '/home/linuxhint/InstaCaptionGenrate/upload_images'  

# Define the allowed file extensions for uploaded images
# This list is used by the 'allowed_file' function
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

# Configure the upload folder and allowed extensions for uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the API details for AI model
API_URL = "https://api-inference.huggingface.co/models/prasanna2003/blip-image-captioning"
headers = {"Authorization": ""}

class AIResponseGenerator:
    def __init__(self):
        pass

    def generate_response(self, filename):
        """
        Generate a response from an AI model using the data from a file.

        This method reads data from the specified file, sends it to an AI model
        via an API request, and returns the response from the AI model.

        Args:
            filename (str): The name of the file containing data to be processed
                            by the AI model.

        Returns:
            dict: A dictionary containing the AI model's response or an error message.
                If the response is successful, it will have a 'response' key with the
                AI model's generated response. If there is an error, it will have an
                'error' key with an error description.
        """
        if not filename:
            return {'error': 'No filename provided'}
        
        try:
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=headers, data=data)
            response = response.json()
            return {'response': response}
        except Exception as e:
            return {'error': str(e)}
    
    

response_generator = AIResponseGenerator()


@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    """
    Check if a given filename has an allowed extension.

    This function checks whether the provided filename has an extension that is
    included in the list of allowed extensions.

    Args:
        filename (str): The name of the file to be checked.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Your Flask route
@app.route('/generate', methods=['POST'])
def generate_response():
    """
    Generate a caption for an uploaded image using an AI model.

    This function handles image uploads, validates the file format,
    saves the image to the server, generates a caption for the image
    using an AI model, and returns the caption.

    HTTP Status Codes:
        - 200: Successful processing and caption generation.
        - 400: Bad request due to no image uploaded or invalid file format.
        - 500: Internal server error due to an unexpected exception.
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        
        if image_file and allowed_file(image_file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
            image_file.save(filename)
            caption = response_generator.generate_response(filename)
            return jsonify({'caption': caption['response']}) 

        else:
            return jsonify({'error': 'Invalid file format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run()
