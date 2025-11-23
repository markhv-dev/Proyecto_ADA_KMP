import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

class VentanaCamara:
    def __init__(self, cap):
        self.cap = cap
        self.ventana = tk.Toplevel()
        self.ventana.title("Cámara de seguridad - Reconocimiento de Gestos")
        self.ventana.geometry("800x600")
        
        self.frame_video = ttk.Frame(self.ventana)
        self.frame_video.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label_video = ttk.Label(self.frame_video)
        self.label_video.pack(fill=tk.BOTH, expand=True)
        
        # Frame para información de estado
        self.frame_estado = ttk.Frame(self.ventana)
        self.frame_estado.pack(fill=tk.X, padx=10, pady=5)
        
        self.label_estado = ttk.Label(self.frame_estado, 
                                     text="Mostrando gestos a la cámara...", 
                                     font=("Arial", 11, "bold"))
        self.label_estado.pack()
        
        # Frame para información de colores
        self.frame_colores = ttk.Frame(self.ventana)
        self.frame_colores.pack(fill=tk.X, padx=10, pady=2)
        
        info_colores = ttk.Label(self.frame_colores,
                               text="Verde: Gesto detectado | Azul: Gesto registrado | Amarillo: Gesto confirmado",
                               font=("Arial", 8),
                               foreground="gray")
        info_colores.pack()
        
        self.label_instrucciones = ttk.Label(self.frame_estado,
                                           text="Mantén el gesto 1.5 segundos para repetirlo en la secuencia",
                                           font=("Arial", 9),
                                           foreground="blue")
        self.label_instrucciones.pack()
        
        self.ultimo_gesto = ""
        self.contador_frames_sin_gesto = 0
        
        # Configurar cierre seguro
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        
    def actualizar_frame(self, frame, gesto_detectado):
        try:
            # Convertir frame de BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Redimensionar manteniendo aspect ratio
            h, w = frame_rgb.shape[:2]
            max_w, max_h = 780, 500
            
            # Calcular nuevas dimensiones
            if w > max_w or h > max_h:
                ratio = min(max_w / w, max_h / h)
                new_w = int(w * ratio)
                new_h = int(h * ratio)
                frame_resized = cv2.resize(frame_rgb, (new_w, new_h))
            else:
                frame_resized = frame_rgb
                
            # Convertir a ImageTk
            img = Image.fromarray(frame_resized)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Actualizar label
            self.label_video.configure(image=imgtk)
            self.label_video.image = imgtk
            
            # Actualizar estado
            if gesto_detectado:
                self.ultimo_gesto = gesto_detectado
                self.contador_frames_sin_gesto = 0
                
                # Mapear gestos a descripciones
                descripciones = {
                    'A': 'Mano Abierta (5 dedos)',
                    'B': '3 Dedos Arriba', 
                    'C': 'Puño Cerrado'
                }
                
                descripcion = descripciones.get(gesto_detectado, "Desconocido")
                self.label_estado.configure(text=f"Gesto detectado: {gesto_detectado} - {descripcion}")
                
            elif not gesto_detectado:
                self.contador_frames_sin_gesto += 1
                if self.contador_frames_sin_gesto > 10:  # Después de 10 frames sin gesto
                    self.ultimo_gesto = ""
                    self.label_estado.configure(text="Mostrando gestos a la cámara...")
                
        except Exception as e:
            print(f"Error actualizando frame: {e}")
            
    def cerrar(self):
        self.ventana.destroy()
        
    def esta_abierta(self):
        try:
            return self.ventana.winfo_exists()
        except:
            return False