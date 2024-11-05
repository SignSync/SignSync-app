from flask import jsonify
import models
from models import db

from models import Empresas, Contratistas

class Get_Contratista:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idEmpresa || id_usuario *
    @return 
        ERROR
            status, message
        NO ERROR
            status, contratistas
    '''
    def Get(self, idContratista):
        try:
            contratista = Contratistas.query.filter_by(idContratista =idContratista).first()
            
            if not contratista: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún contratista con el id de contratista: {idContratista}"}), 400
            
            contratistas_data = {
                "idContratista": contratista.idContratista,           # Reemplaza 'id' con el nombre real de la columna de ID en Contratistas
                "nombre": contratista.nombre,
                "edad": contratista.edad,   # Reemplaza con los campos que tenga tu modelo Contratistas
                "ocupacion": contratista.ocupacion,
                "domicilio": contratista.domicilio,
                "telefono": contratista.telefono,
                "id_empresa": contratista.id_empresa
            }
                        
            
            data = jsonify({"status": True, "contratista": contratistas_data}), 201
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error