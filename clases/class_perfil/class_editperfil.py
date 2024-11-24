from flask import jsonify
import models
from models import db

from models import Usuario

class Edit_Perfil:
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
    def Edit(self, datos):
        try:
            id_user = datos.get('idUsuario')
            usuario = datos.get('usuario')
            sexo = datos.get('sexo')
            fecha_nacimiento = datos.get('fecha_nacimiento')
            
            if not id_user:
                return jsonify({"status": False, "message": "No se ha enviado el ID del usuario (id_user)"}), 400
            
            usuario_db = Usuario.query.filter_by(id_user = id_user).first()
            if not usuario_db: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningua empresa con el id_user: {id_user}"}), 400
        
    
            usuario_db.usuario = usuario if usuario else usuario_db.usuario
            usuario_db.sexo = sexo if sexo else usuario_db.sexo
            usuario_db.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else usuario_db.fecha_nacimiento
            
            db.session.commit()
            
        
            data = jsonify({"status": True, "message": "Usurio editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    