from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "KankaGPT aktif!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_input = req.get("queryResult", {}).get("queryText", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"fulfillmentText": reply})