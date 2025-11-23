from datetime import datetime

class Reloj:
    @staticmethod
    def obtener_timestamp():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
    @staticmethod
    def obtener_fecha_hora():
        return datetime.now().strftime("%d/%m/%Y - %H:%M:%S")