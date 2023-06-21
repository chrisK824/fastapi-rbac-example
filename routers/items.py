import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from authentication import PermissionChecker
from permissions.models_permissions import Items
from database import get_db
from database_crud import items_db_crud as db_crud
from schemas import ItemIn, Item, ItemUpdate

router = APIRouter(prefix="/v1")


@router.post("/items",
             dependencies=[Depends(PermissionChecker([Items.permissions.CREATE]))],
             response_model=Item, summary="Create a new item",
             tags=["Items"])
def create_item(item: ItemIn, db: Session = Depends(get_db)):
    """
    Creates a new item.
    """
    try:
        item_created = db_crud.create_item(db, item)
        return item_created
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.get("/items",
            dependencies=[Depends(PermissionChecker([Items.permissions.READ]))],
            response_model=List[Item], summary="Get all items",
            tags=["Items"])
def get_items(db: Session = Depends(get_db)):
    """
    Returns all items.
    """
    try:
        items = db_crud.get_items(db)
        return items
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.delete("/items/{item_id}",
               dependencies=[Depends(PermissionChecker([Items.permissions.DELETE]))],
               summary="Delete an item", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Deletes an item.
    """
    try:
        db_crud.delete_item(db, item_id)
        return {"result": f"Item with ID {item_id} has been deleted successfully!"}
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.patch("/items/{item_id}",
              dependencies=[Depends(PermissionChecker([Items.permissions.READ, Items.permissions.UPDATE]))],
              response_model=Item,
              summary="Update an item", tags=["Items"])
def update_operating_spot(item_id: int, item_update: ItemUpdate,
                          db: Session = Depends(get_db)):
    """
    Updates an item.
    """
    try:
        item = db_crud.update_item(db, item_id, item_update)
        return item
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


