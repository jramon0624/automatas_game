import pygame
import random as rd
import math
from objects.entities import Jugador, Portero, Balon
from cons import *

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego autómata de Fútbol")

# Cargar sonidos pygame.mixer.init() 
# sonido_gol = pygame.mixer.Sound("rsc/gol.wav") 
# sonido_pausa = pygame.mixer.Sound("rsc/pausa.wav") 
# sonido_reanudar = pygame.mixer.Sound("rsc/reanudar.wav")

# Fuentes
fuente_grande = pygame.font.Font(None, 50)
fuente_media = pygame.font.Font(None, 40)
fuente_pequena = pygame.font.Font(None, 30)

# Cargar la imagen de la cancha
imagen_cancha = pygame.image.load("rsc/cancha.png")
imagen_cancha = pygame.transform.scale(imagen_cancha, (ANCHO_CANCHA, ALTO_CANCHA))

# Crear equipos, porteros y balón
equipo_1 = [Jugador(1, rd.uniform(50*ANCHO_CANCHA/800, 350*ANCHO_CANCHA/800), rd.uniform(100*ALTO_CANCHA/550, 500*ALTO_CANCHA/500), None, aleatorio=True) for _ in range(10)]
equipo_2 = [Jugador(2, rd.uniform(450*ANCHO_CANCHA/800, 750*ANCHO_CANCHA/800), rd.uniform(100*ALTO_CANCHA/550, 500*ALTO_CANCHA/500), None, aleatorio=True) for _ in range(10)]
portero_1 = Portero(1, 50*ANCHO_CANCHA/800, (ALTO // 2)*ALTO_CANCHA/550, None, aleatorio=True)
portero_1.color = AMARILLO
portero_2 = Portero(2, (ANCHO - 50)*ANCHO_CANCHA/800, (ALTO // 2)*ALTO_CANCHA/550, None, aleatorio=True)
portero_2.color = NEGRO
balon = Balon()

# Contadores y estado del juego
goles = {1: 0, 2: 0}
tiempo_juego = 0
en_juego = False
pausa = False
juego_terminado = False

# Botones
botones = [
    {"label": "INICIAR JUEGO", "color": VERDE, "rect": pygame.Rect(0, ALTO - 50, ANCHO // 3, 50)},
    {"label": "PAUSA", "color": AZUL_OSCURO, "rect": pygame.Rect(ANCHO // 3, ALTO - 50, ANCHO // 3, 50)},
    {"label": "REINICIAR", "color": ROJO, "rect": pygame.Rect(2 * (ANCHO // 3), ALTO - 50, ANCHO // 3, 50)},
]

reloj = pygame.time.Clock()

def reiniciar_balon():
    balon.x, balon.y = (AREA_CANCHA.right - AREA_CANCHA.left)/2 + AREA_CANCHA.left, (AREA_CANCHA.bottom - AREA_CANCHA.top)/2 + AREA_CANCHA.top
    balon.vx = rd.uniform(-5,5)
    balon.vy = rd.choice([-1,1]) * math.sqrt(balon.speed**2 - balon.vx**2)

def dibujar_circulos_tiempo(x, y, minutos_transcurridos):
    """Dibuja los círculos de estado del tiempo."""
    for i in range(5):
        if i < minutos_transcurridos:
            color = BLANCO
            pygame.draw.circle(pantalla, color, (x + i * 30, y), 9)
        else:
            fondo = NEGRO
            contorno = BLANCO
            pygame.draw.circle(pantalla, fondo, (x + i * 30, y), 9)
            pygame.draw.circle(pantalla, contorno, (x + i * 30, y), 9, 3)


def mostrar_ganador():
    """Muestra un mensaje indicando el ganador."""
    global juego_terminado
    pantalla.fill(BLANCO)
    resultado = "EMPATE"
    if goles[1] > goles[2]:
        resultado = "GANADOR: EQUIPO A"
    elif goles[2] > goles[1]:
        resultado = "GANADOR: EQUIPO B"
    
    mensaje = fuente_grande.render(resultado, True, NEGRO)
    pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2 - mensaje.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5000)
    juego_terminado = True

def principal():
    global tiempo_juego, en_juego, pausa, juego_terminado

    while True:
        pantalla.fill(BLANCO)

        # Manejar eventos
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botones[0]["rect"].collidepoint(mouse_pos) and not juego_terminado:
                    en_juego = True
                    pausa = False
                elif botones[1]["rect"].collidepoint(mouse_pos) and not juego_terminado:
                    pausa = not pausa
                    if pausa:
                        botones[1]["label"] = "REANUDAR"
                    else:
                        botones[1]["label"] = "PAUSA"
                elif botones[2]["rect"].collidepoint(mouse_pos):
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
        pantalla.blit(imagen_cancha, PUNTO_CANCHA)

        # Dibujar marcador y nombres de equipos
        pygame.draw.rect(pantalla, NARANJA, (0, 0, ANCHO // 3, 65))  # Fondo Equipo A
        pygame.draw.rect(pantalla, AZUL, (2 * ANCHO // 3, 0, ANCHO // 3, 65))  # Fondo Equipo B
        pygame.draw.rect(pantalla, NEGRO, (ANCHO // 3, 0, ANCHO // 3, 65))  # Fondo marcador

        ancho_del_cuadrado, alto_del_cuadrado = 50, 50  
        
        # Dibujar el fondo blanco
        # Marcador A
        pygame.draw.rect(pantalla, BLANCO, (ANCHO // 4.5, 7, ancho_del_cuadrado, alto_del_cuadrado))
        # Marcador B
        pygame.draw.rect(pantalla, BLANCO, (641, 7, ancho_del_cuadrado, alto_del_cuadrado))
        
        # Dibujar el contorno negro
        # Marcador A
        pygame.draw.rect(pantalla, NEGRO, (ANCHO // 4.5, 7, ancho_del_cuadrado, alto_del_cuadrado), 2)  # El último parámetro es el grosor del contorno
        # Marcador A
        pygame.draw.rect(pantalla, NEGRO, (641, 7, ancho_del_cuadrado, alto_del_cuadrado), 2)  # El último parámetro es el grosor del contorno
        
        # Textos
        equipo_a_text = fuente_pequena.render("EQUIPO A", True, BLANCO)
        equipo_b_text = fuente_pequena.render("EQUIPO B", True, BLANCO)
        marcador_text1 = fuente_grande.render(f"{goles[1]}", True, NEGRO)
        marcador_text2 = fuente_grande.render(f"{goles[2]}", True, NEGRO)
        tiempo_text = fuente_media.render(f"{int(tiempo_juego // 60):02}:{int(tiempo_juego % 60):02}", True, BLANCO)

        # Posicionar textos
        pantalla.blit(equipo_a_text, (20, 23))
        pantalla.blit(equipo_b_text, (ANCHO - 120, 23))
        pantalla.blit(marcador_text1, (ANCHO // 4 - marcador_text1.get_width() // 2, 15))
        pantalla.blit(marcador_text2, (ANCHO // 1.35 - marcador_text2.get_width() // 2, 15))
        pantalla.blit(tiempo_text, (ANCHO // 2 - tiempo_text.get_width() // 2, 10))

        # Dibujar círculos de tiempo
        minutos_transcurridos = int(tiempo_juego // 60)
        dibujar_circulos_tiempo(ANCHO // 2 - 61, 46, minutos_transcurridos)

        # Dibujar botones
        for boton in botones:
            pygame.draw.rect(pantalla, boton["color"], boton["rect"])
            label = fuente_pequena.render(boton["label"], True, BLANCO)
            pantalla.blit(label, (boton["rect"].x + (boton["rect"].width - label.get_width()) // 2,
                                boton["rect"].y + (boton["rect"].height - label.get_height()) // 2))

        if en_juego and not pausa:
            tiempo_juego += reloj.get_time() / 1000
            if tiempo_juego >= 300:  # Fin del juego a los 5 minutos
                en_juego = False
                mostrar_ganador()

            for jugador in equipo_1 + equipo_2 + [portero_1, portero_2]:
                jugador.mover_aleatorio()
                jugador.dibujar(pantalla)
                if balon.colisiona_con(jugador):
                    balon.golpear(jugador)

            # Movimiento y dibujo del balón
            balon.mover()
            balon.dibujar(pantalla)
            
            # Detección de gol
            if AREA_GOL_1.collidepoint(balon.x, balon.y):
                goles[2] += 1  # Gol para el equipo 2
                reiniciar_balon()
            elif AREA_GOL_2.collidepoint(balon.x, balon.y):
                goles[1] += 1  # Gol para el equipo 1
                reiniciar_balon()
        
        ############### PRUEBAS ###############
        
        # Áreas de diseño de porterías
        pygame.draw.rect(pantalla, (0, 0, 0), (0*ANCHO_CANCHA/800 + PUNTO_CANCHA[0], 225*ALTO_CANCHA/550 + PUNTO_CANCHA[1], 30*ANCHO_CANCHA/800, 103*ALTO_CANCHA/550), width=2)
        pygame.draw.rect(pantalla, (0, 0, 0), (768*ANCHO_CANCHA/800 + PUNTO_CANCHA[0], 225*ALTO_CANCHA/550 + PUNTO_CANCHA[1], 30*ANCHO_CANCHA/800, 103*ALTO_CANCHA/550), width=2)
        
        # Areas para el movimientos de porteros
        pygame.draw.rect(pantalla,NEGRO,(30*ANCHO_CANCHA/800 + PUNTO_CANCHA[0], 190*ALTO_CANCHA/550 + PUNTO_CANCHA[1], 42*ANCHO_CANCHA/800, 172*ALTO_CANCHA/550),1) # Area portero 1
        pygame.draw.rect(pantalla,ROJO,(727*ANCHO_CANCHA/800 + PUNTO_CANCHA[0], 190*ALTO_CANCHA/550 + PUNTO_CANCHA[1], 42*ANCHO_CANCHA/800, 172*ALTO_CANCHA/550),1) # Area portero 2
        
        # Area de juego para los equipos
        # pygame.draw.rect(pantalla, (218, 98, 14),(32, 81, 600, 560) , width=4)
        # pygame.draw.rect(pantalla, (28, 119, 222),(270, 81, 596, 560) , width=4)
        
        # Area total de la cancha para la colision de la pelota
        pygame.draw.rect(pantalla, NARANJA,(30*ANCHO_CANCHA/800 + PUNTO_CANCHA[0], 18*ALTO_CANCHA/550 + PUNTO_CANCHA[1], 739*ANCHO_CANCHA/800, 516*ALTO_CANCHA/550) , width=2)

        #######################################

        if pausa: 
            pausa_text = fuente_grande.render("Juego pausado", True, BLANCO) 
            pantalla.blit(pausa_text, (ANCHO // 2 - pausa_text.get_width() // 2, ALTO // 2 - pausa_text.get_height() // 2))
            
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    principal()
