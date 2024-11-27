
import pygame
import math
import random as rd

WIDTH, HEIGHT = 800, 650
AREA_PORTERIA_1 = pygame.Rect(30, 250, 42, 172)
AREA_PORTERIA_2 = pygame.Rect(727, 250, 42, 172)

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
                self.steps = rd.randint(5,20)
                theta = math.atan(self.dy/self.dx if self.dx != 0 else 100000)
                # sigma = rd.gauss(mu=math.pi,sigma=1.0)
                # phi = rd.gauss(mu=0.0,sigma=sigma)
                phi = rd.uniform(-math.pi,math.pi)

                self.dx = self.velocidad * math.cos(theta + phi)
                self.dy = self.velocidad * math.sin(theta + phi)
            self.x += self.dx
            self.y += self.dy

            if self.equipo_id == 1:
                self.x = max(30 + self.radius, min(self.x, 30 + (3 * 739//4) - self.radius))
            else:
                self.x = max(30 + 739//4 + self.radius, min(self.x, 739 + 30 - self.radius))
            self.y = max(78 + self.radius, min(self.y, 594 - self.radius))
            self.steps -= 1

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, self.color, (self.x, self.y), self.radius)  # Usamos el radius aquí

class Portero(Jugador):
    def mover_aleatorio(self):
        if self.aleatorio:
            if self.steps <= 0:
                self.steps = rd.randint(5,20)
                theta = math.atan(self.dy/self.dx if self.dx != 0 else 100000)
                # sigma = rd.gauss(mu=math.pi,sigma=1.0)
                # phi = rd.gauss(mu=0.0,sigma=sigma)
                phi = rd.uniform(-math.pi,math.pi)

                self.dx = self.velocidad * math.cos(theta + phi)
                self.dy = self.velocidad * math.sin(theta + phi)
            self.x += self.dx
            self.y += self.dy

            area = AREA_PORTERIA_1 if self.equipo_id == 1 else AREA_PORTERIA_2
            if not area.collidepoint(self.x + self.radius, self.y + self.radius):
                self.x, self.y = max(area.left + self.radius, min(area.right - self.radius, self.x)), max(area.top + self.radius, min(area.bottom - self.radius, self.y))
            self.steps -= 1

class Balon:
    steps = 500
    restrict = 500

    def __init__(self):
        self.x, self.y = 30 + 739//2, 78 + 516// 2
        self.speed = 5
        self.vx = rd.uniform(-5,5)
        self.vy = rd.choice([-1,1]) * math.sqrt(self.speed**2 - self.vx**2)
        self.radius = 8

    def mover(self):
        if self.steps != 0:
            self.steps -=1
        self.x += (self.steps/self.restrict) * self.vx
        self.y += (self.steps/self.restrict) * self.vy
        # Rebotar en los bordes
        if (self.x <= 30 + self.radius or self.x >= 769 - self.radius) and (self.y < 285 + self.radius or self.y > 388 - self.radius):
            self.vx *= -1
        if self.y <= 78 + self.radius or self.y >= 594 - self.radius:
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
