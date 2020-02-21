from math import * 
import pygame

class Vertex:
    def __init__(self, v): 
        self.x = v
        self.y = v

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vertex(self.x * other.x, self.y * other.y)

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, other):
        return Color(self.r * other, self.g * other, self.b * other)

def area(vertex1, vertex2, vertex3):
    v1 = vertex2 - vertex1
    v2 = vertex3 - vertex1
    return v1.x * v2.y - v1.y * v2.x

def drawTriangle(screen, outputW, outputH, v1, v2, v3, c1, c2, c3):
    areaTotal = area(v1, v2, v3)
    x1 = floor(max(min(min(v1.x, v2.x), v3.x), 0))
    y1 = floor(max(min(min(v1.y, v2.y), v3.y), 0))

    x2 = ceil(min(max(max(v1.x, v2.x),v3.x), outputW))
    y2 = ceil(min(max(max(v1.y, v2.y),v3.y), outputH))

    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            v = Vertex(x,y)

            b1 = area(v,v2,v3) / areaTotal
            b2 = area(v,v3,v1) / areaTotal
            b3 = area(v,v1,v2) / areaTotal

            if b1 >= 0 and b1 <= 1 and b2 >= 0 and b2 <= 1 and b3 >= 0 and b3 <= 1:
                c = c1 * b1 + c2 * b2 + c3 * b3
                pygame.draw.rect(screen, (int(c.r), int(c.g), int(c.b)), (x,y,1,1))

w = 200
h = 200
screen = pygame.display.set_mode((w,h))
side = w - 20

v1 = Vertex(w / 2, h / 2 - side * 1.414 / 4)
v2 = Vertex(w - 10, h / 2 + side * 1.414 / 4)
v3 = Vertex(10, h / 2 + side * 1.414 / 4)

c1 = Color(255, 0, 0)
c2 = Color(0, 255, 0)
c3 = Color(0, 0, 255)

i = 0
while True:
    i += 0.1 
    screen.fill((0,0,0))
    drawTriangle(screen, w, h, v1 + Vertex(sin(i) * 10, cos(i) * 10),v2 + Vertex(cos(i) * 10, sin(i) * 10),v3 + Vertex(sin(i+0.5) * 10, cos(i+0.5) * 10),c1,c2,c3)
    pygame.display.flip()
    pygame.event.pump()
