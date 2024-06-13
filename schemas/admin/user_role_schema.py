from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    slug: str


class RoleCreate(RoleBase):
    pass


class RoleSchema(RoleBase):
    id: int

    class Config:
        orm_mode = True
