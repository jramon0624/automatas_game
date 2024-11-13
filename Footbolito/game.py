#Librerias
import pygame
from entities import Jugador, Portero, Balon
from utils import jugador_mas_cercano

ANCHO, ALTO = 800, 600
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Minifootball")

# Imagen de la cancha
cancha_imagen = pygame.image.load("Images/cancha.png")
cancha_imagen = pygame.transform.scale(cancha_imagen, (ANCHO, ALTO))

# Áreas de gol para cada portería
AREA_GOL_1 = pygame.Rect(0, ALTO // 4, 20, ALTO // 2)  # izquierda
AREA_GOL_2 = pygame.Rect(ANCHO - 20, ALTO // 4, 20, ALTO // 2)  # derecha

# Mapeo de teclas
controles_jugador_1 = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izquierda': pygame.K_a, 'derecha': pygame.K_d}
controles_jugador_2 = {'arriba': pygame.K_KP_8, 'abajo': pygame.K_KP_2, 'izquierda': pygame.K_KP_4, 'derecha': pygame.K_KP_6}

# Creación de jugadores y balón
equipo_1 = [Jugador(1, 100, 100, controles_jugador_1)]
equipo_2 = [Jugador(2, 700, 100, controles_jugador_2)]
portero_1 = Portero(1, 50, ALTO // 2, controles_jugador_1)
portero_2 = Portero(2, ANCHO - 50, ALTO // 2, controles_jugador_2)
balon = Balon()

# Contador de goles y de tiempo
goles = {1: 0, 2: 0}
reloj = pygame.time.Clock()

# marcador y tiempo
pygame.font.init()
fuente = pygame.font.Font(None, 36)  # Tamaño de la fuente
tiempo_juego = 0  # tiempo en segundos


#Comportamineto de juego
def reiniciar_balon():
    balon.x, balon.y = ANCHO // 2, ALTO // 2
    balon.vx, balon.vy = 0, 0


def main():
    global tiempo_juego  
    en_juego = True
    while en_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_juego = False

        teclas = pygame.key.get_pressed()


        ventana.blit(cancha_imagen, (0, 0))

        # Movimiento de jugadores
        for jugador in equipo_1 + equipo_2 + [portero_1, portero_2]:
            jugador.mover(teclas)
            jugador.dibujar(ventana)
            
            # Colisión entre jugador y balón
            if balon.colisiona_con(jugador):
                balon.golpear(jugador)

        # Movimiento del balón
        balon.mover()
        balon.dibujar(ventana)

        # Detección de gol
        if AREA_GOL_1.collidepoint(balon.x, balon.y):
            goles[2] += 1  # anota equipo 2
            print(f"Gol del Equipo 2! Marcador: Equipo 1 - {goles[1]}, Equipo 2 - {goles[2]}")
            reiniciar_balon()

        elif AREA_GOL_2.collidepoint(balon.x, balon.y):
            goles[1] += 1  # anota equipo 1
            print(f"Gol del Equipo 1! Marcador: Equipo 1 - {goles[1]}, Equipo 2 - {goles[2]}")
            reiniciar_balon()

        # Detección de cambio de jugador (Q y 7)
        if teclas[pygame.K_q]: 
            jugador_activo = jugador_mas_cercano(equipo_1, balon)
            jugador_activo.active = True
        if teclas[pygame.K_7]:
            jugador_activo = jugador_mas_cercano(equipo_2, balon)
            jugador_activo.active = True

        # Actualizar el tiempo de juego
        tiempo_juego += reloj.get_time() / 1000  # milisegundos a segundos
        minutos = int(tiempo_juego // 60)
        segundos = int(tiempo_juego % 60)

        # Texto en pantalla
        texto_marcador = fuente.render(f"Equipo 1: {goles[1]}  Equipo 2: {goles[2]}", True, (255, 255, 255))
        texto_tiempo = fuente.render(f"Tiempo: {minutos:02}:{segundos:02}", True, (255, 255, 255))

        # Mostrar marcador y tiempo en la pantalla
        ventana.blit(texto_marcador, (ANCHO // 2 - texto_marcador.get_width() // 2, 10))
        ventana.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, 40))

        # Actualización de pantalla
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
