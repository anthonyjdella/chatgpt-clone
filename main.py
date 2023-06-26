from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def chatgpt():
    inb_msg = request.form['Body'].lower()
    print(inb_msg)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inb_msg,
        max_tokens=3000,
        temperature=0.7
    )

    resp = MessagingResponse()
    resp.message(response["choices"][0]["text"])
    print(response["choices"][0]["text"])

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
