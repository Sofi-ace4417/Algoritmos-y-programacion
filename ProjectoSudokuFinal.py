import random                              # Invocamos a la biblioteca de random
import tkinter as tk                       # librería gráfica
from tkinter import ttk, messagebox             # (por si después necesitas avisos)
from PIL import Image, ImageTk             # para mostrar el logo
from pathlib import Path                   # para encontrar la imagen junto al programa

TAM = 50                       # tamaño de cada casilla del tablero (pixeles)
MARGEN = 10                    # espacio alrededor del tablero

#  GENERACIÓN DEL SUDOKU

def resueltoFacil():
    subCuadro = []
    while len(subCuadro) < 9:
        digito = random.randint(1, 9)
        if digito not in subCuadro:
            subCuadro.append(digito)

    cuadro = []

    for fila in range(9):
        subCuadro1 = []
        for columna in range(9):
            indice = (columna + (fila % 3) * 3 + fila // 3) % 9
            subCuadro1.append(subCuadro[indice])

        cuadro.append(subCuadro1)
        
    return cuadro

def facil(cuadro, ocultar=0):
    cuadroCopia = [fila[:] for fila in cuadro]
    ocultos = 0

    while ocultos < ocultar:
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)

        if cuadroCopia[fila][columna] != 0:
            cuadroCopia[fila][columna] = 0
            ocultos += 1

    return cuadroCopia

# FUNCIONES AUXILIARES

def mostrarLogo(contenedor, ancho, alto): # Muestra 'imagen.png' dentro del contenedor. Si no existe, simplemente no la muestra

    rutaImagen = Path(__file__).parent / "imagen.png"        # imagen.png junto a este archivo
    if not rutaImagen.exists():                              # si no está, salimos sin error
        print("Aviso: no se encontró 'imagen.png', se muestra el menú sin logo.")
        return
    try:
        imagen = Image.open(rutaImagen).resize((ancho, alto))     # abre y ajusta el tamaño
        imagenTk = ImageTk.PhotoImage(imagen)                     # la convierte para Tkinter
        etiquetaLogo = tk.Label(contenedor, image=imagenTk, bg=contenedor["bg"]) # crea una etiqueta con la imagen; bg copia el color de fondo del contenedor
        etiquetaLogo.image = imagenTk                             # guardar referencia (si no, desaparece)
        etiquetaLogo.pack(pady=(0, 10)) # la coloca en pantalla: 0 px de espacio arriba, 10 px abajo
    except Exception as error:
        print("Error al cargar el logo:", error)


def crearBoton(contenedor, texto, comando): #Crea un botón plano azul que se oscurece al pasar el mouse

    boton = tk.Button(contenedor, text=texto, command=comando,
                      font=("Helvetica", 13, "bold"), width=22, pady=8,
                      bg="#3b6fb0", fg="white",
                      relief="flat", bd=0, cursor="hand2")  # sin relieve ni borde (plano); el cursor se vuelve una manita
    return boton


def dibujarTableroVacio(canvas): #Dibuja un tablero de 9x9 con líneas gruesas cada 3 casillas

    canvas.delete("all") # borra todo lo que hubiera dibujado antes
    for fila in range(9): # repite 9 veces: fila = 0, 1, 2, ..., 8
        for col in range(9): # dentro de cada fila, repite 9 veces: col = 0, 1, ..., 8
            x = MARGEN + col * TAM  # posición horizontal de la casilla (más columna = más a la derecha)
            y = MARGEN + fila * TAM # posición vertical de la casilla (más fila = más abajo)
            canvas.create_rectangle(x, y, x + TAM, y + TAM,  # dibuja un cuadrado: de la esquina (x, y) a la esquina (x+TAM, y+TAM)
                                    fill="#f7f9fc", outline="#9aa5b8")
    fin = MARGEN + 9 * TAM # coordenada donde termina el tablero (después de 9 casillas)

    for i in range(0, 10, 3):                               # 0, 3, 6, 9  (de 3 en 3: son las líneas que separan los cuadros grandes)
        pos = MARGEN + i * TAM # posición en pixeles de esa línea gruesa
        canvas.create_line(MARGEN, pos, fin, pos, width=3, fill="#14213d")   # horizontal
        canvas.create_line(pos, MARGEN, pos, fin, width=3, fill="#14213d")   # vertical


# VENTANA DE JUEGO

