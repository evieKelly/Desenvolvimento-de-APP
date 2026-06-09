
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    senha = db.Column(db.String(255), nullable=False)


class RegistroHumor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humor = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)

# tabela diário (Amanda)
class Diario(db.Model):

    __tablename__ = "diario"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    texto = db.Column(
        db.Text,
        nullable=False
    )

    data = db.Column(
        db.String(50)
    )