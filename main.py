import os
import openai
from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv


load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
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

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=response["choices"][0].message.content,
        from_=os.getenv('MY_TWILIO_NUMBER'),
        to=request.form['From']
    )

    return str(message)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
