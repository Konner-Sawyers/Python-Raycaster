import pyglet
import math
from pyglet import shapes
from pyglet import graphics
from pyglet.window import Window
from pyglet import app

class Ray:
    def __init__(self, avatar_x, avatar_y, end_x, end_y):
        self.avatar_x = avatar_x
        self.avatar_y = avatar_y
        self.end_x = end_x
        self.end_y = end_y

    def detect_collision(grid, dim_x, dim_y):
        
        pass

    def draw_ray():
        pass

class Grid_Cell:
    def __init__(self, pos_x, pos_y, width, height):
        self.width_world = width
        self.height_world = height
        self.occupied = False

        self.display_shape = None

        self.pos_x = None
        self.pos_y = None

class Avatar:
    def __init__(self, x, y, target_grid, dim_x, dim_y, fov = 60):
        self.pos_x = x
        self.pos_y = y
        self.fov = fov

        self.dim_x = dim_x
        self.dim_y = dim_y

        self.view_line = None

    def avatar_line(self, mouse_x, mouse_y):
        view_angle = math.atan(mouse_x/mouse_y)
        magnitude = math.sqrt(math.pow(mouse_x, 2) + math.pow(mouse_y, 2))
        
        #Creates the bound lines of the fov
        fov_1 = -(view_angle + math.radians(self.fov/2) - math.pi/2)
        fov_2 = -(view_angle - math.radians(self.fov/2) - math.pi/2)

        pos_x_1 = magnitude * math.cos(fov_1)
        pos_y_1 = magnitude * math.sin(fov_1)
        pos_x_2 = magnitude * math.cos(fov_2)
        pos_y_2 = magnitude * math.sin(fov_2)
        
        #print(view_angle, fov_1, fov_2)
        #print(mouse_x, mouse_y)

        rays = 5
        self.view_lines = [None] * rays
        for x in range(rays):
            print(f'Stats {x} {rays}')
            print(x/rays)
            print(math.radians((self.fov)))
            print(x/rays * math.radians((self.fov)))
            self.view_lines[x] = (shapes.Line(0, 0, 
                                               magnitude * math.cos((fov_1 + (x + 1)/(rays + 1) * math.radians((self.fov)))), 
                                               magnitude * math.sin((fov_1 + (x + 1)/(rays + 1) * math.radians((self.fov)))), 
                                               1, color = (255, 255, 0, 255), batch = batch))

        #self.view_line = shapes.Line(0, 0, mouse_x, mouse_y, 1, color = (255, 255, 0, 255), batch = batch)
        self.fov_lines = [
            shapes.Line(0, 0, pos_x_1, pos_y_1, 1, color = (0, 0, 255, 255), batch = batch),
            shapes.Line(0, 0, pos_x_2, pos_y_2, 1, color = (0, 0, 255, 255), batch = batch)
        ]

win_title = 'Overhead Raycast'

width = 480
height = 480

win_overhead = Window(width, height, win_title)

batch = graphics.Batch()

#Creating lines for testing


dim_x = 10
dim_y = 10
world_grid = []
for x in range(dim_x):
    world_grid.append([])
    for y in range(dim_y):
        world_grid[x].append(Grid_Cell(pos_x = x, pos_y = y, width = width / dim_x, height = height / dim_y))

world_grid[2][2].occupied = True
world_grid[3][4].occupied = True
world_grid[1][2].occupied = True

world_grid[0][0].occupied = False
#print(world_grid[0][0].occupied)

def display_grid(world_grid):
    for x in range(len(world_grid)):
        for y in range(len(world_grid[x])):
            #print(world_grid[x][y].occupied, x, y)
            if world_grid[x][y].occupied == True:
                color = (255, 0, 0, 255)
            elif world_grid[x][y].occupied == False:
                color = (0, 0, 0, 255)
            
            world_grid[x][y].display_shape = (shapes.BorderedRectangle( x * world_grid[x][y].width_world, y * world_grid[x][y].height_world, world_grid[x][y].width_world, world_grid[x][y].height_world, 1, color = color, border_color = (255, 255, 255), batch = batch))

camera = Avatar(0, 0, fov = 30, dim_x = dim_x, dim_y = dim_y, target_grid = world_grid)

@win_overhead.event
def on_mouse_motion(x, y, dx, dy):
    #print(x, y)
    camera.avatar_line(x, y)

@win_overhead.event
def on_draw():
    display_grid(world_grid)
    Window.clear()
    batch.draw()

app.run(1/60)