import tkinter as tk
from tkinter import ttk
import cv2
import threading
import time
from datetime import datetime
import os
import sys

# Configurar encoding para Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from interfaz.ventana_cam import VentanaCamara
from interfaz.ventana_estado import VentanaEstado
from interfaz.ventana_alertas import VentanaAlertas
from interfaz.ventana_popup_alerta import VentanaAlertaPopup
from vision.detector_gestos import DetectorGestos
from vision.procesador_eventos import ProcesadorEventos
from kmp.detector_patron import DetectorPatron
from utils.reloj import Reloj
from config.gestos_auxilio import GestosAuxilio
from config.patrones_auxilio import PatronesAuxilio

class SistemaDeteccionAuxilio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Detección de Auxilio por Gestos")
        self.root.geometry("350x320")
        
        # Sistema de configuración
        self.gestos_auxilio = GestosAuxilio()
        self.patrones_auxilio = PatronesAuxilio()
        
        # Componentes del sistema
        self.detector_gestos = DetectorGestos()
        self.procesador_eventos = ProcesadorEventos()
        self.reloj = Reloj()
        self.detectores_patron = self._inicializar_detectores_patron()
        self.alerta_sonora = self._inicializar_sonido()
        
        # Estado del sistema
        self.secuencia = ""
        self.ultimo_gesto = ""
        self.alertas = []
        self.ultimo_indice_detectado = -1
        
        # Control de ventanas y cámara
        self.ventana_camara = None
        self.ventana_estado = None
        self.ventana_alertas = None
        self.cap = None
        self.ejecutando = False
        
        self._crear_interfaz_principal()
    
    def _inicializar_detectores_patron(self):
        """Inicializar detectores KMP para todos los patrones"""
        detectores = {}
        try:
            patrones = self.patrones_auxilio.patrones_auxilio
            for nombre_patron, info in patrones.items():
                detector = DetectorPatron(info["patron"])
                detectores[nombre_patron] = detector
        except Exception:
            pass
        return detectores
        
    def _inicializar_sonido(self):
        """Inicializar sistema de sonido con manejo de errores"""
        try:
            from utils.alerta_sonora import AlertaSonora
            return AlertaSonora()
        except ImportError:
            class SonidoDummy:
                def sonar_alerta(self): pass
                def silenciar(self): pass
                def activar(self): pass
                activado = True
            return SonidoDummy()
        
    def _crear_interfaz_principal(self):
        """Crear interfaz principal del sistema"""
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título y información
        titulo = ttk.Label(frame_principal, 
                          text="Sistema de Detección de Auxilio", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        info_gestos = ttk.Label(frame_principal, 
                               text="Gestos de Auxilio:\n• A: Mano abierta\n• B: Tres dedos\n• C: Puño cerrado\n• D: Pulgar médico\n• Mantener 1s para repetir",
                               justify=tk.LEFT)
        info_gestos.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Botones de control del sistema
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
        
        # Control de sonido
        frame_sonido = ttk.Frame(frame_principal)
        frame_sonido.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.btn_sonido = ttk.Button(
            frame_sonido, 
            text="🔊 Silenciar Alertas", 
            command=self.toggle_sonido
        )
        self.btn_sonido.pack(side=tk.LEFT, padx=(0, 10))
        
        self.label_estado_sonido = ttk.Label(
            frame_sonido, 
            text="Sonido: ACTIVADO", 
            foreground="green",
            font=("Arial", 9)
        )
        self.label_estado_sonido.pack(side=tk.LEFT)
        
        # Configuración de grid
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        
    def toggle_sonido(self):
        """Alternar entre sonido activado/desactivado"""
        if self.alerta_sonora.activado:
            self.alerta_sonora.silenciar()
            self.btn_sonido.config(text="🔈 Activar Sonido")
            self.label_estado_sonido.config(text="Sonido: SILENCIADO", foreground="red")
        else:
            self.alerta_sonora.activar()
            self.btn_sonido.config(text="🔊 Silenciar Alertas")
            self.label_estado_sonido.config(text="Sonido: ACTIVADO", foreground="green")
        
    def iniciar_sistema(self):
        """Iniciar sistema de captura y procesamiento"""
        if self.ejecutando:
            return
            
        if self.ventana_camara and not self.ventana_camara.esta_abierta():
            self.ventana_camara = None
            
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return
            
        # Configurar cámara
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 15)
            
        self.ejecutando = True
        
        # Iniciar ventana y procesamiento
        self.ventana_camara = VentanaCamara(self.cap)
        self.hilo_procesamiento = threading.Thread(target=self._procesar_video)
        self.hilo_procesamiento.daemon = True
        self.hilo_procesamiento.start()
        
    def detener_sistema(self):
        """Detener sistema de forma segura"""
        self.ejecutando = False
        time.sleep(0.5)
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
        if self.ventana_camara:
            try:
                self.ventana_camara.cerrar()
            except:
                pass
            self.ventana_camara = None
            
        cv2.destroyAllWindows()
        
    def abrir_ventana_estado(self):
        """Abrir ventana de estado del sistema"""
        if self.ventana_estado and not self.ventana_estado.esta_abierta():
            self.ventana_estado = None
            
        if not self.ventana_estado:
            self.ventana_estado = VentanaEstado(self)
        self.ventana_estado.mostrar()
            
    def abrir_ventana_alertas(self):
        """Abrir ventana de registro de alertas"""
        if self.ventana_alertas and not self.ventana_alertas.esta_abierta():
            self.ventana_alertas = None
            
        if not self.ventana_alertas:
            self.ventana_alertas = VentanaAlertas(self)
        self.ventana_alertas.actualizar_alertas()
        self.ventana_alertas.mostrar()
    
    def _procesar_video(self):
        """Procesar video en hilo separado"""
        try:
            while self.ejecutando and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                frame = cv2.flip(frame, 1)
                
                gesto_confirmado = self.procesador_eventos.gesto_esta_confirmado()
                frame_procesado, gesto = self.detector_gestos.process_frame(frame, gesto_confirmado)
                
                if gesto:
                    secuencia_anterior = self.secuencia
                    self.root.after(0, self._procesar_gesto_en_main_thread, gesto, secuencia_anterior, frame_procesado)
                else:
                    if self.ventana_camara and self.ventana_camara.esta_abierta():
                        self.root.after(0, self._actualizar_camara_en_main_thread, frame_procesado, gesto)
                
                time.sleep(0.05)
                        
        except Exception:
            pass
        finally:
            if self.cap:
                self.cap.release()

    def _procesar_gesto_en_main_thread(self, gesto, secuencia_anterior, frame_procesado):
        """Procesar gesto detectado en el hilo principal"""
        try:
            patrones_detectados = []  
            
            nueva_secuencia = self.procesador_eventos.agregar_letra(gesto, self.secuencia)
            
            if nueva_secuencia != self.secuencia:
                self.secuencia = nueva_secuencia
                self.detector_gestos.activar_efecto_color()
                
                patrones_detectados = self._verificar_patrones_auxilio()
                
                if patrones_detectados:
                    self._limpiar_secuencia_despues_alerta()
                    for patron_info in patrones_detectados:
                        self._activar_alerta_especifica(patron_info)
            
            # Actualizar interfaces
            if self.ventana_camara and self.ventana_camara.esta_abierta():
                self.ventana_camara.actualizar_frame(frame_procesado, gesto)
                
            if self.ventana_estado and self.ventana_estado.esta_abierta():
                self.ventana_estado.actualizar_estado(self.secuencia, bool(patrones_detectados))
                
        except Exception:
            pass

    def _limpiar_secuencia_despues_alerta(self):
        """Limpiar secuencia después de detectar patrón"""
        self.secuencia = ""
        self.ultimo_indice_detectado = -1

    def _verificar_patrones_auxilio(self):
        """Verificar todos los patrones de auxilio en la secuencia"""
        patrones_detectados = []
        
        for nombre_patron, detector in self.detectores_patron.items():
            info_patron = self.patrones_auxilio.patrones_auxilio[nombre_patron]
            resultado = detector.detectar_patron(self.secuencia, self.ultimo_indice_detectado)
            
            if resultado["detectado"] and resultado["nuevo"]:
                self.ultimo_indice_detectado = resultado["indice"]
                patrones_detectados.append({
                    'nombre': nombre_patron,
                    'patron': info_patron['patron'],
                    'descripcion': info_patron['descripcion'],
                    'urgencia': info_patron['urgencia'],
                    'accion': info_patron['accion']
                })
        
        return patrones_detectados

    def _activar_alerta_especifica(self, patron_info):
        """Activar alerta específica según el patrón detectado"""
        self.alerta_sonora.sonar_alerta()
        VentanaAlertaPopup()
        self._guardar_alerta_auxilio(patron_info)
        
        if self.ventana_alertas and self.ventana_alertas.esta_abierta():
            self.ventana_alertas.actualizar_alertas()

    def _actualizar_camara_en_main_thread(self, frame_procesado, gesto):
        """Actualizar cámara en hilo principal"""
        try:
            if self.ventana_camara and self.ventana_camara.esta_abierta():
                self.ventana_camara.actualizar_frame(frame_procesado, gesto)
        except Exception:
            pass

    def _guardar_alerta_auxilio(self, patron_info):
        """Guardar alerta en archivo de registro"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        alerta = f"AUXILIO [{patron_info['urgencia']}] - {patron_info['descripcion']} - {timestamp}"
        
        os.makedirs("data", exist_ok=True)
        with open("data/alertas_auxilio.txt", "a", encoding="utf-8") as f:
            f.write(f"{alerta}\n")
        
        self.alertas.append(alerta)
            
    def obtener_alertas(self):
        """Obtener historial de alertas"""
        try:
            with open("data/alertas_auxilio.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
            
    def ejecutar(self):
        """Ejecutar aplicación principal"""
        self.root.mainloop()
        self.detener_sistema()

if __name__ == "__main__":
    app = SistemaDeteccionAuxilio()
    app.ejecutar()