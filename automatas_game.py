import pygame
import random as rd
import math
from objects.entities import Jugador, Portero, Balon

ANCHO, ALTO = 800, 600
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Football Automatas Game")


cancha_imagen = pygame.image.load("rsc/football_bg.png")
cancha_imagen = pygame.transform.scale(cancha_imagen, (ANCHO, ALTO))


AREA_GOL_1 = pygame.Rect(0, 219, 20, 169)  # Portería izquierda
AREA_GOL_2 = pygame.Rect(780, 219, 20, 169)  # Portería derecha


equipo_1 = []
equipo_2 = []
portero_1 = Portero(1, 50, ALTO // 2, None, aleatorio=True)
portero_1.color = (255,255,0)
portero_2 = Portero(2, ANCHO - 50, ALTO // 2, None, aleatorio=True)
portero_2.color = (0,0,0)
balon = Balon()


goles = {1: 0, 2: 0}
reloj = pygame.time.Clock()


pygame.font.init()
fuente = pygame.font.Font(None, 36)  # Tamaño de la fuente


tiempo_juego = 0  # tiempo en segundos


def crear_jugadores_aleatorios(equipo_id, cantidad):
    jugadores = []
    for _ in range(cantidad):
        # Posición aleatoria en su mitad del campo
        x = rd.randint(50, ANCHO // 2 - 50) if equipo_id == 1 else rd.randint(ANCHO // 2 + 50, ANCHO - 50)
        y = rd.randint(50, ALTO - 50)
        jugador = Jugador(equipo_id, x, y, None, aleatorio=True)  # Se agrega parámetro 'aleatorio' para movimiento aleatorio
        jugadores.append(jugador)
    return jugadores


equipo_1 += crear_jugadores_aleatorios(1, 10)  # Agregar 6 jugadores al equipo 1
equipo_2 += crear_jugadores_aleatorios(2, 10)  # Agregar 6 jugadores al equipo 2


def reiniciar_balon():
    balon.x, balon.y = ANCHO // 2, ALTO // 2
    balon.vx = rd.uniform(-5,5)
    balon.vy = rd.choice([-1,1]) * math.sqrt(balon.speed**2 - balon.vx**2)


def main():
    global tiempo_juego
    en_juego = True
    while en_juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_juego = False

        teclas = pygame.key.get_pressed()


        ventana.blit(cancha_imagen, (0, 0))
        ############### PRUEBAS ###############

        pygame.draw.rect(ventana,(0,0,0),(23,156,129,293),1)
        pygame.draw.rect(ventana,(255,10,0),(647,156,129,293),1)
        
        pygame.draw.rect(ventana,(0,0,0),(0,219,20,169),1)
        pygame.draw.rect(ventana,(255,10,0),(780,219,20,169),1)
        
        pygame.draw.rect(ventana,(255,0,200),(20,17,760,566),1)

        #######################################


        for jugador in equipo_1 + equipo_2 + [portero_1, portero_2]:
            if jugador.aleatorio:
                jugador.mover_aleatorio()  # Llamada al movimiento aleatorio
            else:
                jugador.mover(teclas)  # Movimiento controlado solo para el jugador activo
            jugador.dibujar(ventana)
            
            # Colisión entre jugador y balón
            if balon.colisiona_con(jugador):
                balon.golpear(jugador)

        # Movimiento y dibujo del balón
        balon.mover()
        balon.dibujar(ventana)

        # Detección de gol
        if AREA_GOL_1.collidepoint(balon.x, balon.y):
            goles[2] += 1  # Gol para el equipo 2
            print(f"Gol del Equipo 2! Marcador: Equipo 1 - {goles[1]}, Equipo 2 - {goles[2]}")
            reiniciar_balon()

        elif AREA_GOL_2.collidepoint(balon.x, balon.y):
            goles[1] += 1  # Gol para el equipo 1
            print(f"Gol del Equipo 1! Marcador: Equipo 1 - {goles[1]}, Equipo 2 - {goles[2]}")
            reiniciar_balon()


        tiempo_juego += reloj.get_time() / 1000  # convertimos de milisegundos a segundos
        minutos = int(tiempo_juego // 60)
        segundos = int(tiempo_juego % 60)


        texto_marcador = fuente.render(f"Equipo 1: {goles[1]}  Equipo 2: {goles[2]}", True, (255, 255, 255))
        texto_tiempo = fuente.render(f"Tiempo: {minutos:02}:{segundos:02}", True, (255, 255, 255))


        ventana.blit(texto_marcador, (ANCHO // 2 - texto_marcador.get_width() // 2, 10))
        ventana.blit(texto_tiempo, (ANCHO // 2 - texto_tiempo.get_width() // 2, 40))


        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
