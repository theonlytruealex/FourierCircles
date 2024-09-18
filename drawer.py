import pygame.draw
import pygame.time
import pygame
import math
import coef_calculator as cf
import numpy as np
import get_points

pygame.init()

white = (255, 255, 255)
gray = (255 // 2, 255 // 2, 255 // 2)
red = (255, 0, 0)
black = (0, 0, 0)

# parameters
width = 1600
height = 900
program_speed = 1
vector_count = 301

# 1 for no change, -1 for upside down
flip_up = -1
vector_size = 1
draw_length = 1000
point_count = 1001
svg_file = './images/witch.svg'

# calculate the point coordinates of a butterfly curve
""" points = np.zeros([2, point_count])
dt = 12 * math.pi / (point_count + 1)
t = dt
for i in range(point_count):
    points[0][i] = 10 * math.sin(t) * (math.pow(math.e, math.cos(t)) - 2 * math.cos(4 * t) - math.pow(math.sin(t / 12), 5))
    points[1][i] = 10 * math.cos(t) * (math.pow(math.e, math.cos(t)) - 2 * math.cos(4 * t) - math.pow(math.sin(t / 12), 5))
    t += dt
 """
vector_size *= flip_up
points = get_points.get_point_array(point_count, svg_file, width, height)
mid_x = width / 2
mid_y = height / 2
screen = pygame.display.set_mode((width, height))
time_converter = 2 * math.pi / 6000 * program_speed

def main():
    prev_time = pygame.time.get_ticks()

    coefs = np.zeros([2, vector_count])
    coefs = cf.get_coefs(points, vector_count)

    # create the vectors, multiply them by their respective coefficients
    vectors = []
    vectors.append(Vector([mid_x, mid_y], [0, 0], 0))
    for i in range(1, vector_count, 2):
        vectors.append(Vector(vectors[i - 1].end, complex_mul(coefs[0][i], coefs[1][i], vector_size, 0), i // 2 + 1))
        vectors.append(Vector(vectors[i].end, complex_mul(coefs[0][i + 1], coefs[1][i + 1], vector_size, 0), -i // 2))
        
    # start the drawing
    draw = drawing(draw_length)
    draw.add_point(vectors[vector_count - 1].end)
    global screen
    pygame.display.set_caption('Drawing time')

    while True:
        screen.fill(black)
        curr_time = pygame.time.get_ticks()

        # how much time has passed
        time_passed = (curr_time - prev_time) * time_converter
        prev_time = curr_time

        # update vectors
        vectors[0].update_angle(time_passed)
        vectors[0].draw_self()
        for i in range(1, vector_count):
            vectors[i].update_angle(time_passed)
            vectors[i].update_center(vectors[i - 1].end)
            vectors[i].draw_self()
        
        # update drawing
        draw.add_point(vectors[vector_count - 1].end)
        draw.draw_me()

        pygame.display.update()

        # quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def complex_mul(a1, b1, a2, b2):
    return [a1 * a2 - b1 * b2, a1 * b2 + b1 * a2]

class drawing:
    def __init__(self, max_points):
        self.max_points = max_points
        self.points = []
    def add_point(self, point):
        self.points.append(point)
        if len(self.points) > self.max_points:
            self.points.pop(0)
    def draw_me(self):
        pygame.draw.circle(screen, red, self.points[len(self.points)-1], 5, 5)
        for i in range(1, len(self.points)-2):
            pygame.draw.line(screen, white, self.points[i], self.points[i + 1])
        
class Vector:
    def __init__(self, center, complex_number, speed):
        self.center = center
        self.complex_number = complex_number
        self.speed = speed
        self.end = (self.complex_number[0] + center[0], self.complex_number[1] + center[1])
        if complex_number[0] == 0 and complex_number[1] == 0:
            self.angle = 0
        elif complex_number[0] == 0:
            self.angle = math.pi * complex_number[1] / abs(complex_number[1]) / 2
        else:
            self.angle = math.atan2(complex_number[1], complex_number[0])
        self.R = math.sqrt(self.complex_number[0] * self.complex_number[0] + self.complex_number[1] * self.complex_number[1])

    def update_angle(self, time):
        self.angle += time * self.speed
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle <= -2 * math.pi:
            self.angle += 2 * math.pi
        self.complex_number[0] = math.cos(self.angle) * self.R
        self.complex_number[1] = math.sin(self.angle) * self.R
        self.end = self.complex_number[0] + self.center[0], self.complex_number[1] + self.center[1]

    def update_center(self, center):
        self.center = center
        self.end = self.complex_number[0] + self.center[0], self.complex_number[1] + self.center[1]

    def draw_self(self):
        pygame.draw.circle(screen, gray, self.center, self.R, 1)
        pygame.draw.line(screen, gray, self.center, self.end)



if __name__ == '__main__':
    main()