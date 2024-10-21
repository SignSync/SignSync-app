from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True)
    usuario  = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    contrasena = db.Column(db.String(200))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
