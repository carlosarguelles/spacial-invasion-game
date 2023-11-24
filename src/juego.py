import pygame

from constantes import *
from boton import Boton
from enemigo import Enemigo
from jugador import Jugador

# Clase Juego
# Crea el juego, inicializa variables y la librería PyGame
class Juego:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Invasión Espacial 2")
        pygame.display.set_icon(pygame.image.load(ICONO_EXTRATERRESTRE))
        self._pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self._fondo = pygame.image.load(FONDO)
        self._jugando = True
        self._seccion = MENU
        self._tipografia = pygame.font.Font(TIPOGRAFIA, 16)
        # Crea las instancias de la clase Jugador con una posición inicial
        self._jugador1 = Jugador(self._pantalla, self._tipografia, posicion_inicial=(ANCHO * 0.5, 500))
        self._jugador2 = Jugador(self._pantalla, self._tipografia, posicion_inicial=(ANCHO * 0.20, 500))
        self._enemigos: list[Enemigo] = []
        self._tipografia_g = pygame.font.Font(TIPOGRAFIA, 40)

    # Sección MENU que muestra los botones para cada modo de juego
    def _menu(self) -> None:
        nombre = pygame.image.load(NOMBRE)
        self._pantalla.blit(nombre, (280, 82.75))

        boton1 = Boton(280, 220, pygame.image.load(BOTON_1))
        boton2 = Boton(280, 320, pygame.image.load(BOTON_2))
        boton3 = Boton(280, 420, pygame.image.load(BOTON_3))

        # Si el boton1 fue presionado
        if boton1.mostrar(self._pantalla):
            self._reproducir_sonido(GOLPE)
            self._crear_enemigos(7)
            self._jugador1.revivir()
            self._jugador1.reaparecer()
            self._seccion = 1
        # Si el boton2 fue presionado
        if boton2.mostrar(self._pantalla):
            self._reproducir_sonido(GOLPE)
            self._crear_enemigos(14)
            self._jugador1.revivir()
            self._jugador1.reaparecer()
            self._jugador1.nombrar("Jugador 1")
            self._jugador2.revivir()
            self._jugador2.reaparecer()
            self._jugador2.nombrar("Jugador 2")
            self._seccion = 2
        # Si el boton2 fue presionado (Quitar juego)
        if boton3.mostrar(self._pantalla):
            self._reproducir_sonido(GOLPE)
            self._jugando = False

    # Función para reproducir sonidos
    def _reproducir_sonido(self, sonido) -> None:
        s = pygame.mixer.Sound(sonido)
        s.play()

    # Verifica si el código de la tecla hace parte de las teclas con las que se juega
    def _es_tecla_del_juego(self, tecla: int) -> bool:
        teclas = [
          pygame.K_LEFT,
          pygame.K_RIGHT,
          pygame.K_UP,
          pygame.K_DOWN,
          pygame.K_a,
          pygame.K_d,
          pygame.K_w,
          pygame.K_s,
        ]
        return tecla in teclas

    # Crea y sobreescribe los enemigos (Lista de clase Enemigo)
    def _crear_enemigos(self, cantidad: int) -> None:
        if len(self._enemigos) > 0:
            self._enemigos = []
        for _ in range(cantidad):
            enemigo = Enemigo(self._pantalla)
            enemigo.posicionar_aleatoriamente()
            enemigo.delta(0.33, 0.04)
            self._enemigos.append(enemigo)

    # Ciclo principal del juego
    def jugar(self) -> None:
        pygame.mixer.music.load(MUSICA_FONDO)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        # Indican si la tecla correspondiente fue presionada en cada iteración
        izquierda = False
        derecha = False
        arriba = False
        abajo = False
        w = False
        a = False
        s = False
        d = False
        # Indica si la bala de cada jugador es visible
        bala_1_visible = False
        bala_2_visible = False
        while self._jugando:
            # Establece el fondo del juego
            self._pantalla.blit(self._fondo, (0, 0))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Detiene el juego
                    self._jugando = False

                # Solo verificar las teclas si está en modo de juego (secciones UN_JUGADOR y MULTIJUGADOR)
                if self._seccion == UN_JUGADOR or self._seccion == MULTIJUGADOR:
                    if evento.type == pygame.KEYDOWN:
                        # Establece verdadero si la tecla correspondiente fue presionada
                        if evento.key == pygame.K_LEFT:
                            izquierda = True
                        if evento.key == pygame.K_RIGHT:
                            derecha = True
                        if evento.key == pygame.K_UP:
                            arriba = True
                        if evento.key == pygame.K_DOWN:
                            abajo = True
                        if evento.key == pygame.K_a:
                            a = True
                        if evento.key == pygame.K_d:
                            d = True
                        if evento.key == pygame.K_w:
                            w = True
                        if evento.key == pygame.K_s:
                            s = True
                        # Dispara las balas si y solo si se presiona la tecla y no hay una bala del jugador 1 visible
                        if evento.key == pygame.K_u and self._jugador1.bala.esta_afuera_de_la_pantalla():
                            # Reproduce sonido de disparo
                            self._reproducir_sonido(DISPARO)
                            bala_1_visible = True
                        # Dispara las balas si y solo si se presiona la tecla y no hay una bala del jugador 2 visible
                        if evento.key == pygame.K_t and self._jugador2.bala.esta_afuera_de_la_pantalla() and self._seccion == MULTIJUGADOR:
                            # Reproduce sonido de disparo
                            self._reproducir_sonido(DISPARO)
                            bala_2_visible = True

                    if evento.type == pygame.KEYUP:
                        # Desactiva el movimiento si la tecla es soltada
                        if self._es_tecla_del_juego(evento.key):
                            izquierda = False
                            derecha = False
                            abajo = False
                            arriba = False
                            w = False
                            a = False
                            s = False
                            d = False

            # Si la sección es MENU mostrar MENU
            if self._seccion == MENU:
                izquierda = False
                derecha = False
                abajo = False
                arriba = False
                w = False
                a = False
                s = False
                d = False
                self._menu()

            # Si la sección es UN_JUGADOR mostrar UN_JUGADOR
            if self._seccion == UN_JUGADOR:
                # Regresar al MENU si el jugador no tiene vidas (0)
                if not self._jugador1.sigue_vivo():
                    self._seccion = MENU
                # Mover al jugador con las teclas presionadas
                self._jugador1.mover(arriba, abajo, izquierda, derecha)
                if bala_1_visible:
                    # Mostrar bala si es visible
                    self._jugador1.disparar()
                # Mostrar al jugador
                self._jugador1.mostrar()
                # Mostrar puntaje y vidas del jugador
                self._pantalla.blit(self._tipografia.render(f'Puntaje: {self._jugador1.puntaje}', True, (255, 255, 255)), (10, 10))
                self._pantalla.blit(self._tipografia.render(f'Vidas: {self._jugador1.vidas}', True, (255, 255, 255)), (10, 30))
                # Mostrar bala hasta que salga de la pantalla
                bala_1_visible = not self._jugador1.bala.esta_afuera_de_la_pantalla()

            # Si la sección es MULTIJUGADOR mostrar MULTIJUGADOR
            if self._seccion == MULTIJUGADOR:
                # Ir al MENU si ambos jugadores tienen 0 vidas
                if not self._jugador1.sigue_vivo() and not self._jugador2.sigue_vivo():
                    self._pantalla.blit(self._fondo, (0, 0))
                    self._seccion = MENU
                # Sacar de la pantalla al jugador 1 si no tiene vidas
                if not self._jugador1.sigue_vivo():
                    self._jugador1.sacar()
                # Sacar de la pantalla al jugador 2 si no tiene vidas
                if not self._jugador2.sigue_vivo():
                    self._jugador2.sacar()
                # Mover al jugador 1 con las teclas presionadas
                self._jugador1.mover(arriba, abajo, izquierda, derecha)
                # Mover al jugador 2 con las teclas presionadas w (arriba), s (abajo), a (izquierda), d (derecha)
                self._jugador2.mover(w, s, a, d)
                # Mostrar balas de los jugadores si están visibles
                if bala_1_visible:
                    self._jugador1.disparar()
                self._jugador1.mostrar()
                if bala_2_visible:
                    self._jugador2.disparar()
                # Mostrar jugadores y sus puntajes
                self._jugador2.mostrar()
                self._pantalla.blit(self._tipografia.render("Jugador 2", True, (255, 255, 255)), (10, 10))
                self._pantalla.blit(self._tipografia.render(f'Puntaje: {self._jugador2.puntaje}', True, (255, 255, 255)), (10, 30))
                self._pantalla.blit(self._tipografia.render(f'Vidas: {self._jugador2.vidas}', True, (255, 255, 255)), (10, 60))
                self._pantalla.blit(self._tipografia.render("Jugador 1", True, (255, 255, 255)), (ANCHO - 200, 10))
                self._pantalla.blit(self._tipografia.render(f'Puntaje: {self._jugador1.puntaje}', True, (255, 255, 255)), (ANCHO - 200, 30))
                self._pantalla.blit(self._tipografia.render(f'Vidas: {self._jugador1.vidas}', True, (255, 255, 255)), (ANCHO - 200, 60))
                # Mostrar balas hasta que salga de la pantalla
                bala_1_visible = not self._jugador1.bala.esta_afuera_de_la_pantalla()
                bala_2_visible = not self._jugador2.bala.esta_afuera_de_la_pantalla()

            if self._seccion == UN_JUGADOR or self._seccion == MULTIJUGADOR:
                # Enemigos
                for e in range(len(self._enemigos)):
                    # Mover enemigos de arriba hacia abajo dentro de los límites de la pantalla
                    self._enemigos[e].mover_dentro_pantalla()
                    # Volver al MENU si algún enemigo llegó al border inferior de la pantalla
                    if self._enemigos[e].llego_al_borde():
                        self._seccion = MENU
                    # Revisar si el enemigo(e) colisiona con alguna bala que haya lanzado el jugador 1
                    if bala_1_visible:
                        if self._enemigos[e].colisiona(self._jugador1.bala):
                            self._reproducir_sonido(GOLPE)
                            bala_1_visible = False
                            # Destruye la bala (la saca de la pantalla)
                            self._jugador1.bala.destruir()
                            # Incrementa el puntaje del jugador
                            self._jugador1.punto()
                            # Posiciona de nuevo al enemigo afectado por la bala
                            self._enemigos[e].posicionar_aleatoriamente()
                    # Revisar si el enemigo(e) colisiona con alguna bala que haya lanzado el jugador 1
                    if bala_2_visible:
                        if self._enemigos[e].colisiona(self._jugador2.bala):
                            self._reproducir_sonido(GOLPE)
                            bala_2_visible = False
                            # Destruye la bala (la saca de la pantalla)
                            self._jugador2.bala.destruir()
                            # Incrementa el puntaje del jugador
                            self._jugador2.punto()
                            # Posiciona de nuevo al enemigo afectado por la bala
                            self._enemigos[e].posicionar_aleatoriamente()
                    # Revisar si el enemigo(e) colisiona con el jugador 1
                    if self._enemigos[e].colisiona(self._jugador1):
                        self._reproducir_sonido(GOLPE)
                        # Resta una vida al jugador 1
                        self._jugador1.morir()
                    # Revisar si el enemigo(e) colisiona con el jugador 1
                    if self._enemigos[e].colisiona(self._jugador2):
                        self._reproducir_sonido(GOLPE)
                        # Resta una vida al jugador 2
                        self._jugador2.morir()
                    # Muestra al enemigo
                    self._enemigos[e].mostrar()
            # Actualiza la pantalla con los cambios
            pygame.display.update()
        # Cierra el juego si la variable _jugando es falsa
        pygame.quit()
