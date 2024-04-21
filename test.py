import pygame
import math
import random
from time import sleep

pygame.init()

# Set up the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Procedural pathfinding cube")

# Define colors
RED = (128, 0, 0)
BLUE = (0, 0, 128)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Define cube properties
CUBE_RADIUS = 10
CUBE_SPEED = 2
MAX_SPEED = 4
GOAL_RADIUS = 50

NUM_OBSTACLES = 5
obstacle_radius = 50
obstacles = []

paths = []

class Sphere:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


Main_Cube = Sphere(1, 1, 10)


class Node:
    def __init__(self, x, y, valid, goal, weight):
        self.x = x
        self.y = y
        self.valid = valid
        self.goal = goal
        self.weight = weight

    def check_validity(self, x, y, obstacles):
        pass

class path:
    def __init__(self, x, y, nodes_on_path, path_weight, path_killed):
        self.x = x
        self.y = y
        self.nodes_on_path = nodes_on_path
        self.path_weight = path_weight
        self.path_killed = path_killed


def new_positions():
    obstacles = []

    for _ in range(20):
        obstacles.append(Sphere(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100), 50))

    for obstacle in obstacles:
        while (Main_Cube.x - 60 < obstacle.x < Main_Cube.x + 60) and (Main_Cube.y - 60 < obstacle.y < Main_Cube.y + 60):
            obstacle.x = random.randint(100, SCREEN_WIDTH - 100)
            obstacle.y = random.randint(100, SCREEN_HEIGHT - 100)

    goals = []
    goals.append(
        Sphere(random.randint((SCREEN_WIDTH//40) // 2, SCREEN_WIDTH//40 - 2), random.randint(2, SCREEN_HEIGHT//40 - 2), 20))
    count = 0
    for goal in goals:
        while count < len(obstacles) + 1:
            while (Main_Cube.x - 30 < goal.x * 40 < Main_Cube.x + 30) and (Main_Cube.y - 30 < goal.y * 40 < Main_Cube.y + 30):
                goal.x = random.randint(2, SCREEN_WIDTH//40 - 2)
                goal.y = random.randint(2, SCREEN_HEIGHT//40 - 2)
                count = 0
            count += 1
            for obstacle in obstacles:
                while (obstacle.x - 140 < goal.x*40 < obstacle.x + 140) and (obstacle.y - 140 < goal.y*40 < obstacle.y + 140):
                    goal.x = random.randint(SCREEN_WIDTH//40 // 2, SCREEN_WIDTH//40 - 2)
                    goal.y = random.randint(2, SCREEN_HEIGHT//40 - 2)
                    count = 0
                count += 1

    return obstacles, goals


screen.fill((128, 128, 128))

cols = 26
rows = 26
nodes = [[0 for x in range(cols)] for y in range(rows)]

obstacles, goals = new_positions()


for obstacle in obstacles:
    pygame.draw.circle(screen, RED, [obstacle.x, obstacle.y], obstacle.radius)
for goal in goals:
    pygame.draw.circle(screen, GREEN, [goal.x * 40, goal.y * 40], goal.radius)

valid_coords = []
for y in range(rows):
    for x in range(cols):
        validity = True
        coord = (x,y)
        goal_validity = False
        for obstacle in obstacles:

            if (obstacle.x - 60 < (x * 40) < obstacle.x + 60) and (obstacle.y - 60 < (y * 40) < obstacle.y + 60):
                validity = False
                coord = ()
        for goal in goals:
            if goal.x == x and goal.y == y:
                goal_validity = True

        Edistance = (((goal.x - x)**2 + (goal.y - y)**2)**0.5)
        if coord != ():
            valid_coords.append(coord)
        nodes[y][x] = Node(x, y, validity, goal_validity, Edistance)

paths.append(path(Main_Cube.x,Main_Cube.y, [(Main_Cube.x,Main_Cube.y)], nodes[Main_Cube.x][Main_Cube.y].weight,False))
reached_goal = False
directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
while reached_goal == False:
    for dir in directions:
        for oldpath in paths:
            newx = oldpath.x + dir[0]
            newy = oldpath.y + dir[1]
            newpath = [*oldpath.nodes_on_path, (newx, newy)]
            print(newpath)
            for goal in goals:
                if newx == goal.x and newy == goal.y:
                    reached_goal = [*oldpath.nodes_on_path,(newx,newy)]
                elif 25> newx > 0 and 25> newy > 0 and tuple((newx,newy)) in valid_coords and tuple((newx,newy)) not in oldpath.nodes_on_path and oldpath.path_killed == False:
                    newpath = [*oldpath.nodes_on_path,(newx,newy)]
                    paths.append(path(newx,newy, newpath, oldpath.path_weight + nodes[newy][newx].weight,False))

paths = []
paths.append(path(Main_Cube.x,Main_Cube.y, [(Main_Cube.x,Main_Cube.y)], nodes[Main_Cube.x][Main_Cube.y].weight,False))
reached_goal_bread = False
screen.fill("white")
for oldpath in paths:
    print(len(paths))
    for dir in directions:

        newx = oldpath.x + dir[0]
        newy = oldpath.y + dir[1]
        print(newpath)
        for i in range(len(newpath) - 1):
            # (3,4) *40
            newtuple = (newpath[i][0] * 40, newpath[i][1] * 40)

            newtuple2 = (newpath[i + 1][0] * 40, newpath[i + 1][1] * 40)

            pygame.draw.line(screen, "black", newtuple, newtuple2)
        pygame.display.flip()
        for goal in goals:
            if newx == goal.x and newy == goal.y:
                reached_goal = [*oldpath.nodes_on_path,(newx,newy)]
                break
            elif 25> newx > 0 and 25> newy > 0 and tuple((newx,newy)) in valid_coords and tuple((newx,newy)) not in oldpath.nodes_on_path and oldpath.path_killed == False:
                newpath = [*oldpath.nodes_on_path,(newx,newy)]
                paths.append(path(newx,newy, newpath, oldpath.path_weight + nodes[newy][newx].weight,False))

pygame.draw.circle(screen, BLUE, [Main_Cube.x*40, Main_Cube.y*40], Main_Cube.radius)

for i in range(25):
    pygame.draw.line(screen, BLACK, (0 + i * 40, 0), (0 + i * 40, SCREEN_HEIGHT), width=2)
for i in range(25):
    pygame.draw.line(screen, BLACK, (0, 0 + i * 40), (SCREEN_WIDTH, 0 + i * 40), width=2)

for rows in nodes:
    for node in rows:
        if node.valid:
            red = min(255, int(255 * (node.weight / 25)))
            green = max(0,int(255 * (1 - node.weight / 25)))
            color = pygame.Color(red, green, 0)
            pygame.draw.circle(screen, color, [node.x*40, node.y*40], 5)
        if node.goal:
            pygame.draw.circle(screen, BLACK, [node.x * 40, node.y * 40], 5)
        if node.valid == False:
            pygame.draw.circle(screen, BLACK, [node.x * 40, node.y * 40], 5)

print("\n", reached_goal)
for i in range(len(reached_goal)-1):
    # (3,4) *40
    newtuple = (reached_goal[i][0]*40,reached_goal[i][1]*40)


    newtuple2 = (reached_goal[i+1][0]*40,reached_goal[i+1][1]*40)

    pygame.draw.line(screen, "yellow", newtuple, newtuple2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()



    sleep(1)
    pygame.display.flip()
