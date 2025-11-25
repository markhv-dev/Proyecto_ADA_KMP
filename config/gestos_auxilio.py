class GestosAuxilio:
    def __init__(self):
        self.gestos_auxilio = {
            'A': {
                'nombre': 'Mano Abierta',
                'dedos': 5,
                'descripcion': 'Mano completamente abierta - 5 dedos extendidos',
                'uso': 'Señal básica de auxilio',
                'color': 'verde'
            },
            'B': {
                'nombre': 'Tres Dedos Emergencia', 
                'dedos': 3,
                'descripcion': 'Índice, medio y anular extendidos - señal de emergencia',
                'uso': 'Auxilio discreto en público',
                'color': 'amarillo'
            },
            'C': {
                'nombre': 'Puño Cerrado',
                'dedos': 0,
                'descripcion': 'Mano completamente cerrada - 0 dedos extendidos',
                'uso': 'Parte de secuencias de auxilio',
                'color': 'naranja'
            },
            'D': {
                'nombre': 'Pulgar Auxilio Médico',
                'dedos': 1,
                'descripcion': 'Solo pulgar extendido - emergencia médica silenciosa',
                'uso': 'Auxilio médico cuando no se puede hablar',
                'color': 'rojo'
            }
        }
    
    def obtener_info_gesto(self, letra_gesto):
        """Obtener información de un gesto específico"""
        return self.gestos_auxilio.get(letra_gesto, None)
    
    def listar_gestos(self):
        """Listar todos los gestos disponibles"""
        return list(self.gestos_auxilio.keys())