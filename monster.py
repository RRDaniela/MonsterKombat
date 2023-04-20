import pygame
from settings import *
from colors import *

class Monster():
    '''Clase de los monstruos del juego'''
    def __init__(self, x, y, flip, velocidad, player_2, data, sprite_sheet, animation_steps):
        self.height = data[0]
        self.width = data[1]
        self.image_scale = data[2]
        self.offset = data[3]
        self.flip = flip
        self.animation_list = self.cargar_imagenes(sprite_sheet, animation_steps) 
        self.rect = pygame.Rect((x, y, 100, 180))
        self.velocidad=velocidad
        self.velY = 0
        self.player_2:bool = player_2 
        self.salto = False
        self.tipo_ataque:int = 0
        self.cooldown_ataque = 0
        self.atacando=False
        self.corriendo = False
        self.salud = 100
        #0:walk, 1:Heavy Attack, 2:Idle, 3:Take Hit. 4: Death 
        self.accion = 2
        self.frame_index = 2
        self.image = self.animation_list[self.accion][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.take_hit = False
        self.vivo = True

    def cargar_imagenes(self, sprite_sheet, animation_steps):
        '''Función que carga las animaciones para cada acción desde el spritesheet de cada personaje'''
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.width, y * self.height, self.width, self.height)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.width * self.image_scale, self.height * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def caminar(self, surface, target):
        ''''Funcion que controla todo el movimiento del personaje'''
        gravedad = 2
        dx = 0
        dy = 0
        self.corriendo = False
        self.tipo_ataque = 0

        #Dependiendo de las teclas.. moverse
        key = pygame.key.get_pressed()
        if self.vivo == False:
            pygame.QUIT
        else:
            if self.atacando == False:
                #Movimiento
                if self.player_2:
                    if key[pygame.K_a]:
                        dx = -(self.velocidad)
                        self.corriendo = True
                    if key[pygame.K_d]:
                        dx = self.velocidad
                        self.corriendo = True
                    if key[pygame.K_w] and self.salto == False:
                        self.velY = -SALTO+self.velocidad
                        self.salto = True
                    if key[pygame.K_q] or key[pygame.K_e] or key[pygame.K_r]:
                        
                        if key[pygame.K_q]:
                            self.tipo_ataque = 1
                            self.atacar(surface, target)
                        if key[pygame.K_e]:
                            self.tipo_ataque = 2
                            self.atacar(surface, target)
                        if key[pygame.K_r]:
                            self.tipo_ataque = 3
                            self.atacar(surface, target)
                else:
                    if key[pygame.K_LEFT]:
                        dx = -(self.velocidad)
                        self.corriendo = True
                    if key[pygame.K_RIGHT]:
                        dx = self.velocidad
                        self.corriendo = True
                    if key[pygame.K_UP] and self.salto == False:
                        self.velY = -SALTO+self.velocidad
                        self.salto = True
                    if key[pygame.K_KP_1] or key[pygame.K_KP_2] or key[pygame.K_KP_3]:
                        self.atacar(surface, target)
                        if key[pygame.K_KP_1]:
                            self.tipo_ataque = 1
                            self.atacar(surface, target)
                        if key[pygame.K_KP_2]:
                            self.tipo_ataque = 2
                            self.atacar(surface, target)
                        if key[pygame.K_KP_3]:
                            self.tipo_ataque = 3
                            self.atacar(surface, target)
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
                #Aplicar cooldown a ataque
                if self.cooldown_ataque > 0:
                    self.cooldown_ataque -=1

                #Modificar la posición del monstruo
                self.rect.x += dx
                self.rect.y += dy
    
    def update(self):
        '''Función que se encarga de actualizar la animación del personaje dependiendo de la acción que esté realizando'''
        #Verificar acciones en uso
        if self.salud <= 0:
            self.salud = 0
            self.vivo = False
            self.cambio_accion(4) #4: Muerte
        elif self.take_hit == True:
            self.cambio_accion(3) #3: hit
        elif self.atacando == True:
            if self.tipo_ataque == 1:
                hit.play()
                self.cambio_accion(5) #5 ataque rapido
            elif self.tipo_ataque == 2:
                hit.play()
                self.cambio_accion(1) #1: Ataque pesado
            elif self.tipo_ataque == 3:
                hit.play()
                self.cambio_accion(6) #6: ataque ligero
        elif self.corriendo == True:
            self.cambio_accion(0) #0:caminar
        else:
            self.cambio_accion(2) #2:idle
        anim_cooldown = 90
        #Actualizar frame que se debe ver en el personaje
        self.image = self.animation_list[self.accion][self.frame_index]
        #Verificar si suficiente tiempo ha pasado desde último update 
        if pygame.time.get_ticks() - self.update_time > anim_cooldown:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        #Verificar si terminó la animación
        if self.frame_index >= len(self.animation_list[self.accion]):
            #Checar si el personaje murió
            if self.vivo == False:
                self.frame_index = len(self.animation_list[self.accion]) -1
            else:
                self.frame_index = 0
                if self.accion == 1:
                    self.atacando = False
                    self.cooldown_ataque = 50
                if self.accion == 3 or self.accion == 5 or self.accion == 6:
                    self.take_hit = False
                    self.atacando = False
                    if self.accion == 5:
                        self.cooldown_ataque = 10
                    elif self.accion == 6:
                        self.cooldown_ataque = 20
                    elif self.accion == 3:
                        self.cooldown_ataque = 50
                    

    def atacar(self, surface, target):
        '''Función que crea el rectángulo de colisión del ataque del personaje y hace el cálculo de daño'''
        if self.cooldown_ataque == 0:
            self.atacando = True
            rect_arma = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, 3* self.rect.width, self.rect.height)
            if rect_arma.colliderect(target.rect):
                if self.tipo_ataque == 1:
                    target.salud -= 5
                    target.take_hit = True
                elif self.tipo_ataque == 2:
                    target.salud -= 10
                    target.take_hit = True
                elif self.tipo_ataque == 3:
                    target.salud -= 5
                    target.take_hit = True
            pygame.draw.rect(surface, VERDE, rect_arma)
    

    def cambio_accion(self, nueva_accion):
        '''Función que verifica si la nueva acción introducida es diferente a la anterior'''
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            #Actualizar settings de la animación
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        ''''Funcion para dibujar a los monstruos en la pantalla'''
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, ROJO, self.rect)
        surface.blit(img, (self.rect.x -(self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
    
