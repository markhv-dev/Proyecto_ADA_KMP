import cv2
import mediapipe as mp
import numpy as np
import time

class DetectorGestos:
    def __init__(self):
        # Configuración de MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Definición de gestos de auxilio
        self.gestures = {
            'A': 'Mano Abierta (5 dedos)',
            'B': '3 Dedos Emergencia', 
            'C': 'Puño Cerrado',
            'D': 'Pulgar Auxilio Médico'
        }
        
        # Control de efectos visuales
        self.efecto_color_activo = False
        self.tiempo_inicio_color = 0
        self.duracion_color = 0.5
        
    def count_fingers(self, landmarks):
        """Contar dedos levantados basado en los landmarks"""
        finger_tips = [8, 12, 16, 20]  # puntas de dedos (excepto pulgar)
        finger_dips = [6, 10, 14, 18]  # bases de dedos
        
        thumb_tip = 4
        thumb_ip = 2
        
        fingers = []
        
        # Detección del pulgar
        if landmarks[thumb_tip].x < landmarks[thumb_ip].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Detección de otros dedos
        for tip, dip in zip(finger_tips, finger_dips):
            if landmarks[tip].y < landmarks[dip].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers
    
    def recognize_gesture(self, fingers):
        """Reconocer gestos de auxilio específicos"""
        total_fingers = sum(fingers)
        
        # Gestos principales
        if total_fingers == 5:
            return 'A'  # Mano abierta
        
        elif total_fingers == 3:
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                return 'B'  # Tres dedos emergencia
            else:
                return None
        
        elif total_fingers == 0:
            return 'C'  # Puño cerrado
        
        elif total_fingers == 1:
            if fingers[0] == 1:
                return 'D'  # Pulgar auxilio médico
            else:
                return None
        
        # Gestos flexibles para mejor detección
        elif total_fingers == 4:
            return 'A'  # Casi mano abierta
        elif total_fingers == 2 and fingers[1] == 1 and fingers[2] == 1:
            return 'B'  # Dos dedos centrales
        
        else:
            return None
    
    def activar_efecto_color(self):
        """Activar el efecto de color azul por 0.5 segundos"""
        self.efecto_color_activo = True
        self.tiempo_inicio_color = time.time()
    
    def efecto_color_esta_activo(self):
        """Verificar si el efecto de color sigue activo"""
        if not self.efecto_color_activo:
            return False
            
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_color
        
        if tiempo_transcurrido < self.duracion_color:
            return True
        else:
            self.efecto_color_activo = False
            return False
    
    def process_frame(self, frame, gesto_confirmado=False):
        """Procesar un frame y reconocer gestos"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture_detected = None
        annotated_frame = frame.copy()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                
                fingers = self.count_fingers(landmarks)
                gesture = self.recognize_gesture(fingers)
                
                if gesture:
                    gesture_detected = gesture
                    efecto_activo = self.efecto_color_esta_activo()
                    
                    # Definir colores según el estado
                    if efecto_activo:
                        color_landmarks = (255, 200, 0)
                        color_conexiones = (255, 150, 0)
                        color_bbox = (255, 100, 0)
                        color_texto = (255, 100, 0)
                    elif gesto_confirmado:
                        color_landmarks = (0, 255, 255)
                        color_conexiones = (0, 200, 200)
                        color_bbox = (0, 255, 255)
                        color_texto = (0, 255, 255)
                    else:
                        color_landmarks = (0, 255, 0)
                        color_conexiones = (0, 200, 0)
                        color_bbox = (0, 255, 0)
                        color_texto = (0, 255, 0)
                    
                    # Dibujar landmarks y conexiones
                    self.mp_drawing.draw_landmarks(
                        annotated_frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=color_landmarks, thickness=3, circle_radius=4),
                        self.mp_drawing.DrawingSpec(color=color_conexiones, thickness=3)
                    )
                    
                    # Dibujar información del gesto
                    h, w, _ = frame.shape
                    bbox = self.calculate_bounding_box(landmarks, w, h)
                    
                    cv2.rectangle(annotated_frame, 
                                (bbox[0], bbox[1]), 
                                (bbox[2], bbox[3]), 
                                color_bbox, 3)
                    
                    nombre_gesto = self.gestures.get(gesture, "Desconocido")
                    texto_gesto = f"Gesto: {gesture} - {nombre_gesto}"
                    
                    if efecto_activo:
                        texto_gesto += "  DETECTADO"
                    elif gesto_confirmado:
                        texto_gesto += " ✔"
                    
                    cv2.putText(annotated_frame, 
                              texto_gesto, 
                              (bbox[0], bbox[1] - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_texto, 2)
                    
                    if efecto_activo:
                        cv2.putText(annotated_frame,
                                  "Agregado a secuencia",
                                  (bbox[0], bbox[3] + 25),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 2)
        
        # Información general en el frame
        cv2.putText(annotated_frame, 
                   "Sistema de Deteccion de Auxilio", 
                   (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.efecto_color_esta_activo():
            cv2.putText(annotated_frame,
                      "✓ Gesto registrado",
                      (10, 60),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
        
        cv2.putText(annotated_frame, 
                   "A: Mano abierta | B: 3 dedos | C: Puño | D: Pulgar medico", 
                   (10, annotated_frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return annotated_frame, gesture_detected
    
    def calculate_bounding_box(self, landmarks, width, height):
        """Calcular bounding box alrededor de la mano"""
        x_coords = [lm.x * width for lm in landmarks]
        y_coords = [lm.y * height for lm in landmarks]
        
        x_min, x_max = int(min(x_coords)), int(max(x_coords))
        y_min, y_max = int(min(y_coords)), int(max(y_coords))
        
        # Agregar margen
        margin = 20
        x_min = max(0, x_min - margin)
        y_min = max(0, y_min - margin)
        x_max = min(width, x_max + margin)
        y_max = min(height, y_max + margin)
        
        return (x_min, y_min, x_max, y_max)