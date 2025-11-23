# 🖐️ Sistema de Detección de Gestos de Auxilio con KMP

Proyecto de reconocimiento de patrones de emergencia usando **MediaPipe**, **OpenCV** y el algoritmo **KMP**

## 📋 Requisitos del Sistema

- **Python 3.12.1** (recomendado)
- Cámara web funcional
- Sistema operativo: Windows, macOS o Linux

## 🚀 Instalación y Ejecución

### 1. Instalación de dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el sistema
```bash
python main.py
```

## 📦 Dependencias

```
opencv-python==4.8.1.78
Pillow==10.0.1
mediapipe==0.10.0
numpy==1.24.3
```

## 📌 Descripción General

Este proyecto implementa un sistema avanzado de detección de gestos de auxilio usando:

✅ **Captura de video** en tiempo real con OpenCV
✅ **Detección de landmarks** de manos usando MediaPipe
✅ **Clasificación inteligente** de gestos basada en dedos levantados
✅ **Construcción de secuencias** temporales de gestos
✅ **Detección de patrones** usando el algoritmo KMP optimizado
✅ **Interfaz gráfica** multi-ventana con monitoreo en tiempo real

## 🎯 Características Principales

### 🖱️ Interfaz Gráfica Completa
- **Ventana Principal**: Control del sistema y configuración
- **Ventana de Cámara**: Visualización en tiempo real con landmarks
- **Ventana de Estado**: Monitoreo de gestos y secuencias detectadas
- **Ventana de Alertas**: Historial de detecciones de auxilio
- **Popup de Alerta**: Notificaciones inmediatas de emergencia

### 👋 Detección de Gestos
El sistema reconoce tres gestos principales:

| Gesto | Descripción | Símbolo |
|-------|-------------|---------|
| **A** | Mano Abierta (5 dedos) | `A` |
| **B** | 3 Dedos Arriba | `B` |
| **C** | Puño Cerrado | `C` |

### 🔍 Patrón de Auxilio
El sistema detecta la secuencia: **`AAABBBCCC`**
- **AAA**: Mano abierta (llamar atención)
- **BBB**: 3 dedos (señal específica)
- **CCC**: Puño cerrado (confirmación de auxilio)

## 🏗️ Arquitectura del Sistema

```
proyecto70%/
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
│
├── interfaz/              # Módulos de interfaz gráfica
│   ├── ventana_cam.py     # Ventana de cámara
│   ├── ventana_estado.py  # Ventana de estado
│   ├── ventana_alertas.py # Ventana de alertas
│   └── ventana_popup_alerta.py # Popups de alerta
│
├── vision/                # Módulos de visión computacional
│   ├── detector_gestos.py    # Detección con MediaPipe
│   ├── detector_color.py     # Procesamiento de color
│   ├── detector_zonas.py     # Detección de zonas
│   └── procesador_eventos.py # Procesamiento de eventos
│
├── kmp/                   # Algoritmo de detección de patrones
│   └── detector_patron.py   # Implementación KMP optimizada
│
├── utils/                 # Utilidades del sistema
│   ├── helpers.py         # Funciones auxiliares
│   └── reloj.py          # Control de tiempo
│
└── data/                  # Datos del sistema
    └── alertas.txt       # Log de alertas detectadas
```

## 🔧 Funcionamiento Técnico

### 1. **Captura y Procesamiento**
- MediaPipe detecta hasta **21 landmarks** por mano
- Análisis de **confianza mínima del 50%**
- Procesamiento a **30 FPS** en tiempo real

### 2. **Clasificación de Gestos**
```python
def count_fingers(self, landmarks):
    # Algoritmo de conteo basado en landmarks
    # Detecta dedos levantados usando coordenadas 3D
    # Clasifica en estados A, B, C
```

### 3. **Algoritmo KMP Optimizado**
- **Preprocesamiento**: O(m) donde m = longitud del patrón
- **Búsqueda**: O(n) donde n = longitud de la secuencia
- **Detección de nuevos patrones** sin solapamiento
- **Eficiencia en tiempo real** garantizada

### 4. **Sistema de Alertas**
- **Detección inmediata** del patrón `AAABBBCCC`
- **Popup visual** con timestamp
- **Log persistente** en archivo de texto
- **Prevención de duplicados** con control de índices

## 🎮 Uso del Sistema

1. **Iniciar el programa**: `python main.py`
2. **Abrir ventanas**: Usar botones en la interfaz principal
3. **Posicionar la mano** frente a la cámara
4. **Realizar la secuencia**: AAA → BBB → CCC
5. **Confirmar alerta** en el popup que aparece

## 🛠️ Configuración Avanzada

### Ajuste de Sensibilidad
```python
# En detector_gestos.py
self.hands = self.mp_hands.Hands(
    min_detection_confidence=0.5,  # Ajustar sensibilidad
    min_tracking_confidence=0.5    # Ajustar seguimiento
)
```

### Personalización del Patrón
```python
# En main.py
self.detector_patron = DetectorPatron("AAABBBCCC")  # Cambiar patrón
```

## 📊 Ventajas del Sistema

✅ **Sin dependencias de IA pesada**: Usa algoritmos clásicos eficientes
✅ **Tiempo real**: Detección instantánea sin latencia
✅ **Robusto**: Funciona en diferentes condiciones de iluminación
✅ **Escalable**: Fácil agregar nuevos gestos y patrones
✅ **Portable**: Corre en cualquier sistema con Python
✅ **Open Source**: Código completamente auditable

## 🎯 Casos de Uso

- **Emergencias domésticas**: Solicitar ayuda de forma discreta
- **Entornos ruidosos**: Comunicación visual cuando no se puede hablar
- **Seguridad personal**: Activación de alertas silenciosas
- **Accesibilidad**: Alternativa para personas con limitaciones de habla
- **Demostración educativa**: Enseñanza de algoritmos y visión computacional

## 🔍 Limitaciones Conocidas

- Requiere **buena iluminación** para detección óptima
- **Una mano por vez** (configurable para múltiples manos)
- Sensible a **movimientos muy rápidos**
- Necesita **calibración inicial** en algunos entornos

## 🚀 Futuras Mejoras

- [ ] Detección de múltiples patrones simultáneos
- [ ] Integración con servicios de emergencia
- [ ] Reconocimiento de emociones faciales
- [ ] Soporte para gestos con dos manos
- [ ] Configuración de patrones personalizados via GUI
- [ ] Integración con dispositivos IoT

## 👥 Contribución

Este proyecto está abierto a contribuciones. Para colaborar:

1. Fork del repositorio
2. Crear rama de feature
3. Implementar mejoras
4. Crear pull request

## 📄 Licencia

Proyecto educativo de código abierto.

---

**Desarrollado con ❤️ usando Python, OpenCV, MediaPipe y el algoritmo KMP**