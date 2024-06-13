from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException

from db.database import get_db
from schemas.admin.country_schema import CountrySchema, CountryCreate
from serices.admin.country_services import (
    get_all_counties,
    delete_country,
    create_country,
    update_country,
)

router = APIRouter()


@router.get("/countries", response_model=List[CountrySchema])
async def get(db: Session = Depends(get_db)):
    return get_all_counties(db=db)


@router.post("/countries", response_model=CountrySchema, status_code=201)
async def create(country: CountryCreate, db: Session = Depends(get_db)):
    return create_country(db=db, country=country)


@router.delete("/countries/{country_id}", response_model=CountrySchema)
async def delete(country_id: int, db: Session = Depends(get_db)):
    return delete_country(db=db, country_id=country_id)


@router.put("/countries", response_model=CountrySchema)
async def update(country: CountrySchema, db: Session = Depends(get_db)):
    return update_country(db=db, country=country)
