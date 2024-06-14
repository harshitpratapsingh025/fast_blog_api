from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException

from db.database import get_db
from schemas.admin.country_schema import CountrySchema, CountryCreate
from schemas.admin.language_schema import LanguageCreate, LanguageSchema
from schemas.admin.user_role_schema import RoleCreate, RoleSchema
from serices.admin import country_services, language_services, user_role_services
from db.models.users_model import Role

router = APIRouter()


# Country routes
@router.get("/countries", response_model=List[CountrySchema])
async def get(db: Session = Depends(get_db)):
    return country_services.get_all_counties(db=db)


@router.post("/countries", response_model=CountrySchema, status_code=201)
async def create(country: CountryCreate, db: Session = Depends(get_db)):
    return country_services.create_country(db=db, country=country)


@router.delete("/countries/{country_id}", response_model=CountrySchema)
async def delete(country_id: int, db: Session = Depends(get_db)):
    return country_services.delete_country(db=db, country_id=country_id)


@router.put("/countries", response_model=CountrySchema)
async def update(country: CountrySchema, db: Session = Depends(get_db)):
    return country_services.update_country(db=db, country=country)


# Language routes
@router.get("/languages", response_model=List[LanguageSchema])
async def get(db: Session = Depends(get_db)):
    return language_services.get_all_languages(db=db)


@router.post("/languages", response_model=LanguageSchema, status_code=201)
async def create(language: LanguageCreate, db: Session = Depends(get_db)):
    return language_services.create_language(db=db, language=language)


@router.delete("/languages/{language_id}", response_model=LanguageSchema)
async def delete(language_id: int, db: Session = Depends(get_db)):
    return language_services.delete_language(db=db, language_id=language_id)


@router.put("/languages", response_model=LanguageSchema)
async def update(language: LanguageSchema, db: Session = Depends(get_db)):
    return language_services.update_language(db=db, language=language)


# Role routes
@router.get("/role", response_model=List[RoleSchema])
async def get(db: Session = Depends(get_db)):
    return user_role_services.get_all_roles(db=db)


@router.post("/role", response_model=RoleSchema, status_code=201)
async def create(role: RoleCreate, db: Session = Depends(get_db)):
    try:
        db_role = user_role_services.get_role_by_slug(db=db, slug=role.slug)
        if db_role:
            raise HTTPException(status_code=400, detail="Slug is already in use")
        return user_role_services.create_role(db=db, role=role)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.delete("/role/{role_id}", response_model=RoleSchema)
async def delete(role_id: int, db: Session = Depends(get_db)):
    return user_role_services.delete_role(db=db, role_id=role_id)


@router.put("/role", response_model=RoleSchema)
async def update(role: RoleSchema, db: Session = Depends(get_db)):
    return user_role_services.update_role(db=db, role=role)
