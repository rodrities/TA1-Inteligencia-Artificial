import random
import numpy as np
import math 
from random import choice
import statistics 

   
#Funcion para calcular el numero de errores en el sudoku   
def CalcularNumeroDeErrores(sudoku):
    numeroDeErrores = 0 
    for i in range (0,9):
        numeroDeErrores += CalcularNumeroDeErroresPorFilasYColumnas(i ,i ,sudoku)
    return(numeroDeErrores)

#Funcion para calcular el numero de errores en una fila y columa "i"
def CalcularNumeroDeErroresPorFilasYColumnas(fila, columna, sudoku):
    numeroDeErrores = (9 - len(np.unique(sudoku[:,columna]))) + (9 - len(np.unique(sudoku[fila,:])))
    return(numeroDeErrores)

#Funcion para hallar un sudoku de 1 y 0; 1 si el cuadro es fijo y 0 si variable
def ResolverValorSudoku(sudoku_binario):
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_binario[i,j] != 0:
                sudoku_binario[i,j] = 1
    return(sudoku_binario)

#Funcion para crear listas de las posiciones de los 9 bloques en el sudoku
def CrearListaDeBloques ():
    listaFinalDeBloques = []
    for r in range (0,9):
        listaTemp = []
        bloque1 = [i + 3*((r)%3) for i in range(0,3)]
        bloque2 = [i + 3*math.trunc((r)/3) for i in range(0,3)]
        for x in bloque1:
            for y in bloque2:
                listaTemp.append([x,y])
        listaFinalDeBloques.append(listaTemp)
        #print(listaFinalDeBloques)
    return(listaFinalDeBloques)

#Funcion para llenar el sudoku con numeros aletorios pero cumpliendo 
# en que cada bloque debe tener 9 numeros unicos
def LLenarBloquesAletoriamente(sudoku, listaDeBloques):
    for bloque in listaDeBloques:
        for caja in bloque:
            if sudoku[caja[0],caja[1]] == 0:
                currentBlock = sudoku[bloque[0][0]:(bloque[-1][0]+1),bloque[0][1]:(bloque[-1][1]+1)]
                sudoku[caja[0],caja[1]] = choice([i for i in range(1,10) if i not in currentBlock])
    return sudoku

#Funcion para sumar el numero de cuadrados con solucion 
def SumaEnUnBloque (sudoku, unBloque):
    sumaFinal = 0
    for caja in unBloque:
        sumaFinal += sudoku[caja[0], caja[1]]
    return(sumaFinal)

#Funcion para selecionar 2 cajas aletorias en un bloque (las cajas no pueden ser la misma o cajas fijas)
def DosCuadradosAletoriosEnUnBloque(sudokuBinario, bloque):
    while (1):
        primeraCaja = random.choice(bloque)
        segundaCaja = choice([caja for caja in bloque if caja is not primeraCaja])

        if sudokuBinario[primeraCaja[0], primeraCaja[1]] != 1 and sudokuBinario[segundaCaja[0], segundaCaja[1]] != 1:
            return([primeraCaja, segundaCaja])

#Funcion para intercambiar 2 cajas en un bloque
def IntercambiarBloques(sudoku, cajasParaIntercambiar):
    sudokuPropuesto = np.copy(sudoku)
    Auxiliar = sudokuPropuesto[cajasParaIntercambiar[0][0], cajasParaIntercambiar[0][1]]
    sudokuPropuesto[cajasParaIntercambiar[0][0], cajasParaIntercambiar[0][1]] = sudokuPropuesto[cajasParaIntercambiar[1][0], cajasParaIntercambiar[1][1]]
    sudokuPropuesto[cajasParaIntercambiar[1][0], cajasParaIntercambiar[1][1]] = Auxiliar
    return (sudokuPropuesto)

#Funcion para hallar un nuevo estado del sudoku con una variacion de dos cajas aletorias
def EstadoPropuesto (sudoku, sudokuBinario, listaDeBloques):
    bloqueAletorio = random.choice(listaDeBloques)

    if SumaEnUnBloque(sudokuBinario, bloqueAletorio) > 6:  
        return(sudoku, 1, 1)
    cajasParaIntercambiar = DosCuadradosAletoriosEnUnBloque(sudokuBinario, bloqueAletorio)
    sudokuPropuesto = IntercambiarBloques(sudoku,  cajasParaIntercambiar)
    return([sudokuPropuesto, cajasParaIntercambiar])

#Funcion para escoger entre el sudoku actual o uno nuevo con una variacion dependiendo de la formula 
#   rho = e^(diferencia de los costos/sigma)
def EscogerNuevoEstado (sudokuActual, sudokuBinario, listaDeBloques, sigma):
    propuesta = EstadoPropuesto(sudokuActual, sudokuBinario, listaDeBloques)
    nuevoSudoku = propuesta[0]
    cajasParaRevisar = propuesta[1]
    costoActual = CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[0][0], cajasParaRevisar[0][1], sudokuActual) + CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[1][0], cajasParaRevisar[1][1], sudokuActual)
    nuevoCosto = CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[0][0], cajasParaRevisar[0][1], nuevoSudoku) + CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[1][0], cajasParaRevisar[1][1], nuevoSudoku)
    diferenciaDeCostos = nuevoCosto - costoActual
    rho = math.exp(-diferenciaDeCostos/sigma)
    if(np.random.uniform(1,0,1) < rho):
        return([nuevoSudoku, diferenciaDeCostos])
    return([sudokuActual, 0])

