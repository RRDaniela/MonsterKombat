import pygame
from healthbars import *
from monster import Monster
from settings import  *
from menu import *
from boton import *
from monster_factory import *
from monsterblock import * 

#Si alguno de los 2 personajes murieron
font_size = 30
font = pygame.font.Font(font_path, font_size)
game_over_text = font.render("Game Over", True, (255, 0, 0))
text_x = ANCHO / 2 - game_over_text.get_width() / 2 -200
text_y = ALTO/2
text_velocity = -1

#Menu
menu = True
flag = True

#Creando instancias de los personajes
#monster_1 = Monster(200, 370, False, 10, True, DOSBRAZOS_DATA, dosBrazos_sheet, DOSBRAZOS_ANIMATION_STEPS)
#monster_2 = Monster(700, 370, True,  20, False, MDB_DATA, mdb_sheet, MDB_ANIMATION_STEPS)
fabrica_pesado = MonsterFactoryHeavy()
fabrica_rapido = MonsterFactoryAgile()

monster_1 = fabrica_pesado.crear_monstruo()
monster_2 = fabrica_rapido.crear_monstruo()

#Decorar al personaje con la funcionalidad de bloqueo
monster_1_block = MonsterBlock(monster_1)
monster_2_block = MonsterBlock(monster_2)

#Botones del menú
button = Boton('PLAY', ANCHO//2, ALTO//2-100)
button1 = Boton('QUIT', ANCHO//2, ALTO//2+100)
#loop del juego principal
run = True
while run:
    clock.tick(fps)
    #Poner el fondo
    draw_bg()
    if(menu!=True):
        if(monster_1_block.monster.salud>=0 and monster_2_block.monster.salud>=0):
            #Mostrar vida
            draw_health_bar(monster_1_block.monster.salud, 20, 20)
            draw_health_bar(monster_2_block.monster.salud, 630, 20)

            #update
            monster_1_block.update()
            monster_2_block.update()

            #Dibujar monstruos
            monster_1_block.draw(screen)
            monster_2_block.draw(screen)

            #mover jugadores
            monster_1_block.caminar(screen, monster_2_block.monster)
            monster_2_block.caminar(screen, monster_1_block.monster)
        else:
            if(text_y!=115.0):
                text_y += text_velocity
                if (flag):
                    font_size += 1
                font = pygame.font.Font(font_path, font_size)
                game_over_text = font.render("Game Over", True, (255, 0, 0))
                gameover.play()
                # Draw "Game Over" text
                screen.blit(game_over_text, (text_x, text_y))
                flag = not flag
            else:
                screen.blit(game_over_text, (text_x, text_y))
                gameover.stop()
    else:
        button.draw(screen)
        button1.draw(screen)
    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:
            # Ver si el mouse está sobre el botón
            if menu!=False:
                button.mouse_over = button.rect.collidepoint(event.pos)
                button1.mouse_over = button1.rect.collidepoint(event.pos)
                if button.mouse_over == True or button1.mouse_over ==True:
                    sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button.rect.collidepoint(event.pos):
                button.mouse_over=False
                button1.mouse_over=False
                menu = False
            elif button1.rect.collidepoint(event.pos):
                pygame.quit()
    #Actualizar el display
    pygame.display.update()
#Salir del juego
pygame.quit()