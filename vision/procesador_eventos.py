import time

class ProcesadorEventos:
    def __init__(self, max_caracteres=500):
        self.max_caracteres = max_caracteres
        self.ultimo_gesto = None
        self.ultimo_tiempo_gesto = 0
        self.tiempo_repeticion = 1.0  # 1 segundo para repetir (antes era 1.5)
        self.gesto_confirmado = False
        self.contador_frames_mismo_gesto = 0
        self.frames_para_confirmar = 8
        
    def agregar_letra(self, letra, secuencia_actual):
        # Si no hay gesto detectado, resetear contadores
        if not letra:
            self.contador_frames_mismo_gesto = 0
            self.gesto_confirmado = False
            return secuencia_actual
            
        tiempo_actual = time.time()
        
        # Si es un gesto nuevo
        if letra != self.ultimo_gesto:
            self.ultimo_gesto = letra
            self.ultimo_tiempo_gesto = tiempo_actual
            self.contador_frames_mismo_gesto = 1
            self.gesto_confirmado = False
            return secuencia_actual  # No agregar inmediatamente
            
        # Si es el mismo gesto
        else:
            self.contador_frames_mismo_gesto += 1
            
            # Si hemos tenido el mismo gesto por suficientes frames Y ha pasado el tiempo de repetición
            if (self.contador_frames_mismo_gesto >= self.frames_para_confirmar and 
                (tiempo_actual - self.ultimo_tiempo_gesto) >= self.tiempo_repeticion):
                
                self.ultimo_tiempo_gesto = tiempo_actual
                self.gesto_confirmado = True
                
                # Agregar letra a la secuencia
                nueva_secuencia = secuencia_actual + letra
                
                # Limitar longitud máxima
                if len(nueva_secuencia) > self.max_caracteres:
                    nueva_secuencia = nueva_secuencia[-self.max_caracteres:]
                    
                print(f"[AUXILIO] Gesto '{letra}' agregado - Secuencia: {nueva_secuencia}")
                return nueva_secuencia
        
        # No cumplió las condiciones para agregar
        self.gesto_confirmado = False
        return secuencia_actual
    
    def gesto_esta_confirmado(self):
        """Indica si el gesto actual fue confirmado y agregado a la secuencia"""
        return self.gesto_confirmado