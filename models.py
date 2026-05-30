from flask_sqlalchemy import SQLAlchemy

    # conexão com banco
db = SQLAlchemy()

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