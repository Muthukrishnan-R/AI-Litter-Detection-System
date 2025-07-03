from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

account_sid = os.getenv("SID")
auth_token = os.getenv("TOKEN")

# Debug print statements
print(f"SID: {account_sid}")
print(f"TOKEN: {auth_token}")

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='+18644419915',
    body='Test message from Twilio!',
    to='+919363094155'
)

print(message.sid)
