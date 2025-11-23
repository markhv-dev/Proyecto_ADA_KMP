import tkinter as tk
from tkinter import ttk
import cv2
import threading
import time
from datetime import datetime
import os

from interfaz.ventana_cam import VentanaCamara
from interfaz.ventana_estado import VentanaEstado
from interfaz.ventana_alertas import VentanaAlertas
from interfaz.ventana_popup_alerta import VentanaAlertaPopup
from vision.detector_gestos import DetectorGestos
from vision.procesador_eventos import ProcesadorEventos
from kmp.detector_patron import DetectorPatron
from utils.reloj import Reloj

class SistemaDeteccionAuxilio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Detección de Señal de Auxilio - Por Gestos")
        self.root.geometry("400x250")
        
        # Inicializar componentes
        self.detector_gestos = DetectorGestos()
        self.detector_patron = DetectorPatron("AAABBBCCC")
        self.procesador_eventos = ProcesadorEventos()
        self.reloj = Reloj()
        
        # Variables compartidas
        self.secuencia = ""
        self.ultimo_gesto = ""
        self.patron_detectado = False
        self.ultimo_indice_detectado = -1
        self.alertas = []
        
        # Configurar ventanas
        self.ventana_camara = None
        self.ventana_estado = None
        self.ventana_alertas = None
        
        self.cap = None
        self.ejecutando = False
        
        self._crear_interfaz_principal()
        
    def _crear_interfaz_principal(self):
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        titulo = ttk.Label(frame_principal, 
                          text="Sistema de Detección por Gestos", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Información de gestos
        info_gestos = ttk.Label(frame_principal, 
                               text="Gestos:\n• A: Mano abierta (5 dedos)\n• B: 3 dedos arriba\n• C: Puño cerrado\n• Mantener 1.5s para repetir",
                               justify=tk.LEFT)
        info_gestos.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        btn_iniciar = ttk.Button(frame_principal, 
                                text="Iniciar Sistema", 
                                command=self.iniciar_sistema)
        btn_iniciar.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="ew")
        
        btn_detener = ttk.Button(frame_principal, 
                                text="Detener Sistema", 
                                command=self.detener_sistema)
        btn_detener.grid(row=2, column=1, padx=(10, 0), pady=5, sticky="ew")
        
        btn_estado = ttk.Button(frame_principal, 
                               text="Abrir Ventana Estado", 
                               command=self.abrir_ventana_estado)
        btn_estado.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        
        btn_alertas = ttk.Button(frame_principal, 
                                text="Registro de Alertas", 
                                command=self.abrir_ventana_alertas)
        btn_alertas.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Configurar grid
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        
    def iniciar_sistema(self):
        if self.ejecutando:
            return
            
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return
            
        # Configurar cámara
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
            
        self.ejecutando = True
        
        # Iniciar ventana de cámara
        self.ventana_camara = VentanaCamara(self.cap)
        
        # Iniciar hilo de procesamiento
        self.hilo_procesamiento = threading.Thread(target=self._procesar_video)
        self.hilo_procesamiento.daemon = True
        self.hilo_procesamiento.start()
        
        print("Sistema de gestos iniciado")
        
    def detener_sistema(self):
        self.ejecutando = False
        if self.cap:
            self.cap.release()
        if self.ventana_camara:
            self.ventana_camara.cerrar()
        print("Sistema detenido")
        
    def abrir_ventana_estado(self):
        if not self.ventana_estado:
            self.ventana_estado = VentanaEstado(self)
        else:
            self.ventana_estado.mostrar()
            
    def abrir_ventana_alertas(self):
        if not self.ventana_alertas:
            self.ventana_alertas = VentanaAlertas(self)
        else:
            self.ventana_alertas.actualizar_alertas()
            self.ventana_alertas.mostrar()
    
    def _procesar_video(self):
        while self.ejecutando and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Voltear frame horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)
            
            # Detectar gestos
            gesto_confirmado = self.procesador_eventos.gesto_esta_confirmado()
            frame_procesado, gesto = self.detector_gestos.process_frame(frame, gesto_confirmado)
            
            # Procesar evento
            if gesto:
                secuencia_anterior = self.secuencia
                self.secuencia = self.procesador_eventos.agregar_letra(gesto, self.secuencia)
                
                # Si se agregó un nuevo gesto, activar efecto de color azul
                if self.secuencia != secuencia_anterior:
                    self.detector_gestos.activar_efecto_color()
                    print(f"🎯 Gesto '{gesto}' agregado a secuencia: {self.secuencia}")
                    
                    # Detectar patrón
                    resultado = self.detector_patron.detectar_patron(self.secuencia, self.ultimo_indice_detectado)
                    
                    if resultado["detectado"] and resultado["nuevo"]:
                        self.patron_detectado = True
                        self.ultimo_indice_detectado = resultado["indice"]
                        self._activar_alerta()
                        print(f"🚨 ALERTA! Patrón detectado en índice: {resultado['indice']}")
                    else:
                        self.patron_detectado = False
                    
            # Actualizar ventana de cámara
            if self.ventana_camara:
                self.ventana_camara.actualizar_frame(frame_procesado, gesto)
                
            # Actualizar ventana de estado si está abierta
            if self.ventana_estado and self.ventana_estado.esta_abierta():
                self.ventana_estado.actualizar_estado(self.secuencia, self.patron_detectado)
                
            time.sleep(0.05)  # Controlar FPS
            
    def _activar_alerta(self):
        # Registrar alerta
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        alerta = f"ALERTA - {timestamp}"
        self.alertas.append(alerta)
        
        # Guardar en archivo
        self._guardar_alerta(alerta)
        
        # Mostrar ventana de alerta
        VentanaAlertaPopup()
        
        # Actualizar ventana de alertas si está abierta
        if self.ventana_alertas and self.ventana_alertas.esta_abierta():
            self.ventana_alertas.actualizar_alertas()
            
    def _guardar_alerta(self, alerta):
        os.makedirs("data", exist_ok=True)
        with open("data/alertas.txt", "a", encoding="utf-8") as f:
            f.write(f"{alerta}\n")
            
    def obtener_alertas(self):
        try:
            with open("data/alertas.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
            
    def ejecutar(self):
        self.root.mainloop()
        
        # Limpiar al cerrar
        self.detener_sistema()

if __name__ == "__main__":
    app = SistemaDeteccionAuxilio()
    app.ejecutar()