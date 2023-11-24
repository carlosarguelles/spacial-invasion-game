import pygame

from constantes import *

# Clase Entidad
# Clase abstracta que implementa la lógica para dibujar y posicionar superficies con PyGame
class Entidad:
    def __init__(self, pantalla: pygame.Surface, imagen: str) -> None:
        self._pantalla = pantalla
        self._imagen = pygame.image.load(imagen)
        self._x = 0
        self._y = 0
        self._delta_x = 0.33
        self._delta_y = 0.33
        self._imagen_x, self._imagen_y = self._imagen.get_size()
        max_x, max_y = self._pantalla.get_size()
        self._limite_x = max_x - self._imagen_x
        self._limite_y = max_y - self._imagen_y

    # Asignador al delta, esto es el incremento de la posición en cada cambio de posición
    def delta(self, delta_x, delta_y) -> None:
        self._delta_x = delta_x
        self._delta_y = delta_y

    # Asignador de coordernadas (posición)
    def posicionar(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    # Dibuja en pantalla la imagen en las coordernadas
    def mostrar(self) -> None:
        self._pantalla.blit(self._imagen, (self._x, self._y))

    # Retorna una tupla con las dimensiones de la imagen
    def tamano_imagen(self) -> tuple[float, float]:
        return self._imagen_x, self._imagen_y

    # Mueve la superficie asegurándose que no se salga del límite de la pantalla
    def _mover(self, x: float, y: float) -> None:
        _x = max(0, min(self._limite_x, self._x + x))
        _y = max(0, min(self._limite_y, self._y + y))
        self.posicionar(_x, _y)

    # Alias de _mover hacia arriba con el delta establecido
    def mover_arriba(self) -> None:
        self._mover(0, -self._delta_y)

    # Alias de _mover hacia abajo con el delta establecido
    def mover_abajo(self) -> None:
        self._mover(0, self._delta_y)

    # Alias de _mover hacia la derecha con el delta establecido
    def mover_derecha(self) -> None:
        self._mover(self._delta_x, 0)

    # Alias de _mover hacia la izquierda con el delta establecido
    def mover_izquierda(self) -> None:
        self._mover(-self._delta_x, 0)

    # Múltiples movimientos
    def mover(self, arriba: bool, abajo: bool, izquierda: bool, derecha: bool) -> None:
        if izquierda:
            self.mover_izquierda()
        if derecha:
            self.mover_derecha()
        if arriba:
            self.mover_arriba()
        if abajo:
            self.mover_abajo()

    # Retorna la posición o coordernadas
    def posicion(self) -> tuple[float, float]:
        return self._x, self._y

    # Posiciona a la superficie por fuera de la pantalla
    def sacar(self) -> None:
        x, y = self.tamano_imagen()
        self.posicionar(-x - 10, -y - 10)
