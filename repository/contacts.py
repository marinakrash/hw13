from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contacts, User
from src.schemas import ContactsModel


async def get_contact(skip: int, limit: int, user: User, db: Session) -> List[Contacts]:
    return db.query(Contacts).filter(Contacts.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contacts:
    return db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()


async def create_contact(body: ContactsModel, user: User, db: Session) -> Contacts:
    contact = Contacts(name=body.name, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactsModel, user: User, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        contact.name = body.name
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(and_(Contacts.id == contact_id, Contacts.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
