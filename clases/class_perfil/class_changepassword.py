from flask import jsonify
import models
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario

class Cambiar_Contrasena:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, empresa
    '''
    def Change(self, datos):
        try:
            id_user = datos.get('idUsuario')
            contrasena = datos.get('contrasena')
            contrasena_new = datos.get('contrasena_new')
            
            if not id_user:
                return jsonify({"status": False, "message": "No se ha enviado el ID del usuario (id_user)"}), 400
            
            if not contrasena or not contrasena_new:
                return jsonify({"status": False, "message": "No se ha enviado los datos necesarios (contrasena_new, contrasena)"}), 400
            
            usuario = Usuario.query.filter_by(id_user = id_user).first()
            if not usuario: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningua usuario con el id_user: {id_user}"}), 400
            
            if not check_password_hash(usuario.contrasena, contrasena):
                return jsonify({"status": False, "message": f"Contraseñas incorrectas"}), 400
            
            hashed_password_new = generate_password_hash(contrasena_new)
            usuario.contrasena = hashed_password_new
            db.session.commit()
        
            data = jsonify({"status": True, "message": "Usurio editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500 