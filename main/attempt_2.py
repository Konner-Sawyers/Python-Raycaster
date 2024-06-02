import pyglet
import math
from pyglet import shapes
from pyglet import graphics
from pyglet.text import Label
from pyglet.window import Window
from pyglet import app
from pyglet.window import key

class Camera:
    def __init__(self, screen_size: tuple):
        self.screen_size = screen_size
        self.world_pos = (0, 0)

class Ray:
    def __init__(self, origin: tuple, parent_direction: math.radians, direction_offset: math.radians):
        self.origin = origin
        self.direction_offset = direction_offset
        self.direction =  direction_offset - parent_direction
        self.magnitude = 480
        self.direction_line = shapes.Line(self.origin[0], self.origin[1], (self.magnitude) * (math.sin(self.direction)) + self.origin[0], (self.magnitude) * (math.cos(self.direction)) + self.origin[1], 1, color = (255, 255, 0), batch = batch, group = foreground)


    def camera_translation(self, camera_position: tuple = (0, 0)):
        self.direction_line.position = (camera_position)

    def set_camera_offset(self, offset):
        self.camera_offset = offset
        
    def world_translation(self, delta_position: tuple = (0, 0), parent_direction: math.radians = 0):
        self.direction =  (self.direction_offset) - (parent_direction)
        self.origin = (self.origin[0] + delta_position[0], self.origin[1] + delta_position[1])
        self.direction_line.position = (self.origin[0], self.origin[1])
        self.direction_line.rotation = self.direction

        x_diff = self.origin[0]
        y_diff = self.origin[1]
        
        self.direction_line.x2 = (self.magnitude) * (math.cos(self.direction)) + x_diff
        self.direction_line.y2 = (self.magnitude) * (math.sin(self.direction)) + y_diff

    def set_position(self, position: tuple):
        self.origin = position

    def set_magnitude(self, magnitude: float):
        self.magnitude = abs(magnitude)
        #self.direction_line.width = self.magnitude
        #self.direction_line = shapes.Line(self.origin[0], self.origin[1], (self.origin[0] + self.magnitude) * (math.sin(self.direction)), (self.origin[1] + self.magnitude) * (math.cos(self.direction)), 1, color = (255, 255, 0), batch = batch, group = foreground)
        #self.direction_line.position = (self.origin[0] - camera_adjustment[0], self.origin[1] - camera_adjustment[1])

        x_diff = self.origin[0]
        y_diff = self.origin[1]

        self.direction_line.x2 = (self.magnitude) * (math.cos(self.direction)) + x_diff - self.camera_offset[0]
        self.direction_line.y2 = (self.magnitude) * (math.sin(self.direction)) + y_diff - self.camera_offset[1]
        self.direction_line.rotation = self.direction



        #print(f'{self.direction}')


