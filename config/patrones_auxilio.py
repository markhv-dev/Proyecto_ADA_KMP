class PatronesAuxilio:
    def __init__(self):
        self.patrones_auxilio = {
            "violencia_domestica": {
                "patron": "ABC",
                "descripcion": "Gesto internacional contra violencia doméstica",
                "urgencia": "CRITICA",
                "accion": "contactar_autoridades_locales",
                "sonido": "alerta_critica",
                "color": "rojo"
            },
            "emergencia_medica": {
                "patron": "DDDDD", 
                "descripcion": "Emergencia médica silenciosa - no puedo hablar",
                "urgencia": "ALTA",
                "accion": "contactar_servicios_medicos",
                "sonido": "alerta_medica",
                "color": "naranja"
            },
            "secuestro_retencion": {
                "patron": "AAAAA",
                "descripcion": "Señal de auxilio por secuestro o retención forzada",
                "urgencia": "CRITICA", 
                "accion": "activar_protocolo_antisecuestro",
                "sonido": "alerta_critica",
                "color": "rojo"
            },
            "auxilio_urgente": {
                "patron": "BBBBB",
                "descripcion": "Necesito ayuda urgente - señal discreta",
                "urgencia": "ALTA",
                "accion": "notificar_contactos_emergencia",
                "sonido": "alerta_urgente",
                "color": "naranja"
            },
            "peligro_inminente": {
                "patron": "ACACAC", 
                "descripcion": "Peligro inminente - necesito ayuda inmediata",
                "urgencia": "CRITICA",
                "accion": "activar_alerta_maxima",
                "sonido": "alerta_critica",
                "color": "rojo"
            }
        }
    
    def obtener_patron(self, nombre_patron):
        """Obtener información de un patrón específico"""
        return self.patrones_auxilio.get(nombre_patron, None)
    
    def listar_patrones(self):
        """Listar todos los patrones disponibles"""
        return list(self.patrones_auxilio.keys())