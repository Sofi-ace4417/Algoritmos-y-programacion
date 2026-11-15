import random # Invocamos a la biblioteca de random
import tkinter as tk # Importamos la librería gráfica
from tkinter import ttk, messagebox # Para el combobox y mensajes
from PIL import Image, ImageTk # Importar librería para imágenes
from pathlib import Path # Para obtener el origen de la imagen

ventana = tk.Tk() # Creamos la ventana
ventana.title("Sudoku Python") # Título de la ventana
ventana.geometry("700x620") # Tamaño de la ventana
ventana.resizable(False, False) # No permite el cambio de tamaño de la ventana
ventana.configure(bg="#FFFFFF") # Cambia el color del fondo de la ventana


tiempoSeg = 0

def timer(etiqueta):
    global tiempoSeg

    minutos = tiempoSeg // 60
    segundos = tiempoSeg % 60

    formatoTiempo = f"Temporizador: {minutos:02d}:{segundos:02d}"
    etiqueta.configure(text = formatoTiempo) 

    tiempoSeg+=1
    ventana.after(1000,lambda: timer(etiqueta))

def imagenVent(contenedor):
    try:
        rutaBase = Path(__file__).parent 
        rutaImagen = rutaBase / "imagen.png" 
        print("Ruta imagen:", rutaImagen)
        print("Existe:", rutaImagen.exists()) # Comprueba si existe la imagen

        if rutaImagen.exists():
            imagen = Image.open(rutaImagen) # Abre la imagen
            imagen = imagen.resize((280, 110)) # Ajusta tamaño
            imagenTk = ImageTk.PhotoImage(imagen) # Convierte para Tkinter
        
            etiquetaLogo = tk.Label(ventana, image=imagenTk, bg="#FFFFFF") # Muestra el logo
            etiquetaLogo.image = imagenTk # Mantener referencia vital a la imagen
            etiquetaLogo.pack(pady=10)
        else:
            raise FileNotFoundError("No se encontró el archivo 'imagen.png' en la carpeta.")

    except Exception as error:
        print("Error al cargar el logo:")
        print(error)
        etiquetaErrorLogo = tk.Label(ventana, text="No se pudo cargar el logo.", bg="#FFFFFF", fg="red")
        etiquetaErrorLogo.pack(pady=10)

etiquetaPresentacion = tk.Label(ventana, text = "Bienvenido a Sudoku Python \n"
                                                "Elige la dificultad...\n", fg="#0097b2",font=("Helvetica", 12)) # Texto que dice los datos a llenar
etiquetaPresentacion.pack(anchor = "w", 
                 padx = 20, pady = (25,5))

frameBotones = tk.Frame(ventana)
frameBotones.pack(pady=(85, 10)) # 85 = espacio superior (empuja los botones hacia abajo). 10 = espacio inferior.

boton = tk.Button(frameBotones, text="Facil",
                    bg="#0097b2", fg="white",font=("Arial", 12, "bold"),width=15)
boton.pack(side="left", padx=10)

boton = tk.Button(frameBotones, text = "Medio",
                    bg="#0097b2", fg="white",font=("Arial", 12, "bold"),width=15)
boton.pack(side="left", padx=10)

boton = tk.Button(frameBotones, text = "Dificil", 
                    bg="#0097b2", fg="white",font=("Arial", 12, "bold"),width=15)
boton.pack(side="left", padx=10)

imagenVent(ventana)
etiquetaTiempo = tk.Label(ventana, text = "Temporizador 00:00", font =("Arial", 14), bg="#FFFFFF", fg="#000000", padx = 15, pady=5 )
etiquetaTiempo.pack(pady=5)
timer(etiquetaTiempo)

ventana.mainloop()