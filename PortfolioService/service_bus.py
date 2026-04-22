import json
import os

from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

CONNECTION_STRING = os.getenv("MESSAGE_QUEUE_WRITE_CONNECTION_STRING")
QUEUE_NAME = "dzmitrytsublianok"


def send_feedback_message(payload: dict):

    client = ServiceBusClient.from_connection_string(CONNECTION_STRING)

    sender = client.get_queue_sender(
        queue_name=QUEUE_NAME
    )

    with sender:
        message = ServiceBusMessage(json.dumps(payload))
        sender.send_messages(message)

    print("Message sent")