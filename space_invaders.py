import pygame
import random
import math
from pygame import mixer
import io


def fuente_byte(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()
        return io.BytesIO(ttf_bytes)


# Inicilizar pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("1200px-Center_of_the_Milky_Way_Galaxy_IV_–_Composite.jpg")

# Musica
mixer.music.load('musica space invaders.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)


# Jugador
img_jugador = pygame.image.load("nave-espacial.png")
jugador_X = 368
jugador_y = 520
jugador_X_cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("astronave.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(30)

# Bala
img_bala = pygame.image.load("bala (1).png")
bala_x = 0
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

# Puntaje
puntaje = 0
fuente_como_bytes = fuente_byte("FreeSansBold.ttf")
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Final del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 40)


def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (70, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Cerra evento
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_X_cambio = -0.4
            if evento.key == pygame.K_RIGHT:
                jugador_X_cambio = 0.4
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_X
                    disparar_bala(bala_x, bala_y)

    # Soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_X_cambio = 0

    # Modificar ubicacion jugador
    jugador_X += jugador_X_cambio

    # Mantener en margen jugador
    if jugador_X <= 0:
        jugador_X = 0
    elif jugador_X >= 734:
        jugador_X = 734

    # Modificar ubicacion enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 400:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener en margen enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 734:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_X, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    # Actualizacion
    pygame.display.update()
