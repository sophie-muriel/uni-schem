# repositories/item_repository.py
# from sqlalchemy.orm import Session
# from sqlalchemy import delete, update
# from app.models.item import Item
# from schemas.item import ItemCreate, ItemBase


# def create_item(db: Session, item: ItemCreate):
#     db_item = Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def get_item(db: Session, item_id: int):
#     return db.query(Item).filter(Item.id == item_id).first()

# def edit_item(db: Session, item_id: int, item: ItemBase):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if not db_item:
#         return None
#     db.query(Item).filter(Item.id == item_id).update(item.dict())
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def delete_item(db: Session, item_id: int):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if not db_item:
#         return False
#     db.delete(db_item)
#     db.commit()
#     return True
