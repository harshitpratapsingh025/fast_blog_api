from sqlalchemy.orm import Session
from db.models.users_model import Categories
from schemas.admin.category_schema import CategoryCreate, CategorySchema


def get_category(db: Session, category_id: int):
    return db.query(Categories).filter(Categories.id == category_id).first()


def get_all_categories(db: Session):
    return db.query(Categories).all()


def create_category(db: Session, category: CategoryCreate):
    db_category = Categories(
        name=category.name,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = db.query(Categories).filter(Categories.id == category_id).first()
    db.delete(category)
    db.commit()
    return category


def update_category(db: Session, category: CategorySchema):
    selected_category = (
        db.query(Categories).filter(Categories.id == category.id).first()
    )
    selected_category.name = category.name
    db.commit()
    return selected_category
