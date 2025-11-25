import threading
import platform
import time

class AlertaSonora:
    def __init__(self):
        self.activado = True
        
    def sonar_alerta(self):
        """Activar sonido de alerta"""
        print(f"[SONIDO] Intentando reproducir alerta - Activado: {self.activado}")
        if not self.activado:
            return
            
        hilo = threading.Thread(target=self._reproducir_alerta, daemon=True)
        hilo.start()
    
    def _reproducir_alerta(self):
        """Reproducir sonido de alerta"""
        print("[SONIDO] Iniciando reproducción...")
        try:
            if platform.system() == "Windows":
                import winsound
                print("[SONIDO] Usando winsound en Windows")
                # Sonido de emergencia (3 bip-bip rápidos)
                for i in range(3):
                    winsound.Beep(1000, 300)  # Frecuencia alta
                    print(f"[SONIDO] Beep {i+1}")
                    time.sleep(0.2)
                    winsound.Beep(800, 300)   # Frecuencia media
                    time.sleep(0.2)
                    
            else:
                # Para Linux/Mac - sonido del sistema
                print("[SONIDO] Usando beep del sistema")
                for i in range(3):
                    print('\a')  # Beep del sistema
                    time.sleep(0.5)
                    
        except Exception as e:
            print(f"[ERROR SONIDO] {e}")
    
    def silenciar(self):
        self.activado = False
        print("[SONIDO] Silenciado")
        
    def activar(self):
        self.activado = True
        print("[SONIDO] Activado")