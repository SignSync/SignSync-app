from flask import jsonify
import models
from models import db

from models import Paquetes

class Listar_Paquete:
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
    def Listar(self, idContrato):
        try:            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            paquetes = Paquetes.query.filter_by(idContrato=idContrato).all()
            
            if not paquetes:
                return jsonify({"status": False, "message": f"No se han encontrado paquetes con el ID contrato: {idContrato}"}), 400
            
            paquetes_data = [
                { 
                    "idPaquete": paquete.idPaquete,
                    "nombre": paquete.nombre,
                    "costo": paquete.costo,
                    "idContrato": paquete.idContrato, 
                }
                for paquete in paquetes
            ]
            
            data = jsonify({"status": True, "paquetes": paquetes_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    