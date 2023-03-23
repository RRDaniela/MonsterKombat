from settings import *
from colors import *

text_start = font_deutsch.render('START', True, DORADO)
text_quit = font_deutsch.render('QUIT', True, DORADO)

def get_image(sheet, ancho, alto, incrementar, color, frame):
    image = pygame.Surface((ancho, alto)).convert_alpha()
    image.blit(sheet, (0,0), (frame*ancho,frame*alto, ancho, alto))
    image = pygame.transform.scale(image, (ancho*incrementar, alto*incrementar))
    image.set_colorkey(color)
    return image