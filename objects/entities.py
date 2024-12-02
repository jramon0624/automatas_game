
import pygame
import math
import random as rd
from cons import *

class Jugador:
    def __init__(self, equipo_id, x, y, controles=None, aleatorio=False):
        self.equipo_id = equipo_id
        self.x = x
        self.y = y
        self.controles = controles
        self.aleatorio = aleatorio  
        self.velocidad = 3
        self.radius = 10  
        self.active = False
        self.color = (0, 0, 255) if self.equipo_id == 1 else (255, 0, 0)
        self.dx = rd.uniform(-self.velocidad,self.velocidad)
        self.dy = rd.choice([-1,1]) * math.sqrt(self.velocidad ** 2 - self.dx ** 2)
        self.steps = 0

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
            if self.steps <= 0:
                self.steps = rd.randint(0,10)
                theta = math.atan2(self.dy,self.dx)
                # sigma = rd.gauss(mu=math.pi,sigma=1.0)
                phi = rd.gauss(mu=0.0,sigma=1.0)
                # phi = rd.uniform(-math.pi,math.pi)

                self.dx = self.velocidad * math.cos(theta + phi)
                self.dy = self.velocidad * math.sin(theta + phi)
            self.x += self.dx
            self.y += self.dy

            if self.equipo_id == 1:
                self.x = max(AREA_CANCHA.left + self.radius, min(self.x, AREA_CANCHA.right - (AREA_CANCHA.right-AREA_CANCHA.left)//6 - self.radius))
            else:
                self.x = max(AREA_CANCHA.left + (AREA_CANCHA.right-AREA_CANCHA.left)//6 + self.radius, min(self.x, AREA_CANCHA.right - self.radius))
            self.y = max(AREA_CANCHA.top + self.radius, min(self.y, AREA_CANCHA.bottom - self.radius))
            self.steps -= 1

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, self.color, (self.x, self.y), self.radius)  # Usamos el radius aquí

class Portero(Jugador):
    def mover_aleatorio(self):
        if self.aleatorio:
            if self.steps <= 0:
                self.steps = rd.randint(5,20)
                theta = math.atan2(self.dy,self.dx)
                # sigma = rd.gauss(mu=math.pi,sigma=1.0)
                phi = rd.gauss(mu=0.0,sigma=1.0)
                # phi = rd.uniform(-math.pi,math.pi)

                self.dx = self.velocidad * math.cos(theta + phi)
                self.dy = self.velocidad * math.sin(theta + phi)
            x = self.x + self.dx
            y = self.y + self.dy

            area = AREA_PORTERIA_1 if self.equipo_id == 1 else AREA_PORTERIA_2
            self.x, self.y = max(area.left + self.radius, min(area.right - self.radius, x)), max(area.top + self.radius, min(area.bottom - self.radius, y))
            self.steps -= 1

class Balon:
    steps = 500
    restrict = 500

    def __init__(self):
        self.x, self.y = (AREA_CANCHA.right - AREA_CANCHA.left)/2 + AREA_CANCHA.left, (AREA_CANCHA.bottom - AREA_CANCHA.top)/2 + AREA_CANCHA.top
        self.speed = 5
        self.vx = rd.uniform(-5,5)
        self.vy = rd.choice([-1,1]) * math.sqrt(self.speed**2 - self.vx**2)
        self.radius = 8

    def mover(self):
        if self.steps != 200:
            self.steps -=1
        self.x += (self.steps/self.restrict) * self.vx
        self.y += (self.steps/self.restrict) * self.vy
        # Rebotar en los bordes
        if (self.x <= AREA_CANCHA.left + self.radius or self.x >= AREA_CANCHA.right - self.radius) and (self.y < AREA_GOL_1.top + self.radius or self.y > AREA_GOL_1.bottom - self.radius):
            self.vx *= -1
        if self.y <= AREA_CANCHA.top + self.radius or self.y >= AREA_CANCHA.bottom - self.radius:
            self.vy *= -1

    def golpear(self, jugador):
        if jugador.equipo_id == 1:
            dx = rd.uniform(0,self.speed)
        else:
            dx = rd.uniform(-self.speed,0)

        self.vx = dx
        self.vy = rd.choice([-1,1]) * math.sqrt(self.speed**2 - self.vx**2)
        self.steps = self.restrict

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def colisiona_con(self, jugador):
        distancia = math.hypot(self.x - jugador.x, self.y - jugador.y)
        return distancia < self.radius + jugador.radius
