from flask import jsonify
import models
from models import db

from models import Usuario

class Listar_Usuarios:
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
    def Listar(self):
        try:
            usuario_db = Usuario.query.all()
            if not usuario_db: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún usuario"}), 400
            
            data_users = [
                {
                    "id_user": usuario.id_user,
                    "usuario": usuario.usuario,
                    "correo": usuario.correo,
                    "sexo": usuario.sexo,
                    "fecha_nacimiento": usuario.fecha_nacimiento,
                    "created_date": usuario.created_date
                }
                
                for usuario in usuario_db
            ]
            
            db.session.commit()
            
        
            data = jsonify({"status": True, "usuarios": data_users}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    