from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENROUTER_API_KEY")

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body')
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            answer = response['choices'][0]['message']['content']
            msg.body(answer)
        except Exception as e:
            msg.body("Sorry, there was an error.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
