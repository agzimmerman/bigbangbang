import pygame
import random
import numpy as np

# @todo Us vs. Them

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
        
    def struck(self, other):
        # Ideally Body would inherit from Sprite and this would use sprite.collide_circle(); but that has been hard to use.
        r = self.position - other.position
        return np.sqrt(r.dot(r)) < (self.radius + other.radius)

star = Body(mass=200, radius=50)
us = Body(mass=10., radius=25, position=(center[0] + display_width/5., center[1]), velocity=(0., -1.), color=(0, 0, 255))
them = Body(mass=8., radius=20, position=(30, center[1]), velocity=(0., 0.7), color=(255, 0, 0))

clock = pygame.time.Clock()

done = False    
while done == False:
    clock.tick(fps)
    
    screen.fill(0)
    
    star.draw()
    
    for body in [us, them]:
        body.draw()
        force = body.compute_force(star)
        body.move(force)
        
    if 'rock' in locals():
        rock.draw()
            
        force = rock.compute_force(star) + rock.compute_force(us) + rock.compute_force(them)
        rock.move(force)
        
        for body in us, star, them:
            
            if rock.struck(body):
                
                del rock
                
                assert 'rock' not in locals()
                
                if body == them:
                    print "You win!"
                    raw_input("Press the <ENTER> key to continue...")
                    
                break
    
    pygame.display.update()
    
    for event in pygame.event.get():
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            press_position = np.array(event.pos).astype(float)
        
        if event.type == pygame.MOUSEBUTTONUP:
            release_position = np.array(event.pos).astype(float)
            rock = Body(mass=0.01, radius=5, position=press_position, velocity=(press_position - release_position)/float(us.radius), color=(0, 255, 0))
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                done = True

print "That took ", pygame.time.get_ticks()/1000, " seconds."
