#
# TODO
#
# For the case of magnitudes being equivalent
#
#
#
#


import pyglet
import math
from pyglet import shapes
from pyglet import graphics
from pyglet.text import Label
from pyglet.window import Window
from pyglet import app
from pyglet.window import key
import numpy as np
from enum import Enum
from pyglet.window import FPSDisplay

class Relative_Direction(Enum):
    FORWARD = 'FORWARD'
    BACK    = 'BACK'
    LEFT    = 'LEFT'
    RIGHT   = 'RIGHT'

class Cell:
    def __init__(self, position: np.array):
        self.position = position

    def world_position(self, scalar):
        return self.position * scalar

class Avatar:
    def __init__(self, position: np.array) -> None:
        self.position = position
        self.direction = math.radians(0)
        
    def rotate(self, turning_direction: Relative_Direction):
        if turning_direction == Relative_Direction.LEFT:
            self.direction -= .1
        if turning_direction == Relative_Direction.RIGHT:
            self.direction += .1

        if self.direction < 0:
            self.direction += (math.pi * 2)
        
        elif self.direction >= 2 * math.pi:
            self.direction -= (2 * math.pi)
        return
    
    def move(self, strafe_direction: Relative_Direction, current_direction: math.radians):
        if strafe_direction == Relative_Direction.FORWARD:
            self.position[0] += 5 * math.cos(current_direction)
            self.position[1] -= 5 * math.sin(current_direction)

        if strafe_direction == Relative_Direction.BACK:
            self.position[0] += 5 * math.cos(current_direction + math.pi)
            self.position[1] -= 5 * math.sin(current_direction + math.pi)

        if strafe_direction == Relative_Direction.LEFT:
            self.position[0] += 5 * math.cos(current_direction - (math.pi/2))
            self.position[1] += 5 * math.sin(current_direction + (math.pi/2))

        if strafe_direction == Relative_Direction.RIGHT:
            self.position[0] += 5 * math.cos(current_direction + (math.pi/2))
            self.position[1] += 5 * math.sin(current_direction - (math.pi/2))

