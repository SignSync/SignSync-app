import random
from config import DevelopmentConfig
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from models import Usuario, Contratos, Empresas, ContratosContratistas, Contratistas

import matplotlib
matplotlib.use('Agg')  # Cambiar el backend de matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy.random as np
import numpy as np_

from io import BytesIO
import base64

import json
import os

def cargar_contenido(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return None

def guardar_contenido(filepath, contenido):
    with open(filepath, 'w') as file:
        json.dump(contenido, file, indent=4)
        
def manejar_contenido(vista, nombre_archivo):
    filepath = f"clases/class_graficas/json/{nombre_archivo}.json"
    contenido = cargar_contenido(filepath)
    if not contenido:
        contenido = vista.get_context()
        guardar_contenido(filepath, contenido)
    return contenido


class TodosView:
    @staticmethod
    def get_context():
        contentViabilidad = manejar_contenido(ViabilidadView, "viabilidad")
        contentCrecimiento = manejar_contenido(CrecimientoView, "crecimiento")
        contentRentabilidad = manejar_contenido(RentabilidadView, "rentabilidad")
        contentSatisfaccion = manejar_contenido(SastifaccionView, "satisfaccion")
        contentAceptabilidad = manejar_contenido(AceptabilidadView, "aceptabilidad")
        contentFuncionalidad = manejar_contenido(FuncionalidadView, "funcionalidad")
        
        return {
            'template': 'graficos/todos.html',
            'contentViabilidad' : contentViabilidad,
            'contentCrecimiento' : contentCrecimiento,
            'contentRentabilidad' : contentRentabilidad,
            'contentSatisfaccion' : contentSatisfaccion,
            'contentAceptabilidad' : contentAceptabilidad,
            'contentFuncionalidad' : contentFuncionalidad,
        }

class ViabilidadView:
    @staticmethod
    def get_context():
        filepath = f"clases/class_graficas/json/viabilidad.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        # viabilidad_csv = pd.read_csv('clases/class_graficas/encuestas/encuestas-viabilidad.csv')
        # viabilidad_csv.to_sql(name='grafico_viabilidad', con=connection, if_exists='append')
        # 
        sql_viabilidad = 'select * from grafico_viabilidad'
        viabilidad = pd.read_sql_query(sql_viabilidad, con=connection)
        
        preguntas_text = [
            '¿Actualmente, qué método utiliza su PyME para organizar y administrar suscontratos?', 
            '¿Ha encontrado dificultades o problemas con su método actual de organización de contratos?',
            '¿Cuáles son los principales desafíos que enfrenta al gestionar sus datos?',  
            '¿Qué características considera esenciales que contenga una aplicación que organice y gestione contratos?',
            '¿Cuál es su nivel de satisfacción con el método actual de gestión de contratos?',
            '¿Qué tanto tiempo invierte su PyME en la gestión de contratossemanalmente?',
            '¿Qué tan importante considera la automatización en la gestión de contratos?',
            '¿Qué herramientas digitales utiliza actualmente para otras áreas de su negocio?',
            '¿Con qué frecuencia encuentra errores en la gestión de contratos manual?',
            '¿Considera que una aplicación de gestión de contratos podría mejorar la eficiencia operativa de su PyME?',
        ]
        respuestas_text = [
            ['a) Sistema manual (por ejemplo, carpetas físicas, hojas de cálculo)', 'b) Software de gestión de contratos','c) Otros'],
            ['a) Sí, con frecuencia', 'b) Sí, no seguido', 'c) No tengo ningún problema'],
            ['a) Falta de organización', 'b) Dificultad para encontrar la información que necesita','c) Incapacidad para analizar los datos de manera efectiva','d) Falta de herramientas adecuadas', 'e) Otras'],
            ["a) Registro y organización de contratos","b) Búsqueda y filtrado de contratos","c) Alertas y notificaciones","d) Gestión de fechas y plazos","e) Generación de informes y análisis","f) Integración con otras herramientas empresariales (por ejemplo, CRM, facturación)","g) Otras (especifique)"],
            ["a) Muy satisfecho","b) Satisfecho","c) Neutral","d) Insatisfecho"],
            ["a) Menos de 5 horas","b) 5-10 horas","c) 10-20 horas","d) Más de 20 horas"],
            ["a) Muy importante","b) Importante","c) Moderadamente importante","d) Poco importante"],
            ["a) CRM","b) ERP","c) Software de contabilidad","d) Ninguna"],
            ["a) Muy frecuente","b) Frecuente","c) Ocasional","d) Raro"],
            ["a) Sí, significativamente","b) Sí, en cierta medida","c) No mucho","d) No"]
        ]
        
        preguntas = []
        
        for i in range(10):
            pregunta_url = GenerarImgGrafica('Pregunta_'+ str(i+1), '', '', '', viabilidad)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        return {
            'template': 'graficos/viabilidad.html',
            'preguntas_url': preguntas
        }
        

class RentabilidadView:
    @staticmethod
    def get_context():
        filepath = f"json/rentabilidad.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        rentabilidad_csv = pd.read_csv('encuestas/encuestas-rentabilidad.csv')
        rentabilidad_csv.to_sql(name='grafico_rentabilidad', con=connection, if_exists='append')
        #
        preguntas_text = [
            '¿Qué factores consideraría importantes al evaluar el costo de una aplicación de gestión de contratos para PyMEs?', 
            '¿Cuál es su presupuesto aproximado para una solución de gestión de contratos al año?',
            '¿Qué tan dispuesto estaría a invertir en una solución que optimice la gestión de contratos?',  
            '¿Cuánto ahorra en costos operativos al año con su método actual de gestión de contratos?',
            '¿Qué tan importante es para usted el retorno de inversión al adoptar una nueva tecnología?',
            '¿Cuánto tiempo cree que se tardaría en recuperar la inversión en una nueva solución de gestión de contratos?',
            '¿Cuáles son sus principales costos operativos relacionados con la gestión de contratos?',
            '¿Qué tan importante es la escalabilidad de una solución para su PyME?',
            '¿Qué porcentaje de sus ingresos está dispuesto a invertir en tecnologías que mejoren la gestión de su PyME?',
            '¿Qué tan satisfecho está con la relación costo-beneficio de su método actual de gestión de contratos?',
        ]
        respuestas_text = [
            ['a) Funcionalidades', 'b) Facilidad de uso', 'c) Soporte al cliente', 'd) Escalabilidad', 'e) Seguridad', 'f) Integraciones', 'g) Otras (especifique)'],
            ['a) Menos de $500', 'b) $500-$1000', 'c) $1000-$2000', 'd) Más de $2000'],
            ['a) Muy dispuesto', 'b) Dispuesto', 'c) Moderadamente dispuesto', 'd) Poco dispuesto'],
            ['a) Menos de $500', 'b) $500-$1000', 'c) $1000-$2000', 'd) Más de $2000'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Menos de 6 meses', 'b) 6-12 meses', 'c) 1-2 años', 'd) Más de 2 años'],
            ['a) Tiempo de empleados', 'b) Materiales de oficina', 'c) Servicios de asesoría legal', 'd) Otros (especifique)'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Menos del 1%', 'b) 1-2%', 'c) 2-5%', 'd) Más del 5%'],
            ['a) Muy satisfecho', 'b) Satisfecho', 'c) Neutral', 'd) Insatisfecho']
        ]     
        
        sql_rentabilidad = 'select * from signsync.grafico_rentabilidad'
        rentabilidad = pd.read_sql_query(sql_rentabilidad, con=connection)
        
        preguntas = []
        
        for i in range(10):
            pregunta_url = GenerarImgG_pastel('Pregunta_'+ str(i+1), '', '', '', rentabilidad)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        return {
            'template': 'graficos/rentabilidad.html',
            'preguntas_url': preguntas
        }

