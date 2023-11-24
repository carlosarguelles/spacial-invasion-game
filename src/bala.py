import pygame

from constantes import BALA
from entidad import Entidad

# Clase Bala que hereda a la clase Entidad
class Bala(Entidad):
    def __init__(self, pantalla: pygame.Surface) -> None:
        # Llamado del constructor de entidad con la imagen de la bala
        super().__init__(pantalla, BALA)

    # Mover sin limites de la pantalla
    def _mover(self, x: float, y: float) -> None:
        super().posicionar(self._x + x, self._y + y)

    # Retorna verdadero si la posición de la superficie se encuentra fuera de la pantalla
    def esta_afuera_de_la_pantalla(self) -> bool:
        return self._x < 0 or self._y < 0

    # Alias de sacar()
    def destruir(self) -> None:
        self.sacar()
