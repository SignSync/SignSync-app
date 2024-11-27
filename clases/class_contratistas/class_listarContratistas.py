from flask import jsonify
import models
from models import db

from models import Empresas, Contratistas

class Listar_Contratistas:
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
    def Listar(self):
        try:
            contratistas = Contratistas.query.all()
            
            if not contratistas: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún contratista."}), 400
            
            contratistas_data = [
                {
                    "idContratista": contratista.idContratista,           # Reemplaza 'id' con el nombre real de la columna de ID en Contratistas
                    "nombre": contratista.nombre,
                    "edad": contratista.edad,   # Reemplaza con los campos que tenga tu modelo Contratistas
                    "ocupacion": contratista.ocupacion,
                    "domicilio": contratista.domicilio,
                    "telefono": contratista.telefono,
                    "id_empresa": contratista.id_empresa
                }
                for contratista in contratistas
            ]
                        
            
            data = jsonify({"status": True, "contratistas": contratistas_data}), 201
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error