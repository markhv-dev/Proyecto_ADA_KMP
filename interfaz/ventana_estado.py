import tkinter as tk
from tkinter import ttk

class VentanaEstado:
    def __init__(self, sistema):
        self.sistema = sistema
        self.ventana = tk.Toplevel()
        self.ventana.title("Lectura del patrón y estado del sistema - Gestos")
        self.ventana.geometry("700x500")
        
        self._crear_interfaz()
        
        # Configurar cierre seguro
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        
    def _crear_interfaz(self):
        frame_principal = ttk.Frame(self.ventana, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, 
                          text="Estado del Sistema - Reconocimiento por Gestos", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Información de gestos
        frame_info_gestos = ttk.LabelFrame(frame_principal, text="Gestos Reconocidos", padding="10")
        frame_info_gestos.pack(fill=tk.X, pady=(0, 10))
        
        info_gestos = ttk.Label(frame_info_gestos, 
                               text="A: Mano abierta (5 dedos)   |   B: 3 dedos arriba   |   C: Puño cerrado",
                               justify=tk.CENTER,
                               font=("Arial", 10))
        info_gestos.pack()
        
        # Secuencia detectada
        frame_secuencia = ttk.LabelFrame(frame_principal, text="Secuencia detectada (últimos 50 caracteres)", padding="10")
        frame_secuencia.pack(fill=tk.X, pady=(0, 10))
        
        self.label_secuencia = ttk.Label(frame_secuencia, 
                                        text="Esperando gestos...", 
                                        font=("Courier", 14, "bold"),
                                        background="black",
                                        foreground="white",
                                        anchor="center",
                                        padding=10)
        self.label_secuencia.pack(fill=tk.X)
        
        # Contador de caracteres
        frame_contador = ttk.Frame(frame_secuencia)
        frame_contador.pack(fill=tk.X, pady=(5, 0))
        
        self.label_contador = ttk.Label(frame_contador, 
                                       text="Longitud: 0 caracteres",
                                       font=("Arial", 9))
        self.label_contador.pack(side=tk.RIGHT)
        
        # Estado del patrón
        frame_patron = ttk.LabelFrame(frame_principal, text="Estado del patrón 'AAABBBCCC'", padding="15")
        frame_patron.pack(fill=tk.X, pady=(0, 10))
        
        self.label_patron = ttk.Label(frame_patron, 
                                     text="NO DETECTADO", 
                                     font=("Arial", 16, "bold"),
                                     foreground="green")
        self.label_patron.pack()
        
        # Información adicional
        frame_info = ttk.LabelFrame(frame_principal, text="Información del Sistema", padding="10")
        frame_info.pack(fill=tk.BOTH, expand=True)
        
        info_text = (
            "• El sistema detecta gestos de mano en tiempo real\n"
            "• Cada gesto válido se agrega a la secuencia\n" 
            "• Cuando se detecta el patrón AAABBBCCC se activa una alerta\n"
            "• Solo se generan alertas para patrones nuevos (no solapados)"
        )
        
        label_info = ttk.Label(frame_info, text=info_text, justify=tk.LEFT, font=("Arial", 10))
        label_info.pack(anchor=tk.W)
        
    def actualizar_estado(self, secuencia, patron_detectado):
        # Actualizar secuencia (mostrar últimos 50 caracteres)
        if secuencia:
            secuencia_mostrar = secuencia[-50:] if len(secuencia) > 50 else secuencia
            self.label_secuencia.configure(text=secuencia_mostrar)
            self.label_contador.configure(text=f"Longitud: {len(secuencia)} caracteres")
        else:
            self.label_secuencia.configure(text="Esperando gestos...")
            self.label_contador.configure(text="Longitud: 0 caracteres")
        
        # Actualizar estado del patrón
        if patron_detectado:
            self.label_patron.configure(
                text="PATRÓN DETECTADO - ALERTA ACTIVADA", 
                foreground="red"
            )
        else:
            self.label_patron.configure(
                text="NO DETECTADO", 
                foreground="green"
            )
            
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