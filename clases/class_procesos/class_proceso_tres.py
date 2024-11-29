from flask import jsonify
import models
from models import db

from models import Usuario, Contratos
from sqlalchemy.sql import func

from datetime import datetime

class Contratos_Activos:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.id_user = ''
            
    '''
    @param 
    @return 
        ERROR
            status, message
        NO ERROR
            status, contratos
    '''
    def Listar(self):
        try:
            today = datetime.today()

            # Consulta para traer los datos de contratos activos
            contracts = db.session.query(
                Contratos.idContrato,
                Contratos.nombre,
                Contratos.tipo,
                Contratos.lugar,
                Contratos.fecha_inicio,
                Contratos.fecha_entrega,
                Contratos.color
            ).filter(
                Contratos.fecha_inicio <= today,
                Contratos.fecha_entrega >= today
            ).all()

            # Convertir los datos en un formato JSON-friendly
            contracts_data = [
                {
                    'id': contract.idContrato,
                    'nombre': contract.nombre,
                    'tipo': contract.tipo,
                    'lugar': contract.lugar,
                    'fecha_inicio': contract.fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_entrega': contract.fecha_entrega.strftime('%Y-%m-%d'),
                    'color': contract.color
                }
                for contract in contracts
            ]
            
            
            data = jsonify({'active_contracts': contracts_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    