from flask import Flask, request, jsonify
import openai
import os
import os
print("------ DEBUG BAŞLADI ------")
print("API KEY:", os.getenv("OPENAI_API_KEY"))
print("------ DEBUG BİTTİ ------")
app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "KankaGPT aktif!"

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    user_input = req.get("queryResult", {}).get("queryText", "")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
    import traceback
    print("❌ OpenAI HATASI:", e)
    traceback.print_exc()
    reply = f"Bir hata oldu kanka: {str(e)}"

    return jsonify({"fulfillmentText": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