def abrirJuego(dificultad):
    ventanaJuego = tk.Toplevel(ventana)                      # ventana nueva, hija del menú
    ventanaJuego.title(f"Sudoku Python - {dificultad}")
    ventanaJuego.resizable(False, False)
    ventanaJuego.configure(bg="#e9ecf1")

    estado = {"segundos": 0, "id": None}                     # tiempo y id del temporizador de ESTA ventana

    # Tablero a la izquierda 
    lado = MARGEN * 2 + TAM * 9  # tamaño total del tablero: 9 casillas + margen a ambos lados
    canvas = tk.Canvas(ventanaJuego, width=lado, height=lado, # crea el lienzo cuadrado donde se dibuja el tablero
                       bg="#e9ecf1", highlightthickness=0)  # mismo fondo que la ventana; sin borde alrededor
    canvas.grid(row=0, column=0, padx=20, pady=20) # lo coloca en la fila 0, columna 0 (izquierda) con 20 px de espacio
    dibujarTableroVacio(canvas)   # llama a la función que dibuja las casillas y las líneas

    if dificultad == "Fácil":
        ocultos = 30
    elif dificultad == "Medio":
        ocultos = 40
    else:
        ocultos = 50

    tableroResuelto = resueltoFacil()
    tableroSinResolver = facil(tableroResuelto, ocultar=ocultos)

    matrizCeldas = [[None for i in range (9)] for i in range (9)]

    for fila in range (9):
        for columna in range (9):
            valor = tableroSinResolver[fila][columna]

            x = MARGEN + columna * TAM + 4
            y = MARGEN + fila * TAM + 4

            celda = tk.Entry(canvas, width=2, font=("Helvetica", 16, "bold"), justify = "center", relief = "flat", bd= 0)

            if valor != 0:
                celda.insert(0, str(valor))
                celda.config(state="disabled", disabledbackground="#e9ecf1", disabledforeground="#14213d")
            else:
                celda.config(bg="white", fg= "#14213d")

            canvas.create_window(x,y, anchor= "nw", window= celda, width = TAM - 7, height= TAM -7)
            matrizCeldas[fila][columna] = celda

    

    # Panel a la derecha 
    panel = tk.Frame(ventanaJuego, bg="#f4f6fa", padx=30, pady=20)  # Frame = caja contenedora; fondo claro y relleno interno
    panel.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=20)  # fila 0, columna 1 (derecha); sticky="ns" lo estira de arriba a abajo

    mostrarLogo(panel, 200, 80)                              # logo (si existe)

    etiquetaTiempo = tk.Label(panel, text="Timer: 00:00", font=("Helvetica", 15),
                              fg="#14213d", bg="#f4f6fa")
    etiquetaTiempo.pack(pady=5)  # la coloca en el panel con 5 px de espacio arriba y abajo
    tk.Label(panel, text=f"Dificultad: {dificultad}", font=("Helvetica", 15),
             fg="#14213d", bg="#f4f6fa").pack(pady=5)
    tk.Label(panel, text="Errores: 0/3", font=("Helvetica", 15),
             fg="#14213d", bg="#f4f6fa").pack(pady=5)

    # Temporizador (se llama a sí mismo cada segundo) ---
    def actualizarTimer():  # función dentro de otra función: solo existe dentro de abrirJuego
        minutos = estado["segundos"] // 60  # // es división entera: 125 segundos -> 2 minutos
        segundos = estado["segundos"] % 60  # % es el residuo: 125 segundos -> 5 segundos sobrantes
        etiquetaTiempo.config(text=f"Timer: {minutos:02d}:{segundos:02d}") # cambia el texto; :02d fuerza 2 dígitos (5 -> 05)
        estado["segundos"] += 1
        estado["id"] = ventanaJuego.after(1000, actualizarTimer)  # programa que esta misma función se ejecute en 1000 ms; guarda el id para poder cancelarla

    # Cerrar: primero cancela el temporizador para evitar errores ---
    def cerrar():
        if estado["id"] is not None:  # si el temporizador ya estaba programado...
            ventanaJuego.after_cancel(estado["id"]) # ...lo cancela, para que no intente actualizar una ventana que ya no existe
        ventanaJuego.destroy()

    crearBoton(panel, "Volver al menú", cerrar).pack(pady=(25, 0))
    ventanaJuego.protocol("WM_DELETE_WINDOW", cerrar)        # también al cerrar con la X: en lugar de cerrar directo, ejecuta cerrar()

    actualizarTimer()                                        # arranca el reloj


# MENÚ PRINCIPAL

ventana = tk.Tk()
ventana.title("Menú de Sudoku Python")
ventana.geometry("480x520")
ventana.resizable(False, False)
ventana.configure(bg="#e9ecf1")

# Tarjeta central (da la sensación de "panel flotante")
tarjeta = tk.Frame(ventana, bg="#f4f6fa", padx=40, pady=30)
tarjeta.pack(expand=True)     # expand=True la centra en la ventana                               

mostrarLogo(tarjeta, 280, 110)  # muestra el logo dentro de la tarjeta (280 x 110 px)

tk.Label(tarjeta, text="Elige la dificultad para comenzar", font=("Helvetica", 12),
         fg="#4a5568", bg="#f4f6fa").pack(pady=(5, 25))

crearBoton(tarjeta, "Fácil", lambda: abrirJuego("Fácil")).pack(pady=6) # botón Fácil; lambda hace que abrirJuego se ejecute hasta que se haga clic
crearBoton(tarjeta, "Medio", lambda: abrirJuego("Medio")).pack(pady=6) # botón Medio; igual, pero manda "Medio"
crearBoton(tarjeta, "Difícil", lambda: abrirJuego("Difícil")).pack(pady=6)

ventana.mainloop()