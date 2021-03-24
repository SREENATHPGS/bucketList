from . import DB_URL, Base, engine, session, InvalidUpdate, UserDetailsNotProvided, NoDataBaseSession
import os, secrets, string, json
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import backref, relationship

user_wishes_secondary_table = Table(
    'wishes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('account_user.id')),
    Column('wish_id', Integer, ForeignKey('wish.id'))
    )

alphabet = string.ascii_letters + string.digits
# class Admins(Base):
#     __tablename__ = "admins"
#     id = Column(Integer, primary_key = True)
#     username = Column(String(32), index = True)
#     password_hash = Column(String(128))
def getApiKey(length = 6):
    return ''.join(secrets.choice(alphabet) for i in range(length))

def formatify(ob):
    ob = json.loads(json.dumps(dict(ob), default=str))
    ob.pop('id')
    return ob


class Wish(Base):
    __tablename__ = "wish"
    id = Column(Integer, primary_key = True)
    wish = Column(Text, nullable=True)

class AccountUser(Base):
    __tablename__ = "account_user"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    username = Column(String(32), index = True, nullable = False, unique = True)
    password_hash = Column(String(128))
    email = Column(String(100), nullable = False, unique =  True)
    apikey = Column(String(64), unique = True, default = getApiKey(32))
    wishes = relationship("Wish", secondary = user_wishes_secondary_table)
    profile = relationship("Profile", uselist = False, lazy="joined", back_populates = "account_user")


    def create(self):
        session.add(self)
        session.commit()
        uid = self.uid
        session.close()

        return uid
        
    @staticmethod
    def update(uid, attribute_name, value):
        if not uid:
            raise UserDetailsNotProvided("Uid needed for patch.")

        if not attribute_name:
            raise UserDetailsNotProvided("Atlease one attribute name is needed for patching.")

        if attribute_name == "uid":
            raise InvalidUpdate("Uid cannot be modified.")

        if attribute_name == "username" and value is None:        
            raise InvalidUpdate("Usename cannot be none.")
        
        if attribute_name == "email" and value is None:
            raise InvalidUpdate("Email cannot be none.")

        user = AccountUser.get("single", uid)
        setattr(user, attribute_name, value)
        session.commit()


    @staticmethod
    def get(get_type = "all", uid = None):
        if get_type == "single":
            if uid:
                pass
            else:
                raise UserDetailsNotProvided("Uid needed for quering user data.")
        
            user = session.query(AccountUser).filter(AccountUser.uid == uid).first()
            return user
        else:
            return session.query(AccountUser).all()

    @staticmethod
    def delete(uid):
        user = AccountUser.get("single",uid)
        session.delete(user)
        session.commit()

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    profile_image = Column(Text)
    about = Column(Text)
    account_user_id = Column(Integer, ForeignKey('account_user.id'))
    account_user = relationship("AccountUser", back_populates = "profile")

    def create(self):
        pass

    def update(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    comment_text = Column(Text)
    reply_to = Column(Integer)
    user_id = Column(Integer, ForeignKey('account_user.id'))
    wish_id = Column(Integer, ForeignKey('wish.id'))

    def create(self):
        pass

    def update(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

class Reaction(Base):
    __tablename__ = "reaction"
    id = Column(Integer, primary_key = True)
    uid = Column(String(64), nullable=False, unique= True, default = getApiKey(16))
    reaction_type = Column(String(50))
    wish_id = Column(Integer, ForeignKey('wish.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))

    def create(self):
        pass

    def update(self):
        pass

    def get(self):
        pass

    def delete(self):
        pass

Base.metadata.create_all(engine)

if __name__ == "__main__":
    pass
