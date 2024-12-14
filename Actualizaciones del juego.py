import pygame
import random
import math
from pygame import mixer
import io

def fuente_byte(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()
        return io.BytesIO(ttf_bytes)

# Inicializar pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("1200px-Center_of_the_Milky_Way_Galaxy_IV_–_Composite.jpg")

# Música
mixer.music.load('musica space invaders.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Clase Jugador
class Jugador:
    def __init__(self, x, y):
        self.imagen = pygame.image.load("nave-espacial.png")
        self.x = x
        self.y = y
        self.cambio = 0

    def mover(self):
        self.x += self.cambio
        self.x = max(0, min(self.x, 734))  # Mantener en margen

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase Enemigo
class Enemigo:
    def __init__(self):
        self.imagen = pygame.image.load("astronave.png")
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 200)
        self.cambio_x = 0.3
        self.cambio_y = 30

    def mover(self):
        self.x += self.cambio_x
        if self.x <= 0 or self.x >= 734:
            self.cambio_x *= -1
            self.y += self.cambio_y

    def dibujar(self):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase Bala
class Bala:
    def __init__(self):
        self.imagen = pygame.image.load("bala (1).png")
        self.x = 0
        self.y = 520
        self.cambio_y = 2
        self.visible = False

    def disparar(self, x, y):
        self.visible = True
        self.x = x + 16
        self.y = y + 10

    def mover(self):
        if self.visible:
            self.y -= self.cambio_y
            if self.y <= -64:
                self.visible = False

    def dibujar(self):
        if self.visible:
            pantalla.blit(self.imagen, (self.x, self.y))

# Funciones del juego
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (70, 200))

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))
    return distancia < 27

# Inicialización de variables
puntaje = 0
fuente_como_bytes = fuente_byte("FreeSansBold.ttf")
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10
fuente_final = pygame.font.Font(fuente_como_bytes, 40)

# Crear instancias
jugador = Jugador(368, 520)
enemigos = [Enemigo() for _ in range(8)]
bala = Bala()

# Loop del juego
se_ejecuta = True
while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador.cambio = -0.4
            if evento.key == pygame.K_RIGHT:
                jugador.cambio = 0.4
            if evento.key == pygame.K_SPACE and not bala.visible:
                mixer.Sound('disparo.mp3').play()
                bala.disparar(jugador.x, jugador.y)
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador.cambio = 0

    # Mover jugador
    jugador.mover()

    # Mover enemigos y verificar colisiones
    for enemigo in enemigos:
        enemigo.mover()
        colision = hay_colision(enemigo.x, enemigo.y, bala.x, bala.y)
        if colision:
            mixer.Sound('Golpe.mp3').play()
            bala.visible = False
            bala.y = 520  # Resetear la bala
            puntaje += 1
            enemigo.x = random.randint(0, 736)
            enemigo.y = random.randint(50, 200)

        enemigo.dibujar()

        if enemigo.y > 400:
            for e in enemigos:
                e.y = 1000  # Mover todos los enemigos fuera de la pantalla
            texto_final()
            break

    # Mover y dibujar bala
    bala.mover()
    if bala.visible:
        bala.dibujar()

    # Dibujar jugador
    jugador.dibujar()

    # Mostrar puntaje
    mostrar_puntaje(texto_x, texto_y)

    # Actualización de pantalla
    pygame.display.update()
