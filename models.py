from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)