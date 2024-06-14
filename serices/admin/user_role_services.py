from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.users_model import Role
from schemas.admin.user_role_schema import RoleCreate, RoleSchema


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_slug(db: Session, slug: str):
    return db.query(Role).filter(Role.slug == slug).first()


def get_all_roles(db: Session):
    return db.query(Role).all()


def create_role(db: Session, role: RoleCreate):
    db_role = Role(
        name=role.name,
        slug=role.slug,
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()
    db.delete(role)
    db.commit()
    return role


def update_role(db: Session, role: RoleSchema):
    slug = db.query(Role).filter(Role.id != role.id, Role.slug == role.slug).first()
    if slug:
        raise HTTPException(status_code=400, detail="Slug is already in use")
    selected_role = db.query(Role).filter(Role.id == role.id).first()
    selected_role.name = role.name
    selected_role.slug = role.slug
    db.commit()
    return selected_role
