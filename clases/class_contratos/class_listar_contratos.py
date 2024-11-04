from flask import jsonify
import models
from models import db
import datetime

from models import Contratos, Empresas
class Listar_Contrato:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idempresa
    @return contratos_alldata
    '''
    def Listar(self, datos):
        try:
            idEmpresa = datos['idEmpresa']
            id_usuario = datos['id_usuario']
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
            
            contratos = Contratos.query.filter_by(id_empresa=idEmpresa).all()
            if not contratos: 
                return jsonify({"status": False, "message": "No se ha encontrado contratos con el idEmpresa: " + idEmpresa}), 400
            contratos_alldata = []
        
            for contrato in contratos:
                start = contrato.fecha_inicio <= datetime.datetime.now().date()  # Determinar si ha comenzado
                fecha_entrega = contrato.fecha_entrega
                dias_restantes = (fecha_entrega - datetime.datetime.now().date()).days
                contratos_alldata.append({
                    'contrato': contrato,
                    'dias_restantes': dias_restantes,
                    'contrato_inicio': start,
                    'color': contrato.color  # Agregar el color del contrato
                })
            
            data = jsonify({"status": True, "contratos": contratos_alldata}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    