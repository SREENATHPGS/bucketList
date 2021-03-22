from . import DB_URL, Base, engine, Session
import os
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import backref, relationship, sessionmaker

user_wishes_secondary_table = Table(
    'wishes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('account_user.id')),
    Column('wish_id', Integer, ForeignKey('wish.id'))
    )

# class Admins(Base):
#     __tablename__ = "admins"
#     id = Column(Integer, primary_key = True)
#     username = Column(String(32), index = True)
#     password_hash = Column(String(128))

class Wish(Base):
    __tablename__ = "wish"
    id = Column(Integer, primary_key = True)
    wish = Column(Text, nullable=True)

class AccountUser(Base):
    __tablename__ = "account_user"
    id = Column(Integer, primary_key = True)
    username = Column(String(32), index = True)
    password_hash = Column(String(128))
    email = Column(String(100))
    apikey = Column(String(64))
    wishes = relationship("Wish", secondary = user_wishes_secondary_table)
    profile = relationship("Profile", uselist = False, back_populates = "account_user")

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key = True)
    profile_image = Column(Text)
    about = Column(Text)
    account_user_id = Column(Integer, ForeignKey('account_user.id'))
    account_user = relationship("AccountUser", back_populates = "profile")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key = True)
    comment_text = Column(Text)
    reply_to = Column(Integer)
    user_id = Column(Integer, ForeignKey('account_user.id'))
    wish_id = Column(Integer, ForeignKey('wish.id'))

class Reaction(Base):
    __tablename__ = "reaction"
    id = Column(Integer, primary_key = True)
    reaction_type = Column(String(50))
    wish_id = Column(Integer, ForeignKey('wish.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))

Base.metadata.create_all(engine)

if __name__ == "__main__":
    pass
