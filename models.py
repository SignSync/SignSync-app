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
    #empresas = db.relationship('Empresas', backref='usuario', cascade="all, delete-orphan")
    
'''class Empresas(db.Model):
    __tablename__ = 'Empresas'
    idEmpresa = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)'''
    
    #contratos = db.relationship('Contratos', backref='empresa', cascade="all, delete-orphan")
    #contratistas = db.relationship('Contratistas', backref='empresa', cascade="all, delete-orphan")