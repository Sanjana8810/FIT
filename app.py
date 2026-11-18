
import os
import io
import json

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError
from google import genai
from google.genai import types

from chatbot import get_bot_response


# ==========================================
# 1. LOAD CONFIGURATION
# ==========================================

load_dotenv()

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)

MODEL_NAME = "gemini-3.8-flash"


# ==========================================
# 2. FOOD RESPONSE STRUCTURE
# ==========================================

FOOD_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "food_name": {"type": "string"},
                    "estimated_grams": {"type": "number"},
                    "calories_per_100g": {"type": "number"},
                    "confidence": {"type": "string"}
                },
                "required": [
                    "food_name",
                    "estimated_grams",
                    "calories_per_100g",
                    "confidence"
                ]
            }
        },
        "notes": {"type": "string"}
    },
    "required": ["items", "notes"]
}
       
@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# 4. CHATBOT
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "Please enter a message."
        }), 400

    reply = get_bot_response(message)

    return jsonify({
        "reply": reply
    })

@app.route("/scan-food", methods=["POST"])
def scan_food():

    if client is None:
        return jsonify({
            "error": "Gemini API key is not configured. Please check your .env file."
        }), 503

    if "image" not in request.files:
        return jsonify({
            "error": "Please upload a food photograph."
        }), 400

    uploaded_file = request.files["image"]

    if not uploaded_file.filename:
        return jsonify({
            "error": "No image selected."
        }), 400

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if uploaded_file.mimetype not in allowed_types:
        return jsonify({
            "error": "Please upload a JPG, PNG or WEBP image."
        }), 400

    try:

        # Read image without saving it permanently

        image_bytes = uploaded_file.read()

        if not image_bytes:
            return jsonify({
                "error": "The uploaded image is empty."
            }), 

        image = Image.open(io.BytesIO(image_bytes))
        image.verify()

        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")

        if image.width * image.height > 16000000:
            return jsonify({
                "error": "Please upload a smaller-resolution image."
            }), 400

        # Prompt Gemini to inspect the entire plate

        prompt = """
        You are FITBOT's food recognition assistant.

        Carefully inspect the uploaded photograph of a meal.

        TASKS:

        1. Identify every clearly visible food item.
        2. Treat separate foods as separate items.
        3. For example, identify roti, rice, dal,
           gulab jamun and vegetables separately.
        4. Estimate the edible serving weight of
           each item in grams.
        5. Estimate calories per 100 grams using
           a reasonable standard food reference.
        6. Do not invent hidden food items.
        7. Do not claim exact weight from a photograph.
        8. If the image is unclear, express uncertainty
           through the confidence field.
        9. If no food is visible, return an empty items list.
        10. Do not include drinks or utensils as food.

        Return only the structured response.
        """

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=[
                prompt,
                image
            ],

            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=FOOD_SCHEMA,
                temperature=0.2
            )
        )

        # Convert Gemini response to Python data

        analysis = json.loads(response.text)

        detected_items = analysis.get("items", [])

        results = []

        total_grams = 0
        total_calories = 0

        # Calculate individual food nutrition

        for item in detected_items:

            name = str(
                item.get("food_name", "Unknown")
            ).strip()[:80]

            grams = float(
                item.get("estimated_grams", 0)
            )

            calories_per_100g = float(
                item.get("calories_per_100g", 0)
            )

            confidence = str(
                item.get("confidence", "low")
            ).lower()

            if confidence not in ["low", "medium", "high"]:
                confidence = "low"

            # Validate estimated values

            if not name:
                continue

            if not (0 < grams <= 5000):
                continue

            if not (0 <= calories_per_100g <= 1000):
                continue

            # Calculate calories

            calories = (
                grams * calories_per_100g / 100
            )

            food_result = {
                "food_name": name,
                "estimated_grams": round(grams, 1),
                "calories": round(calories),
                "confidence": confidence
            }

            results.append(food_result)

            total_grams += grams
            total_calories += calories

        return jsonify({

            "success": True,

            "items": results,

            "total_grams": round(total_grams, 1),

            "total_calories": round(total_calories),

            "notes": analysis.get(
                "notes",
                "Nutrition values are estimates."
            ),

            "disclaimer": (
                "Food weight and calories are approximate. "
                "A photograph cannot establish exact weight."
            )

        })

    except UnidentifiedImageError:

        return jsonify({
            "error": "The uploaded file is not a valid image."
        }), 400

    except json.JSONDecodeError:

        return jsonify({
            "error": "AI returned an unreadable result. Please try again."
        }), 502

    except Exception as error:

        app.logger.exception("Food scanning failed")

        return jsonify({
            "error": "Food analysis failed. Check your API configuration and try again."
        }), 500


# ==========================================
# 6. FILE SIZE ERROR
# ==========================================

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "error": "Image is too large. Maximum size is 8 MB."
    }), 413


# ==========================================
# 7. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
