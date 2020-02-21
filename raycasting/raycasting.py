from math import *
import pygame

import time
layout =\
[\
[0,0,0,0,0,0],\
[0,1,1,1,1,0],\
[0,1,0,1,0,0],\
[0,1,0,0,0,1],\
[0,0,0,0,0,1],\
[0,0,0,0,0,0],\
]
class Grid:
    def __init__(self, layout):
        self.w = len(layout[0]) 
        self.h = len(layout) 
        self.layout = layout

    def inside(self, pos):
        return pos.x >= 0 and pos.x < self.w and pos.y >= 0 and pos.y < self.h

    def contains(self, pos):
        if self.inside(pos):
            return self.layout[pos.y][pos.x]
        return True

class Vector:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __truediv__(self, vec):
        x = float('Inf') if vec.x == 0 else self.x / vec.x
        y = float('Inf') if vec.y == 0 else self.y / vec.y
        return Vector(x, y)

    def __getitem__(self, index):
        if index % 2 == 0:
            return self.x
        else:
            return self.y

    def __setitem__(self, index, value):
        if index % 2 == 0:
            self.x = value
        else:
            self.y = value

def sign(vec):
    x = 0 if vec.x == 0 else vec.x / abs(vec.x)
    y = 0 if vec.y == 0 else vec.y / abs(vec.y)
    return Vector(int(x), int(y))

def rotate(vec, angle):
    s = sin(angle)
    c = cos(angle)
    return Vector(vec.x * c + vec.y * s, -vec.x * s + vec.y * c)

def inside(grid, pos):
    return pos.x >= 0 and pos.x < grid.w and pos.y >= 0 and pos.y < grid.h

def traverse(grid, startPos, direction):
    nextPlane = Vector(\
            ceil(startPos.x - 1) if direction.x < 0 else floor(startPos.x + 1),\
            ceil(startPos.y - 1) if direction.y < 0 else floor(startPos.y + 1))
    stepDir = sign(direction)
    pos = Vector(floor(startPos.x), floor(startPos.y))
    t = (nextPlane - startPos) / direction

    tStep = Vector(1,1) / Vector(abs(direction.x), abs(direction.y))
    length = 0
    while grid.inside(pos):
        tmin = min(t.x, t.y)
        length += tmin
        t = Vector(t.x - tmin, t.y - tmin)
        
        axis = 0 if t.x == 0 else 1

        pos[axis] += stepDir[axis]
        if grid.contains(pos):
            return True, length, pos, axis

        t[axis] = tStep[axis]
    return False, 0


    
w = 400
h = 200
fov = 45 
near = 0.001
nearPlaneX = near * tan(fov/2)
nearPlaneY = nearPlaneX * h / w 
d = nearPlaneX * 2 / w
    
def draw(screen, grid, position, viewAngle):
    lastRes = False, 0, Vector(0,0), 0
    firstIter = True 
    for i in range(0, w):
        di = d * (i - w // 2)
        pos = Vector(di , near)
        pos = rotate(pos, viewAngle)
        
        angle = viewAngle + atan(di / near) 
        
        res = traverse(grid, position + pos, Vector(cos(angle), sin(angle)))
        if firstIter:
            lastRes = res
            firstIter = False

        if res[0]:
            height = int(h * near / nearPlaneY / (2 * res[1]))
            lastHeight = int(h * near / nearPlaneY / (2 * lastRes[1]))
            if (lastRes[3] != res[3] or abs(lastRes[2].x - res[2].x) + abs(lastRes[2].y - res[2].y) > 1):
                if lastRes[1] > res[1]:
                    pygame.draw.line(screen, (0,0,0), (i, (h - height) // 2),((i, (h + height) // 2)))
                else:
                    pygame.draw.line(screen, (0,0,0), (i-1, (h - lastHeight) // 2),((i-1, (h + lastHeight) // 2)))
            else:
                pygame.draw.line(screen, (0,0,0), (i-1, (h - lastHeight) // 2), (i, (h - height) // 2))
                pygame.draw.line(screen, (0,0,0), (i-1, (h + lastHeight) // 2), (i, (h + height) // 2))
        lastRes = res 

grid = Grid(layout)
screen = pygame.display.set_mode((w,h))
pos = Vector(2.1, 5.9)
viewAngle = -1.1

while True:
    deltaPos = Vector(0,0);
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        viewAngle -= 0.02 
    if keys[pygame.K_RIGHT]:
        viewAngle += 0.02 
    if keys[pygame.K_w]:
        deltaPos.x += 0.02 
    if keys[pygame.K_s]:
        deltaPos.x -= 0.02 
    if keys[pygame.K_a]:
        deltaPos.y -= 0.02 
    if keys[pygame.K_d]:
        deltaPos.y += 0.02 
    if keys[pygame.K_c]:
        print(str(pos) + " " + str(viewAngle))
    if keys[pygame.K_x]:
        pos = Vector(2.1, 5.9)
        viewAngle = -1.1
    pos += rotate(deltaPos,-viewAngle)
    screen.fill((255,255,255))
    draw(screen, grid, pos, viewAngle)
    pygame.display.flip()
    pygame.event.pump()
