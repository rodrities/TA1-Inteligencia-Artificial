import pygame
import numpy as np
from SimulatedAneling import ResolverSudoku
import time
pygame.font.init()

#tablero = [
 #       [0,2,4,0,0,7,0,0,0],
  #      [6,0,0,0,0,0,0,0,0],
   #     [0,0,3,6,8,0,4,1,5],
    #    [4,3,1,0,0,5,0,0,0],
     #   [5,0,0,0,0,0,0,3,2],
      #  [7,9,0,0,0,0,0,6,0],
       # [2,0,9,7,1,0,8,0,0],
        #[0,4,0,0,9,3,0,0,0],
        #[3,1,0,0,0,4,7,5,0]        
    #]
sudokuInicial = """
                    024007000
                    600000000
                    003680415
                    431005000
                    500000032
                    790000060
                    209710800
                    040093000
                    310004750
                """

tableroInicial = np.array([[int(i) for i in linea] for linea in sudokuInicial.split()])

class Cuadricula:
    def __init__(self, filas, columnas, ancho, alto, tablero):
        self.filas = filas
        self.columnas = columnas
        self.tablero = tablero
        self.cubos = [[Cubo(self.tablero[i][j], i, j, ancho, alto) for j in range(columnas)] for i in range(filas)]
        self.ancho = ancho
        self.alto = alto
        self.model = None
        self.selected = None

    def dibujar(self, win):
        division = self.ancho / 9
        for i in range(self.filas+1):
            if i % 3 == 0 and i != 0:
                grosor = 4
            else:
                grosor = 1
            pygame.draw.line(win, (0,0,0), (0, i*division), (self.ancho, i*division), grosor)
            pygame.draw.line(win, (0, 0, 0), (i * division, 0), (i * division, self.alto), grosor)

        for i in range(self.filas):
            for j in range(self.columnas):
                self.cubos[i][j].dibujar(win)

class Cubo:
    filas = 9
    columnas = 9

    def __init__(self, numero, fila, columna, ancho ,alto):
        self.numero = numero
        self.temp = 0
        self.fila = fila
        self.columna = columna
        self.ancho = ancho
        self.alto = alto
        

    def dibujar(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        division = self.ancho / 9
        x = self.columna * division
        y = self.fila * division

        if self.temp != 0 and self.numero == 0:
            texto = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(texto, (x+5, y+5))
        elif not(self.numero == 0):
            texto = fnt.render(str(self.numero), 1, (0, 0, 0))
            win.blit(texto, (x + (division/2 - texto.get_width()/2), y + (division/2 - texto.get_height()/2)))

def actualizar_tablero(win, tablero):
    win.fill((255,255,255))
    tablero.dibujar(win)


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    tablero = Cuadricula(9, 9, 540, 540, tableroInicial)
    key = None
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    solucion = ResolverSudoku(tableroInicial)
                    tablero = Cuadricula(9, 9, 540, 540, solucion)

        actualizar_tablero(win, tablero)
        pygame.display.update()


main()
pygame.quit()