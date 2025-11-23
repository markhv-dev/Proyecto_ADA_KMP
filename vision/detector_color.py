import cv2
import numpy as np

class DetectorColor:
    def __init__(self):
        # Rangos para color rojo en HSV
        self.rojo_bajo1 = np.array([0, 120, 70])
        self.rojo_alto1 = np.array([10, 255, 255])
        self.rojo_bajo2 = np.array([170, 120, 70])
        self.rojo_alto2 = np.array([180, 255, 255])
        
    def detectar_rojo(self, frame):
        # Convertir a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Crear máscaras para rojo
        mascara1 = cv2.inRange(hsv, self.rojo_bajo1, self.rojo_alto1)
        mascara2 = cv2.inRange(hsv, self.rojo_bajo2, self.rojo_alto2)
        mascara_rojo = cv2.bitwise_or(mascara1, mascara2)
        
        # Operaciones morfológicas para reducir ruido
        kernel = np.ones((5, 5), np.uint8)
        mascara_rojo = cv2.morphologyEx(mascara_rojo, cv2.MORPH_OPEN, kernel)
        mascara_rojo = cv2.morphologyEx(mascara_rojo, cv2.MORPH_CLOSE, kernel)
        
        return mascara_rojo