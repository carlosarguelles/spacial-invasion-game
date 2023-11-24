import pygame

# Clase para crear botones a partir de imagenes
class Boton:
    # Recibe una image y coordenadas
    def __init__(self, x: int, y: int, imagen: pygame.Surface) -> None:
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        # Variable que indica si la imagen fue presionada
        self.click = False

    # Mostrar el botón y retornar verdadero si fue presionado por el mouse
    def mostrar(self, pantalla: pygame.Surface) -> bool:
        cliqueado = False
        # Obtiene las coordenadas del click en la pantalla
        posicion = pygame.mouse.get_pos()
        # Compara la posición y verifica si colisiona con la imagen
        if self.rect.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                cliqueado = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        # Dibuja la superficie en la pantalla
        pantalla.blit(self.imagen, (self.rect.x, self.rect.y))
        return cliqueado
