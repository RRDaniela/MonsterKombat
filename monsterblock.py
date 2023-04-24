import pygame
from settings import *
from colors import *

class MonsterBlock:
    def __init__(self, monster):
        self.monster = monster
        self.bloqueando=False

    def cargar_imagenes(self, sprite_sheet, animation_steps):
        self.monster.cargar_imagenes(sprite_sheet, animation_steps)

    def caminar(self, surface, target):
        key = pygame.key.get_pressed()
        if self.monster.player_2:
            if key[pygame.K_x]:
                print('bloqueando')
                self.bloquear()
            else:
                self.desbloquear()
        else:
            if key[pygame.K_KP_4]:
                self.bloquear()
            else:
                self.desbloquear()
        self.monster.caminar(surface, target)

    def update(self):
        self.monster.update()

    def atacar(self, surface, target):
        print('atacando')
        if self.bloqueando:
            target.salud -= 2.5
        else:
            self.monster.atacar(surface, target)

    def cambio_accion(self, nueva_accion):
        self.monster.cambio_accion( nueva_accion)

    def draw(self, surface):
        self.monster.draw(surface)

    def bloquear(self):
        self.bloqueando = True

    def desbloquear(self):
        self.bloqueando = False