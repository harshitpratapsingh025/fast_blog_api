from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Relationship

from ..database import Base
from .mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(250), nullable=False)
    is_active = Column(Boolean, default=True)

    profile = Relationship(
        "UserProfile", back_populates="user", passive_deletes=True, uselist=False
    )
    roles = Relationship(
        "Role",
        secondary="user_roles",
        back_populates="user",
        passive_deletes=True,
        uselist=True,
    )
    interests = Relationship(
        "Categories",
        secondary="user_interest",
        back_populates="user_intrested",
        passive_deletes=True,
        uselist=True,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.email}"


class UserProfile(Timestamp, Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    education = Column(String(80), nullable=True)
    addess = Column(Text, nullable=True)
    city = Column(String(80), nullable=True)
    state = Column(String(80), nullable=True)
    pincode = Column(String(10), nullable=True)
    image = Column(String(250), nullable=True)
    language_id = Column(
        Integer, ForeignKey("languages.id"), nullable=False, index=True
    )
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
    )

    user = Relationship("User", back_populates="profile")
    country = Relationship("Counties", back_populates="profile")
    language = Relationship("Languages", back_populates="profile")

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.city}"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    slug = Column(String(80), nullable=False, unique=True)

    user = Relationship(
        "User", secondary="user_roles", back_populates="roles", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"


class UserRole(Timestamp, Base):
    __tablename__ = "user_roles"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )


class Counties(Base):

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    county_code = Column(String(5), nullable=False)

    profile = Relationship("UserProfile", back_populates="country", uselist=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"


class Languages(Base):

    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)

    profile = Relationship("UserProfile", back_populates="language", uselist=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"


class Categories(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)

    user_intrested = Relationship(
        "User",
        secondary="user_interest",
        back_populates="interests",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"


class UserInterest(Base):

    __tablename__ = "user_interest"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"


class UserFollowing(Base):

    __tablename__ = "user_following"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.name}"
