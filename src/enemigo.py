import pygame
import math
import random

from constantes import *
from entidad import Entidad

DERECHA = 0
IZQUIERDA = 1

# Clase Enemigo que hereda de la clase Entidad
class Enemigo(Entidad):
    def __init__(self, pantalla: pygame.Surface) -> None:
        # Constructor clase Entidad con la imagen del Enemigo
        super().__init__(pantalla, ENEMIGO)
        self._direccion = DERECHA

    # Posiciona a la superficie en el rango del ancho de la pantalla y de la mitad del alto de la pantalla
    def posicionar_aleatoriamente(self) -> None:
        x, y = (random.randint(0, ANCHO), random.randint(0, round(ALTO / 2)))
        self.posicionar(x, y)

    # Calcula la distancia euclediana entre dos superficies según la posición en la que están (x, y)
    def colisiona(self, entidad: Entidad) -> bool:
        distancia = math.sqrt(math.pow(self._x - entidad._x, 2) + math.pow(entidad._y - self._y, 2))
        return distancia < 27

    # Mueve la superficie hacia abajo y cambia de dirección si llega al limite de la pantalla
    def mover_dentro_pantalla(self) -> None:
        self.mover_abajo()

        if self._direccion == DERECHA:
            self.mover_derecha()
        
        if self._direccion == IZQUIERDA:
            self.mover_izquierda()

        if self._x == self._limite_x:
            self._direccion = IZQUIERDA

        if self._x == 0:
            self._direccion = DERECHA

    # Retorna verdadero si el Enemigo llegó al borde inferior de la pantalla
    def llego_al_borde(self) -> bool:
        return self._y == self._limite_y
