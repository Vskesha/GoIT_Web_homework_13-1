from datetime import datetime
from typing import Union

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(user: User, db: Session, skip: int, limit: int, favorite: Union[bool, None] = None):
    query = db.query(Contact).filter_by(user_id=user.id)
    if favorite is not None:
        query = query.filter_by(favorite=favorite)
    contact = query.offset(skip).limit(limit).all()
    return contact


async def get_contact_by_id(contact_id: int, db: Session, user: User):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def get_contact_by_email(email: str, db: Session, user: User):
    contact = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id)).first()
    return contact


async def create(body: ContactModel, db: Session, user: User):
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        comments=body.comments,
        favorite=body.favorite,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session, user: User):
    contact = await get_contact_by_id(contact_id, db, user)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.comments = body.comments
        contact.favorite = body.favorite
        db.commit()
    return contact


async def favorite_update(contact_id: int, body: ContactModel, db: Session, user: User):
    contact = await get_contact_by_id(contact_id, db, user)
    if contact:
        contact.favorite = body.favorite
        db.commit()
    return contact


async def delete(contact_id, db: Session, user: User):
    contact = await get_contact_by_id(contact_id, db, user)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session, user: User):
    contacts = db.query(Contact).filter_by(user_id=user.id).filter(
        func.lower(Contact.first_name).contains(func.lower(query)) |
        func.lower(Contact.last_name).contains(func.lower(query)) |
        func.lower(Contact.email).contains(func.lower(query))
    ).all()
    return contacts


async def search_birthday(par: dict, db: Session, user: User):
    days_param = par.get("days", 7)
    days = int(days_param)
    days += 1
    now = datetime.now().date()
    birthdays_contacts = []
    query = db.query(Contact).filter_by(user_id=user.id)
    contacts = query.offset(par.get("skip")).limit(par.get("limit"))

    for contact in contacts:
        birthday = contact.birthday
        if birthday:
            birthday_this_year = birthday.replace(year=now.year)
            days_until_birthday = (birthday_this_year - now).days
            if days_until_birthday in range(days):
                birthdays_contacts.append(contact)
    return birthdays_contacts
