from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    county_code: str


class CountryCreate(CountryBase):
    pass


class CountrySchema(CountryBase):
    id: int

    class Config:
        orm_mode = True