class Avatar:
    def __init__(self, starting_pos: tuple = (0, 0), starting_direction: math.radians = (0)):
        self.world_pos = starting_pos
        self.direction = starting_direction
        print(f'STARTING DIRECTION AVATAR: {self.direction}')
        self.visual = shapes.Circle(self.world_pos[0], self.world_pos[1], 15, 12, (0, 255, 0, 255), batch, group = foreground)
        self.direction_line = shapes.Line(self.world_pos[0], self.world_pos[1], (self.world_pos[0] + 60) * (math.cos(self.direction)), (self.world_pos[1] + 60) * (math.sin(self.direction)), 1, color = (255, 0, 0), batch = batch, group = foreground)

        self.rays = []
        self.fov = math.radians(90)
        self.ray_count = 0
        
        for x in range(self.ray_count):
            #ray_direction = ((x / self.ray_count) * math.radians(self.fov)) + self.direction - (math.radians(self.fov) / 2)
            #offset formula ((1) * math.radians(self.fov)) + math.radians(self.fov / 2)
            #ray_direction = (self.direction / 2) + ((x / self.ray_count) * math.radians(self.fov)) + math.radians(self.fov / 2)
            ray_offset = ((x / self.ray_count) * (self.fov)) - (self.fov / 2)
            #ray_offset = math.radians(0)
            self.rays.append(Ray(self.world_pos, self.direction , ray_offset))
            print(f'RAY {x} OFFSET {ray_offset} AND ORIGINAL DIRECTION {self.direction} FINAL {self.rays[x].direction}')
        #ray_direction = (self.direction / 2) + ((1) * math.radians(self.fov)) + math.radians(self.fov / 2)
        ray_offset = 0#((1) * (self.fov)) - (self.fov / 2)
        self.rays.append(Ray(self.world_pos, self.direction , ray_offset))
        self.rays[self.ray_count].direction_line.color = (255,0,255,255)
        print(f'RAY {self.ray_count} OFFSET {ray_offset} AND ORIGINAL DIRECTION {self.direction} FINAL {self.rays[self.ray_count].direction}')

    def camera_translation(self, delta_position: tuple = (0, 0)):
        self.visual.position = (self.world_pos[0] - delta_position[0], self.world_pos[1] - delta_position[1])
        self.direction_line.position = (self.visual.position)
        for x in range(len(self.rays)):
            self.rays[x].camera_translation(self.visual.position)

        
    def world_translation(self, delta_position: tuple = (0, 0), delta_rotation: math.radians = 0):
        self.direction += delta_rotation
        if self.direction >= math.pi * 2:
            self.direction = self.direction - (math.pi * 2)
        elif self.direction < 0:
            self.direction = math.pi * 2 + self.direction
        self.world_pos = (self.world_pos[0] + delta_position[0], self.world_pos[1] + delta_position[1])
        self.direction_line.position = (self.world_pos[0], self.world_pos[1])
        self.direction_line.rotation = math.degrees(self.direction)
        for x in range(len(self.rays)):
            self.rays[x].world_translation(delta_position, self.direction)
        #print(f'Avatar Direction: {self.direction}')

    def origin_rays(self):
        for x in range(len(self.rays)):
            #print(self.rays[x].direction_line.position, self.visual.position)
            self.rays[x].set_position(self.world_pos)
        

class Grid_Cell:
    def __init__(self, size: int, row: int, col: int, grid_origin: tuple):
        self.size = size
        self.row = row
        self.col = col
        self.grid_origin = grid_origin

        self.wall = False
        self.draw = False

        self.world_pos = (row * size, col * size)

        

        self.visual = shapes.BorderedRectangle(self.world_pos[0], self.world_pos[1], 
                    self.size, self.size, 1,
                    color = (0, 0, 0, 50), border_color = (255, 255, 255, 50), batch = batch, group = background)
        
    def camera_translation(self, camera_position: tuple = (0, 0)):
        self.visual.position = (self.world_pos[0] - camera_position[0], self.world_pos[1] - camera_position[1])


