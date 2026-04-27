from src.accounting.domain.domain_event_publisher import DomainEventPublisher

class RabbitMQEventPublisher(DomainEventPublisher):
    """ Publisher for sending events to RabbitMQ """