class FuncionalidadView:
    @staticmethod
    def get_context():
        filepath = f"json/funcionalidad.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        funcionalidad_csv = pd.read_csv('encuestas/encuestas-funcionabilidad.csv')
        funcionalidad_csv.to_sql(name='grafico_funcionabilidad', con=connection, if_exists='append')
        #
        preguntas_text = [
            '¿Qué funcionalidades adicionales considera esenciales en una aplicación de gestión de contratos?',
            '¿Cómo evalúa la importancia de la facilidad de uso en una aplicación de gestión de contratos?',
            '¿Qué tipo de alertas y notificaciones considera más útiles?',
            '¿Con qué frecuencia necesitaría actualizaciones de la aplicación?',
            '¿Qué nivel de personalización considera necesario para su PyME?',
            '¿Cómo prefiere recibir soporte técnico para la aplicación?',
            '¿Qué tan importante es la integración con otras herramientas empresariales?',
            '¿Cuán relevante es la capacidad de generar informes y análisis detallados?',
            '¿Cuánto valora la capacidad de acceso móvil a la aplicación?',
            '¿Qué tan esencial es la función de respaldo automático de datos?',
            '¿Qué factores consideraría importantes al evaluar el costo de una aplicación de gestión de contratos para PyMEs?', 
            '¿Cuál es su presupuesto aproximado para una solución de gestión de contratos al año?',
            '¿Qué tan dispuesto estaría a invertir en una solución que optimice la gestión de contratos?',  
            '¿Cuánto ahorra en costos operativos al año con su método actual de gestión de contratos?',
            '¿Qué tan importante es para usted el retorno de inversión al adoptar una nueva tecnología?',
            '¿Cuánto tiempo cree que se tardaría en recuperar la inversión en una nueva solución de gestión de contratos?',
            '¿Cuáles son sus principales costos operativos relacionados con la gestión de contratos?',
            '¿Qué tan importante es la escalabilidad de una solución para su PyME?',
            '¿Qué porcentaje de sus ingresos está dispuesto a invertir en tecnologías que mejoren la gestión de su PyME?',
            '¿Qué tan satisfecho está con la relación costo-beneficio de su método actual de gestión de contratos?'
        ]
        respuestas_text = [
            ['a) Integración con calendarios', 'b) Acceso móvil', 'c) Análisis avanzado de datos', 'd) Otras (especifique)'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Plazos de contrato próximos', 'b) Recordatorios de revisión', 'c) Alertas de vencimiento', 'd) Otras (especifique)'],
            ['a) Mensualmente', 'b) Trimestralmente', 'c) Semestralmente', 'd) Anualmente'],
            ['a) Muy alto', 'b) Alto', 'c) Moderado', 'd) Bajo'],
            ['a) Chat en línea', 'b) Soporte telefónico', 'c) Correo electrónico', 'd) Base de conocimiento en línea'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Muy relevante', 'b) Relevante', 'c) Moderadamente relevante', 'd) Poco relevante'],
            ['a) Muy valorado', 'b) Valorado', 'c) Moderadamente valorado', 'd) Poco valorado'],
            ['a) Muy esencial', 'b) Esencial', 'c) Moderadamente esencial', 'd) Poco esencial'],
            ['a) Funcionalidades', 'b) Facilidad de uso', 'c) Soporte al cliente', 'd) Escalabilidad', 'e) Seguridad', 'f) Integraciones', 'g) Otras (especifique)'],
            ['a) Menos de $500', 'b) $500-$1000', 'c) $1000-$2000', 'd) Más de $2000'],
            ['a) Muy dispuesto', 'b) Dispuesto', 'c) Moderadamente dispuesto', 'd) Poco dispuesto'],
            ['a) Menos de $500', 'b) $500-$1000', 'c) $1000-$2000', 'd) Más de $2000'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Menos de 6 meses', 'b) 6-12 meses', 'c) 1-2 años', 'd) Más de 2 años'],
            ['a) Tiempo de empleados', 'b) Materiales de oficina', 'c) Servicios de asesoría legal', 'd) Otros (especifique)'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Menos del 1%', 'b) 1-2%', 'c) 2-5%', 'd) Más del 5%'],
            ['a) Muy satisfecho', 'b) Satisfecho', 'c) Neutral', 'd) Insatisfecho']
        ]
        
        sql_funcionabilidad = 'select * from grafico_funcionabilidad'
        funcionabilidad = pd.read_sql_query(sql_funcionabilidad, con=connection)
        
        preguntas = []
        
        for i in range(10):
            pregunta_url = GenerarImgGrafica('Pregunta_'+ str(i+1), '', '', '', funcionabilidad)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        
        
        return {
            'template': 'graficos/funcionalidad.html',
            'preguntas_url': preguntas
        }