def raycast(dictionary_Cells, position: np.array, direction: math.radians, scalar: int, window_width, window_height, fov: int) -> np.array:
        def x_mag(x: float, angle: math.radians):
            return abs(x) / math.cos(math.pi-angle)
        def y_mag(y: float, angle: math.radians):
            if math.sin(angle) != 0:
                return abs(y) / math.sin(angle)
            else:
                return abs(y) / math.sin(.0000000000000001)

        if direction < 0:
            direction = direction + (2 * math.pi)
        elif direction >= (2 * math.pi):
            direction = direction - (2 * math.pi)

        timeout_max = 16
        timeout = 0
        
        
        #Up and Right #PROBLEM AREA
        if direction >= (2 * math.pi) - (math.pi/2) and direction < (2 * math.pi):
            offset_x = 1 - ((position[0]/scalar) % 1)
            offset_y = 1 - ((position[1]/scalar) % 1)
            while True:
                magnitudes = [x_mag(offset_x, direction), y_mag(offset_y, direction)]
                calc_y = magnitudes[0] *  math.sin(direction)
                calc_x = magnitudes[1] * -math.cos(direction)
                
                x_intercept_coordinates = np.array([round(scalar * calc_x + avatar.position[0], 3), round(scalar * offset_y + avatar.position[1], 3)])
                y_intercept_coordinates = np.array([round(scalar * offset_x + avatar.position[0], 3), round(scalar * calc_y + avatar.position[1], 3)])

                x_intercept_coordinates_normal = np.array([math.floor(x_intercept_coordinates[0]/scalar), math.floor(x_intercept_coordinates[1]/scalar)])
                y_intercept_coordinates_normal = np.array([math.floor(y_intercept_coordinates[0]/scalar), math.floor(y_intercept_coordinates[1]/scalar)])
                
                if magnitudes[0] <= magnitudes[1]:
                    if f'{x_intercept_coordinates_normal[0]}:{x_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * calc_x + window_width/2, scalar * offset_y + window_height/2, 7, 12, (255, 255, 0, 255), batch, foreground)) #Needs to be locked to the x-axis
                        return({'magnitude': abs(magnitudes[1]), 'color': (255,255,0,255), 'circle': circle, 'angle': direction})
                    offset_y += 1
                
                elif magnitudes[1] < magnitudes[0]:
                    if f'{y_intercept_coordinates_normal[0]}:{y_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * offset_x + window_width/2, scalar * calc_y + window_height/2, 7, 12, (255, 0, 255, 255), batch, foreground))
                        return({'magnitude': abs(magnitudes[0]), 'color': (255,100,0,255), 'circle': circle, 'angle': direction })
                    offset_x += 1

                timeout += 1
                if timeout == timeout_max:
                    return 0
                
        
        #Up and Left
        elif direction >= (math.pi) and direction < ((2 * math.pi) - (math.pi / 2)):
            offset_x = (1 - ((position[0]/scalar) % 1)) - 1
            offset_y = 1 - ((position[1]/scalar) % 1)
            while True:
                magnitudes = [x_mag(offset_x, direction), y_mag(offset_y, direction)]
                calc_y = magnitudes[0] * -math.sin(direction)
                calc_x = magnitudes[1] * -math.cos(direction)
                
                x_intercept_coordinates = np.array([round(scalar * calc_x + avatar.position[0], 3), round(scalar * offset_y + avatar.position[1], 3)])
                y_intercept_coordinates = np.array([round(scalar * offset_x + avatar.position[0], 3), round(scalar * calc_y + avatar.position[1], 3)])

                x_intercept_coordinates_normal = np.array([math.floor(x_intercept_coordinates[0]/scalar), math.floor(x_intercept_coordinates[1]/scalar)])
                y_intercept_coordinates_normal = np.array([(math.floor(y_intercept_coordinates[0]/scalar - 1)), (math.floor(y_intercept_coordinates[1]/scalar))])
                
                if magnitudes[0] > abs(magnitudes[1]):
                    if f'{x_intercept_coordinates_normal[0]}:{x_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * calc_x + window_width/2, scalar * offset_y + window_height/2, 7, 12, (255, 255, 0, 255), batch, foreground)) #Needs to be locked to the x-axis
                        return({'magnitude': abs(magnitudes[1]), 'color': (255,255,0,255), 'circle': circle, 'angle': direction})
                    offset_y += 1
                
                elif abs(magnitudes[1]) >= magnitudes[0]:
                    if f'{y_intercept_coordinates_normal[0]}:{y_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * offset_x + window_width/2, scalar * calc_y + window_height/2, 7, 12, (255, 0, 255, 255), batch, foreground))
                        return({'magnitude': abs(magnitudes[0]), 'color': (255,100,0,255), 'circle': circle, 'angle': direction})
                    offset_x -= 1
                timeout += 1
                if timeout == timeout_max:
                    return 0

        #Down and Right
        elif direction >= (0) and direction < ((math.pi / 2)):
            offset_x = (1 - ((position[0]/scalar) % 1)) 
            offset_y = 1 - ((position[1]/scalar) % 1) - 1 #-.000000000001
            while True:
                magnitudes = [x_mag(offset_x, direction), y_mag(offset_y, direction)]
                calc_y = magnitudes[0] * math.sin(direction)
                calc_x = magnitudes[1] * math.cos(direction)
                
                if math.isinf(calc_x):
                    if calc_x < 0:
                        calc_x = -999999
                    else:
                        calc_x = 999999

                x_intercept_coordinates = np.array([round(scalar * calc_x + avatar.position[0], 3), round(scalar * offset_y + avatar.position[1], 3)])
                y_intercept_coordinates = np.array([round(scalar * offset_x + avatar.position[0], 3), round(scalar * calc_y + avatar.position[1], 3)])

                x_intercept_coordinates_normal = np.array([math.floor(x_intercept_coordinates[0]/scalar), math.floor(x_intercept_coordinates[1]/scalar - 1)])
                y_intercept_coordinates_normal = np.array([(math.floor(y_intercept_coordinates[0]/scalar)), (math.floor(y_intercept_coordinates[1]/scalar))])
 
                if abs(magnitudes[0]) >= magnitudes[1]:
                    if f'{x_intercept_coordinates_normal[0]}:{x_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * calc_x + window_width/2, scalar * offset_y + window_height/2, 7, 12, (255, 255, 0, 255), batch, foreground)) #Needs to be locked to the x-axis
                        return({'magnitude': abs(magnitudes[1]), 'color': (255,255,0,255), 'circle': circle, 'angle': direction})
                    offset_y -= 1
                
                elif magnitudes[1] > abs(magnitudes[0]):
                    if f'{y_intercept_coordinates_normal[0]}:{y_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * offset_x + window_width/2, scalar * calc_y + window_height/2, 7, 12, (255, 0, 255, 255), batch, foreground))
                        return({'magnitude': abs(magnitudes[0]), 'color': (255,100,0,255), 'circle': circle, 'angle': direction})
                    offset_x += 1
                timeout += 1
                if timeout == timeout_max:
                    return 0


        #Down and Left
        elif direction >= ((math.pi / 2)) and direction < ((math.pi)):
            offset_x = (1 - ((position[0]/scalar) % 1)) - 1
            offset_y = 1 - ((position[1]/scalar) % 1) - 1
            while True:
                magnitudes = [x_mag(offset_x, direction), y_mag(offset_y, direction)]
                calc_y = magnitudes[0] * -math.sin(direction)
                calc_x = magnitudes[1] * math.cos(direction)
                
                if math.isinf(calc_x):
                    if calc_x < 0:
                        calc_x = -999999
                    else:
                        calc_x = 999999

                x_intercept_coordinates = np.array([round(scalar * calc_x + avatar.position[0], 3), round(scalar * offset_y + avatar.position[1], 3)])
                y_intercept_coordinates = np.array([round(scalar * offset_x + avatar.position[0], 3), round(scalar * calc_y + avatar.position[1], 3)])

                x_intercept_coordinates_normal = np.array([math.floor(x_intercept_coordinates[0]/scalar), math.floor(x_intercept_coordinates[1]/scalar - 1)])
                y_intercept_coordinates_normal = np.array([(math.floor(y_intercept_coordinates[0]/scalar - 1)), (math.floor(y_intercept_coordinates[1]/scalar))])
                
                

                if abs(magnitudes[0]) > magnitudes[1]:
                    if f'{x_intercept_coordinates_normal[0]}:{x_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * calc_x + window_width/2, scalar * offset_y + window_height/2, 7, 12, (255, 255, 0, 255), batch, foreground)) #Needs to be locked to the x-axis
                        return({'magnitude': abs(magnitudes[1]), 'color': (255,255,0,255), 'circle': circle, 'angle': direction})
                    offset_y -= 1
                
                elif magnitudes[1] >= abs(magnitudes[0]):
                    if f'{y_intercept_coordinates_normal[0]}:{y_intercept_coordinates_normal[1]}' in dictionary_Cells:
                        circle = (shapes.Circle(scalar * offset_x + window_width/2, scalar * calc_y + window_height/2, 7, 12, (255, 0, 255, 255), batch, foreground))
                        return({'magnitude': abs(magnitudes[0]), 'color': (255,100,0,255), 'circle': circle, 'angle': direction})
                    offset_x -= 1

                timeout += 1
                if timeout == timeout_max:
                    return 0


        
            

        

