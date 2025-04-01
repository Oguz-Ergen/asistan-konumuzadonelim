from flask import Flask, request, jsonify
import openai
import os
import traceback

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "KankaGPT Webhook Aktif!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    print("📥 Gelen veri:", req)

    user_input = req.get("queryResult", {}).get("queryText", "")
    print("💬 Kullanıcı mesajı:", user_input)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI HATASI:", e)
        traceback.print_exc()
        reply = f"Bende bir hata oldu kanka: {str(e)}"

    return jsonify({"fulfillmentText": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
