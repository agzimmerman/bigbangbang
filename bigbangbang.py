from pygame import *
import random
import numpy as np

# @todo Us vs. Them

partcount = 3
delay = 100
dt = 1.
G = 200.

init()
display_height = 640.
display_width = 640.
center = (display_height/2., display_width/2.)
screen = display.set_mode((int(display_height), int(display_width)))
display.set_caption('Big Bang! Bang!')

# @todo How to just change white pixels to a different color? Otherwise I need to make a new partpic that has a transparent background.

def color_surface(surface, red, green, blue):
    # https://gamedev.stackexchange.com/questions/26550/how-can-a-pygame-image-be-colored
    arr = surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue
    

partpic = image.load('pics/circle.png')
partpic = transform.scale(partpic, (30, 30))
partpic.set_colorkey((0,0,0))
partpic.convert_alpha()
blue_partpic = partpic.copy()
red_partpic = partpic.copy()
color_surface(blue_partpic, 0, 0, 255)
color_surface(red_partpic, 255, 0, 0)
big_partpic = transform.scale2x(partpic)
width, height = partpic.get_size()

print width, height

masses = [1., 1., 1.]
starting_positions = [(center[0], center[1]), (center[0] + display_width/4., center[1]), (center[0] - display_width/4., center[1])]
starting_velocities = [(0., 0.), (0., -1.), (0., 1.)]

parts = []
for ip in range(partcount):
    parts.append(dict)
    parts[ip] = {'mass': masses[ip], 'x': starting_positions[ip][0], 'y': starting_positions[ip][1], 'u': starting_velocities[ip][0], 'v': starting_velocities[ip][1], 'pic': partpic}
    
parts[0]['pic'] = big_partpic
parts[1]['pic'] = blue_partpic
parts[2]['pic'] = red_partpic
    
done = False    
while done == False:

    screen.fill(0)
    
    screen.blit(parts[0]['pic'], (int(round(parts[0]['x']))  - width, int(round(parts[0]['y']))  - height))
    
    for ip in range(1, partcount):
        screen.blit(parts[ip]['pic'], (int(round(parts[ip]['x'])) - width/2, int(round(parts[ip]['y'])) - height/2))
        parts[ip]['x'] += parts[ip]['u']*dt
        parts[ip]['y'] += parts[ip]['v']*dt
        rx = (parts[ip]['x'] - parts[0]['x'])
        ry = (parts[ip]['y'] - parts[0]['y'])
        r = np.sqrt(rx**2 + ry**2)
        F = G*parts[0]['mass']*parts[ip]['mass']/r**2*np.array((rx, ry))/np.sqrt(rx**2 + ry**2)
        a = -F/parts[ip]['mass']
        parts[ip]['u'] += a[0]*dt
        parts[ip]['v'] += a[1]*dt
    
    display.update()    
    time.delay(delay)
    
    for e in event.get():
        if e.type == KEYUP:
            if e.key == K_ESCAPE:
                done = True

print "You lasted for", time.get_ticks()/1000, "seconds!"