from twilio.rest import Client

from project_m.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
)


def send_sms(to: str, body: str):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=body)


def batch_send_sms(to: list, body: str) -> list:
    status = []
    for phone in to:
        status.append(send_sms(phone, body).status)
    return status
