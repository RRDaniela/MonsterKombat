from settings import *
from colors import *

text_start = font.render('START', True, DORADO)
text_quit = font.render('QUIT', True, DORADO)

def get_image(sheet, ancho, alto, incrementar, color, frame):
    image = pygame.Surface((ancho, alto)).convert_alpha()
    image.blit(sheet, (0,0), (frame*ancho,frame*alto, ancho, alto))
    image = pygame.transform.scale(image, (ancho*incrementar, alto*incrementar))
    image.set_colorkey(color)
    return image

#Botón 1
Botón1= get_image(button_sheet, 70, 42, 6, NEGRO, 0)
Boton_rect = Botón1.get_rect()
Boton_rect.x = ANCHO/2-100
Boton_rect.y = ALTO/2-100