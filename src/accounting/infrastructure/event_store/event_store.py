from sqlmodel import SQLModel, Session, create_engine, select, update
from src.accounting.infrastructure.event_store.models import Event
from datetime import datetime

class EventStore:
    def __init__(self, session: Session):
        self.session = session

    def append(self, events):
        for event in events:
            self.session.add(event)
        self.session.commit()

    def get_unpublished_events(self):
        return self.session.exec(select(Event).where(Event.published == False)).all()
    
    def mark_as_published(self, event_ids):
        self.session.exec(update(Event).where(Event.id.in_(event_ids)).values(published=True, published_at=datetime.now()))
        self.session.commit()