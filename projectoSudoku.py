# Sofía Alejandra Contreras Mendoza y Valeria Islas Jorge
opcion = 0
while opcion!= 3:

        print("""
|============================|
|       Bienvenido a...      |
|        SUDOKU PYTHON       |
|============================|
| Dificultades...            |
|                            |
|  1. Facíl                  |
|                            |
|  2. Medio                  |
|                            |
|  3. Dificil                |
|                            |
|============================|
|  4.Ayuda                   |
|============================|

        """)
        opcion = input("Elige una dificultad: ")
        match opcion:
            case '1':
                sudokuFacil = [
                [0, 4, 3, 0, 0, 6, 1, 0, 8, '1'],
                [1, 7, 0, 0, 0, 0, 9, 0, 3, '2'],
                [9, 8, 0, 3, 0, 4, 6, 7, 0, '3'],
                [2, 6, 8, 9, 0, 3, 7, 5, 0, '4'],
                [0, 0, 5, 0, 2, 7, 8, 0, 4, '5'],
                [7, 1, 4, 8, 6, 5, 3, 9, 2, '6'],
                [6, 3, 9, 2, 0, 1, 4, 8, 7, '7'],
                [4, 2, 1, 6, 7, 8, 5, 0, 6, '8'],
                [0, 5, 0, 4, 0, 9, 0, 1, 9, '9'],
                ]
                print ("A   B   C     D   E   F     G   H   I ")
                print ("- - - - - - - - - - - - - - - - - - - ")

                for fila in range (9):
                    if fila % 3 == 0 and fila!=0:
                        print ("- - - - - - - - - - - - - - - - - - - ")
                    for columna in range (10):
                        if columna % 3 == 0 and columna != 0:
                            print("| ", end="")

                        if sudokuFacil[fila][columna] != 0:
                            valor = sudokuFacil[fila][columna]
                        else:
                            valor = "."

                        print (valor, " ", end= " ")
                    print ()
                error = 0
                print (f"""
                |============================|
                |        SUDOKU PYTHON       |
                |============================|
                | Estadisticas:              |
                |                            |
                |  Timer: __:__              |
                |                            |
                |  Dificultad: Facil         |
                |                            |
                |  Errores: {error}/1              |
                |                            |
                |============================|
                | a. Nuevo juego             |
                | b. Ayuda                   |
                | c. Resolver                |
                | d. Resetear                |
                |============================|
                """)

                print("En base a las cordenadas mostradas en el tablero elige donde empezar a resolver el tablero")

                coordenadasV = input ("Que letra de las coordenadas quieres ocupar:")
                match coordenadasV:
                    case 'A':
                        coordenadasH = int(input("Ahora ingresa el numero de las coordenadas quieres usar:"))
                        nuevoDato = int(input("Ingresa el nuevo valor: "))
                        sudokuFacil[0][coordenadasH].append(nuevoDato)
                        print ("A   B   C     D   E   F     G   H   I ")
                        print ("- - - - - - - - - - - - - - - - - - - ")
                        
                        for fila in range (9):
                            if fila % 3 == 0 and fila!=0:
                                print ("- - - - - - - - - - - - - - - - - - - ")
                            for columna in range (10):
                                if columna % 3 == 0 and columna != 0:
                                    print("| ", end="")
                        
                                if sudokuFacil[fila][columna] != 0:
                                    valor = sudokuFacil[fila][columna]
                                else:
                                    valor = "."
                        
                                print (valor, " ", end= " ")
                                print ()




                            




                

            
            
