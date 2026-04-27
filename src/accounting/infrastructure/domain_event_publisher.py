from src.accounting.domain.domain_event_publisher import DomainEventPublisher

class RabbitMQEventPublisher(DomainEventPublisher):
    """ Publisher for sending events to RabbitMQ. Persists it in Event Store. """
    def __init__(self):
        super().__init__()

    def handle(self, event):
        # Implementation for handling events
        pass
