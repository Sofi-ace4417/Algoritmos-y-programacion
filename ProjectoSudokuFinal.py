import random                              # Invocamos a la biblioteca de random
import tkinter as tk                       # librería gráfica
from tkinter import ttk, messagebox             # (por si después necesitas avisos)
from PIL import Image, ImageTk             # para mostrar el logo
from pathlib import Path                   # para encontrar la imagen junto al programa

TAM = 50                       # tamaño de cada casilla del tablero (pixeles)
MARGEN = 10                    # espacio alrededor del tablero
nombreJugador = ""            # aquí se guarda el nombre que escriba el usuario

#  GENERACIÓN DEL SUDOKU

def resuelto():
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

def noResuelto(cuadro, ocultar=0):
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

    estado = {"segundos": 0, "id": None, "Errores": 0}         # tiempo y id del temporizador
    
    # 1. CREAMOS PRIMERO EL PANEL DERECHO (para que la variable 'panel' exista)
    panel = tk.Frame(ventanaJuego, bg="#f4f6fa", padx=30, pady=20)  
    panel.grid(row=0, column=1, sticky="ns", padx=(0, 20), pady=20)  

    mostrarLogo(panel, 200, 80)                              

    tk.Label(panel, text=f"Jugador: {nombreJugador}", font=("Helvetica", 15, "bold"),   
             fg="#3b6fb0", bg="#f4f6fa").pack(pady=5)                                    

    etiquetaTiempo = tk.Label(panel, text="Timer: 00:00", font=("Helvetica", 15),
                              fg="#14213d", bg="#f4f6fa")
    etiquetaTiempo.pack(pady=5)  

    tk.Label(panel, text=f"Dificultad: {dificultad}", font=("Helvetica", 15),
             fg="#14213d", bg="#f4f6fa").pack(pady=5)
    
    etiquetaErrores = tk.Label(panel, text="Errores: 0/3", font=("Helvetica", 15),
             fg="#14213d", bg="#f4f6fa")
    etiquetaErrores.pack(pady=5)

    def contadorErrores(fila, columna, event):
        valor = matrizCeldas[fila][columna].get()

        if valor == "":
            return

        if not valor.isdigit() or valor == "0":
            matrizCeldas[fila][columna].delete(0, tk.END)
            return

        if len(valor) > 1:
            valor = valor[-1]
            matrizCeldas[fila][columna].delete(0, tk.END)
            matrizCeldas[fila][columna].insert(0, valor)

        numeroIngresado = int(valor)
        numeroCorrecto = tableroResuelto[fila][columna]

        if numeroIngresado == numeroCorrecto:
            matrizCeldas[fila][columna].config(bg="white", fg="#14213d")
        else: 
            estado["Errores"] += 1
            etiquetaErrores.config(text=f"Errores:{estado['Errores']}/3")
            matrizCeldas[fila][columna].config(fg="red", bg="#fadbd8")

        if estado["Errores"] >= 3:
            messagebox.showerror("Lo siento, haz llegado al máximo numero de errores","Fin del juego")
            cerrar()

    # 2. CREAMOS EL TABLERO A LA IZQUIERDA

    lado = MARGEN * 2 + TAM * 9  
    canvas = tk.Canvas(ventanaJuego, width=lado, height=lado, 
                       bg="#e9ecf1", highlightthickness=0)  
    canvas.grid(row=0, column=0, padx=20, pady=20) 
    dibujarTableroVacio(canvas)   

    if dificultad == "Fácil":
        ocultos = 30
    elif dificultad == "Medio":
        ocultos = 50
    else:
        ocultos = 60

    tableroResuelto = resuelto()
    tableroSinResolver = noResuelto(tableroResuelto, ocultar=ocultos)

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
                celda.bind("<KeyRelease>", lambda event, f = fila, c = columna: contadorErrores(f, c, event))

            canvas.create_window(x, y, anchor= "nw", window= celda, width = TAM - 7, height= TAM - 7)
            matrizCeldas[fila][columna] = celda

    def reiniciarJuego():
        estado["segundos"] = 0
        estado["Errores"] = 0
        etiquetaErrores.config(text="Errores: 0/3")

        for fila in range(9):
            for columna in range(9):
                if matrizCeldas[fila][columna].cget("state") != "disabled":
                    matrizCeldas[fila][columna].delete(0, tk.END)
                    matrizCeldas[fila][columna].config(bg="white", fg="#14213d")

    def resolverJuego():
        for fila in range(9):
            for columna in range(9):
                celda =  matrizCeldas[fila][columna]
                if celda.cget("state") != "disabled":
                    celda.config(state="normal")
                    celda.delete(0, tk.END)
                    celda.insert(0, str(tableroResuelto[fila][columna]))
                    celda.config(fg="#00b14a", bg = "white")

    def comprobarJuego():
        for fila in range(9):
            for columna in range(9):
                valor = matrizCeldas[fila][columna].get()
                if valor == "":
                    messagebox.showwarning("El tablero esta incompleto", "Algunas casillas faltan por completar")    
                    return 

                if not valor.isdigit() or int(valor) != tableroResuelto[fila][columna]:
                    messagebox.showwarning("Revisa bien", "Hay números incorrectos en el tablero.")
                    return

        if estado["id"] is not None:
            ventanaJuego.after_cancel(estado["id"])

        minutos = (estado["segundos"]- 1) // 60
        segundos = (estado["segundos"]- 1) % 60

        felicitaciones = f"Muy bien trabajo {nombreJugador}\n Haz completado el Sudoku en un tiempo de {minutos:02d}:{segundos:02d}"
        messagebox.showinfo("Felicidades!!!", felicitaciones)
        cerrar()

    # Temporizador 
    def actualizarTimer():  
        minutos = estado["segundos"] // 60  
        segundos = estado["segundos"] % 60  
        etiquetaTiempo.config(text=f"Timer: {minutos:02d}:{segundos:02d}") 
        estado["segundos"] += 1
        estado["id"] = ventanaJuego.after(1000, actualizarTimer)  

    # Cerrar 
    def cerrar():
        if estado["id"] is not None:  
            ventanaJuego.after_cancel(estado["id"]) 
        ventanaJuego.destroy()

    # 3. AÑADIMOS LOS BOTONES AL PANEL DERECHO YA CREADO

    crearBoton(panel, "Reiniciar", reiniciarJuego).pack(pady=5)
    crearBoton(panel, "Resolver", resolverJuego).pack(pady=5)
    crearBoton(panel, "Nuevo juego", cerrar).pack(pady=5)
    crearBoton(panel, "Validar", comprobarJuego).pack(pady=5)

    ventanaJuego.protocol("WM_DELETE_WINDOW", cerrar)        
    actualizarTimer()


