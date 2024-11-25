from flask import jsonify
import models
from models import db
from werkzeug.security import generate_password_hash

from models import Usuario

class Create_User:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Create(self, datos):
        try:
            usuario = datos.get('usuario')
            correo = datos.get('correo')
            contrasena = datos.get('contrasena')
            sexo = datos.get('sexo')
            fecha_nacimiento = datos.get('fecha_nacimiento')
            
            if not usuario or not correo or not contrasena:
                return jsonify({"status": False, "message": "No se ha campos obligatorios (usuario, correo, contrasena)"}), 400
            
            hashed_password = generate_password_hash(contrasena)
            
            newUser = Usuario(
                usuario = usuario,
                correo = correo, 
                contrasena = hashed_password,
                sexo = sexo,
                fecha_nacimiento = fecha_nacimiento
            )
            
            db.session.add(newUser)
            db.session.commit()
            
            id_new_usuario = newUser.id_user
            data = jsonify({"status": True, "id_new_usuario": id_new_usuario}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    