class AceptabilidadView:
    @staticmethod
    def get_context():
        filepath = f"json/aceptabilidad.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        aceptabilidad_csv = pd.read_csv('encuestas/encuestas-aceptabilidad.csv')
        aceptabilidad_csv.to_sql(name='grafico_aceptabilidad', con=connection, if_exists='append')
        #
        preguntas_text = [
            '¿Qué tan probable es que recomiende una aplicación de gestión de contratos a otros propietarios de PyMEs?', 
            '¿Con qué frecuencia revisa y actualiza los contratos en su PyME?',
            '¿Cómo evalúa el rendimiento de los contratos en su PyME?',  
            '¿Qué métodos utiliza para asegurarse de que se cumplan los plazos y términos de los contratos?',
            '¿Cómo maneja su PyME la confidencialidad y la seguridad de los contratos?',
            '¿Qué tan satisfecho está con la precisión de los contratos gestionados manualmente?',
            '¿Qué tan importante es para usted tener una visión general clara de todos los contratos activos?',
            '¿Qué tan satisfecho está con el tiempo que toma crear y finalizar contratos manualmente?',
            '¿Qué tan fácil es para usted encontrar información específica en los contratos actuales?',
            '.¿Qué tan dispuesto estaría a cambiar a una solución digital para la gestión de contratos?',
        ]
        respuestas_text = [
            ['a) Muy probable','b) Probable','c) Poco probable','d) Nada probable'], 
            ['a) Diariamente','b) Semanalmente','c) Mensualmente','d) Trimestralmente','e) Otras'],
            ['a) Seguimiento de cumplimiento de términos y condiciones','b) Evaluación de resultados financieros relacionados','c) Revisión de la satisfacción del cliente','d) Análisis de riesgos y problemas surgidos','e) Otro'],
            ['a) Recordatorios manuales','b) Recordatorios automáticos por correo electrónico','c) Sistema de gestión de proyectos','d) Otro'],
            ['a) Contraseñas y acceso restringido','b) Cifrado de documentos','c) Almacenamiento en servidores seguros','d) Otro'],
            ['a) Muy satisfecho','b) Satisfecho','c) Neutral','d) Insatisfecho'],
            ['a) Muy importante','b) Importante','c) Moderadamente importante','d) Poco importante'],
            ['a) Muy satisfecho','b) Satisfecho','c) Neutral','d) Insatisfecho'],
            ['a) Muy fácil','b) Fácil','c) Moderadamente fácil','d) Difícil'],
            ['a) Muy dispuesto','b) Dispuesto','c) Moderadamente dispuesto','d) Poco dispuesto']
        ]
        
        sql_aceptabilidad = 'select * from grafico_aceptabilidad'
        aceptabilidad = pd.read_sql_query(sql_aceptabilidad, con=connection)
        
        preguntas = []
        
        for i in range(10):
            pregunta_url = GenerarImgGrafica('Pregunta_'+ str(i+1), '', '', '', aceptabilidad)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        return {
            'template': 'graficos/aceptabilidad.html',
            'preguntas_url': preguntas
        }