# MENÚ PRINCIPAL

ventana = tk.Tk()
ventana.title("Menú de Sudoku Python")
ventana.geometry("520x680")
ventana.resizable(False, False)
ventana.configure(bg="#e9ecf1")

# Tarjeta central (da la sensación de "panel flotante")
tarjeta = tk.Frame(ventana, bg="#f4f6fa", padx=40, pady=30)
tarjeta.pack(expand=True)     # expand=True la centra en la ventana                               

mostrarLogo(tarjeta, 280, 110)  # muestra el logo dentro de la tarjeta (280 x 110 px)

# PANTALLA 1: pedir el nombre
pantallaNombre = tk.Frame(tarjeta, bg="#f4f6fa")             # caja que agrupa todo lo de la pantalla del nombre
pantallaNombre.pack()                                        # esta pantalla es la que se ve al abrir el programa

tk.Label(pantallaNombre, text="¡Bienvenido a Sudoku Python!", font=("Helvetica", 16, "bold"),   # título de bienvenida
         fg="#3b6fb0", bg="#f4f6fa").pack(pady=(5, 10))
tk.Label(pantallaNombre, text="Escribe tu nombre para comenzar:", font=("Helvetica", 12),       # le pide el nombre
         fg="#4a5568", bg="#f4f6fa").pack(pady=(0, 10))

