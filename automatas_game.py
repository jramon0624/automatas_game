from multiprocessing import Process
from turtle import Turtle
import random as rd
import turtle
import math
import time

# Configuraciones
sc_width = 1000
sc_height = 766

# Crear escenario
sc = turtle.Screen()
sc.title("Automatas Game")
sc.bgpic("rsc/football_bg.png")
sc.setup(width=sc_width, height=sc_height)

class Object(Turtle):
    height = sc_height//2 -20
    width = sc_width//2 -20
    center = 0
    
    def __init__(self):
        super().__init__()

    def detect_border(self):
        height = self.height
        width = self.width
        center = self.center

        if self.ycor() > height:
            self.sety(height)
            self.dy *= -1
        
        if self.ycor() < -height:
            self.sety(-height)
            self.dy *= -1

        if self.xcor() > (center + width):
            self.setx(center + width)
            self.dx *= -1

        if self.xcor() < (center - width):
            self.setx(center - width)
            self.dx *= -1
    

class Ball(Object):

    dr: int = 5
    
    def __init__(self):
        super().__init__()
        self.speed(4)
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0,0)
        self.dx: float = rd.uniform(-5,5)
        self.dy: float = rd.choice([-1,1]) * math.sqrt(self.dr**2 - self.dx**2)

    def kicking(self):
        # self.dx = rd.choice([-1,1]) * rd.gauss(self.dx,1)
        # self.dy = rd.choice([-1,1]) * math.sqrt(abs(self.dr**2 - self.dx**2))
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

class Player(Object):

    dr = 20
    box = 20
    
    def __init__(self, x: int, y: int, color: str):
        super().__init__()
        self.speed(4)
        self.shape("circle")
        self.color(color)
        self.penup()
        self.goto(x,y)
        self.dx: float = rd.uniform(-5,5)
        self.dy: float = rd.choice([-1,1]) * math.sqrt(self.dr**2 - self.dx**2)
    
    def movement(self):
        x = self.dx
        y = self.dy
        theta = math.atan(y/x if x!= 0 else 100000)
        phi = rd.triangular(theta - math.pi/2,theta + math.pi/2)

        # bounds = (self.dr * math.cos(theta + math.pi/2), self.dr * math.cos(theta - math.pi/2))
        # if rd.choice([True,False]):
            # self.dx = rd.uniform(min(bounds),max(bounds))
            # self.dy = math.sin(math.acos(self.dx/self.dr))
        self.dx = self.dr * math.cos(phi)
        self.dy = self.dr * math.sin(phi)
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)
    
    def kick_ball(self, ball: Ball, weight: int = -1):
        distance = math.sqrt((self.xcor()-ball.xcor())**2 + (self.ycor()-ball.ycor())**2)

        if distance < self.box:
            if weight > 0:
                ball.dx = rd.uniform(0,5)
                ball.dy = rd.choice([-1,1]) * math.sqrt(self.dr**2 - self.dx**2)
            else:
                ball.dx = rd.uniform(-5,0)
                ball.dy = rd.choice([-1,1]) * math.sqrt(self.dr**2 - self.dx**2)

if __name__ == "__main__":
    ball = Ball()

    # position_red = [(100,-125),(100,0)]
    position_red = [
        (100,-125),  (100,0),  (100,125),
        (175,-75),      (175,75),
    (250,-175),     (250,0),     (250,175),
        (325,-300),     (325,300)
    ]

    team_red = [Player(x,y,"red") for x, y in position_red]

    # position_blue = [(-100,-125),(-100,0)]
    position_blue = [
        (-100,-125),  (-100,0),  (-100,125),
        (-175,-75),      (-175,75),
    (-250,-175),     (-250,0),     (-250,175),
        (-325,-300),     (-325,300)
    ]

    team_blue = [Player(x,y,"blue") for x, y in position_blue]

    goalkeeper_red = Player(400,0,"yellow")
    goalkeeper_red.center = 390
    goalkeeper_red.height = 150
    goalkeeper_red.width = 60

    goalkeeper_blue = Player(-400,0,"black")
    goalkeeper_blue.center = -390
    goalkeeper_blue.height = 150
    goalkeeper_blue.width = 60

    while True:
        sc.update()

        ball.kicking()
        ball.detect_border()

        # for player_red, player_blue in zip(team_red,team_blue):
        #     player_red.movement()
        #     player_blue.movement()

        #     player_red.kick_ball(ball)
        #     player_blue.kick_ball(ball,1)

        #     player_red.detect_border()
        #     player_blue.detect_border()

        player = rd.choice(team_red)
        player.movement()
        player.kick_ball(ball)
        player.detect_border()

        player = rd.choice(team_blue)
        player.movement()
        player.kick_ball(ball,1)
        player.detect_border()

        goalkeeper_red.movement()
        goalkeeper_red.kick_ball(ball)
        goalkeeper_red.detect_border()

        goalkeeper_blue.movement()
        goalkeeper_blue.kick_ball(ball,1)
        goalkeeper_blue.detect_border()





