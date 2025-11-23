import tkinter as tk
from tkinter import ttk
import threading
import time

class VentanaAlertaPopup:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title("ALERTA")
        self.ventana.geometry("400x200")
        self.ventana.configure(bg='red')
        
        # Centrar ventana
        self.ventana.geometry("+%d+%d" % (
            self.ventana.winfo_screenwidth() // 2 - 200,
            self.ventana.winfo_screenheight() // 2 - 100
        ))
        
        # Hacer ventana modal
        self.ventana.transient()
        self.ventana.grab_set()
        
        # Texto de alerta
        label_alerta = ttk.Label(
            self.ventana, 
            text="ALERTA", 
            font=("Arial", 32, "bold"),
            foreground="white",
            background="red"
        )
        label_alerta.pack(expand=True)
        
        # Iniciar temporizador para cerrar automáticamente
        self.hilo_temporizador = threading.Thread(target=self._cerrar_automaticamente)
        self.hilo_temporizador.daemon = True
        self.hilo_temporizador.start()
        
    def _cerrar_automaticamente(self):
        time.sleep(2)  # 2 segundos
        self.ventana.after(0, self.cerrar)
        
    def cerrar(self):
        try:
            self.ventana.destroy()
        except:
            pass