if __name__ == '__main__':
    init = False
    
    if init == False:
        window_width = 640  
        window_height = 480
        window_1 = Window(window_width, window_height, 'Main Window')
        #window_2 = Window(window_width, window_height, 'Casted Window')

        #GRID CELL SIZE SCALING VALUE
        overhead_scaling = 50

        grid_lines = [[],[]]

        avatar = Avatar(np.array([0,0]))

        #BATCH AND GROUP CREATION
        background = pyglet.graphics.Group(order = 0)
        foreground = pyglet.graphics.Group(order = 1)
        batch = graphics.Batch()
        unit_cell = graphics.Batch()
        walls_batch = graphics.Batch()

        keys_pressed = key.KeyStateHandler()
        window_1.push_handlers(keys_pressed)

        cell_list = []
        cell_dict = {}
        cell_list_visual = []
        cell_list.append(Cell(np.array([1,1])))
        cell_list.append(Cell(np.array([2,1])))
        cell_list.append(Cell(np.array([0,0])))
        cell_list.append(Cell(np.array([3,0])))
        cell_list.append(Cell(np.array([3,1])))
        cell_list.append(Cell(np.array([3,2])))
        cell_list.append(Cell(np.array([2,2])))
        cell_list.append(Cell(np.array([2,4])))
        cell_list.append(Cell(np.array([-2,-3])))
        cell_list.append(Cell(np.array([2,-3])))
        cell_list.append(Cell(np.array([2,-2])))
        cell_list.append(Cell(np.array([-2,-2])))
        cell_list.append(Cell(np.array([-2,-1])))
        cell_list.append(Cell(np.array([-2,0])))

        for x in range(len(cell_list)):
            cell_dict[f'{cell_list[x].position[0]}:{cell_list[x].position[1]}'] = cell_list[x]

        for i in range(len(cell_list)):
            world_pos = cell_list[i].world_position(overhead_scaling)
            cell_list_visual.append(
                shapes.BorderedRectangle(world_pos[0], world_pos[1],
                                         overhead_scaling, overhead_scaling, 1,
                                         (50, 50, 255, 100), (255, 255, 255, 100),
                                         unit_cell, foreground)
            )

        for x in range(round(window_width/overhead_scaling) + 2):
            grid_lines[0].append(shapes.Line(x * overhead_scaling, 0, 
                                             x * overhead_scaling, window_height, 
                                             1, (255,255,255,100), batch, background))
        for x in range(round(window_width/overhead_scaling) + 2):
            grid_lines[1].append(shapes.Line(0, x * overhead_scaling, 
                                             window_width, x * overhead_scaling, 
                                             1, (255,255,255,100), batch, background))

        avatar_circle = shapes.Circle(window_width/2, window_height/2, 16, 16, (0, 255, 0, 255), batch = batch, group = foreground)
        avatar_line = shapes.Line(avatar_circle.x, avatar_circle.y, avatar_circle.x + 16, avatar_circle.y, 3, (255,0,0,255), batch, foreground)
        
        fps_display = FPSDisplay(window_1)

        overhead_map = False

    init = True

    @window_1.event
    def on_draw():

        global overhead_map

        ray_circle = []
    
        """
        Keyboard Input Settings
        """
        if keys_pressed[key.W]:
            avatar.move(Relative_Direction.FORWARD, avatar.direction)
        if keys_pressed[key.S]:
            avatar.move(Relative_Direction.BACK, avatar.direction)
        if keys_pressed[key.A]:
            avatar.move(Relative_Direction.LEFT, avatar.direction)
        if keys_pressed[key.D]:
            avatar.move(Relative_Direction.RIGHT, avatar.direction)
        if keys_pressed[key.Q]:
            avatar.rotate(Relative_Direction.LEFT)
        if keys_pressed[key.E]:
            avatar.rotate(Relative_Direction.RIGHT)
        if keys_pressed[key.SPACE]:
            overhead_map = not overhead_map

        fov = 90
        info = []
        global walls 
        walls = []


        
        for x in range(int(math.degrees(avatar.direction) - fov/2), int(math.degrees(avatar.direction) + fov/2), 1):
            if x > 0:
                z = x
            else:
                z = x + 360
            info.append(raycast(cell_dict, avatar.position, math.radians((x + 1)), overhead_scaling, window_width, window_height, fov))
        
        sky = shapes.Rectangle(0,window_height/2, window_width, window_height/2, (50, 50, 50, 255), walls_batch, background)
        floor = shapes.Rectangle(0,0, window_width, window_height/2, (50, 50, 255, 255), walls_batch, background)

        for x in range(len(info)):
            if info[x] != 0 and info[x] != None:
                correction = (info[x]['angle'] - avatar.direction)
                walls.append(
                    shapes.Rectangle(window_width * (x/fov), 0 + ((window_height - window_height/(info[x]['magnitude'] * (math.cos(correction))))/2), window_width * (1/fov),window_height/(info[x]['magnitude'] * (math.cos(correction))), info[x]['color'], walls_batch, foreground)
                )
            

        """
        Changes line positions to give an illusion  of infinite grid space
        """
        for x in range(len(grid_lines[0])):
            grid_lines[0][x].x = x * overhead_scaling - (avatar.position[0] % overhead_scaling) - 2 * (window_width % overhead_scaling)
            grid_lines[0][x].x2 = x * overhead_scaling - (avatar.position[0] % overhead_scaling) - 2 * (window_width % overhead_scaling)

        for x in range(len(grid_lines[1])):
            grid_lines[1][x].y = x * overhead_scaling - (avatar.position[1] % overhead_scaling) - 2 * (window_height % overhead_scaling)
            grid_lines[1][x].y2 = x * overhead_scaling - (avatar.position[1] % overhead_scaling) - 2 * (window_height % overhead_scaling)

        """
        Adjust the screen position of the world cells
        """
        for x in range(len(cell_list_visual)):
            cell_position = cell_list[x].world_position(overhead_scaling)
            cell_list_visual[x].x = cell_position[0] - avatar.position[0] + (window_width/2)
            cell_list_visual[x].y = cell_position[1] - avatar.position[1] + (window_height/2)

        """
        Update Avatar Direction Line
        """
        avatar_line.rotation = math.degrees(avatar.direction)

        window_1.clear()
        if overhead_map == True:
            batch.draw()
            unit_cell.draw()
        else:
            walls_batch.draw()
        fps_display.draw()

    app.run(1/60)