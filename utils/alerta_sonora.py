import threading
import platform
import time

class AlertaSonora:
    def __init__(self):
        self.activado = True
        
    def sonar_alerta(self):
        """Activar sonido de alerta"""
        if not self.activado:
            return
            
        hilo = threading.Thread(target=self._reproducir_alerta, daemon=True)
        hilo.start()
    
    def _reproducir_alerta(self):
        """Reproducir sonido de alerta multiplataforma"""
        try:
            if platform.system() == "Windows":
                import winsound
                # Sonido de emergencia (3 bip-bip rápidos)
                for i in range(3):
                    winsound.Beep(1000, 300)  # Frecuencia alta
                    time.sleep(0.2)
                    winsound.Beep(800, 300)   # Frecuencia media
                    time.sleep(0.2)
            else:
                # Para Linux/Mac - sonido del sistema
                for i in range(3):
                    print('\a')  # Beep del sistema
                    time.sleep(0.5)
        except Exception:
            pass
    
    def silenciar(self):
        self.activado = False
        
    def activar(self):
        self.activado = True