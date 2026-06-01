from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)

class RegistroHumor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humor = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)