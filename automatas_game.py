import pygame
import random as rd
import math
from objects.entities import Jugador, Portero, Balon

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 650

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 120, 0)
BLUE = (0, 120, 255)
GREEN = (0, 128, 0)
RED = (200, 0, 0)
DARK_BLUE = (0, 51, 102)
GRAY = (65, 65, 65)
YELLOW = (255, 255, 0)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football Automatas Game")

# Fuentes
font_large = pygame.font.Font(None, 50)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 30)

# Cargar la imagen de la cancha
cancha_imagen = pygame.image.load("rsc/cancha.png")
cancha_imagen = pygame.transform.scale(cancha_imagen, (WIDTH, HEIGHT - 100))

# Áreas de gol
AREA_GOL_1 = pygame.Rect(0, 285, 30, 103)  # Portería izquierda
AREA_GOL_2 = pygame.Rect(768, 285, 30, 103)  # Portería derecha

# Crear equipos, porteros y balón
equipo_1 = [Jugador(1, rd.randint(50, 350), rd.randint(100, 500), None, aleatorio=True) for _ in range(10)]
equipo_2 = [Jugador(2, rd.randint(450, 750), rd.randint(100, 500), None, aleatorio=True) for _ in range(10)]
portero_1 = Portero(1, 50, HEIGHT // 2, None, aleatorio=True)
portero_1.color = YELLOW
portero_2 = Portero(2, WIDTH - 50, HEIGHT // 2, None, aleatorio=True)
portero_2.color = BLACK
balon = Balon()

# Contadores y estado del juego
goles = {1: 0, 2: 0}
tiempo_juego = 0
en_juego = False
pausa = False
juego_terminado = False

# Botones
buttons = [
    {"label": "INICIAR JUEGO", "color": GREEN, "rect": pygame.Rect(0, HEIGHT - 50, WIDTH // 3, 50)},
    {"label": "PAUSA", "color": DARK_BLUE, "rect": pygame.Rect(WIDTH // 3, HEIGHT - 50, WIDTH // 3, 50)},
    {"label": "REINICIAR", "color": RED, "rect": pygame.Rect(2 * (WIDTH // 3), HEIGHT - 50, WIDTH // 3, 50)},
]

reloj = pygame.time.Clock()

def reiniciar_balon():
    balon.x, balon.y = 30 + 739//2, 78 + 516// 2
    balon.vx = rd.uniform(-5,5)
    balon.vy = rd.choice([-1,1]) * math.sqrt(balon.speed**2 - balon.vx**2)

def dibujar_circulos_tiempo(x, y, minutos_transcurridos):
    """Dibuja los círculos de estado del tiempo."""
    for i in range(5):
        color = WHITE if i < minutos_transcurridos else GRAY
        pygame.draw.circle(ventana, color, (x + i * 30, y), 8)

def mostrar_ganador():
    """Muestra un mensaje indicando el ganador."""
    global juego_terminado
    ventana.fill(WHITE)
    resultado = "EMPATE"
    if goles[1] > goles[2]:
        resultado = "GANADOR: EQUIPO A"
    elif goles[2] > goles[1]:
        resultado = "GANADOR: EQUIPO B"
    
    mensaje = font_large.render(resultado, True, BLACK)
    ventana.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, HEIGHT // 2 - mensaje.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5000)
    juego_terminado = True

def main():
    global tiempo_juego, en_juego, pausa, juego_terminado
    
    while True:
        ventana.fill(WHITE)

        # Manejar eventos
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]["rect"].collidepoint(mouse_pos) and not juego_terminado:
                    en_juego = True
                    pausa = False
                elif buttons[1]["rect"].collidepoint(mouse_pos) and not juego_terminado:
                    pausa = not pausa
                elif buttons[2]["rect"].collidepoint(mouse_pos):
                    en_juego = False
                    pausa = False
                    juego_terminado = False
                    reiniciar_balon()
                    goles[1], goles[2] = 0, 0
                    tiempo_juego = 0
        
        if juego_terminado:
            mostrar_ganador()
            continue

        # Dibujar cancha
        ventana.blit(cancha_imagen, (0, 60))

        # Dibujar marcador y nombres de equipos
        pygame.draw.rect(ventana, ORANGE, (0, 0, WIDTH // 3, 65))  # Fondo Equipo A
        pygame.draw.rect(ventana, BLUE, (2 * WIDTH // 3, 0, WIDTH // 3, 65))  # Fondo Equipo B
        pygame.draw.rect(ventana, BLACK, (WIDTH // 3, 0, WIDTH // 3, 65))  # Fondo marcador

        # Textos
        equipo_a_text = font_small.render("EQUIPO A", True, WHITE)
        equipo_b_text = font_small.render("EQUIPO B", True, WHITE)
        marcador_text1 = font_large.render(f"{goles[1]}", True, WHITE)
        marcador_text2 = font_large.render(f"{goles[2]}", True, WHITE)
        tiempo_text = font_medium.render(f"{int(tiempo_juego // 60):02}:{int(tiempo_juego % 60):02}", True, WHITE)

        # Posicionar textos
        ventana.blit(equipo_a_text, (20, 23))
        ventana.blit(equipo_b_text, (WIDTH - 120, 23))
        ventana.blit(marcador_text1, (WIDTH // 4 - marcador_text1.get_width() // 2, 15))
        ventana.blit(marcador_text2, (WIDTH // 1.35 - marcador_text2.get_width() // 2, 15))
        ventana.blit(tiempo_text, (WIDTH // 2 - tiempo_text.get_width() // 2, 10))

        # Dibujar círculos de tiempo
        minutos_transcurridos = int(tiempo_juego // 60)
        dibujar_circulos_tiempo(WIDTH // 2 - 61, 46, minutos_transcurridos)

        # Dibujar botones
        for button in buttons:
            pygame.draw.rect(ventana, button["color"], button["rect"])
            label = font_small.render(button["label"], True, WHITE)
            ventana.blit(label, (button["rect"].x + (button["rect"].width - label.get_width()) // 2,
                                button["rect"].y + (button["rect"].height - label.get_height()) // 2))

        if en_juego and not pausa:
            tiempo_juego += reloj.get_time() / 1000
            if tiempo_juego >= 300:  # Fin del juego a los 5 minutos
                en_juego = False
                mostrar_ganador()

            for jugador in equipo_1 + equipo_2 + [portero_1, portero_2]:
                jugador.mover_aleatorio()
                jugador.dibujar(ventana)
                if balon.colisiona_con(jugador):
                    balon.golpear(jugador)

            # Movimiento y dibujo del balón
            balon.mover()
            balon.dibujar(ventana)

            # Detección de gol
            if AREA_GOL_1.collidepoint(balon.x, balon.y):
                goles[2] += 1  # Gol para el equipo 2
                reiniciar_balon()
            elif AREA_GOL_2.collidepoint(balon.x, balon.y):
                goles[1] += 1  # Gol para el equipo 1
                reiniciar_balon()
        
        ############### PRUEBAS ###############

        # pygame.draw.rect(ventana,BLACK,(30,250,42,172),1) # Area portero
        # pygame.draw.rect(ventana,RED,(727,250,42,172),1) # Area portero
        
        # pygame.draw.rect(ventana,BLACK,(0,285,30,103),1) # Area Gol
        # pygame.draw.rect(ventana,RED,(768,285,30,103),1) # Area Gol
        
        # pygame.draw.rect(ventana,ORANGE,(30,78,739,516),1) # Area chancha

        #######################################

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
