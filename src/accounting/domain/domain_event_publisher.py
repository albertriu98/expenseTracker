from abc import ABC, abstractmethod

class DomainEventPublisher(ABC):
    @abstractmethod
    def publish(self, events):
        pass
    
    def publish_many(self, events):
        for event in events:
            self.publish(event)
