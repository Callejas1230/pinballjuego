import pygame
import random
import unittest
import json

pygame.init()
# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 128, 0)
ANCHO = 650
ALTO = 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Pinball")
fps = pygame.time.Clock()
paleta_ancho = 100
paleta_alto = 10
paleta_vel = 7
bola_radio = 10
bola_vel_x = 4
bola_vel_y = -4
ladrillo_ancho = 60
ladrillo_alto = 20
ladrillos = []
fuente = pygame.font.SysFont("Arial", 30)
# Sonidos 
sonido_colision_paleta = pygame.mixer.Sound("colision_paleta.wav")
sonido_colision_ladrillo = pygame.mixer.Sound("colision_paleta.wav")
sonido_game_over = pygame.mixer.Sound("colision_paleta.wav")
# Funciones de persistencia
def cargar_record():
    """Carga el récord de puntaje desde un archivo JSON."""
    try:
        with open("record.json", "r") as archivo:
            datos = json.load(archivo)
            return datos.get("record", 0)
    except FileNotFoundError:
        return 0
def guardar_record(puntaje):
    """Guarda el récord de puntaje en un archivo JSON."""
    with open("record.json", "w") as archivo:
        json.dump({"record": puntaje}, archivo)
# Clases del juego
class ObjetoJuego:
    """Clase que representa los atributos comunes de los objetos en el juego."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Paleta:
    """Clase que representa la paleta del juego."""
    def __init__(self, x, y, ancho, alto, velocidad):
        self.objeto = ObjetoJuego(x, y)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
    def mover(self, direccion):
        if direccion == 'izquierda' and self.objeto.x > 0:
            self.objeto.x -= self.velocidad
        elif direccion == 'derecha' and self.objeto.x < ANCHO - self.ancho:
            self.objeto.x += self.velocidad
    def dibujar(self, imagen=None):
        if imagen:
            paleta_img = pygame.image.load(imagen).convert_alpha()
            paleta_img = pygame.transform.scale(paleta_img, (self.ancho, self.alto))
            pantalla.blit(paleta_img, (self.objeto.x, self.objeto.y))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.objeto.x, self.objeto.y, self.ancho, self.alto))
class Bola:
    """Clase que representa la bola del juego."""
    def __init__(self, x, y, radio, vel_x, vel_y):
        self.objeto = ObjetoJuego(x, y)
        self.radio = radio
        self.vel_x = vel_x
        self.vel_y = vel_y

    def mover(self):
        self.objeto.x += self.vel_x
        self.objeto.y += self.vel_y

    def dibujar(self):
        pygame.draw.circle(pantalla, BLANCO, (self.objeto.x, self.objeto.y), self.radio)

class Ladrillo:
    """Clase que representa un ladrillo en el juego."""
    def __init__(self, x, y, ancho, alto):
        self.objeto = ObjetoJuego(x, y)
        self.ancho = ancho
        self.alto = alto
        self.rect = pygame.Rect(x, y, ancho, alto)

    def dibujar(self):
        pygame.draw.rect(pantalla, NARANJA, self.rect)
        pygame.draw.rect(pantalla, NEGRO, self.rect, 2)

    def colisiona(self, bola):
        return self.rect.collidepoint(bola.objeto.x, bola.objeto.y)

# Funciones del juego
def mostrar_puntaje(puntaje):
    texto = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

def crear_ladrillos(filas):
    global ladrillos
    ladrillos = []
    for i in range(filas):
        for j in range(10):
            ladrillos.append(Ladrillo(j * (ladrillo_ancho + 5), 30 + i * (ladrillo_alto + 5), ladrillo_ancho, ladrillo_alto))

def mostrar_menu():
    pantalla.fill(NEGRO)
    titulo = fuente.render("Selecciona un nivel", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 4))
    nivel_facil = fuente.render("1. Fácil", True, BLANCO)
    nivel_intermedio = fuente.render("2. Intermedio", True, BLANCO)
    nivel_dificil = fuente.render("3. Difícil", True, BLANCO)
    pantalla.blit(nivel_facil, (ANCHO // 2 - nivel_facil.get_width() // 2, ALTO // 2))
    pantalla.blit(nivel_intermedio, (ANCHO // 2 - nivel_intermedio.get_width() // 2, ALTO // 2 + 40))
    pantalla.blit(nivel_dificil, (ANCHO // 2 - nivel_dificil.get_width() // 2, ALTO // 2 + 80))
    pygame.display.flip()

def seleccionar_nivel():
    seleccionando = True
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 0
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return "facil"
                if evento.key == pygame.K_2:
                    return "intermedio"
                if evento.key == pygame.K_3:
                    return "dificil"

def juego(nivel):
    global paleta_vel, bola_vel_x, bola_vel_y
    filas_ladrillos = 1
    if nivel == "facil":
        bola_vel_x = random.choice([-3, 3])
        bola_vel_y = -3
        paleta_vel = 8
    elif nivel == "intermedio":
        bola_vel_x = random.choice([-4, 4])
        bola_vel_y = -4
        paleta_vel = 7
    elif nivel == "dificil":
        bola_vel_x = random.choice([-5, 5])
        bola_vel_y = -5
        paleta_vel = 6

    paleta = Paleta((ANCHO // 2) - (paleta_ancho // 2), ALTO - paleta_alto - 10, paleta_ancho, paleta_alto, paleta_vel)
    bola = Bola(random.randint(0 + bola_radio, ANCHO - bola_radio), ALTO // 2, bola_radio, bola_vel_x, bola_vel_y)
    puntaje = 0
    record = cargar_record()  # Cargar récord
    jugando = True
    crear_ladrillos(filas_ladrillos)

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            paleta.mover('izquierda')
        if teclas[pygame.K_d]:
            paleta.mover('derecha')

        bola.mover()

        if bola.objeto.x - bola.radio <= 0 or bola.objeto.x + bola.radio >= ANCHO:
            bola.vel_x = -bola.vel_x

        if bola.objeto.y - bola.radio <= 0:
            bola.vel_y = -bola.vel_y

        if paleta.objeto.y <= bola.objeto.y + bola.radio <= paleta.objeto.y + paleta.alto and paleta.objeto.x <= bola.objeto.x <= paleta.objeto.x + paleta.ancho:
            bola.vel_y = -bola.vel_y
            puntaje += 1
            sonido_colision_paleta.play()

        for ladrillo in ladrillos[:]:
            if ladrillo.colisiona(bola):
                ladrillos.remove(ladrillo)
                bola.vel_y = -bola.vel_y
                puntaje += 5
                sonido_colision_ladrillo.play()
                break

        if bola.objeto.y + bola.radio >= ALTO:
            print("¡Game Over!")
            sonido_game_over.play()
            if puntaje > record:
                guardar_record(puntaje)  # Guardar nuevo récord
                print(f"Nuevo récord: {puntaje}")
            jugando = False

        if len(ladrillos) == 0:
            filas_ladrillos += 2
            if filas_ladrillos > 5:
                print("¡Has ganado el juego!")
                if puntaje > record:
                    guardar_record(puntaje)  # Guardar nuevo récord
                    print(f"Nuevo récord: {puntaje}")
                jugando = False
                break
            else:
                crear_ladrillos(filas_ladrillos)
                bola.objeto.x = random.randint(0 + bola_radio, ANCHO - bola_radio)
                bola.objeto.y = ALTO // 2
                bola.vel_y = -abs(bola.vel_y)

        pantalla.fill(NEGRO)
        paleta.dibujar('paleta.png')
        bola.dibujar()
        for ladrillo in ladrillos:
            ladrillo.dibujar()

        mostrar_puntaje(puntaje)
        texto_record = fuente.render(f"Récord: {record}", True, BLANCO)
        pantalla.blit(texto_record, (ANCHO - texto_record.get_width() - 10, 10))

        pygame.display.flip()
        fps.tick(60)
        
if __name__ == "__main__":
    mostrar_menu()
    nivel = seleccionar_nivel()
    if nivel:
        juego(nivel)
