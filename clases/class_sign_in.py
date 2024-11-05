from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import models
from models import db

class Sign_in:
    #definicion propiedades de la clase
    datos = any 
    usuario = ''
    correo = ''
    contrasena = ''
    
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.correo = ''
        self.contrasena= ''
    
    def loginUser(self, datos):
        try:
            if 'correo' not in datos or 'contrasena' not in datos:
                return jsonify({"error": "Faltan datos"}), 400
        
            correo = datos.get('correo')
            contrasena = datos.get('contrasena')            
            user = models.Usuario.query.filter_by(correo=correo).first()
            if user:
                if check_password_hash(user.contrasena, contrasena):
                    data = jsonify({"status": True, 'user_id': user.id_user,
                            'user_name': user.usuario,
                            'correo':user.correo}), 201
                else:
                    data = jsonify({"status": False, "message": "Contraseña o correo electornico no validos."}), 201
            else:
                data = jsonify({"status": False,"message": "Correo electronico no registrado"}), 201
                 
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    