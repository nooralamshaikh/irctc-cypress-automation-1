import argparse
import numpy as np
from PIL import Image
import io
import base64
import easyocr
from flask import Flask, request, jsonify

reader = None

# Initialize Flask app
app = Flask(__name__)

def create_reader(use_gpu=False):
  return easyocr.Reader(
      ["en"],
      model_storage_directory="./EasyOCR",
      gpu=use_gpu,
      verbose=use_gpu,
  )

def extract_text_from_image(base64_image):
  try:
    if reader is None:
      return "Error processing image: OCR reader is not initialized"

    # Convert the base64 image to bytes
    image_bytes = base64.b64decode(base64_image[22:])
    # Create a BytesIO object from the image bytes
    image_buffer = io.BytesIO(image_bytes)
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(image_buffer)
    # Convert the image to grayscale (optional but can improve OCR accuracy)
    image = image.convert("L")

    # Convert PIL image to OpenCV format
    open_cv_image = np.array(image)

    result = reader.readtext(open_cv_image, detail=0)
    if result:
      return result[0].replace(" ", "")
    else:
      return "ABCDEF"
  except Exception as e:
    return f"Error processing image: {str(e)}"

@app.route("/extract-text", methods=["POST"])
def extract_text():
  # Get the base64 image from the request
  data = request.get_json()
  base64_image = data.get("image", "")

  if not base64_image:
    return jsonify({"error": "No base64 image string provided"}), 400

  extracted_text = extract_text_from_image(base64_image)
  return jsonify({"extracted_text": extracted_text})

@app.route('/')
def health_check():
  return "Server is running", 200

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Run the OCR extraction server."
  )
  parser.add_argument(
      "--host",
      type=str,
      default="0.0.0.0",
      help="Host address to run the server on (default: 0.0.0.0)",
  )
  parser.add_argument(
      "--port",
      type=int,
      default=5000,
      help="Port to run the server on (default: 5000)",
  )
  parser.add_argument(
      "--gpu",
      action="store_true",
      help="Use CUDA GPU acceleration if your PyTorch install supports it",
  )
  args = parser.parse_args()

  reader = create_reader(use_gpu=args.gpu)

  # Run Flask server
  app.run(host=args.host, port=args.port)
