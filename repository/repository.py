from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contacts
from src.schemas import ContactsModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Tag]:
    return db.query(Contacts).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contacts:
    return db.query(Contacts).filter(Contacts.id = contact_id).first()


async def create_contact(body: ContactsModel, db: Session) -> Contacts:
    contact = Contacts(name=body.name)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactsModel, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact