from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True)
    usuario  = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    contrasena = db.Column(db.String(200))
    sexo = db.Column(db.String(50))
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    empresas = db.relationship('Empresas', backref='usuario', cascade="all, delete-orphan")
    
class Empresas(db.Model):
    __tablename__ = 'Empresas'
    idEmpresa = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    sector = db.Column(db.String(60), nullable=False)
    correo = db.Column(db.String(60), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    sitio_web = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(1000), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)
    
    contratos = db.relationship('Contratos', backref='empresa', cascade="all, delete-orphan")
    contratistas = db.relationship('Contratistas', backref='empresa', cascade="all, delete-orphan")

class Contratos(db.Model):
    __tablename__ = 'Contratos'
    idContrato = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(30))
    lugar = db.Column(db.String(50))
    fecha_entrega = db.Column(db.Date, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    color = db.Column(db.String(7), nullable=False)  # Agrega la columna color
    id_empresa = db.Column(db.Integer, db.ForeignKey('Empresas.idEmpresa'), nullable=False)
    contratos_contratistas = db.relationship('ContratosContratistas', backref='contrato', cascade="all, delete-orphan")

class Contratistas(db.Model):
    __tablename__ = 'Contratistas'
    idContratista = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.SmallInteger, nullable=False)
    ocupacion = db.Column(db.String(50), nullable=False)
    domicilio = db.Column(db.String(60), nullable=True)
    telefono = db.Column(db.String(18), nullable=True)
    id_empresa = db.Column(db.Integer, db.ForeignKey('Empresas.idEmpresa'), nullable=False)
    
    contratos_contratistas = db.relationship('ContratosContratistas', backref='contratista', cascade="all, delete-orphan")
    
class ContratosContratistas(db.Model):
    __tablename__ = 'Contratos_Contratistas'
    idContratosContratista = db.Column(db.Integer, primary_key=True)
    idContrato = db.Column(db.Integer, db.ForeignKey('Contratos.idContrato'), nullable=False)
    idContratista = db.Column(db.Integer, db.ForeignKey('Contratistas.idContratista'), nullable=False)
    
class Preguntas(db.Model):
    __tablename__ = 'Preguntas'
    idPregunta = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(250))
    respuestas = db.relationship('Respuestas', backref='pregunta', lazy=True)

class Respuestas(db.Model):
    __tablename__ = 'Respuestas'
    idRespuesta = db.Column(db.Integer, primary_key=True)
    respuesta = db.Column(db.String(250))
    idPregunta = db.Column(db.Integer, db.ForeignKey('Preguntas.idPregunta'), nullable=False)