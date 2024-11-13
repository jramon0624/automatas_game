
import pygame
import math
import random

ANCHO, ALTO = 800, 600
AREA_PORTERIA_1 = pygame.Rect(0, ALTO // 4, 50, ALTO // 2)
AREA_PORTERIA_2 = pygame.Rect(ANCHO - 50, ALTO // 4, 50, ALTO // 2)

class Jugador:
    def __init__(self, equipo, x, y, controls):
        self.equipo = equipo
        self.x, self.y = x, y
        self.controls = controls
        self.speed = 5
        self.radius = 10
        self.active = False

    def mover(self, teclas):
        if teclas[self.controls['arriba']]: self.y -= self.speed
        if teclas[self.controls['abajo']]: self.y += self.speed
        if teclas[self.controls['izquierda']]: self.x -= self.speed
        if teclas[self.controls['derecha']]: self.x += self.speed

    def dibujar(self, ventana):
        color = (255, 0, 0) if self.equipo == 1 else (0, 0, 255)
        pygame.draw.circle(ventana, color, (int(self.x), int(self.y)), self.radius)

    def distancia_a(self, balon):
        return math.hypot(self.x - balon.x, self.y - balon.y)

class Portero(Jugador):
    def mover(self, teclas):
        super().mover(teclas)
        area = AREA_PORTERIA_1 if self.equipo == 1 else AREA_PORTERIA_2
        if not area.collidepoint(self.x, self.y):
            self.x, self.y = max(area.left, min(area.right, self.x)), max(area.top, min(area.bottom, self.y))

class Balon:
    def __init__(self):
        self.x, self.y = ANCHO // 2, ALTO // 2
        self.vx, self.vy = 0, 0
        self.radius = 8
        self.speed = 5

    def mover(self):
        self.x += self.vx
        self.y += self.vy
        # Rebotar en los bordes
        if self.x <= 0 or self.x >= ANCHO:
            self.vx *= -1
        if self.y <= 0 or self.y >= ALTO:
            self.vy *= -1

    def golpear(self, jugador):
        # Con esto calculamos la dirección del balón dependiendo de la posición del jugador
        dx = self.x - jugador.x
        dy = self.y - jugador.y
        distancia = math.hypot(dx, dy)
        
        # para acelerar el balon
        self.vx = (dx / distancia) * self.speed
        self.vy = (dy / distancia) * self.speed

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def colisiona_con(self, jugador):
        distancia = math.hypot(self.x - jugador.x, self.y - jugador.y)
        return distancia < self.radius + jugador.radius
