from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import models
from models import db

class Sign_up:
    #definicion propiedades de la clase
    datos = any 
    usuario = ''
    correo = ''
    contrasena = ''
    
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.usuario = ''
        self.correo = ''
        self.contrasena= ''
    
    '''
        @param usuario, correo, contrasena
        @return
            ERROR 
            status, message
            NO ERROR
            status, message, id_nuevo_user
    '''
    
    def RegistrarUser(self, datos):
        try:
            if not datos or 'usuario' not in datos or 'correo' not in datos or 'contrasena' not in datos:
                return jsonify({"status": False, "error": "Faltan datos obligatorios"}), 400

            usuario = datos['usuario']
            correo = datos['correo']
            contrasena = datos['contrasena']

            # Verificar si el correo ya está registrado
            usuario_existente = models.Usuario.query.filter_by(correo=correo).first()
            if usuario_existente:
                return jsonify({"status": False, "message": "El correo ya está registrado"}), 400

            # Crear un nuevo usuario
            hashed_password = generate_password_hash(contrasena)
            newUser = models.Usuario(usuario=usuario, correo=correo, contrasena=hashed_password)

            db.session.add(newUser)
            db.session.commit()
            id_nuevo_user = newUser.id_user

            return jsonify({"status": True, "id": id_nuevo_user}), 201

        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500
    
    