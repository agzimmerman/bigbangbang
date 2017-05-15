import pygame
import random
import numpy as np

pygame.font.init()
fontsize = 20
myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
textstrings = ["Click and drag the mouse near your blue planet to throw a rock.", "Try to hit the red planet!"]

fps = 60
dt = 1.
G = 1.

pygame.init()
display_height = 800.
display_width = 800.
center = (display_height/2., display_width/2.)
screen = pygame.display.set_mode((int(display_height), int(display_width)))
pygame.display.set_caption('Big Bang! Bang!')

circle = pygame.image.load('pics/circle.png')

def color_surface(surface, red, green, blue):
    # https://gamedev.stackexchange.com/questions/26550/how-can-a-pygame-image-be-colored
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue
    
    
class Body:

    def __init__(self, mass=1., radius=1, position=(center[0], center[1]), velocity=(0,0), color=(255,255,255)):
        
        self.mass = mass
        self.radius = radius
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        
        self.pic = pygame.transform.scale(circle.copy(), (2*radius, 2*radius))
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
        
    def distance(self, position):
        r = self.position - position
        return np.sqrt(r.dot(r))
    
    def near(self, position):
        return (self.radius < self.distance(position)) and (self.distance(position) < 2*self.radius)
        
    def struck(self, other):
        return  self.distance(other.position) < (self.radius + other.radius)

star = Body(mass=200, radius=50)
us = Body(mass=10., radius=25, position=(center[0] + display_width/5., center[1]), velocity=(0., -1.), color=(0, 0, 255))
them = Body(mass=8., radius=20, position=(30, center[1]), velocity=(0., 0.7), color=(255, 0, 0))

clock = pygame.time.Clock()

aiming = False
done = False    
while done == False:
    clock.tick(fps)
    
    screen.fill(0)
    
    text = []
    for string in textstrings:
        text.append(myfont.render(string, False, (255, 255, 255)))
    linepos = 0
    for line in text:
        screen.blit(line, (10,linepos))
        linepos += 1.5*fontsize
    
    star.draw()
    

    for body in [us, them]:
        body.draw()
        if not aiming:
            force = body.compute_force(star)
            body.move(force)
        
    if 'rock' in locals():
        rock.draw()
            
        force = rock.compute_force(star) + rock.compute_force(us) + rock.compute_force(them)
        
        if not aiming:
            rock.move(force)
        
        for body in us, star, them:
            
            if rock.struck(body):
                
                del rock
                
                aiming = False # @todo Design a context for aiming
                
                if body == them:
                    textstrings = ["You win!"]
                    
                break

    pygame.display.update()
    
    for event in pygame.event.get():
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            press_position = np.array(event.pos).astype(float)
            if us.near(press_position):
                aiming = True
                rock = Body(mass=0.01, radius=5, position=press_position, color=(0, 255, 0))
        
        if event.type == pygame.MOUSEBUTTONUP:
            if aiming:
                release_position = np.array(event.pos).astype(float)
                rock.velocity=(press_position - release_position)/float(us.radius)
                aiming = False
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                done = True