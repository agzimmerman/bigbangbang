from pygame import *
import random
import numpy as np

# @todo Us vs. Them

delay = 100
dt = 1.
G = 200.

init()
display_height = 640.
display_width = 640.
center = (display_height/2., display_width/2.)
screen = display.set_mode((int(display_height), int(display_width)))
display.set_caption('Big Bang! Bang!')

circle = image.load('pics/circle.png')

def color_surface(surface, red, green, blue):
    # https://gamedev.stackexchange.com/questions/26550/how-can-a-pygame-image-be-colored
    arr = surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue
    
    
class Body:

    def __init__(self, mass=1, radius=1, position=(center[0], center[1]), velocity=(0,0), color=(255,255,255)):
        
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        
        self.pic = transform.scale(circle.copy(), (2*radius, 2*radius))
        self.pic.set_colorkey((0,0,0))
        self.pic.convert_alpha()
        color_surface(self.pic, color[0], color[1], color[2])
        
    def draw(self):
        screen.blit(self.pic, (int(round(self.position[0])) - self.radius, int(round(self.position[1])) - self.radius))
        
    def compute_force(self, other):
        r = self.position - other.position
        force = G*self.mass*other.mass*r/np.sqrt(r[0]**2 + r[1]**2)**3
        return force
        
    def move(self, force):
        self.position += self.velocity*dt
        a = -force/self.mass
        self.velocity += a*dt

star = Body(mass=1, radius=50)
us = Body(mass=1, radius=25, position=(center[0] + display_width/4., center[1]), velocity=(0., -1.), color=(0, 0, 255))
them = Body(mass=1, radius=20, position=(center[0] - display_width/4., center[1]), velocity=(0., 1.), color=(255, 0, 0))

done = False    
while done == False:

    screen.fill(0)
    
    star.draw()
    
    for body in [us, them]:
        body.draw()
        force = body.compute_force(star)
        body.move(force)
    
    display.update()
    
    time.delay(delay)
    
    for e in event.get():
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                done = True

print "That took ", time.get_ticks()/1000, " seconds."