class Grid:
    def __init__(self, avatar : Avatar, matrix_dim: tuple = (3, 3)):
        self.avatar = avatar

        self.matrix_dim = matrix_dim #Determines rows and columns inside of the grid

        self.cell_size = 50 #10 Chosen as the world cord cell size in order to increase accuracy during division operations

        self.cell_arr = [] #placeholder

        self.world_pos = (0, 0) #The origin of the grid. Will be kept at 0,0 unless there is reason to move it

        self.world_size = (self.cell_size * self.matrix_dim[0], self.cell_size * self.matrix_dim[1])

        self.map_border = shapes.BorderedRectangle(self.world_pos[0], self.world_pos[1], 
                    self.world_size[0], self.world_size[1], 1,
                    color = (0, 0, 0, 255), border_color = (0, 0, 255, 255), batch = batch, group = background)
        
        for x in range(self.matrix_dim[0]):
            self.cell_arr.append([])
            for y in range(self.matrix_dim[1]):
                self.cell_arr[x].append(Grid_Cell(self.cell_size, x, y, self.world_pos))

        self.cell_arr[2][1].wall = True
        self.cell_arr[2][2].wall = True
        self.cell_arr[2][3].wall = True
        self.cell_arr[2][4].wall = True
        self.cell_arr[5][3].wall = True
        self.cell_arr[6][3].wall = True
        self.cell_arr[6][2].wall = True

        for x in range(len(self.cell_arr)):
                for y in range(len(self.cell_arr[x])):
                    if self.cell_arr[x][y].wall == True:
                        self.cell_arr[x][y].visual.border_color = (255,255,255,255)

    def camera_translation(self, camera_position: tuple = (0, 0)):
        self.map_border.position = (self.world_pos[0] - camera_position[0], self.world_pos[1] - camera_position[1])
        for x in range(len(self.cell_arr)):
            for y in range(len(self.cell_arr[x])):
                self.cell_arr[x][y].camera_translation(camera_position)
        self.avatar.camera_translation(camera_position)

        for x in range(len(self.avatar.rays)):
            self.avatar.rays[x].set_camera_offset(camera_position)
            #self.avatar.rays[x].set_magnitude(self.avatar.rays[x].magnitude + 1)
        

    def avatar_bounds(self):
        if self.avatar.world_pos[0] <= self.world_pos[0]:
            self.avatar.world_pos = self.world_pos[0], self.avatar.world_pos[1]
            self.avatar.origin_rays()

        elif self.avatar.world_pos[0] >= self.world_pos[0] + self.world_size[0]:
            self.avatar.world_pos = self.world_pos[0] + self.world_size[0], self.avatar.world_pos[1]
            self.avatar.origin_rays()

        if self.avatar.world_pos[1] <= self.world_pos[1]:
            self.avatar.world_pos = self.avatar.world_pos[0], self.world_pos[1]
            self.avatar.origin_rays()

        elif self.avatar.world_pos[1] >= self.world_pos[1] + self.world_size[1]:
            self.avatar.world_pos = self.avatar.world_pos[0], self.world_pos[1] + self.world_size[1]
            self.avatar.origin_rays()

    def ray_collisions(self):
        def intercept_magnitude_x(offset: float, angle: math.radians, intercept: int):
            try:
                return (intercept - (offset % self.cell_size))/math.cos(angle)
            except:
                return self.matrix_dim[0] * self.cell_size + self.cell_size
        
        def intercept_magnitude_y(offset: float, angle: math.radians, intercept: int):
            try:
                return (intercept - (offset % self.cell_size))/math.sin(angle)
            except:
                return self.matrix_dim[1] * self.cell_size + self.cell_size
            
        def get_cell_cord(position: tuple):
            cords = (math.floor(position[0]/ self.cell_size), math.floor(position[1] / self.cell_size))
            if cords[0] > self.matrix_dim[0] - 1:
                cords = (self.matrix_dim[0] - 1, cords[1])
            if cords[1] > self.matrix_dim[1] - 1:
                cords = (cords[0], self.matrix_dim[1] - 1)
            if cords[0] < 0:
                cords = (0, cords[1])
            if cords[1] < 0:
                cords = (cords[0], 0)
            return cords

        for i in range(len(self.avatar.rays)):
            n = 1   #X Intercept Iterator
            m = 1   #Y Intercept Iterator
            avatar_cell_cord = get_cell_cord(self.avatar.world_pos)
            #camera_offset = self.avatar.visual.position
            self.track_circle = shapes.Circle(self.avatar.rays[0].origin[0] - self.avatar.rays[0].camera_offset[0],
                                                self.avatar.rays[0].origin[1] - self.avatar.rays[0].camera_offset[1],
                                                6, 9, (255, 0, 0, 255), batch, foreground2)
            offset = self.avatar.world_pos
            self.intercept_circles = []
            while True:
                magnitude_x = intercept_magnitude_x(offset[0], self.avatar.rays[i].direction + math.pi, n * self.cell_size)
                magnitude_y = intercept_magnitude_y(offset[1], self.avatar.rays[i].direction + math.pi, m * self.cell_size)

                print((self.avatar.world_pos[0], self.avatar.world_pos[1]))
                print(f'Avatar In Cell {avatar_cell_cord} | Ray {i} | X&Y Intercepts {n * self.cell_size, m * self.cell_size} | X&Y Mags {magnitude_x, magnitude_y}')

                self.intercept_circles.append(
                                         shapes.Circle(
                                         offset[0] + magnitude_x * math.cos(self.avatar.rays[i].direction + math.pi) - self.avatar.rays[0].camera_offset[0],
                                         offset[1] + magnitude_x * math.sin(self.avatar.rays[i].direction + math.pi) - self.avatar.rays[0].camera_offset[1],
                                         6, 9, (255, 0, 0, 255), batch, foreground2))
                
                self.intercept_circles.append(
                                         shapes.Circle(
                                         offset[0] + magnitude_y * math.cos(self.avatar.rays[i].direction + math.pi) - self.avatar.rays[0].camera_offset[0],
                                         offset[1] + magnitude_y * math.sin(self.avatar.rays[i].direction + math.pi) - self.avatar.rays[0].camera_offset[1],
                                         6, 9, (0, 255, 0, 255), batch, foreground2))


                '''
                if  magnitude_x < magnitude_y:
                    cell = get_cell_cord((offset[0] + magnitude_x * math.cos(self.avatar.rays[i].direction) ,
                                          offset[1] + magnitude_x * math.sin(self.avatar.rays[i].direction)))
                    
                    if self.cell_arr[cell[0]][cell[1]].wall == False:
                                    n += 1
                    else:
                        print(f'X INT CELL POS {cell} Wall Detected {magnitude_x}')
                        self.avatar.rays[i].set_magnitude(magnitude_x)
                        self.intercept_circles.append(shapes.Circle( offset[0] + magnitude_x * math.cos(self.avatar.rays[i].direction),  
                                                                     offset[1] + magnitude_x * math.sin(self.avatar.rays[i].direction), 
                                                                    20, 12, (255, 255, 255, 255), batch, foreground2))
                        break

                elif magnitude_y < magnitude_x:
                    cell = get_cell_cord((offset[0] + magnitude_y *math.cos(self.avatar.rays[i].direction) ,
                                          offset[1] + magnitude_y *math.sin(self.avatar.rays[i].direction)))
                    if self.cell_arr[cell[0]][cell[1]].wall == False:
                                    m += 1
                    else:
                        print(f'Y INT CELL POS {cell} Wall Detected {magnitude_y}')
                        self.avatar.rays[i].set_magnitude(magnitude_y)
                        self.intercept_circles.append(shapes.Circle(240 + offset[0] + magnitude_y *math.cos(self.avatar.rays[i].direction),
                                                                    240 + offset[1] + magnitude_y *math.sin(self.avatar.rays[i].direction), 
                                                                    20, 12, (255, 255, 255, 255), batch, foreground2))
                        break
                    
                elif magnitude_x == magnitude_y:
                    cell = get_cell_cord((offset[0] + magnitude_y *math.cos(self.avatar.rays[i].direction) ,
                                          offset[1] + magnitude_y *math.sin(self.avatar.rays[i].direction)))
                    if self.cell_arr[cell[0]][cell[1]].wall == False:
                                    m += 1
                                    n += 1
                    else:
                        print(f'INT CELL POS {cell} Wall Detected {magnitude_y}')
                        self.avatar.rays[i].set_magnitude(magnitude_x)
                        self.intercept_circles.append(shapes.Circle(240 + offset[0] + magnitude_y *math.cos(self.avatar.rays[i].direction), 
                                                                    240 + offset[1] + magnitude_y *math.sin(self.avatar.rays[i].direction), 
                                                                    20, 12, (255, 255, 255, 255), batch, foreground2))
                        break'''
                m += 1
                n += 1
                if m >= self.matrix_dim[1] or n >= self.matrix_dim[0]:
                    #if magnitude_x < magnitude_y:
                    #self.avatar.rays[i].set_magnitude(self.avatar.rays[i].magnitude + 1)    #WORKS
                    #else:
                    #self.avatar.rays[i].set_magnitude(magnitude_y)                          #DOES NOT WORK! WHY >:(
                    self.avatar.rays[i].set_magnitude(magnitude_x)
                    print(f'FOREVER LOOP DONE {n , m}')
                    break

