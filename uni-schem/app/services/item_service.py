# services/item_service.py
from sqlalchemy.orm import Session
from repositories.item_repository import create_item, get_item, edit_item, delete_item
from schemas.item import ItemCreate, ItemBase


def create_new_item(db: Session, item: ItemCreate):
    return create_item(db, item)

def fetch_item(db: Session, item_id: int):
    return get_item(db, item_id)

def update_item(db: Session, item_id: int, item: ItemBase):
    return edit_item(db, item_id, item)

def remove_item(db: Session, item_id: int):
    return delete_item(db, item_id)