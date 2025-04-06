# api/v1/item_routes.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from schemas.item import ItemCreate, ItemResponse, ItemBase
from services.item_service import create_new_item, fetch_item, update_item, remove_item
from db.session import get_db

router = APIRouter()


@router.post("/", response_model=ItemResponse)
def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    return create_new_item(db, item)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item_route(item_id: int, db: Session = Depends(get_db)):
    db_item = fetch_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item_route(item_id: int, item: ItemBase, db: Session = Depends(get_db)):
    updated_item = update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}")
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    if not remove_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}