from flask import jsonify
import models
from models import db

from models import Usuario

class Get_Usuarios:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.id_user = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Get(self, id_user):
        try:
            usuario = Usuario.query.filter_by(id_user=id_user).first()
            if not usuario: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún usuario con el ID: {id_user}"}), 400
            
            data_user = [
                {
                    "id_user": usuario.id_user,
                    "usuario": usuario.usuario,
                    "correo": usuario.correo,
                    "sexo": usuario.sexo,
                    "fecha_nacimiento": usuario.fecha_nacimiento,
                    "created_date": usuario.created_date
                }
            ]
            data = jsonify({"status": True, "usuario": data_user}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    