from flask import jsonify
import models
from models import db


###############################PENDIENTE
class Crear_Contrato:
    #definicion propiedades de la clase
    datos = any 
    usuario = ''
    correo = ''
    contrasena = ''
    
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.usuario = ''
        self.correo = ''
        self.contrasena= ''
    
    '''
        @param idEmpresa, idContratista
        @return
            ERROR 
            status, message
            NO ERROR
            status, idContrato_new
    '''
    def RegistrarUser(self, datos):
        try:
            idEmpresa = datos['idEmpresa']
            idContratista = datos['idContratista']
            nombre = datos['nombre']
            tipo = datos['tipo']
            lugar = datos['lugar']
            fecha_inicio = datos['fecha_inicio']
            fecha_entrega = datos['fecha_entrega']
            color = datos['color']
            
            if not idEmpresa:
                return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa)"}), 400
            
            if not idContratista:
                return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idContratista)"}), 400
            
            newContract = db.Contratos(
                nombre= nombre,
                tipo= tipo,
                lugar= lugar,
                fecha_inicio= fecha_inicio,
                fecha_entrega= fecha_entrega,
                color= color,
                id_empresa = idEmpresa
            )
            db.session.add(newContract)
            db.session.commit()
            id_nuevo_contrato = newContract.idContrato
                    
            newContratos_Contratistas = db.ContratosContratistas(
                idContrato = id_nuevo_contrato,
                idContratista = idContratista
            )
            db.session.add(newContratos_Contratistas)
            db.session.commit()
            
            data = jsonify({'status': True, "id_nuevo_contrato": id_nuevo_contrato}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    