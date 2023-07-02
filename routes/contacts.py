from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactsModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactsResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contacts= await repository_contacts.get_contact(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactsResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.post("/", response_model=ContactsResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))]))
async def create_contact(body: ContactsModel, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactsResponse)
async def update_contact(body: ContactsModel, contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactsResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


