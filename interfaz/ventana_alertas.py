import tkinter as tk
from tkinter import ttk, scrolledtext

class VentanaAlertas:
    def __init__(self, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel()
        self.ventana.title("Historial de alertas")
        self.ventana.geometry("500x400")
        
        self._crear_interfaz()
        self.actualizar_alertas()
        
        # Configurar cierre seguro
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        
    def _crear_interfaz(self):
        frame_principal = ttk.Frame(self.ventana, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, 
                          text="Historial de Alertas", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Área de texto para alertas
        self.texto_alertas = scrolledtext.ScrolledText(
            frame_principal, 
            wrap=tk.WORD, 
            width=50, 
            height=15,
            font=("Courier", 10)
        )
        self.texto_alertas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(fill=tk.X)
        
        btn_actualizar = ttk.Button(
            frame_botones, 
            text="Actualizar", 
            command=self.actualizar_alertas
        )
        btn_actualizar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_limpiar = ttk.Button(
            frame_botones, 
            text="Limpiar Historial", 
            command=self.limpiar_historial
        )
        btn_limpiar.pack(side=tk.LEFT)
        
    def actualizar_alertas(self):
        alertas = self.sistema.obtener_alertas()
        
        self.texto_alertas.delete(1.0, tk.END)
        
        if not alertas:
            self.texto_alertas.insert(tk.END, "No hay alertas registradas.")
        else:
            for i, alerta in enumerate(alertas, 1):
                self.texto_alertas.insert(tk.END, f"{i}. {alerta}\n")
                
    def limpiar_historial(self):
        try:
            open("data/alertas.txt", "w").close()
            self.actualizar_alertas()
        except Exception as e:
            print(f"Error limpiando historial: {e}")
            
    def mostrar(self):
        self.ventana.deiconify()
        self.ventana.lift()
        
    def cerrar(self):
        self.ventana.destroy()
            
    def esta_abierta(self):
        try:
            return self.ventana.winfo_exists()
        except:
            return False