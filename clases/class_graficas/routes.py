from flask import jsonify, render_template, abort
from .views import TodosView, ViabilidadView, RentabilidadView, AceptabilidadView, FuncionalidadView, SastifaccionView, CrecimientoView, BaseDatos

class Recuperar_Grafica:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param grafico || tabla
    @return 
        ERROR
            status, message
        NO ERROR
            status, context
    '''
    def dashboard(self, grafico, tabla):
        if(grafico == None):
            return jsonify({"status": False, "message": "No se ha enviado el grafico a generar (grafico)"}), 400
        
        
        # Diccionario que mapea los valores del parámetro a clases de vista
        view_classes = {
            'todos': TodosView,
            'viabilidad': ViabilidadView,
            'rentabilidad': RentabilidadView,
            'funcionalidad': FuncionalidadView,
            'aceptabilidad': AceptabilidadView,
            'satisfaccion': SastifaccionView,
            'crecimiento': CrecimientoView,
            'basedatos': BaseDatos
        }

        # Obtener la clase de vista correspondiente
        view_class = view_classes.get(grafico)

        if view_class:
            if grafico == 'basedatos':
                context = view_class.get_context(tabla)
            else:        
                # Obtener el contexto (diccionario) con las variables necesarias
                context = view_class.get_context()
                
            # Renderizar la plantilla principal con el contexto
            return jsonify({"status": True, "context": context}), 200 
        else:
            # Si el parámetro no es válido, devolver un error 404
            return jsonify({"status": False, "message": "Grafíco no encontrado"}), 400
            
        