class SastifaccionView:
    @staticmethod
    def get_context():
        filepath = f"json/satisfaccion.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        
        
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        satisfaccion_csv = pd.read_csv('encuestas/encuestas-satisfaccion.csv')
        satisfaccion_csv.to_sql(name='grafico_satisfaccion', con=connection, if_exists='append')
        #
        
        preguntas_text = [
            '¿Qué tan satisfecho está con el método actual de gestión de contratos de su PyME?',
            '¿Cómo calificaría la experiencia del cliente con el método actual de gestión de contratos?',
            '¿Qué tan efectivo es su método actual para mantener la confidencialidad de los datos del cliente?',
            '¿Con qué frecuencia los clientes tienen problemas con los contratos?',
            '¿Qué tan fácil es para sus clientes acceder y comprender sus contratos?',
            '¿Qué tan importante es para usted la opinión de sus clientes sobre la gestión de contratos?',
            '¿Qué tan rápido puede resolver los problemas relacionados con contratos?',
            '¿Qué tan satisfechos están sus clientes con la rapidez en la gestión de contratos?',
            '¿Qué tan relevante es la capacidad de los clientes para revisar y actualizar sus contratos?',
            '¿Qué tan importante es la transparencia en la gestión de contratos para sus clientes?'
        ]
        respuestas_text = [
            ['a) Muy satisfecho', 'b) Satisfecho', 'c) Neutral', 'd) Insatisfecho'],
            ['a) Excelente', 'b) Buena', 'c) Regular', 'd) Mala'],
            ['a) Muy efectivo', 'b) Efectivo', 'c) Moderadamente efectivo', 'd) Poco efectivo'],
            ['a) Muy frecuente', 'b) Frecuente', 'c) Ocasional', 'd) Raro'],
            ['a) Muy fácil', 'b) Fácil', 'c) Moderadamente fácil', 'd) Difícil'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Muy rápido', 'b) Rápido', 'c) Moderadamente rápido', 'd) Lento'],
            ['a) Muy satisfechos', 'b) Satisfechos', 'c) Moderadamente satisfechos', 'd) Insatisfechos'],
            ['a) Muy relevante', 'b) Relevante', 'c) Moderadamente relevante', 'd) Poco relevante'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante']
        ]            
            
        sql_satisfaccion = 'select * from grafico_satisfaccion'
        satisfaccion = pd.read_sql_query(sql_satisfaccion, con=connection)
        
        preguntas = []
        for i in range(10):
            pregunta_url = GenerarImgG_pastel('Pregunta_'+ str(i+1), '', '', '', satisfaccion)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        return {
            'template': 'graficos/sastifaccion.html',
            'preguntas_url': preguntas
        }

