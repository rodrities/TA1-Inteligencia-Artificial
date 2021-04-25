import random
import numpy as np
import math 
from random import choice
import statistics 


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

def ResolverValorSudoku(sudoku_binario):
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_binario[i,j] != 0:
                sudoku_binario[i,j] = 1
    
    return(sudoku_binario)
   
def CalcularNumeroDeErrores(sudoku):
    numeroDeErrores = 0 
    for i in range (0,9):
        numeroDeErrores += CalcularNumeroDeErroresPorFilasYColumnas(i ,i ,sudoku)
    return(numeroDeErrores)

def CalcularNumeroDeErroresPorFilasYColumnas(fila, columna, sudoku):
    numeroDeErrores = (9 - len(np.unique(sudoku[:,columna]))) + (9 - len(np.unique(sudoku[fila,:])))
    return(numeroDeErrores)


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

def LLenarBloquesAletoriamente(sudoku, listaDeBloques):
    for bloque in listaDeBloques:
        for caja in bloque:
            if sudoku[caja[0],caja[1]] == 0:
                currentBlock = sudoku[bloque[0][0]:(bloque[-1][0]+1),bloque[0][1]:(bloque[-1][1]+1)]
                sudoku[caja[0],caja[1]] = choice([i for i in range(1,10) if i not in currentBlock])
    return sudoku

def SumaEnUnBloque (sudoku, unBloque):
    sumaFinal = 0
    for caja in unBloque:
        sumaFinal += sudoku[caja[0], caja[1]]
    return(sumaFinal)

def DosCuadradosAletoriosEnUnBloque(sudokuBinario, bloque):
    while (1):
        primeraCaja = random.choice(bloque)
        segundaCaja = choice([caja for caja in bloque if caja is not primeraCaja])

        if sudokuBinario[primeraCaja[0], primeraCaja[1]] != 1 and sudokuBinario[segundaCaja[0], segundaCaja[1]] != 1:
            return([primeraCaja, segundaCaja])

def IntercambiarBloques(sudoku, cajasParaIntercambiar):
    sudokuPropuesto = np.copy(sudoku)
    Auxiliar = sudokuPropuesto[cajasParaIntercambiar[0][0], cajasParaIntercambiar[0][1]]
    sudokuPropuesto[cajasParaIntercambiar[0][0], cajasParaIntercambiar[0][1]] = sudokuPropuesto[cajasParaIntercambiar[1][0], cajasParaIntercambiar[1][1]]
    sudokuPropuesto[cajasParaIntercambiar[1][0], cajasParaIntercambiar[1][1]] = Auxiliar
    return (sudokuPropuesto)

def EstadoPropuesto (sudoku, sudokuBinario, listaDeBloques):
    bloqueAletorio = random.choice(listaDeBloques)

    if SumaEnUnBloque(sudokuBinario, bloqueAletorio) > 6:  
        return(sudoku, 1, 1)
    cajasParaIntercambiar = DosCuadradosAletoriosEnUnBloque(sudokuBinario, bloqueAletorio)
    sudokuPropuesto = IntercambiarBloques(sudoku,  cajasParaIntercambiar)
    return([sudokuPropuesto, cajasParaIntercambiar])

def EscogerNuevoEstado (sudokuActual, sudokuBinario, listaDeBloques, sigma):
    propuesta = EstadoPropuesto(sudokuActual, sudokuBinario, listaDeBloques)
    nuevoSudoku = propuesta[0]
    cajasParaRevisar = propuesta[1]
    costoActual = CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[0][0], cajasParaRevisar[0][1], sudokuActual) + CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[1][0], cajasParaRevisar[1][1], sudokuActual)
    nuevoCosto = CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[0][0], cajasParaRevisar[0][1], nuevoSudoku) + CalcularNumeroDeErroresPorFilasYColumnas(cajasParaRevisar[1][0], cajasParaRevisar[1][1], nuevoSudoku)
    # costoActual = CalcularNumeroDeErrores(sudokuActual)
    # nuevoCosto = CalcularNumeroDeErrores(nuevoSudoku)
    diferenciaDeCostos = nuevoCosto - costoActual
    rho = math.exp(-diferenciaDeCostos/sigma)
    if(np.random.uniform(1,0,1) < rho):
        return([nuevoSudoku, diferenciaDeCostos])
    return([sudokuActual, 0])


def EscogerNumeroDeIteraciones(sudoku_binario):
    numeroDeIteraciones = 0
    for i in range (0,9):
        for j in range (0,9):
            if sudoku_binario[i,j] != 0:
                numeroDeIteraciones += 1
    return numeroDeIteraciones

def CalcularElSigmaInicial (sudoku, sudokuBinario, listaDeBloques):
    listaDeDiferencias = []
    sudokuTmp = sudoku
    print("gsd")
    print(ImprimirSudoku(sudokuTmp))
    for i in range(1,10):
        sudokuTmp = EstadoPropuesto(sudokuTmp, sudokuBinario, listaDeBloques)[0]
        #print("gsd")
        #print(ImprimirSudoku(sudokuTmp))
        listaDeDiferencias.append(CalcularNumeroDeErrores(sudokuTmp))
        #print(listaDeDiferencias)
    return (statistics.pstdev(listaDeDiferencias))


def ResolverSudoku (sudoku):
    f = open("Historial.txt", "a")
    solucionHallada = 0
    while (solucionHallada == 0):
        factorDecreciente = 0.99
        cuentaDeAtascos = 0
        sudokuBinario = np.copy(sudoku)
        #ImprimirSudoku(sudoku)
        ResolverValorSudoku(sudokuBinario)
        listaDeBloques = CrearListaDeBloques()
        sudokuTmp = LLenarBloquesAletoriamente(sudoku, listaDeBloques)
        #ImprimirSudoku(sudokuTmp)
        sigma = CalcularElSigmaInicial(sudoku, sudokuBinario, listaDeBloques)
        puntaje = CalcularNumeroDeErrores(sudokuTmp)
        #print(puntaje)
        iteraciones = EscogerNumeroDeIteraciones(sudokuBinario)
        #print(iteraciones)
        if puntaje <= 0:
            solucionHallada = 1

        while solucionHallada == 0:
            previousScore = puntaje
            for i in range (0, iteraciones):
                nuevoEstado = EscogerNuevoEstado(sudokuTmp, sudokuBinario, listaDeBloques, sigma)
                sudokuTmp = nuevoEstado[0]
                diferenciaDePuntaje = nuevoEstado[1]
                puntaje += diferenciaDePuntaje
                #print(puntaje)
                f.write(str(puntaje) + '\n')
                if puntaje <= 0:
                    solucionHallada = 1
                    break

            sigma *= factorDecreciente
            if puntaje <= 0:
                solucionHallada = 1
                break
            if puntaje >= previousScore:
                cuentaDeAtascos += 1
            else:
                cuentaDeAtascos = 0
            if (cuentaDeAtascos > 80):
                sigma += 2
            if(CalcularNumeroDeErrores(sudokuTmp)==0):
                #ImprimirSudoku(sudokuTmp)
                print(sudokuTmp)
                break
    f.close()
    return(sudokuTmp)

#solution = ResolverSudoku(sudoku)
#print(CalcularNumeroDeErrores(solution))
#ImprimirSudoku(solution)