from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import os
import time
import subprocess
from threading import Thread
import logging

app = Flask(__name__)

# CORS configuration: allow all origins and disable CORS checking
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FASTSAM_DIR = os.path.join(BASE_DIR, 'FastSAM')
IMAGES_DIR = os.path.join(FASTSAM_DIR, 'images')
OUTPUT_DIR = os.path.join(FASTSAM_DIR, 'output')
LATEST_IMAGE = os.path.join(IMAGES_DIR, 'latest.jpg')
SEGPREDICT_PATH = os.path.join(FASTSAM_DIR, 'segpredict.py')

# Python interpreter path for FastSAM environment
PYTHON_INTERPRETER = "/opt/anaconda3/envs/FastSAM/bin/python"

# Create directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def capture_image():
    while True:
        try:
            camera = cv2.VideoCapture(0)

            ret, frame = camera.read()
            if ret:
                cv2.imwrite(LATEST_IMAGE, frame)
                logging.info(f"Captured image saved to {LATEST_IMAGE}")
            else:
                logging.warning("Failed to capture image")
            camera.release()

            # Delete old images except the latest
            for img in os.listdir(IMAGES_DIR):
                if img != 'latest.jpg':
                    os.remove(os.path.join(IMAGES_DIR, img))

            time.sleep(60)  # Wait for 1 minute
        except Exception as e:
            logging.error(f"Error in capture_image: {e}")
            time.sleep(60)  # Wait before retrying

# Start the image capture thread
Thread(target=capture_image, daemon=True).start()

@app.route('/find_object', methods=['POST'])
def find_object():
    prompt = request.json['prompt']
    logging.info(f"Received prompt: {prompt}")

    try:
        # Run the segpredict.py script with the user's prompt
        command = [PYTHON_INTERPRETER, SEGPREDICT_PATH, "--prompt", prompt]
        logging.info(f"Running command: {' '.join(command)}")

        result = subprocess.run(
            command,
            cwd=FASTSAM_DIR,
            capture_output=True,
            text=True
        )

        logging.info(f"Command output: {result.stdout}")
        logging.error(f"Command error: {result.stderr}")

        if result.returncode != 0:
            error_msg = f"Error running segpredict.py: {result.stderr}"
            logging.error(error_msg)
            return jsonify({'error': error_msg}), 500

        # Send the output image
        output_image = os.path.join(OUTPUT_DIR, 'output.jpg')
        if os.path.exists(output_image):
            logging.info(f"Sending output image: {output_image}")
            return send_file(output_image, mimetype='image/jpeg')
        else:
            error_msg = 'Output image not found'
            logging.error(error_msg)
            return jsonify({'error': error_msg}), 404
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Unexpected error: {error_msg}")
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
