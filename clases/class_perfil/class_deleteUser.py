from flask import jsonify
import models
from models import db

from models import Usuario

class Delete_Usuarios:
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
    def Detele(self, id_user):
        try:
           
            usuario_db = Usuario.query.filter_by(id_user=id_user).first()
            if not usuario_db: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún usuario con el id {id_user}"}), 400
            
            db.session.delete(usuario_db)
            db.session.commit()
        
            data = jsonify({"status": True, "message": "Usuario eliminado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    