class CrecimientoView:
    @staticmethod
    def get_context():
        filepath = f"json/crecimiento.json"
        contenido = cargar_contenido(filepath)
        if contenido:
            return contenido
        
        preguntas_text = [
            '¿Cómo ha cambiado el tamaño de su PyME en los últimos cinco años?',
            '¿Cuál ha sido el principal motor de crecimiento de su PyME en los últimos cinco años?',
            '¿Qué porcentaje de su personal actual ha sido contratado en los últimos cinco años?',
            '¿Qué tan importante es la seguridad de los datos para su PyME?',
            '¿Qué tan seguros se sienten sus empleados al utilizar nuevas aplicaciones tecnológicas en su trabajo diario?',
            '¿Cómo calificaría la confianza de sus empleados en la seguridad de las aplicaciones de gestión de datos?',
            '¿Qué tan dispuesto está su equipo a adoptar nuevas tecnologías que mejoren la eficiencia y seguridad?',
            '¿Qué tan satisfecho está con las medidas de seguridad actuales para proteger los datos de su PyME?',
            '¿Cómo perciben sus empleados la facilidad de uso de las nuevas tecnologías implementadas en los últimos años?',
            '¿Qué tan importante es para usted y sus empleados tener una aplicación que asegure la confidencialidad y seguridad de los datos de contratos?'
        ]
        respuestas_text = [
            ['a) Ha crecido significativamente', 'b) Ha crecido moderadamente', 'c) Se ha mantenido igual', 'd) Ha disminuido'],
            ['a) Aumento de la demanda de productos/servicios', 'b) Innovación y desarrollo de nuevos productos', 'c) Expansión a nuevos mercados', 'd) Mejora de la eficiencia operativa', 'e) Otros (especifique)'],
            ['a) Menos del 10%', 'b) 10%-25%', 'c) 25%-50%', 'd) Más del 50%'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante'],
            ['a) Muy seguros', 'b) Seguros', 'c) Moderadamente seguros', 'd) Poco seguros'],
            ['a) Muy alta', 'b) Alta', 'c) Moderada', 'd) Baja'],
            ['a) Muy dispuesto', 'b) Dispuesto', 'c) Moderadamente dispuesto', 'd) Poco dispuesto'],
            ['a) Muy satisfecho', 'b) Satisfecho', 'c) Neutral', 'd) Insatisfecho'],
            ['a) Muy fácil', 'b) Fácil', 'c) Moderadamente fácil', 'd) Difícil'],
            ['a) Muy importante', 'b) Importante', 'c) Moderadamente importante', 'd) Poco importante']
        ]
        
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        #
        crecimiento_csv = pd.read_csv('encuestas/encuestas-crecimiento.csv')
        crecimiento_csv.to_sql(name='grafico_crecimiento', con=connection, if_exists='append')
        #
        sql_crecimiento = 'select * from grafico_crecimiento'
        crecimiento = pd.read_sql_query(sql_crecimiento, con=connection)
        
        preguntas = []
        for i in range(10):
            pregunta_url = GenerarImgG_lineal('Pregunta_'+ str(i+1), '', '', '', crecimiento)
            array = [i+1, pregunta_url, preguntas_text[i], respuestas_text[i]]
            preguntas.append(array)
        
        return {
            'template': 'graficos/crecimiento.html',
            'preguntas_url': preguntas
        }
        
class BaseDatos:
    @staticmethod
    def get_context(tabla):
        try:
            consulta = {}
            tablas_info = {}
            
            engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
            insp = inspect(engine)
            tablas = insp.get_table_names()

            for tabla_ in tablas:
                columns = insp.get_columns(tabla_)  
                fks = insp.get_foreign_keys(tabla_)
                indexes = insp.get_indexes(tabla_)
                
                if(tabla_.startswith('grafico_') or tabla_.startswith('respuestas') or tabla_.startswith('preguntas')):
                    continue
                
                tablas_info[tabla_] = {
                    'columns': columns,
                    'foreign_keys': fks,
                    'indexes': indexes
                }
           
           
            Session = sessionmaker(bind=engine)
            session = Session()
            
            template_tabla = ''
            if tabla and tabla == 'usuarios':
                template_tabla = 'graficos/vistas_tablas/tabla_usuarios.html'
                usuarios = session.query(Usuario).all()
                covert = {'usuarios': usuarios}
                consulta.update(covert)
            elif tabla and tabla == 'Contratos':
                template_tabla = 'graficos/vistas_tablas/tabla_contratos.html'
                contratos = session.query(Contratos).all()
                covert = {'contratos': contratos}
                consulta.update(covert)
            elif tabla and tabla == 'Empresas':
                template_tabla = 'graficos/vistas_tablas/tabla_empresas.html'
                empresas = session.query(Empresas).all()
                covert = {'empresas': empresas}
                consulta.update(covert)
            elif tabla and tabla == 'Contratos_Contratistas':
                template_tabla = 'graficos/vistas_tablas/tabla_ccontratistas.html'
                ccontratistas = session.query(ContratosContratistas).all()
                covert = {'ccontratistas': ccontratistas}
                consulta.update(covert)
            elif tabla and tabla == 'Contratistas':
                template_tabla = 'graficos/vistas_tablas/tabla_contratistas.html'
                contratistas = session.query(Contratistas).all()
                covert = {'contratistas': contratistas}
                consulta.update(covert)
                
            
        except SQLAlchemyError as e:
            print(f"Error al conectar con la base de datos: {e}")
        finally:
            engine.dispose()  # Cierra la conexión de manera explícita
            
        #usuarios = Usuario.query.all()
        
        return {
            'template': 'graficos/basedatos.html',
            'template_tabla':template_tabla,
            'tablas': tablas,
            'tabla': tabla,
            'consulta': consulta,
            'tablas_info': tablas_info
        }
         
def GenerarImgGrafica(array, title, xlabel, ylabel, viabilidad):
    conteo_pregunta = viabilidad[array].value_counts()
    
    ax = conteo_pregunta.plot(kind='bar', color=['#6DC5D1', '#FFB4C2', '#FCDC94', '#C5FF95'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Añadir las etiquetas numéricas en cada barra
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    
    # Convertir el gráfico a imagen en base64
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def GenerarImgG_pastel(array, title, xlabel, ylabel, df):
    conteo_pregunta = df[array].value_counts()
    
    # Crear la gráfica de pastel
    plt.figure()
    plt.pie(conteo_pregunta, labels=conteo_pregunta.index, autopct='%1.1f%%',  colors=['#6DC5D1', '#FFB4C2', '#FCDC94', '#C5FF95'])
    plt.title(title)
    
    # Convertir el gráfico a imagen en base64
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def GenerarImgG_lineal(array, title, xlabel, ylabel, viabilidad):
    conteo_pregunta = viabilidad[array].value_counts()
    
    # Convertir los valores del índice a numéricos
    indices_numericos = np_.arange(len(conteo_pregunta))
    
    ax = plt.plot(indices_numericos, conteo_pregunta.values, marker='o', color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Reemplazar las etiquetas del eje X con los valores originales
    plt.xticks(indices_numericos, conteo_pregunta.index)
    
    # Añadir las etiquetas numéricas en cada punto de la línea
    for x, y in zip(indices_numericos, conteo_pregunta.values):
        plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    
    # Convertir el gráfico a imagen en base64
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()