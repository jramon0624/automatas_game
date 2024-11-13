
import pygame
import math
import random

ANCHO, ALTO = 800, 600
AREA_PORTERIA_1 = pygame.Rect(0, ALTO // 4, 50, ALTO // 2)
AREA_PORTERIA_2 = pygame.Rect(ANCHO - 50, ALTO // 4, 50, ALTO // 2)

class Jugador:
    def __init__(self, equipo_id, x, y, controles=None, aleatorio=False):
        self.equipo_id = equipo_id
        self.x = x
        self.y = y
        self.controles = controles
        self.aleatorio = aleatorio  
        self.velocidad = 5
        self.radius = 10  
        self.active = False

    def mover(self, teclas):
        if not self.aleatorio and self.controles:
            if teclas[self.controles['arriba']]:
                self.y -= self.velocidad
            if teclas[self.controles['abajo']]:
                self.y += self.velocidad
            if teclas[self.controles['izquierda']]:
                self.x -= self.velocidad
            if teclas[self.controles['derecha']]:
                self.x += self.velocidad

    def mover_aleatorio(self):
        if self.aleatorio:
            dx = random.choice([-1, 0, 1]) * self.velocidad
            dy = random.choice([-1, 0, 1]) * self.velocidad
            self.x += dx
            self.y += dy

            if self.equipo_id == 1:
                self.x = max(50, min(self.x, ANCHO // 2 - 50))
            else:
                self.x = max(ANCHO // 2 + 50, min(self.x, ANCHO - 50))
            self.y = max(50, min(self.y, ALTO - 50))

    def dibujar(self, ventana):
        color = (0, 0, 255) if self.equipo_id == 1 else (255, 0, 0)
        pygame.draw.circle(ventana, color, (self.x, self.y), self.radius)  # Usamos el radius aquí

class Portero(Jugador):
    def mover(self, teclas):
        super().mover(teclas)
        area = AREA_PORTERIA_1 if self.equipo_id == 1 else AREA_PORTERIA_2
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
        dx = self.x - jugador.x
        dy = self.y - jugador.y
        distancia = math.hypot(dx, dy)
        
        self.vx = (dx / distancia) * self.speed
        self.vy = (dy / distancia) * self.speed

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def colisiona_con(self, jugador):
        distancia = math.hypot(self.x - jugador.x, self.y - jugador.y)
        return distancia < self.radius + jugador.radius
