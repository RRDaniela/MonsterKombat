import pygame
from healthbars import *
from monster import Monster
from settings import  *
from menu import *

#Menu
menu = True

#Creando instancias de los personajes
monster_1 = Monster(200, 370, False, 20, True, DOSBRAZOS_DATA, dosBrazos_sheet, DOSBRAZOS_ANIMATION_STEPS)
monster_2 = Monster(700, 370, True,  10, False, MDB_DATA, mdb_sheet, MDB_ANIMATION_STEPS)

#loop del juego principal
run = True
while run:
    clock.tick(fps)
    #Poner el fondo
    draw_bg()
    if(menu!=True):
        #Mostrar vida
        draw_health_bar(monster_1.salud, 20, 20)
        draw_health_bar(monster_2.salud, 630, 20)

        #update
        monster_1.update()
        monster_2.update()

        #Dibujar monstruos
        monster_1.draw(screen)
        monster_2.draw(screen)

        #mover jugadores
        monster_1.caminar(screen, monster_2)
        monster_2.caminar(screen, monster_1)
    else:
        screen.blit(Botón1, (ANCHO/2-200,ALTO/2-200))
        screen.blit(Botón1, (ANCHO/2-200,ALTO-300))
        screen.blit(text_start, (ANCHO/2-80,ALTO/2-88))
        screen.blit(text_quit, (ANCHO/2-55,ALTO-170))
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif (event.type==pygame.MOUSEBUTTONDOWN):
            if Boton_rect.collidepoint(event.pos):
                menu=False
    #Actualizar el display
    pygame.display.update()
#Salir del juego
pygame.quit()