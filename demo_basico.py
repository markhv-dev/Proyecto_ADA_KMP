#!/usr/bin/env python3
"""
DEMO BÁSICO - Sistema de Gestos sin MediaPipe
Para presentación cuando MediaPipe no funciona por incompatibilidad de macOS
"""

import cv2
import tkinter as tk
from tkinter import messagebox
import threading
import time

class GestoDemoBasico:
    def __init__(self):
        self.cap = None
        self.running = False
        self.gestos_simulados = ['A', 'B', 'C', 'D']
        self.gesto_actual = 0
        self.secuencia = ""
        self.patrones = {
            'ABC': 'Violencia Doméstica - CRÍTICA',
            'DDDDD': 'Emergencia Médica - ALTA',
            'AAAAA': 'Secuestro/Retención - CRÍTICA'
        }

    def iniciar_demo(self):
        """Iniciar demo básico con simulación de gestos"""
        print("🎬 DEMO BÁSICO INICIADO")
        print("📋 Instrucciones:")
        print("   Presiona ESPACIO para simular detección de gestos A->B->C")
        print("   Presiona 'q' para salir")
        print("   Presiona 'r' para reiniciar secuencia")
        print()

        try:
            self.cap = cv2.VideoCapture(0)
            self.running = True

            print("✅ Cámara iniciada correctamente")
            print("🎯 Simulando Sistema de Detección de Gestos de Auxilio")
            print("=" * 60)

            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Error al leer la cámara")
                    break

                # Voltear frame horizontalmente
                frame = cv2.flip(frame, 1)

                # Dibujar información del demo
                self._dibujar_interfaz_demo(frame)

                # Mostrar frame
                cv2.imshow('🎬 DEMO - Sistema de Detección de Auxilio', frame)

                # Manejar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord(' '):  # ESPACIO
                    self._simular_deteccion()
                elif key == ord('r'):  # R
                    self._reiniciar_secuencia()

        except Exception as e:
            print(f"❌ Error en demo: {e}")
        finally:
            self._limpiar_recursos()

    def _dibujar_interfaz_demo(self, frame):
        """Dibujar interfaz del demo"""
        h, w = frame.shape[:2]

        # Título principal
        cv2.putText(frame, "DEMO - Sistema de Deteccion de Auxilio",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # Estado actual
        estado = f"Secuencia actual: {self.secuencia if self.secuencia else '[Vacía]'}"
        cv2.putText(frame, estado, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Gestos disponibles
        gestos_texto = "Gestos: A(Mano abierta) B(3 dedos) C(Puño) D(Pulgar)"
        cv2.putText(frame, gestos_texto, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Patrones de emergencia
        y_pos = 140
        cv2.putText(frame, "PATRONES DE EMERGENCIA:", (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        y_pos += 25

        for patron, descripcion in self.patrones.items():
            texto = f"  {patron}: {descripcion}"
            cv2.putText(frame, texto, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 200, 0), 1)
            y_pos += 20

        # Instrucciones
        instrucciones = [
            "CONTROLES:",
            "ESPACIO: Simular gesto (A->B->C->D)",
            "R: Reiniciar secuencia",
            "Q: Salir"
        ]

        y_start = h - 100
        for i, inst in enumerate(instrucciones):
            color = (100, 255, 255) if i == 0 else (255, 255, 255)
            cv2.putText(frame, inst, (10, y_start + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        # Simulación de área de detección
        cv2.rectangle(frame, (w//2 - 100, h//2 - 100), (w//2 + 100, h//2 + 100), (0, 255, 0), 2)
        cv2.putText(frame, "Área de detección", (w//2 - 80, h//2 - 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Mostrar próximo gesto
        proximo_gesto = self.gestos_simulados[self.gesto_actual]
        cv2.putText(frame, f"Próximo: {proximo_gesto}", (w//2 - 50, h//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    def _simular_deteccion(self):
        """Simular detección de un gesto"""
        gesto = self.gestos_simulados[self.gesto_actual]
        self.secuencia += gesto

        print(f"🖐️  GESTO DETECTADO: {gesto}")
        print(f"📝 Secuencia actual: {self.secuencia}")

        # Verificar patrones
        self._verificar_patrones()

        # Avanzar al siguiente gesto
        self.gesto_actual = (self.gesto_actual + 1) % len(self.gestos_simulados)

    def _verificar_patrones(self):
        """Verificar si se detectó algún patrón de emergencia"""
        for patron, descripcion in self.patrones.items():
            if patron in self.secuencia:
                print("=" * 60)
                print("🚨 ¡PATRÓN DE AUXILIO DETECTADO!")
                print(f"🔴 Patrón: {patron}")
                print(f"📋 Tipo: {descripcion}")
                print(f"⏰ Timestamp: {time.strftime('%H:%M:%S')}")
                print("🔊 [ALERTA SONORA ACTIVADA]")
                print("=" * 60)

                # Simular sonido (print en lugar de beep)
                print("♪♪♪ BEEP BEEP BEEP ♪♪♪")

                # Crear popup de alerta
                self._mostrar_alerta_popup(patron, descripcion)

                # Limpiar secuencia después de detección
                self.secuencia = ""
                return True
        return False

    def _mostrar_alerta_popup(self, patron, descripcion):
        """Mostrar popup de alerta en hilo separado"""
        def crear_popup():
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal

            mensaje = f"¡ALERTA DE AUXILIO DETECTADA!\n\nPatrón: {patron}\n{descripcion}\n\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"

            messagebox.showwarning("🚨 ALERTA DE AUXILIO 🚨", mensaje)
            root.destroy()

        # Ejecutar popup en hilo separado
        threading.Thread(target=crear_popup, daemon=True).start()

    def _reiniciar_secuencia(self):
        """Reiniciar la secuencia actual"""
        self.secuencia = ""
        self.gesto_actual = 0
        print("🔄 Secuencia reiniciada")

    def _limpiar_recursos(self):
        """Limpiar recursos al salir"""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Demo finalizado")

def main():
    """Función principal del demo"""
    print("🎬 INICIANDO DEMO BÁSICO DEL SISTEMA DE GESTOS")
    print("💡 Este demo simula el sistema original sin MediaPipe")
    print("🔧 Útil para demostraciones cuando hay problemas de compatibilidad")
    print()

    demo = GestoDemoBasico()

    try:
        demo.iniciar_demo()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        print("👋 ¡Gracias por probar el demo!")

if __name__ == "__main__":
    main()