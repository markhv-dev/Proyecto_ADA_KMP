import time

class ProcesadorEventos:
    def __init__(self, max_caracteres=500):
        self.max_caracteres = max_caracteres
        self.ultimo_gesto = None
        self.ultimo_tiempo_gesto = 0
        self.tiempo_repeticion = 1.5  # segundos para repetir el mismo gesto
        self.gesto_confirmado = False
        
    def agregar_letra(self, letra, secuencia_actual):
        # Si no hay gesto detectado, no hacer nada
        if not letra:
            self.gesto_confirmado = False
            return secuencia_actual
            
        tiempo_actual = time.time()
        
        # Si es un gesto nuevo
        if letra != self.ultimo_gesto:
            self.ultimo_gesto = letra
            self.ultimo_tiempo_gesto = tiempo_actual
            self.gesto_confirmado = True
            
            # Agregar letra a la secuencia
            nueva_secuencia = secuencia_actual + letra
            
            # Limitar longitud máxima
            if len(nueva_secuencia) > self.max_caracteres:
                nueva_secuencia = nueva_secuencia[-self.max_caracteres:]
                
            print(f"✅ Nuevo gesto detectado: {letra} - Secuencia: {nueva_secuencia}")
            return nueva_secuencia
            
        # Si es el mismo gesto y ha pasado el tiempo de repetición
        elif (tiempo_actual - self.ultimo_tiempo_gesto) >= self.tiempo_repeticion:
            self.ultimo_tiempo_gesto = tiempo_actual
            self.gesto_confirmado = True
            
            # Agregar letra a la secuencia (repetir)
            nueva_secuencia = secuencia_actual + letra
            
            # Limitar longitud máxima
            if len(nueva_secuencia) > self.max_caracteres:
                nueva_secuencia = nueva_secuencia[-self.max_caracteres:]
                
            print(f"🔄 Gesto repetido: {letra} - Secuencia: {nueva_secuencia}")
            return nueva_secuencia
        
        # Mismo gesto pero aún no pasa el tiempo de repetición
        else:
            self.gesto_confirmado = False
            return secuencia_actual
    
    def gesto_esta_confirmado(self):
        """Indica si el gesto actual fue confirmado y agregado a la secuencia"""
        return self.gesto_confirmado