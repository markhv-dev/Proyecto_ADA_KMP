import time

class ProcesadorEventos:
    def __init__(self, max_caracteres=500):
        self.max_caracteres = max_caracteres
        self.ultimo_gesto = None
        self.ultimo_tiempo_gesto = 0
        self.tiempo_repeticion = 1.0  # 1 segundo para repetir gesto
        self.gesto_confirmado = False
        self.contador_frames_mismo_gesto = 0
        self.frames_para_confirmar = 8  # Frames necesarios para confirmar gesto
        
    def agregar_letra(self, letra, secuencia_actual):
        """Procesar gesto y agregar a secuencia si cumple condiciones"""
        if not letra:
            self.contador_frames_mismo_gesto = 0
            self.gesto_confirmado = False
            return secuencia_actual
            
        tiempo_actual = time.time()
        
        # Gestos nuevos reinician contadores
        if letra != self.ultimo_gesto:
            self.ultimo_gesto = letra
            self.ultimo_tiempo_gesto = tiempo_actual
            self.contador_frames_mismo_gesto = 1
            self.gesto_confirmado = False
            return secuencia_actual
            
        # Mismo gesto - incrementar contador
        else:
            self.contador_frames_mismo_gesto += 1
            
            # Verificar condiciones para agregar a secuencia
            if (self.contador_frames_mismo_gesto >= self.frames_para_confirmar and 
                (tiempo_actual - self.ultimo_tiempo_gesto) >= self.tiempo_repeticion):
                
                self.ultimo_tiempo_gesto = tiempo_actual
                self.gesto_confirmado = True
                
                # Agregar letra y limitar longitud
                nueva_secuencia = secuencia_actual + letra
                if len(nueva_secuencia) > self.max_caracteres:
                    nueva_secuencia = nueva_secuencia[-self.max_caracteres:]
                    
                return nueva_secuencia
        
        # No cumplió condiciones para agregar
        self.gesto_confirmado = False
        return secuencia_actual
    
    def gesto_esta_confirmado(self):
        """Verificar si el gesto actual fue confirmado"""
        return self.gesto_confirmado