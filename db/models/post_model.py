from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Relationship
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from ..database import Base
from .mixins import Timestamp


class Post(Timestamp, Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String(250), nullable=False)
    blog = Column(JSON)
    categories = Column(ARRAY(Integer, ForeignKey("categories.id")))
    tags = Column(
        ARRAY(
            String,
        )
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    user = Relationship("User", back_populates="post")

    comments = Relationship(
        "PostComments",
        back_populates="post",
        uselist=True,
    )

    likes = Relationship(
        "PostLikes",
        back_populates="post",
        uselist=True,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__tablename__}, name: {self.title}"


class PostLikes(Timestamp, Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

    post = Relationship("Post", back_populates="likes")


class PostComments(Timestamp, Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(Text, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

    post = Relationship("Post", back_populates="comments")
