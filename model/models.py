from datetime import datetime
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=True)
    orders = db.relationship("Orders")

    def __repr__(self):
        return f"User {self.name}, {self.name}, {self.email}, {self.phone_number}, {self.address}, {self.is_admin}"


# class Customer(db.Model, UserMixin):
#     __tablename__ = "customer"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150))
#     email = db.Column(db.String(50))
#     phone_number = db.Column(db.Integer)
#     address = db.Column(db.String)
#     password = db.Column(db.String(255))

#     def __repr__(self):
#         return f"Customer {self.name}, {self.name}, {self.email}, {self.phone_number}, {self.address}"


class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    ordered_date = db.Column(db.DateTime, default=datetime.utcnow())
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ebook_id = db.Column(db.Integer, db.ForeignKey("ebook.id"))

    def __repr__(self):
        return f"Orders {self.ordered_date}, {self.order_ebook}"


class Ebook(db.Model):
    __tablename__ = "ebook"

    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(150))
    penulis = db.Column(db.String(50))
    sinopsis = db.Column(db.String)
    harga = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    content_url = db.Column(db.String(255))
