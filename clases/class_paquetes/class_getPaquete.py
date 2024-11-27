from flask import jsonify
import models
from models import db

from models import Paquetes

class Get_Paquete:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_empresa
    '''
    def Get(self, idPaquete):
        try:            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID del paquete (idPaquete)"}), 400
            
            paquete = Paquetes.query.filter_by(idPaquete=idPaquete).first()
            
            if not paquete:
                return jsonify({"status": False, "message": f"No se han encontrado paquetes con el ID paquete: {idPaquete}"}), 400
            
            paquetes_data = [
                { 
                    "idPaquete": paquete.idPaquete,
                    "nombre": paquete.nombre,
                    "costo": paquete.costo,
                    "idContrato": paquete.idContrato, 
                }
            ]
            
            data = jsonify({"status": True, "paquete": paquetes_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    