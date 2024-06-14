from sqlalchemy.orm import Session
from db.models.users_model import Languages
from schemas.admin.language_schema import LanguageCreate, LanguageSchema


def get_language(db: Session, language_id: int):
    return db.query(Languages).filter(Languages.id == language_id).first()


def get_all_languages(db: Session):
    return db.query(Languages).all()


def create_language(db: Session, language: LanguageCreate):
    db_language = Languages(
        name=language.name,
    )
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def delete_language(db: Session, language_id: int):
    language = db.query(Languages).filter(Languages.id == language_id).first()
    db.delete(language)
    db.commit()
    return language


def update_language(db: Session, language: LanguageSchema):
    selected_language = db.query(Languages).filter(Languages.id == language.id).first()
    selected_language.name = language.name
    db.commit()
    return selected_language
