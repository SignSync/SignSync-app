from flask import jsonify
import models
from models import db
import datetime

from models import Empresas, Contratos

class Listar_Contrato_Usurio:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param id_usuario
    @return contratos_alldata
    '''
    def Listar(self, datos):
        try:
            #CHECA SI HAY DATOS 
            id_usuario = datos['id_usuario']
            
            if id_usuario == None:
                return jsonify({"error": "Faltan datos (id_usuario)"}), 400
            
            empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
            if not empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el id_usuario: " + id_usuario}), 400
            
            idEmpresa = empresa.idEmpresa
            contratos = Contratos.query.filter_by(id_empresa=idEmpresa).all()
            if not contratos: 
                return jsonify({"status": False, "message": "No se ha encontrado contratos con el id_usuario: " + id_usuario + " e idEmpresa: " + idEmpresa}), 400
            
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
    
    