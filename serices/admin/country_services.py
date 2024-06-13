from sqlalchemy.orm import Session
from db.models.users_model import Counties
from schemas.admin.country_schema import CountryCreate, CountrySchema


def get_country(db: Session, country_id: int):
    return db.query(Counties).filter(Counties.id == country_id).first()


def get_all_counties(db: Session):
    return db.query(Counties).all()


def create_country(db: Session, country: CountryCreate):
    db_country = Counties(
        name=country.name,
        county_code=country.county_code,
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def delete_country(db: Session, country_id: int):
    country = db.query(Counties).filter(Counties.id == country_id).first()
    db.delete(country)
    db.commit()
    return country


def update_country(db: Session, country: CountrySchema):
    selected_country = db.query(Counties).filter(Counties.id == country.id).first()
    selected_country.name = country.name
    selected_country.county_code = country.county_code
    db.commit()
    return selected_country
