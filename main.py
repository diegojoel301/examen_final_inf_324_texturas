import tkinter as tk
from PIL import ImageTk, Image

import cv2
import numpy as np

def obtener_histograma(imagen):
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    histograma = cv2.calcHist([imagen_gris], [0], None, [256], [0, 256])
    histograma_normalizado = cv2.normalize(histograma, histograma).flatten()
    return histograma_normalizado


def detectar_textura(imagen, histogramas_entrenamiento, etiquetas_entrenamiento):
    histograma_imagen = obtener_histograma(imagen)
    
    distancias = []
    for histograma_entrenamiento in histogramas_entrenamiento:
        distancia = np.linalg.norm(histograma_imagen - histograma_entrenamiento)
        distancias.append(distancia)
    
    indice_min = np.argmin(distancias)
    textura_detectada = etiquetas_entrenamiento[indice_min]
    
    return textura_detectada


# Preparar los datos de entrenamiento
ruta_imagenes = ['textura_madera.jpg', 'textura_marmol.jpg', 'textura_piedra.jpg', 'textura_nube.jpg', 'textura_pasto.jpg', 'textura_agua.jpg']
etiquetas_entrenamiento = ['madera', 'marmol', 'piedra', 'nube', 'pasto', 'agua']
histogramas_entrenamiento = []

for ruta_imagen in ruta_imagenes:
    imagen = cv2.imread(ruta_imagen)
    histograma = obtener_histograma(imagen)
    histogramas_entrenamiento.append(histograma)




# FunciÃ³n para manejar el evento de clic del ratÃ³n
def clic_raton(event):
    x = event.x
    y = event.y

    # Coordenadas de la regiÃ³n de interÃ©s (x, y)
    #x = 50
    #y = 100
    ancho = 10
    alto = 10

    # Recortar la regiÃ³n de interÃ©s de la imagen de prueba
    region_interes = imagen_prueba[y:y+alto, x:x+ancho]

    # Detectar la textura en la regiÃ³n de interÃ©s
    textura_detectada = detectar_textura(region_interes, histogramas_entrenamiento, etiquetas_entrenamiento)

    # Mostrar el resultado
    print(f'La textura detectada en la regiÃ³n de interÃ©s es: {textura_detectada}')

    etiqueta_coordenadas.config(text=f'Textura: {textura_detectada}')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz grÃ¡fica")
ventana.geometry("1200x720")

# Cargar la imagen
#ruta_imagen = "/home/diegojoel301/tmp/texturas/imagen_prueba.jpg"
ruta_imagen = input("[+] Introduce el directorio de la imagen: ")
#ruta_imagen = 'paisaje.jpg'  # Ruta de la imagen de prueba
imagen = Image.open(ruta_imagen)

# Cargar la imagen de prueba

imagen_prueba = cv2.imread(ruta_imagen)


# Mostrar la imagen en un widget Canvas
canvas = tk.Canvas(ventana, width=imagen.width, height=imagen.height)
canvas.pack()
imagen_tk = ImageTk.PhotoImage(imagen)
canvas.create_image(0, 0, anchor="nw", image=imagen_tk)

# Crear una etiqueta para mostrar las coordenadas
etiqueta_coordenadas = tk.Label(ventana, text="Textura:")
etiqueta_coordenadas.pack()

# Asociar la funciÃ³n clic_raton al evento Button-1 (clic izquierdo del ratÃ³n) en el Canvas
canvas.bind("<Button-1>", clic_raton)

# Iniciar el bucle principal de la interfaz grÃ¡fica
ventana.mainloop()
