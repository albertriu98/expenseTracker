from abc import ABC, abstractmethod

class DomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, events):
        pass

