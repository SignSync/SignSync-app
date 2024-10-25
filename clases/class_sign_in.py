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
        
            correo = datos['correo']
            contrasena = datos['contrasena']
            
            user = models.Usuario.query.filter_by(correo=correo).first()
            if user:
                if check_password_hash(user.contrasena, contrasena):
                    data = {'user_id': user.id_user,
                            'user_name': user.usuario,
                            'correo':user.correo}
                else:
                    data = {"message": "Contraseña o correo electornico no validos."}
            else:
                data = {"message": "Correo electronico no registrado"}
                 
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    