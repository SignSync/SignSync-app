from flask import jsonify
import models
from models import db

from models import Usuario
from sqlalchemy.sql import func


class registros_diarios:
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
            results = db.session.query(
                func.date(Usuario.created_date).label('fecha'),
                func.count(Usuario.id_user).label('registros_por_dia')
            ).group_by(
                func.date(Usuario.created_date)
            ).order_by(
                func.date(Usuario.created_date).desc()
            ).all()

            metrics = [{'fecha': str(row.fecha), 'registros_por_dia': row.registros_por_dia} for row in results]
            data = jsonify({"status": True, "metricas": metrics}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    