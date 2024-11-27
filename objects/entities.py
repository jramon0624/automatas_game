
import pygame
import math
import random as rd

WIDTH, HEIGHT = 800, 650
AREA_PORTERIA_1 = pygame.Rect(23, 156, 129, 293)
AREA_PORTERIA_2 = pygame.Rect(647, 156, 129, 293)

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
                theta = math.atan(self.dy/self.dx if self.dx != 0 else 100000)
                sigma = rd.gauss(mu=math.pi,sigma=1.0)
                phi = rd.gauss(mu=0.0,sigma=sigma)
                # phi = rd.uniform(-math.pi,math.pi)

                self.dx = self.velocidad * math.cos(theta + phi)
                self.dy = self.velocidad * math.sin(theta + phi)
            self.x += self.dx
            self.y += self.dy

            # if (self.x <= 20 + self.radius or self.x >= 780 - self.radius):
            #     self.dx *= -1
            # if self.y <= 17 + self.radius or self.y >= 583 - self.radius:
            #     self.dy *= -1

            if self.equipo_id == 1:
                self.x = max(50, min(self.x, WIDTH // 2 - 50))
            else:
                self.x = max(WIDTH // 2 + 50, min(self.x, WIDTH - 50))
            self.y = max(50, min(self.y, HEIGHT - 50))
            self.steps -= 1

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, self.color, (self.x, self.y), self.radius)  # Usamos el radius aquí

class Portero(Jugador):
    def mover_aleatorio(self):
        super().mover_aleatorio()
        area = AREA_PORTERIA_1 if self.equipo_id == 1 else AREA_PORTERIA_2
        if not area.collidepoint(self.x + self.radius, self.y + self.radius):
            self.x, self.y = max(area.left, min(area.right, self.x)), max(area.top, min(area.bottom, self.y))

class Balon:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.speed = 5
        self.vx = rd.uniform(-5,5)
        self.vy = rd.choice([-1,1]) * math.sqrt(self.speed**2 - self.vx**2)
        self.radius = 8

    def mover(self):
        self.x += self.vx
        self.y += self.vy
        # Rebotar en los bordes
        if (self.x <= 20 + self.radius or self.x >= 780 - self.radius) and (self.y < 219 + self.radius or self.y > 388 - self.radius):
            self.vx *= -1
        if self.y <= 17 + self.radius or self.y >= 583 - self.radius:
            self.vy *= -1

    def golpear(self, jugador):
        if jugador.equipo_id == 1:
            dx = rd.uniform(0,self.speed)
        else:
            dx = rd.uniform(-self.speed,0)

        self.vx = dx
        self.vy = rd.choice([-1,1]) * math.sqrt(self.speed**2 - self.vx**2)
        #distancia = math.hypot(dx, dy)
        
        #self.vx = (dx / distancia) * self.speed
        #self.vy = (dy / distancia) * self.speed

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

    def colisiona_con(self, jugador):
        distancia = math.hypot(self.x - jugador.x, self.y - jugador.y)
        return distancia < self.radius + jugador.radius
