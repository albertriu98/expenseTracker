from sqlmodel import Session, select, update
from src.accounting.src.infrastructure.event_store.models import Event
from datetime import datetime

class EventStore:
    def __init__(self, session: Session):
        self.session = session

    def append(self, events):
        for event in events:
            serialized = event.to_dict()
            self.session.add(Event(event_type=serialized['eventType'], 
                                   payload=str(serialized['payload']), 
                                   published=False))

    def get_unpublished_events(self):
        return self.session.exec(select(Event).where(Event.published == False)).all()
    
    def mark_as_published(self, event_ids):
        self.session.exec(update(Event).where(Event.id.in_(event_ids)).values(published=True, published_at=datetime.now()))
