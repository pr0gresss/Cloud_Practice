import json
import os

from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient

from db import SessionLocal
from models import Feedback

load_dotenv()

CONNECTION_STRING = os.getenv("MESSAGE_QUEUE_READ_CONNECTION_STRING")
QUEUE_NAME = "dzmitrytsublianok"


def start_consumer():
    print("Consumer started")

    client = ServiceBusClient.from_connection_string(CONNECTION_STRING)

    receiver = client.get_queue_receiver(
        queue_name=QUEUE_NAME
    )

    with receiver:
        for message in receiver:

            try:
                body = str(message)

                print("Received message:", body)

                data = json.loads(body)

                db = SessionLocal()

                feedback = Feedback(
                    portfolioId=data["portfolioId"],
                    content=data["content"]
                )

                db.add(feedback)
                db.commit()

                receiver.complete_message(message)

                print("Feedback saved")

            except Exception as e:
                print("ERROR:", e)