from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255))
    password = db.Column(db.String(256), nullable=False)
    contacts = db.relationship("Contact", backref="user", lazy=True)


class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    country = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
