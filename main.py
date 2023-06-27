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
    if (inb_msg == 'sos'):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful friend that will come up with a good excuse to get me out of an awkward situation. Make it sound like a real phone call to a friend."},
                {"role": "user", "content": inb_msg}
            ],
            temperature=1
        )

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            twiml=f"<Response><Say>{response['choices'][0].message.content}</Say></Response>",
            from_=os.getenv('MY_TWILIO_NUMBER'),
            to=os.getenv('ANTHONYS_NUMBER')
        )
        return str(call.sid)
    else:
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
            to=os.getenv('ANTHONYS_NUMBER')
        )

        return str(message.sid)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
