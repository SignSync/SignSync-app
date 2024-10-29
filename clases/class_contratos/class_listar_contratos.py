from flask import jsonify
import models
from models import db
import datetime

class Listar_Contrato:
    #definicion propiedades de la clase
    datos = any 
   
    
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
        self.correo = ''
        self.contrasena= ''
    
    def Listar(self, datos):
        try:
            #CHECA SI HAY DATOS 
            if not datos or 'idEmpresa':
                return jsonify({"error": "Faltan datos (idEmpresa)"}), 400
            
            idEmpresa = datos['idEmpresa']
            
            if not idEmpresa:
                data = {"message": "No se ha enviado el ID de la empresa correctamente"}
            contratos = db.Contratos.query.filter_by(id_empresa=idEmpresa).all()
            
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
            
            data = {"message": "Usuario registrado correctamente", "contratos": contratos_alldata}
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    