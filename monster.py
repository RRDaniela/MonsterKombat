import pygame
from settings import *
from colors import *

class Monster():
    def __init__(self, x, y, velocidad, player_2, data, sprite_sheet, animation_steps):
        
        self.height = data[0]
        self.width = data[1]
        self.flip = False
        self.animation_list = self.cargar_imagenes(sprite_sheet)
        self.rect = pygame.Rect((x, y, 80, 180))
        self.velocidad=velocidad
        self.velY = 0
        self.player_2:bool = player_2
        self.salto = False
        self.tipo_ataque:int = 0
        self.atacando=False
        self.salud = 100

    def cargar_imagenes(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.width, y * self.height, self.width, self.height)
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def caminar(self, surface, target):
        ''''Funcion para hacer que el monstruo camine'''
        gravedad = 2
        dx = 0
        dy = 0


        #Dependiendo de las teclas.. moverse
        key = pygame.key.get_pressed()

        if self.atacando == False:
            #Movimiento
            if self.player_2:
                if key[pygame.K_a]:
                    dx = -(self.velocidad)
                if key[pygame.K_d]:
                    dx = self.velocidad
                if key[pygame.K_w] and self.salto == False:
                    self.velY = -SALTO+self.velocidad
                    self.salto = True
                if key[pygame.K_q] or key[pygame.K_e] or key[pygame.K_r]:
                    self.atacar(surface, target)
                    if key[pygame.K_q]:
                        self.tipo_ataque = 1
                    if key[pygame.K_e]:
                        self.tipo_ataque = 2
                    if key[pygame.K_r]:
                        self.tipo_ataque = 3
            else:
                if key[pygame.K_LEFT]:
                    dx = -(self.velocidad)
                if key[pygame.K_RIGHT]:
                    dx = self.velocidad
                if key[pygame.K_UP] and self.salto == False:
                    self.velY = -SALTO+self.velocidad
                    self.salto = True
                if key[pygame.K_KP_1] or key[pygame.K_KP_2] or key[pygame.K_KP_3]:
                    self.atacar(surface, target)
                    if key[pygame.K_q]:
                        self.tipo_ataque = 1
                    if key[pygame.K_e]:
                        self.tipo_ataque = 2
                    if key[pygame.K_r]:
                        self.tipo_ataque = 3
            #efecto de gravedad
            self.velY += gravedad
            dy += self.velY

            #No permitir que el monstruo salga de pantalla
            if self.rect.left+dx <0:
                dx = -self.rect.left

            if self.rect.right+dx > ANCHO:
                dx = ANCHO - self.rect.right
            if self.rect.bottom + dy > ALTO - 130:
                self.velY = 0
                self.salto = False
                dy = ALTO -130 - self.rect.bottom 
            #Los personajes siempre se ven entre ellos
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            #Modificar la posición del monstruo
            self.rect.x += dx
            self.rect.y += dy

    def atacar(self, surface, target):
        self.atacando = True
        rect_arma = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2* self.rect.width, self.rect.height)
        if rect_arma.colliderect(target.rect):
            target.salud -= 10
        pygame.draw.rect(surface, VERDE, rect_arma)
        
    def draw(self, surface):
        ''''Funcion para dibujar a los monstruos en la pantalla'''
        pygame.draw.rect(surface, ROJO, self.rect)
    