entradaNombre = tk.Entry(pantallaNombre, font=("Helvetica", 14), justify="center", width=22,    # cuadro de texto donde se escribe
                         relief="flat", highlightthickness=2,                                   # sin relieve; con borde de 2 px
                         highlightbackground="#9aa5b8", highlightcolor="#3b6fb0")               # borde gris; azul cuando está activo
entradaNombre.pack(pady=5)                          # ipady = hace el cuadro más alto por dentro
entradaNombre.focus_set()                                    # el cursor ya aparece dentro del cuadro, sin dar clic

etiquetaError = tk.Label(pantallaNombre, text="", font=("Helvetica", 10),   # mensaje de error (empieza vacío)
                         fg="#c0392b", bg="#f4f6fa")                         # texto rojo
etiquetaError.pack(pady=(0, 10))

# ---------- PANTALLA 2: bienvenida, instrucciones y dificultad ----------
pantallaMenu = tk.Frame(tarjeta, bg="#f4f6fa")               # caja de la segunda pantalla (todavía NO se muestra)

etiquetaBienvenida = tk.Label(pantallaMenu, text="", font=("Helvetica", 16, "bold"),   # el texto se pone cuando el usuario escribe su nombre
                              fg="#3b6fb0", bg="#f4f6fa")
etiquetaBienvenida.pack(pady=(5, 10))

textoInstrucciones = ("Cómo jugar:\n"                                                  # \n = salto de línea
                      "1. Completa la cuadrícula con números del 1 al 9.\n"
                      "2. No repitas un número en la misma fila.\n"
                      "3. No repitas un número en la misma columna.\n"
                      "4. No repitas un número dentro de cada cuadro de 3x3\n"
                      "    (los marcados con líneas gruesas).\n"
                      "5. Los números ya escritos no se pueden cambiar.\n"
                      "    Haz clic en una casilla blanca y escribe tu número.\n"
                      "6. Entre más difícil el nivel, más casillas vacías.")              # el texto se une porque está entre paréntesis

tk.Label(pantallaMenu, text=textoInstrucciones, font=("Helvetica", 11),     # etiqueta con las instrucciones
         fg="#4a5568", bg="#f4f6fa", justify="left").pack(pady=(0, 15))     # justify="left" alinea el texto a la izquierda

tk.Label(pantallaMenu, text="Elige la dificultad para comenzar:", font=("Helvetica", 12, "bold"),
         fg="#14213d", bg="#f4f6fa").pack(pady=(0, 10))

crearBoton(pantallaMenu, "Fácil", lambda: abrirJuego("Fácil")).pack(pady=6)       # botón Fácil; lambda hace que abrirJuego se ejecute hasta que se haga clic
crearBoton(pantallaMenu, "Medio", lambda: abrirJuego("Medio")).pack(pady=6)       # botón Medio
crearBoton(pantallaMenu, "Difícil", lambda: abrirJuego("Difícil")).pack(pady=6)   # botón Difícil

# ---------- Función que pasa de la pantalla 1 a la 2 ----------
def continuar():                                 
    global nombreJugador                                     # global porque vamos a CAMBIAR la variable de arriba
    nombre = entradaNombre.get().strip()                     # lee lo escrito; strip() quita espacios al inicio y al final
    if nombre == "":                                         # si no escribió nada...
        etiquetaError.config(text="Por favor escribe tu nombre.")   # ...muestra el error
        return                                               # ...y se detiene aquí
    if len(nombre) > 15:                                     # si el nombre es demasiado largo...
        etiquetaError.config(text="El nombre es muy largo (máximo 15 letras).")
        return
    nombreJugador = nombre                                   # guarda el nombre para usarlo en la ventana de juego
    etiquetaBienvenida.config(text=f"¡Bienvenido, {nombreJugador}!")   # personaliza el saludo
    pantallaNombre.pack_forget()                             # oculta la pantalla del nombre
    pantallaMenu.pack()                                      # muestra la pantalla de instrucciones y dificultad

crearBoton(pantallaNombre, "Continuar", continuar).pack(pady=(0, 5))   # botón que llama a continuar()
                 

ventana.mainloop()