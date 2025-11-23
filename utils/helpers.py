import os

def crear_directorios():
    """Crear estructura de directorios necesaria"""
    directorios = [
        "vision",
        "interfaz", 
        "kmp",
        "data",
        "utils"
    ]
    
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        
def verificar_dependencias():
    """Verificar que todas las dependencias estén instaladas"""
    try:
        import cv2
        import tkinter
        import PIL
        return True
    except ImportError as e:
        print(f"Error: Falta dependencia - {e}")
        return False