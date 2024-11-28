from flask import jsonify
import models
from models import db

from models import Contratistas, Contratos, ContratosContratistas, Paquetes

class Listar_Contratos:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.id_user = ''
            
    '''
    @param idContratista
    @return 
        ERROR
            status, message
        NO ERROR
            status, contratos
    '''
    def Listar(self, idContratista):
        try:
            if not idContratista:
                return jsonify({"status": False, "message": f"No se ha enviado los datos obligatoriso (idContratista)"}), 400
            print(idContratista)
            
            contratoscontratistas = ContratosContratistas.query.filter_by(idContratista=idContratista).all()
            if not contratoscontratistas: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún contrato del contratista con el ID: {idContratista}"}), 400
            print(contratoscontratistas)
            contratos = []
            
            for con in contratoscontratistas:
                contrato = Contratos.query.filter_by(idContrato =con.idContrato).first()
                
                if contrato:
                    total = 0
                    paquetes = Paquetes.query.filter_by(idContrato=contrato.idContrato).all()
                    for paquete in paquetes:
                        total += float(paquete.costo)
                    
                    contratos.append({
                        'idContrato': contrato.idContrato,
                        'nombre': contrato.nombre,
                        'tipo': contrato.tipo,
                        'lugar': contrato.lugar,
                        'fecha_entrega': contrato.fecha_entrega,
                        'fecha_inicio': contrato.fecha_inicio,
                        'color': contrato.color,
                        'idEmpresa': contrato.id_empresa,
                        'total': total
                    })
                    
                
            data = jsonify({"status": True, "contratos": contratos}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    