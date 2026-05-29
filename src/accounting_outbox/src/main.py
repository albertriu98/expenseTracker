import json
import time
import pika
from os import getenv

from datetime import datetime
from sqlmodel import Session, create_engine, select
from src.models import Event as Outbox


user = getenv("DB_USER")
password = getenv("DB_PASSWORD")
host = getenv("DB_HOST")
port = getenv("DB_PORT", "5432")
database = getenv("DB_NAME")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

# RabbitMQ
rabbit_conn = pika.BlockingConnection(
    pika.ConnectionParameters(host="rabbitmqcluster-sample.default.svc.cluster.local", port=5672, credentials=pika.PlainCredentials("default_user_UmoQHAU_j_gx7_i5UOE", "m4E0omMaLoj56n-v19s29dvjyADFr9tV"))
)

channel = rabbit_conn.channel()

channel.queue_declare(
    queue="events",
    durable=True
)

POLL_INTERVAL = 2
BATCH_SIZE = 50


def process_outbox():

    while True:
        try:
            with Session(engine) as session:

                stmt = (
                    select(Outbox)
                    .where(Outbox.published == False)
                    .limit(BATCH_SIZE)
                    .with_for_update(skip_locked=True)
                )

                rows = session.exec(stmt).all()

                if not rows:
                    time.sleep(POLL_INTERVAL)
                    continue

                for event in rows:

                    message = {
                        "id": str(event.id),
                        "event_type": event.event_type,
                        "payload": event.payload,
                    }

                    serialized = json.dumps(message)

                    # publish
                    channel.basic_publish(
                        exchange="",
                        routing_key=str(event.event_type),
                        body=serialized,
                        properties=pika.BasicProperties(
                            delivery_mode=2
                        ),
                    )

                    # mark published
                    event.published = True
                    event.published_at = datetime.now()

                session.commit()

                print(
                    f"Published {len(rows)} messages"
                )

        except Exception as e:
            print("Worker error:", e)
            time.sleep(5)


if __name__ == "__main__":
    process_outbox()