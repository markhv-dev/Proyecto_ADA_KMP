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

# ✅ NUEVAS IMPORTACIONES
from config.gestos_auxilio import GestosAuxilio
from config.patrones_auxilio import PatronesAuxilio

class SistemaDeteccionAuxilio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Detección de Auxilio por Gestos")
        self.root.geometry("450x300")
        
        # ✅ NUEVO: Sistema de gestos y patrones mejorado
        self.gestos_auxilio = GestosAuxilio()
        self.patrones_auxilio = PatronesAuxilio()
        
        # Componentes existentes
        self.detector_gestos = DetectorGestos()
        self.procesador_eventos = ProcesadorEventos()
        self.reloj = Reloj()
        
        # ✅ NUEVO: Sistema multi-patrón
        self.detectores_patron = self._inicializar_detectores_patron()
        
        # Sistema de sonido
        self.alerta_sonora = self._inicializar_sonido()
        
        # Variables compartidas
        self.secuencia = ""
        self.ultimo_gesto = ""
        self.alertas = []
        self.ultimo_indice_detectado = -1
        
        # Configurar ventanas
        self.ventana_camara = None
        self.ventana_estado = None
        self.ventana_alertas = None
        
        self.cap = None
        self.ejecutando = False
        
        # ✅ VERIFICAR CONFIGURACIÓN
        self._verificar_carga_config()
        
        self._crear_interfaz_principal()
        self._mostrar_info_sistema()
    
    def _verificar_carga_config(self):
        """Verificar que la configuración se cargó correctamente"""
        print("VERIFICANDO CONFIGURACION...")
        
        # Verificar gestos
        if hasattr(self, 'gestos_auxilio'):
            print(f"OK Gestos cargados: {list(self.gestos_auxilio.gestos_auxilio.keys())}")
        else:
            print("ERROR: gestos_auxilio NO se cargo")
        
        # Verificar patrones
        if hasattr(self, 'patrones_auxilio'):
            print(f"OK Patrones cargados: {list(self.patrones_auxilio.patrones_auxilio.keys())}")
        else:
            print("ERROR: patrones_auxilio NO se cargo")
        
        # Verificar detectores
        if hasattr(self, 'detectores_patron'):
            print(f"OK Detectores creados: {list(self.detectores_patron.keys())}")
        else:
            print("ERROR: detectores_patron NO se crearon")
        
        print("CONFIGURACION VERIFICADA")
    
    def _inicializar_detectores_patron(self):
        """Inicializar detectores KMP para todos los patrones de auxilio"""
        detectores = {}
        try:
            print("Inicializando detectores de patrones...")
            
            if not hasattr(self, 'patrones_auxilio'):
                print("ERROR: patrones_auxilio no disponible")
                return detectores
                
            patrones = self.patrones_auxilio.patrones_auxilio
            if not patrones:
                print("ERROR: No hay patrones definidos")
                return detectores
                
            print(f"Creando detectores para {len(patrones)} patrones...")
            
            for nombre_patron, info in patrones.items():
                try:
                    detector = DetectorPatron(info["patron"])
                    detectores[nombre_patron] = detector
                    print(f"OK Detector: {nombre_patron} -> {info['patron']}")
                except Exception as e:
                    print(f"Error creando detector {nombre_patron}: {e}")
                    
            print(f"Detectores inicializados: {len(detectores)}/{len(patrones)}")
            
        except Exception as e:
            print(f"ERROR en _inicializar_detectores_patron: {e}")
        
        return detectores
        
    def _inicializar_sonido(self):
        """Inicializar sistema de sonido con manejo de errores"""
        try:
            from utils.alerta_sonora import AlertaSonora
            return AlertaSonora()
        except ImportError as e:
            print(f"Advertencia: No se pudo cargar sistema de sonido: {e}")
            class SonidoDummy:
                def sonar_alerta(self): 
                    print("[SONIDO] Alerta sonora simulada")
                def silenciar(self): 
                    print("[SONIDO] Silenciado")
                def activar(self): 
                    print("[SONIDO] Activado")
                activado = True
            return SonidoDummy()
    
    def _mostrar_info_sistema(self):
        """Mostrar información del sistema al iniciar"""
        print("=" * 60)
        print("SISTEMA DE DETECCION DE AUXILIO POR GESTOS")
        print("=" * 60)
        print("GESTOS DISPONIBLES:")
        for letra, info in self.gestos_auxilio.gestos_auxilio.items():
            print(f"   {letra}: {info['nombre']} - {info['descripcion']}")
        print("\nPATRONES DE AUXILIO:")
        for nombre, info in self.patrones_auxilio.patrones_auxilio.items():
            print(f"   {info['patron']}: {info['descripcion']} ({info['urgencia']})")
        print("=" * 60)
        
    def _crear_interfaz_principal(self):
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        titulo = ttk.Label(frame_principal, 
                          text="Sistema de Detección de Auxilio", 
                          font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # ✅ ACTUALIZADO: Información de gestos con D
        info_gestos = ttk.Label(frame_principal, 
                               text="Gestos de Auxilio:\n• A: Mano abierta\n• B: Tres dedos\n• C: Puño cerrado\n• D: Pulgar médico\n• Mantener 1s para repetir",
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
        
        # Configurar grid
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        
    def toggle_sonido(self):
        """Alternar entre sonido activado/desactivado"""
        if self.alerta_sonora.activado:
            self.alerta_sonora.silenciar()
            self.btn_sonido.config(text="🔈 Activar Sonido")
            self.label_estado_sonido.config(text="Sonido: SILENCIADO", foreground="red")
            print("[SONIDO] Alertas sonoras desactivadas")
        else:
            self.alerta_sonora.activar()
            self.btn_sonido.config(text="🔊 Silenciar Alertas")
            self.label_estado_sonido.config(text="Sonido: ACTIVADO", foreground="green")
            print("[SONIDO] Alertas sonoras activadas")
        
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
        
        print("Sistema de deteccion de auxilio iniciado")
        
    def detener_sistema(self):
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
        print("Sistema detenido correctamente")
        
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
        try:
            while self.ejecutando and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: No se pudo leer frame de la cámara")
                    break
                    
                frame = cv2.flip(frame, 1)
                
                gesto_confirmado = self.procesador_eventos.gesto_esta_confirmado()
                frame_procesado, gesto = self.detector_gestos.process_frame(frame, gesto_confirmado)
                
                if gesto:
                    print(f"[DETECTADO] Gesto: {gesto}")
                
                if gesto:
                    secuencia_anterior = self.secuencia
                    self.root.after(0, self._procesar_gesto_en_main_thread, gesto, secuencia_anterior, frame_procesado)
                else:
                    if self.ventana_camara and self.ventana_camara.esta_abierta():
                        self.root.after(0, self._actualizar_camara_en_main_thread, frame_procesado, gesto)
                
                time.sleep(0.05)
                        
        except Exception as e:
            print(f"Error en hilo de video: {e}")
        finally:
            if self.cap:
                self.cap.release()

    def _procesar_gesto_en_main_thread(self, gesto, secuencia_anterior, frame_procesado):
        """Procesar gesto en el hilo principal de Tkinter"""
        try:
            nueva_secuencia = self.procesador_eventos.agregar_letra(gesto, self.secuencia)
            
            print(f"DEBUG: Gesto '{gesto}' - Secuencia anterior: '{secuencia_anterior}' - Nueva: '{nueva_secuencia}'")
            
            if nueva_secuencia != self.secuencia:
                self.secuencia = nueva_secuencia
                self.detector_gestos.activar_efecto_color()
                print(f"AUXILIO Gesto '{gesto}' AGREGADO - Secuencia actual: {self.secuencia}")
                
                # ✅ NUEVO: Verificar TODOS los patrones de auxilio
                patrones_detectados = self._verificar_patrones_auxilio()
                print(f"DEBUG: Patrones verificados: {len(patrones_detectados)} detectados")
                
                for patron_info in patrones_detectados:
                    print(f"ALERTA ACTIVADA: {patron_info['descripcion']}")
                    self._activar_alerta_especifica(patron_info)
            
            if self.ventana_camara and self.ventana_camara.esta_abierta():
                self.ventana_camara.actualizar_frame(frame_procesado, gesto)
                
            if self.ventana_estado and self.ventana_estado.esta_abierta():
                self.ventana_estado.actualizar_estado(self.secuencia, bool(patrones_detectados))
                
        except Exception as e:
            print(f"Error procesando gesto: {e}")

    def _verificar_patrones_auxilio(self):
        """Verificar todos los patrones de auxilio"""
        patrones_detectados = []
        
        print(f"VERIFICANDO PATRONES en secuencia: '{self.secuencia}'")
        
        for nombre_patron, detector in self.detectores_patron.items():
            info_patron = self.patrones_auxilio.patrones_auxilio[nombre_patron]
            resultado = detector.detectar_patron(self.secuencia, self.ultimo_indice_detectado)
            
            print(f"Patron '{info_patron['patron']}': {resultado}")
            
            if resultado["detectado"] and resultado["nuevo"]:
                self.ultimo_indice_detectado = resultado["indice"]
                patrones_detectados.append({
                    'nombre': nombre_patron,
                    'patron': info_patron['patron'],
                    'descripcion': info_patron['descripcion'],
                    'urgencia': info_patron['urgencia'],
                    'accion': info_patron['accion']
                })
                print(f"PATRON DETECTADO: {info_patron['patron']}")
        
        print(f"Total patrones detectados: {len(patrones_detectados)}")
        return patrones_detectados

    def _activar_alerta_especifica(self, patron_info):
        """Activar alerta específica según el patrón detectado"""
        print(f"Activando alerta: {patron_info['urgencia']} - {patron_info['accion']}")
        
        # Sonido de alerta
        self.alerta_sonora.sonar_alerta()
        
        # Popup de alerta
        VentanaAlertaPopup()
        
        # Guardar en log
        self._guardar_alerta_auxilio(patron_info)
        
        # Actualizar interfaz si está abierta
        if self.ventana_alertas and self.ventana_alertas.esta_abierta():
            self.ventana_alertas.actualizar_alertas()

    def _actualizar_camara_en_main_thread(self, frame_procesado, gesto):
        """Actualizar cámara en hilo principal"""
        try:
            if self.ventana_camara and self.ventana_camara.esta_abierta():
                self.ventana_camara.actualizar_frame(frame_procesado, gesto)
        except Exception as e:
            print(f"Error actualizando cámara: {e}")

    def _guardar_alerta_auxilio(self, patron_info):
        """Guardar alerta de auxilio en archivo"""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        alerta = f"AUXILIO [{patron_info['urgencia']}] - {patron_info['descripcion']} - {timestamp}"
        
        os.makedirs("data", exist_ok=True)
        with open("data/alertas_auxilio.txt", "a", encoding="utf-8") as f:
            f.write(f"{alerta}\n")
        
        self.alertas.append(alerta)
            
    def obtener_alertas(self):
        try:
            with open("data/alertas_auxilio.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            return []
            
    def ejecutar(self):
        self.root.mainloop()
        self.detener_sistema()

if __name__ == "__main__":
    app = SistemaDeteccionAuxilio()
    app.ejecutar()