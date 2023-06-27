import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def chatgpt():
    inb_msg = request.form['Body'].lower()
    print(inb_msg)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": inb_msg}
        ],
        temperature=0.7
    )

    resp = MessagingResponse()
    resp.message(response["choices"][0].message.content)
    print(response["choices"][0].message.content)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
