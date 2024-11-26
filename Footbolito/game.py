import pygame
import random as rd
import math
from entities import Jugador, Portero, Balon

ANCHO, ALTO = 800, 700  # Tamaño de la ventana
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Football Automatas Game")

# Imágenes y fuentes
cancha_imagen = pygame.image.load("Images/cancha.png")
cancha_imagen = pygame.transform.scale(cancha_imagen, (ANCHO, 600))
pygame.font.init()
fuente = pygame.font.Font(None, 36)
fuente_pequeña = pygame.font.Font(None, 24)

# Áreas del juego
AREA_GOL_1 = pygame.Rect(0, 219, 20, 169)  # Portería izquierda
AREA_GOL_2 = pygame.Rect(780, 219, 20, 169)  # Portería derecha

# Equipos, porteros y balón
equipo_1 = []
equipo_2 = []
portero_1 = Portero(1, 50, 300, None, aleatorio=True)
portero_2 = Portero(2, ANCHO - 50, 300, None, aleatorio=True)
balon = Balon()

# Contadores
goles = {1: 0, 2: 0}
tiempo_juego = 0  # Tiempo en segundos
reloj = pygame.time.Clock()

# Botones
boton_iniciar = pygame.Rect(50, 655, 200, 30)
boton_pausar = pygame.Rect(300, 655, 200, 30)
boton_reiniciar = pygame.Rect(550, 655, 200, 30)

en_juego = False  # Estado del juego (pausado o activo)
pausa = False


