from flask import Flask, render_template, request, jsonify
from chatbot import get_bot_response
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or not data.get("message"):
            return jsonify({
                "reply": "Please enter a message."
            }), 400
        message = data["message"]
        response = get_bot_response(message)
        return jsonify({
            "reply": response
        })
    except Exception as e:
        print("Chatbot Error:", e)
        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500
if __name__ == "__main__":
    app.run(debug=True)

