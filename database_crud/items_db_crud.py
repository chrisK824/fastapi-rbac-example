import schemas as schemas
from db_models import Item
from sqlalchemy.orm import Session


def create_item(db: Session, item: schemas.ItemIn):
    item = Item(
        name=item.name
    )
    db.add(item)
    db.commit()
    return item


def get_items(db: Session):
    items = list(db.query(Item).all())
    return items


def delete_item(db: Session, item_id: int):
    item_cursor = db.query(Item).filter(
        Item.id == item_id)
    if not item_cursor.first():
        raise ValueError(
            f"There is no item with ID {item_id}")
    else:
        item_cursor.delete()
        db.commit()


def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdate):
    item = db.query(Item).filter(
        Item.id == item_id).first()

    if not item:
        raise ValueError(
            f"There isn't any item with ID {item_id}")

    updated_item = item_update.dict(exclude_unset=True)
    for key, value in updated_item.items():
        setattr(item, key, value)
    db.commit()
    return item