def crear_jugadores_aleatorios(equipo_id, cantidad):
    jugadores = []
    for _ in range(cantidad):
        x = rd.randint(50, ANCHO // 2 - 50) if equipo_id == 1 else rd.randint(ANCHO // 2 + 50, ANCHO - 50)
        y = rd.randint(50, 550)  # Limitar dentro de la cancha
        jugador = Jugador(equipo_id, x, y, None, aleatorio=True)
        jugadores.append(jugador)
    return jugadores


def reiniciar_balon():
    balon.x, balon.y = ANCHO // 2, 300
    balon.vx = rd.uniform(-5, 5)
    balon.vy = rd.choice([-1, 1]) * math.sqrt(balon.speed**2 - balon.vx**2)


# Crear jugadores
equipo_1 += crear_jugadores_aleatorios(1, 10)
equipo_2 += crear_jugadores_aleatorios(2, 10)


def dibujar_boton(ventana, boton, texto, color_fondo, color_texto, hover=False):
    pygame.draw.rect(ventana, color_fondo, boton, border_radius=5)
    pygame.draw.rect(ventana, (0, 0, 0), boton, 2, border_radius=5)  # Borde negro
    if hover:
        pygame.draw.rect(ventana, (255, 255, 255), boton, 2, border_radius=5)  # Borde blanco si está en hover
    texto_render = fuente_pequeña.render(texto, True, color_texto)
    ventana.blit(
        texto_render,
        (boton.x + boton.width // 2 - texto_render.get_width() // 2, boton.y + boton.height // 2 - texto_render.get_height() // 2),
    )


# Áreas ajustadas de la cancha y porterías
LIMITE_SUPERIOR = 50  # Línea superior de la cancha en la imagen
LIMITE_INFERIOR = 650  # Línea inferior de la cancha en la imagen
LIMITE_IZQUIERDO = 40  # Borde izquierdo de la cancha en la imagen
LIMITE_DERECHO = 760  # Borde derecho de la cancha en la imagen

AREA_GOL_1 = pygame.Rect(LIMITE_IZQUIERDO, 270, 20, 110)  # Ajuste para la portería izquierda
AREA_GOL_2 = pygame.Rect(LIMITE_DERECHO - 20, 270, 20, 110)  # Ajuste para la portería derecha


# Función de mover ajustada para que el balón respete los límites de la cancha
def mover_balon(balon):
    balon.x += balon.vx
    balon.y += balon.vy

    # Rebote en los bordes de la cancha
    if balon.x - balon.radius <= LIMITE_IZQUIERDO or balon.x + balon.radius >= LIMITE_DERECHO:
        balon.vx *= -1
    if balon.y - balon.radius <= LIMITE_SUPERIOR or balon.y + balon.radius >= LIMITE_INFERIOR:
        balon.vy *= -1


# Actualización en el ciclo principal
def main():
    global tiempo_juego, en_juego, pausa

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_iniciar.collidepoint(event.pos):
                    en_juego = True
                    pausa = False
                elif boton_pausar.collidepoint(event.pos):
                    pausa = not pausa
                elif boton_reiniciar.collidepoint(event.pos):
                    en_juego = False
                    pausa = False
                    reiniciar_balon()
                    goles[1], goles[2] = 0, 0
                    tiempo_juego = 0

        # Dibujar elementos visuales
        ventana.fill((128, 128, 128))  # Fondo gris oscuro
        pygame.draw.rect(ventana, (30, 30, 30), (0, 0, ANCHO, 50))  # Cabecera superior
        ventana.blit(cancha_imagen, (0, 50))  # Cancha debajo de la cabecera

        # Mostrar información de equipos y marcador
        pygame.draw.rect(ventana, (70, 130, 180), (0, 0, 200, 50))  # Fondo Equipo A
        pygame.draw.rect(ventana, (240, 240, 240), (600, 0, 200, 50))  # Fondo Equipo B

        texto_equipo_1 = fuente_pequeña.render("EQUIPO A", True, (255, 255, 255))
        texto_equipo_2 = fuente_pequeña.render("EQUIPO B", True, (0, 0, 0))
        texto_goles_1 = fuente.render(str(goles[1]), True, (255, 255, 255))
        texto_goles_2 = fuente.render(str(goles[2]), True, (0, 0, 0))
        texto_tiempo = fuente.render(f"{int(tiempo_juego // 60):02}:{int(tiempo_juego % 60):02}", True, (200, 200, 0))

        ventana.blit(texto_equipo_1, (20, 10))
        ventana.blit(texto_equipo_2, (620, 10))
        ventana.blit(texto_goles_1, (150, 10))
        ventana.blit(texto_goles_2, (750, 10))
        ventana.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, 10))

        # Dibujar botones con hover
        dibujar_boton(ventana, boton_iniciar, "INICIAR JUEGO", (0, 102, 204) if not boton_iniciar.collidepoint(mouse_pos) else (51, 153, 255), (255, 255, 255), boton_iniciar.collidepoint(mouse_pos))
        dibujar_boton(ventana, boton_pausar, "PAUSAR", (0, 204, 0) if not boton_pausar.collidepoint(mouse_pos) else (51, 255, 51), (0, 0, 0), boton_pausar.collidepoint(mouse_pos))
        dibujar_boton(ventana, boton_reiniciar, "REINICIAR", (204, 0, 0) if not boton_reiniciar.collidepoint(mouse_pos) else (255, 51, 51), (255, 255, 255), boton_reiniciar.collidepoint(mouse_pos))

        if en_juego and not pausa:
            tiempo_juego += reloj.get_time() / 1000

            for jugador in equipo_1 + equipo_2 + [portero_1, portero_2]:
                jugador.mover_aleatorio()
                jugador.dibujar(ventana)
                if balon.colisiona_con(jugador):
                    balon.golpear(jugador)

            # Actualización del movimiento del balón con límites ajustados
            mover_balon(balon)
            balon.dibujar(ventana)

            # Detección de goles con áreas ajustadas
            if AREA_GOL_1.collidepoint(balon.x, balon.y):
                goles[2] += 1
                reiniciar_balon()
            elif AREA_GOL_2.collidepoint(balon.x, balon.y):
                goles[1] += 1
                reiniciar_balon()

        elif pausa or not en_juego:
            texto_pausa = fuente.render("Pausado" if pausa else "Presione 'INICIAR JUEGO'", True, (255, 255, 255))
            ventana.blit(texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, 300))

        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    main()
