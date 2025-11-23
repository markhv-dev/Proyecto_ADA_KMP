🖐️ Detección de Gestos de Auxilio mediante Secuencias y Algoritmo KMP
Proyecto de reconocimiento de patrones de emergencia usando visión simplificada
📌 Descripción General

Este proyecto implementa un sistema de detección de gestos de auxilio usando:

Captura de video a través de OpenCV

Extracción de un estado simbólico por cada fotograma

Construcción de una secuencia de caracteres que representan la posición o forma de la mano

Búsqueda del patrón crítico mediante el algoritmo KMP (Knuth–Morris–Pratt)

El objetivo es crear una solución ligera, rápida y sin uso de inteligencia artificial, capaz de detectar gestos universales de ayuda, como la señal difundida internacionalmente en 2021.

🎯 Objetivo del Proyecto

Construir un sistema capaz de:

Observar la mano del usuario mediante cámara.

Clasificar la forma de la mano en estados discretos (ej. A, B, C).

Generar una secuencia de símbolos en tiempo real.

Detectar si dentro de la secuencia aparece un patrón que corresponda a un gesto de auxilio.

Activar una alerta inmediata si el patrón es encontrado.

🧩 Arquitectura del Sistema

El sistema está compuesto por cuatro módulos:

1️⃣ Módulo de Captura (OpenCV)

Obtiene fotogramas en tiempo real.

Convierte cada frame a escala de grises.

Aplica suavizado para reducir ruido.

Segmenta la región de la mano mediante:

umbralización,

contornos,

detección de convexidad.

No reconoce imágenes a nivel de IA; solo detecta formas básicas.

2️⃣ Módulo de Clasificación de Estado

Cada fotograma extraído se convierte a un símbolo basado en una métrica sencilla, por ejemplo:

Estado de la mano	Descripción	Símbolo
Mano abierta	contorno grande + dedos extendidos	A
Pulgar oculto	detección de un único cambio en convexidad	B
Mano cerrada	contorno pequeño + sin extensiones	C

Estos valores pueden ajustarse según el prototipo o iluminación.

3️⃣ Módulo de Secuencias

A medida que cada fotograma genera un símbolo, se construye una cadena:

AAAABBBCCCCCAAABB...


Esto representa la evolución temporal del gesto.

4️⃣ Módulo de Detección por KMP

El algoritmo KMP se utiliza para encontrar el patrón objetivo dentro de la secuencia.

Ejemplo del gesto internacional de auxilio:

A = mano abierta  
B = pulgar doblado  
C = mano cerrada  
Patrón final = "ABC"


KMP permite:

Búsqueda en tiempo lineal

Procesamiento en streaming

Comparación eficiente incluso con cadenas largas

La detección se ejecuta en cada actualización de la secuencia.

🧪 Flujo Completo

El usuario realiza un gesto.

La cámara captura el movimiento.

Cada frame se clasifica como A, B o C.

El buffer de secuencia almacena los últimos N símbolos.

KMP analiza si el patrón (“ABC”) aparece en el buffer.

Si se detecta → se activa una alerta gráfica, sonora o de log.

🚨 Patrones Definidos

Actualmente, el sistema detecta:

"ABC" → gesto de auxilio (señal internacional)


Pero la arquitectura permite agregar:

patrones para golpes,

señales repetitivas,

movimientos bruscos,

patrones de gritos (si se integra audio),

gestos personalizados.

⚙️ Tecnologías Utilizadas

Python 3.x

OpenCV

Numpy

Algoritmo KMP implementado manualmente

Interfaz simple en consola o GUI opcional

📁 Estructura del Proyecto
/proyecto-kmp-auxilio
│
├── src/
│   ├── capture.py          # Captura de cámara
│   ├── classifier.py       # Clasificación de estados
│   ├── sequence_buffer.py  # Gestión de secuencia de símbolos
│   ├── kmp.py              # Implementación del algoritmo KMP
│   ├── detector.py         # Integración de todos los módulos
│   └── main.py             # Punto de entrada
│
├── assets/
│   └── demo_videos/        # Videos de demostración
│
├── README.md
└── requirements.txt

🧠 Implementación del Algoritmo KMP (resumen técnico)

El algoritmo se compone de:

🔹 1. Función LPS (Longest Prefix Suffix)

Construye una tabla que evita comparaciones redundantes.

🔹 2. Búsqueda del patrón

Recorre el texto (secuencia) comparando con el patrón.

Complejidad:

Preprocesamiento: O(m)

Búsqueda: O(n)
(n = longitud de la secuencia, m = tamaño del patrón)

Esto permite trabajar en tiempo real sin perder rendimiento.

🖥️ Uso

Ejecutar:

python main.py


La consola mostrará:

video con contorno detectado

símbolo actual (A, B, C)

secuencia generada

alertas si se detecta el patrón

📈 Ventajas del Enfoque

No usa IA: funciona en hardware básico

Ultra eficiente (O(n))

Fácil de extender a múltiples gestos

Bajo consumo de CPU

Interpretable y transparente

Ideal para demostraciones educativas y concursos

🧩 Limitaciones

Sensible a iluminación irregular

Requiere que la mano esté relativamente centrada

No reconoce gestos complejos

Solo detecta patrones definidos explícitamente

🛠️ Posibles Mejoras

Integrar audio (transformado a símbolos)

Implementar varios patrones KMP simultáneos

Interfaz gráfica final

Soporte para diferentes manos (izquierda/derecha)

Integrar filtros adaptativos por piel

🏁 Conclusión

Este proyecto demuestra que es posible detectar gestos de auxilio sin necesidad de inteligencia artificial, simplemente combinando:

visión computacional simplificada

abstracción simbólica

y el algoritmo clásico KMP

La solución es ligera, rápida y funcional para demostraciones reales y entornos con recursos limitados.