class World:
    def __init__(self, world_map : Grid ):
        '''
        The *World* class will contain all objects to allow for easy translation of all items if the need occurs.
        '''
        self.map = world_map




if __name__ == '__main__':

    width = 720
    height = 720

    win_overhead = Window(width, height, 'Overhead')
    keys_pressed = key.KeyStateHandler()
    win_overhead.push_handlers(keys_pressed)

    batch = graphics.Batch()
    background = graphics.Group(order = 0)
    foreground = graphics.Group(order = 1)
    foreground2 = graphics.Group(order = 2)

    world_camera = Camera((width, height))
    indie = Avatar((0, 0), math.pi * 0)
    test_grid = Grid(indie, (9, 9))
    virt_world = World(test_grid)

    move_speed = 4

    label_camera_pos = Label('Camera Position',
                            font_name='Times New Roman',
                            font_size=12,
                            width=0, height=height,
                            color=(255,255,0,255),
                            anchor_x='left', anchor_y='bottom', batch=batch,)

    label_grid_pos = Label('Grid Screen Position',
                            font_name='Times New Roman',
                            font_size=12,
                            width=0, height=height - 16,
                            color=(255,255,0,255),
                            anchor_x='left', anchor_y='bottom', batch=batch)

    label_mouse_pos = Label('Mouse Screen Position: ',
                            font_name='Times New Roman',
                            font_size=12,
                            width=0, height=height - 32,
                            color=(255,255,0,255),
                            anchor_x='left', anchor_y='bottom', batch=batch)

    label_mouse_pos_world = Label('Mouse World Position: ',
                            font_name='Times New Roman',
                            font_size=12,
                            width=0, height=height - 48,
                            color=(255,255,0,255),
                            anchor_x='left', anchor_y='bottom', batch=batch)

    #print(virt_world.map.world_size[0], virt_world.map.world_size[1])

    def camera_keys(keys_pressed):
        if keys_pressed[key.UP]:
            dx = 1
        elif keys_pressed[key.DOWN]:
            dx = -1
        else:
            dx = 0
        if keys_pressed[key.RIGHT]:
            dy = 1
        elif keys_pressed[key.LEFT]:
            dy = -1
        else:
            dy = 0
        return(dy, dx)

    def avatar_keys(keys_pressed):
        if keys_pressed[key.W]:
            dx = 1
        elif keys_pressed[key.S]:
            dx = -1
        else:
            dx = 0
        if keys_pressed[key.A]:
            dy = -1
        elif keys_pressed[key.D]:
            dy = 1
        else:
            dy = 0
        if keys_pressed[key.E]:
            dr = .1
        elif keys_pressed[key.Q]:
            dr = -.1
        else:
            dr = 0
        dy = dy * 5
        dx = dx * 5
        return((dy, dx), dr)

    @win_overhead.event
    def on_mouse_motion(x, y, dx, dy):
        label_mouse_pos.text = f'Mouse Screen Position: {(x, y)}'
        label_mouse_pos_world.text = f'Mouse World Position: {(x - world_camera.world_pos[0] - width / 2, y - world_camera.world_pos[1] - height / 2)}'

    @win_overhead.event
    def on_draw():
        #display_grid(world_grid)

        label_camera_pos.text = f'Camera World Position:  {world_camera.world_pos}'
        label_grid_pos.text   = f'Grid Screen Position:    {virt_world.map.map_border.position}'

        #camera_translation = camera_keys(keys_pressed)
        
        #camera_translation = tuple(x * move_speed for x in camera_translation)

        avatar_translation, avatar_rotation = avatar_keys(keys_pressed)

        #world_camera.world_pos = (world_camera.world_pos[0] + camera_translation[0], world_camera.world_pos[1] + camera_translation[1])

        avatar_rotation = math.radians(avatar_rotation * 35)
        
        virt_world.map.avatar_bounds()
        
        virt_world.map.avatar.world_translation(avatar_translation, avatar_rotation)
        world_camera.world_pos = (virt_world.map.avatar.world_pos[0], virt_world.map.avatar.world_pos[1])
        
        virt_world.map.camera_translation((world_camera.world_pos[0] - width / 2, world_camera.world_pos[1] - height / 2))
        virt_world.map.ray_collisions()
        virt_world.map.camera_translation((world_camera.world_pos[0] - width / 2, world_camera.world_pos[1] - height / 2))

        Window.clear()
        batch.draw()

    app.run(1/60)