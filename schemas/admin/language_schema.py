from pydantic import BaseModel


class LanguageBase(BaseModel):
    name: str


class LanguageCreate(LanguageBase):
    pass


class LanguageSchema(LanguageBase):
    id: int

    class Config:
        orm_mode = True
