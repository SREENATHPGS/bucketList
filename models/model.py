from app import app, db

user_wishes_secondary_table = db.Table(
    'wishes',
    db.Column('user_id', db.Integer, db.ForeignKey('account_qquser.id'), primary_key = True),
    db.Column('wish_id', db.Integer, db.ForeignKey('wish.id'), primary_key = True)
    )

# class Admins(db.Model):
#     __tablename__ = "admins"
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(32), index = True)
#     password_hash = db.Column(db.String(128))

class AccountUser(db.Model):
    __tablename__ = "account_user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100))
    apikey = db.Column(db.String(64))
    wishes = db.relationship('Wish', secondary = user_wishes_secondary_table, lazy = 'subquery', backref = db.backref('users', lazy = True))

# class Profile(db.Model):
#     # __tablename__ = "profile"
#     # id = db.Column(db.Integer, primary_key = True)
#     # profile_image = db.Column(db.Text)
#     # about = db.Column(db.Text)
#     pass

class Wish(db.Model):
    __tablename__ = "wish"
    id = db.Column(db.Integer, primary_key = True)
    wish = db.Column(db.Text, nullable=True)

# class Comment(db.Model):
#     pass

# class Like(db.Model):
#     pass

# class Doit(db.Model):
#     pass
