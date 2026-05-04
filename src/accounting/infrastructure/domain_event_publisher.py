from src.accounting.domain.domain_event_publisher import DomainEventPublisher
import pika

class RabbitMQEventPublisher(DomainEventPublisher):
    """ Publisher for sending events to RabbitMQ. Persists it in Event Store. """
    def __init__(self):
        super().__init__()

    def handle(self, event):
        # Here you would implement the logic to publish the event to RabbitMQ
        # For example, you could use the pika library to connect to RabbitMQ and publish the event
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='account_events')
        channel.basic_publish(exchange='', routing_key='account_events', body=str(event))
        connection.close()

    def publish(self, events):
        for event in events:
            self.handle(event)
