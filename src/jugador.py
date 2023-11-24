import pygame
from pygame.font import Font
from pygame.surface import Surface

from bala import Bala
from constantes import *
from entidad import Entidad

# Clase Jugador
# Hereda propiedades y métodos de la clase Entidad
class Jugador(Entidad):
    def __init__(self, pantalla: pygame.Surface, tipografia: Font, posicion_inicial: tuple[float, float]) -> None:
        super().__init__(pantalla, COHETE)
        # Variable para identificar al jugador
        self.nombre = None
        self._tipografia = tipografia
        # Posición incial
        self._posicion_inicial = posicion_inicial
        # Instancia de la clase Bala
        self.bala = Bala(pantalla)
        self.bala.delta(0, 1)
        # Puntaje en el juego
        self.puntaje = 0
        # Número de vidad
        self.vidas = 3

    # Asignador del nombre
    def nombrar(self, nombre: str) -> None:
        self.nombre = self._tipografia.render(nombre, True, (255, 255, 255)) 

    # Asignador de vidas (3)
    def revivir(self) -> None:
        self.vidas = 3

    # Respawn (Posiciona a la superficie en la posición inicial)
    def reaparecer(self) -> None:
        x, y = self._posicion_inicial
        self.posicionar(x, y)

    # Muestra el nombre del jugador debajo de la imagen si el jugador fue nombrado
    def mostrar(self) -> None:
        if isinstance(self.nombre, Surface):
            _, y = self.tamano_imagen()
            pos_x, pos_y = self.posicion()
            self._pantalla.blit(self.nombre, (pos_x, pos_y + y))
        super().mostrar()

    # Muestra la bala y la mueve hacia arriba
    def disparar(self) -> None:
        if self.bala.esta_afuera_de_la_pantalla():
           self.restaurar_bala()
        self.bala.mover_arriba()
        self.bala.mostrar()

    # Posicionar la bala en la misma coordenada que el jugador
    def restaurar_bala(self) -> None:
        self.bala.posicionar(self._x, self._y)

    # Asignador de puntos
    def punto(self) -> None:
        self.puntaje += 1

    # Resta 1 vida
    def morir(self) -> None:
        self.vidas -= 1
        self.reaparecer()

    # Retorna verdadero si el jugador tiene más de 0 vidas
    def sigue_vivo(self) -> bool:
        return self.vidas > 0

    # Bloquea el movimiento del jugador si no tiene vidas (vidas = 0)
    def mover(self, arriba: bool, abajo: bool, izquierda: bool, derecha: bool) -> None:
        if not self.sigue_vivo():
            return
        super().mover(arriba, abajo, izquierda, derecha)
