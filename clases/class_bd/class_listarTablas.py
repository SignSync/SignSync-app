
from flask import jsonify
from models import db
from config import DevelopmentConfig
from sqlalchemy import create_engine, inspect

import os, json

class Listar_Tablas:
    def __init__(self) -> None:
        self.CACHE_FILE = "./json__/json_tablas_cache.json"
            
    '''
    @param 
    @return 
        ERROR
            
        NO ERROR
           
    '''
    def Listar(self):
        try:
            if os.path.exists(self.CACHE_FILE):
                with open(self.CACHE_FILE, 'r') as cache_file:
                    tablas_info = json.load(cache_file)  # Cargar datos del archivo
                    return jsonify(tablas_info)
            
            engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
            insp = inspect(engine)
            tablas = insp.get_table_names()
            
            tablas_info = {}
            
            tablas_validad = ['Contratistas', 'Contratos', 'Contratos_Contratistas', 'Documentos', 'Empresas', 'Paquetes', 'usuarios']

            for tabla in tablas:
                if not tabla in tablas_validad:
                    continue
                # columns = insp.get_columns(tabla)  
                # fks = insp.get_foreign_keys(tabla)
                # indexes = insp.get_indexes(tabla)
                
                columns = [
                    {key: str(value) if not isinstance(value, (str, int, float, bool)) else value
                    for key, value in column.items()}
                    for column in insp.get_columns(tabla)
                ]
                fks = [
                    {key: str(value) if not isinstance(value, (str, int, float, bool)) else value
                    for key, value in fk.items()}
                    for fk in insp.get_foreign_keys(tabla)
                ]
                indexes = [
                    {key: str(value) if not isinstance(value, (str, int, float, bool)) else value
                    for key, value in index.items()}
                    for index in insp.get_indexes(tabla)
                ]
                
                tablas_info[tabla] = {
                    'columns': columns,
                    'foreign_keys': fks,
                    'indexes': indexes
                }
                
                with open(self.CACHE_FILE, 'w') as cache_file:
                    json.dump(tablas_info, cache_file, indent=4)

            return jsonify({'tablas_info':tablas_info})
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    

# class BaseDatos:
#     @staticmethod
#     def get_context(tabla):
#         try:
#             consulta = {}
#             tablas_info = {}
            
            
#             for tabla_ in tablas:
#                 columns = insp.get_columns(tabla_)  
#                 fks = insp.get_foreign_keys(tabla_)
#                 indexes = insp.get_indexes(tabla_)
                
#                 if(tabla_.startswith('grafico_') or tabla_.startswith('respuestas') or tabla_.startswith('preguntas')):
#                     continue
                
#                 tablas_info[tabla_] = {
#                     'columns': columns,
#                     'foreign_keys': fks,
#                     'indexes': indexes
#                 }
           
#             Session = sessionmaker(bind=engine)
#             session = Session()
            
#             template_tabla = ''
#             if tabla and tabla == 'usuarios':
#                 template_tabla = 'graficos/vistas_tablas/tabla_usuarios.html'
#                 usuarios = session.query(Usuario).all()
#                 covert = {'usuarios': usuarios}
#                 consulta.update(covert)
#             elif tabla and tabla == 'Contratos':
#                 template_tabla = 'graficos/vistas_tablas/tabla_contratos.html'
#                 contratos = session.query(Contratos).all()
#                 covert = {'contratos': contratos}
#                 consulta.update(covert)
#             elif tabla and tabla == 'Empresas':
#                 template_tabla = 'graficos/vistas_tablas/tabla_empresas.html'
#                 empresas = session.query(Empresas).all()
#                 covert = {'empresas': empresas}
#                 consulta.update(covert)
#             elif tabla and tabla == 'Contratos_Contratistas':
#                 template_tabla = 'graficos/vistas_tablas/tabla_ccontratistas.html'
#                 ccontratistas = session.query(ContratosContratistas).all()
#                 covert = {'ccontratistas': ccontratistas}
#                 consulta.update(covert)
#             elif tabla and tabla == 'Contratistas':
#                 template_tabla = 'graficos/vistas_tablas/tabla_contratistas.html'
#                 contratistas = session.query(Contratistas).all()
#                 covert = {'contratistas': contratistas}
#                 consulta.update(covert)
                
            
#         except SQLAlchemyError as e:
#             print(f"Error al conectar con la base de datos: {e}")
#         finally:
#             engine.dispose()  # Cierra la conexión de manera explícita
            
#         #usuarios = Usuario.query.all()
        
#         return {
#             'template': 'graficos/basedatos.html',
#             'template_tabla':template_tabla,
#             'tablas': tablas,
#             'tabla': tabla,
#             'consulta': consulta,
#             'tablas_info': tablas_info
#         }