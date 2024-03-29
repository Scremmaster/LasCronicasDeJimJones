import pygame

import constantes

from platforma import PlataformaConMovimiento
from funciones_spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    """Clase utilizada para desarrollar los jugadores del juego. """
    
    # -- Atributos
    mover_x = 0
    mover_y = 0

    # Estas listas definen todas las imagenes de nuestro jugador.
    jugador_frame_izq = []
    jugador_frame_der = []

    # Direccion en la que va el jugador.
    direccion = "R"

    # Lista de sprite con las cosas que nos podemos chocar.
    nivel = None

    # -- Metodos
    def __init__(self,ruta):
        """ __Funcion constructor__ 
            Aca en donde se debe cargar el sprite sheet del jugador.
            Se debe cargar los sprite con movimiento hacia la izquierda y hacia la derecha.
        """

        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet(ruta)
        
        # Carga de todos los sprite de la imagen hacia la derecha.
        imagen = sprite_sheet.obtener_imagen(31, 50, 86, 149)
        
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(140, 50, 87,141 )
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(244, 50, 70, 141)
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(348, 44, 48, 155)
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(445, 45, 60, 155)
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(549, 50, 77, 155)
        self.jugador_frame_der.append(imagen)
        imagen = sprite_sheet.obtener_imagen(30, 230, 78, 139)
        self.jugador_frame_der.append(imagen)

        # # Carga de todos los sprite de la imagen hacia la derecha y la rotamos.
        imagen = sprite_sheet.obtener_imagen(0, 0, 66, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(66, 0, 66, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(132, 0, 67, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(0, 93, 66, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(66, 93, 66, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(132, 93, 72, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)
        imagen = sprite_sheet.obtener_imagen(0, 186, 70, 90)
        imagen = pygame.transform.flip(imagen, True, False)
        self.jugador_frame_izq.append(imagen)

        # Seteamos con que sprite comenzar
        self.image = self.jugador_frame_der[0]


        self.rect = self.image.get_rect()


    def update(self):
        """ Metodo que actualiza la posicion del jugador. """
        
        # Gravedad
        self.calc_grav()

        # Movimientos Izquierda/Derecha
        self.rect.x += self.mover_x
        pos = self.rect.x + self.nivel.posicion_jugador_nivel
        if self.direccion == "R":
            frame = (pos // 30) % len(self.jugador_frame_der)
            self.image = self.jugador_frame_der[frame]
        else:
            frame = (pos // 30) % len(self.jugador_frame_izq)
            self.image = self.jugador_frame_izq[frame]

        # Verficiamos si colisionamos con algo mientras avanzamos
        lista_de_bloques_colisionados = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas, False)
        for block in lista_de_bloques_colisionados:
            if self.mover_x > 0:
                self.rect.right = block.rect.left
            elif self.mover_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.mover_y

        # Verficiamos si colisionamos con algo si saltamos
        lista_de_bloques_colisionados = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas, False)
        for block in lista_de_bloques_colisionados:

            if self.mover_y > 0:
                self.rect.bottom = block.rect.top
            elif self.mover_y < 0:
                self.rect.top = block.rect.bottom

            self.mover_y = 0

            if isinstance(block, PlataformaConMovimiento):
                self.rect.x += block.mover_x

    def calc_grav(self):
        """ Calcula el efecto de la gravedad. """
        
        if self.mover_y == 0:
            self.mover_y = 1
        else:
            self.mover_y += .35

        # Verificamos si estamos en el suelo.
        if self.rect.y >= constantes.LARGO_PISO - self.rect.height and self.mover_y >= 0:
            self.mover_y = 0
            self.rect.y = constantes.LARGO_PISO - self.rect.height

    def saltar(self):
        """ Metodo que se llamam si saltamos. """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.nivel.lista_plataformas, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= constantes.LARGO_PISO:
            self.mover_y = -10

    def retroceder(self):
        """ Se llama cuando movemos hacia la izq. """
        
        self.mover_x = -6
        self.direccion = "L"

    def avanzar(self):
        """ Se llama cuando movemos hacia la der. """
        
        self.mover_x = 6
        self.direccion = "R"

    def parar(self):
        """ Se llama cuando soltamos la tecla. """
        self.mover_x = 0
