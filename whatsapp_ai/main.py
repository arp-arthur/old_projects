import os
from twilio.rest import Client
print(os.environ)
if not os.getenv('TWILIO_ACCOUNT_SID'):
    os.environ['TWILIO_ACCOUNT_SID'] = 'ACd8e597ddedfc9222bda2f1a7b26af51f'

if not os.getenv('TWILIO_AUTH_TOKEN'):
    os.environ['TWILIO_AUTH_TOKEN'] = 'd0d2e84a99671270db403c843b562d97'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

cliente = Client(account_sid, auth_token)

message = cliente.messages.create(
    body='Hello there!',
    from_='whatsapp:+14155238886',
    to='whatsapp:+5521992487710'
)

print(message.sid)