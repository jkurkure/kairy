# type: ignore

from twilio.rest import Client
from nicegui import app

if app.is_started:
    from phone_iso3166.country import *
    import pycountry, env


def where(number):
    try:
        c = phone_country(number)

        country = pycountry.countries.get(alpha_2=c)
        return (country.flag, country.name)
    except:
        return ("", "")


class SMS:
    account_sid = "AC5ce5fa61d05a0d54a9c84c3f9401acae"
    auth_token = env.secret("twilio token")
    twilio_number = "twilio_number"

    # Create Twilio client
    client = Client(account_sid, auth_token)

    def sendOTP(OTP, recipient):
        # Send SMS
        # in body part you have to write your message
        message = SMS.client.messages.create(
            body=f"Use the OTP {OTP} to verify your phone number for Kairy",
            from_=SMS.twilio_number,
            to=recipient,
        )

        print(f"Message sent to {recipient} with SID: {message.sid}")