#Funcion para escoger el numero de iteraciones que se hara dependiendo de los numeros fijos del sudoku inicial
def EscogerNumeroDeIteraciones(sudoku_binario):
    numeroDeIteraciones = 0
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_binario[i,j] != 0:
                numeroDeIteraciones += 1
    return numeroDeIteraciones

#Funcion para calcular el sigma inicial para poder efectuar la ecuacion inicial, 
# este se halla con la desviacion estandar entre el numero de errores 
# en 9 estados nuevos intercambiando 2 numeros aletorios
def CalcularElSigmaInicial (sudoku, sudokuBinario, listaDeBloques):
    listaDeDiferencias = []
    sudokuTmp = sudoku
    for i in range(1,10):
        sudokuTmp = EstadoPropuesto(sudokuTmp, sudokuBinario, listaDeBloques)[0]
        #print("gsd")
        #print(ImprimirSudoku(sudokuTmp))
        listaDeDiferencias.append(CalcularNumeroDeErrores(sudokuTmp))
        #print(listaDeDiferencias)
    return (statistics.pstdev(listaDeDiferencias))

#Funcion para dibujar el sudoku en consola
def ImprimirSudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        linea = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(sudoku[i])):
            if j == 3 or j == 6:
                linea += "| "
            linea += str(sudoku[i,j])+" "
        print(linea)

#Funcion principal para resolver el sudoku con Simulated Anneling
def ResolverSudoku (sudoku):
    #abrimos un archivo externo para guardar un historial de las iteraciones
    f = open("Historial.txt", "a")
    solucionHallada = 0
    while (solucionHallada == 0):
        #se escoge como factor decreciente para la ecuacion como 0.99 porque es mas efectivo
        factorDecreciente = 0.99
        cuentaDeAtascos = 0
        print("Sudoku Inicial")
        ImprimirSudoku(sudoku)
        #se hace un sudoku binario de 1 y 0, donde 1 son los numeros fijos iniciales y 0 los espacios variables a llenar
        sudokuBinario = np.copy(sudoku)
        ResolverValorSudoku(sudokuBinario)
        print("Sudoku Binario")
        ImprimirSudoku(sudokuBinario)
        #se halla una lista de las posiciones de los espacios por para bloque (9)
        listaDeBloques = CrearListaDeBloques()
        #se llena los espacios vacios aletoriamente cumpliendo en que cada bloque no se repita ningun numero
        sudokuTmp = LLenarBloquesAletoriamente(sudoku, listaDeBloques)
        print("Sudoku Llenado Aletoriamente")
        ImprimirSudoku(sudokuTmp)
        #se calcula el sigma inicial para la ecuacion 
        sigma = CalcularElSigmaInicial(sudoku, sudokuBinario, listaDeBloques)
        print(f"sigma inicial: {sigma}")
        #se halla el numero de errores en el sudoku
        puntaje = CalcularNumeroDeErrores(sudokuTmp)
        print(f"numero de errores: {puntaje}")
        #se halla el numero de iteraciones a realizar
        iteraciones = EscogerNumeroDeIteraciones(sudokuBinario)
        print(f"numero de iteraciones: {iteraciones} ")
        if puntaje <= 0:
            solucionHallada = 1

        while solucionHallada == 0:
            puntajeAnterior = puntaje
            f.write(str("Puntaje en cada iteracion:") + '\n')
            for i in range (0, iteraciones):
                nuevoEstado = EscogerNuevoEstado(sudokuTmp, sudokuBinario, listaDeBloques, sigma)
                sudokuTmp = nuevoEstado[0]
                diferenciaDePuntaje = nuevoEstado[1]
                puntaje += diferenciaDePuntaje
                #print(puntaje)
                f.write(str(puntaje) + '\n')
                if puntaje <= 0:
                    solucionHallada = 1
                    print("Sudoku Final")
                    ImprimirSudoku(sudokuTmp)
                    break
            #la variable sigma varia multiplicandolo por el factorDecreciente (0.99)
            sigma *= factorDecreciente
            if puntaje <= 0:
                solucionHallada = 1
                break
            if puntaje >= puntajeAnterior:
                cuentaDeAtascos += 1
            else:
                cuentaDeAtascos = 0
            if (cuentaDeAtascos > 80):
                sigma += 2
            if(CalcularNumeroDeErrores(sudokuTmp)==0):
                #ImprimirSudoku(sudokuTmp)
                #print(sudokuTmp)
                break
    f.close()
    return(sudokuTmp)

#solution = ResolverSudoku(sudoku)
#print(CalcularNumeroDeErrores(solution))
#ImprimirSudoku(solution)