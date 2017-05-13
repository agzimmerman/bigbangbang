from pygame import *
import random
import numpy as np

partpic = image.load('part.png')
partpic.set_colorkey((0,0,0))
big_partpic = transform.scale2x(partpic)
width, height = partpic.get_size()

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

masses = [1., 1., 1.]
starting_positions = [(center[0], center[1]), (center[0] + display_width/4., center[1]), (center[0] - display_width/4., center[1])]
starting_velocities = [(0., 0.), (0., -1.), (0., 1.)]

parts = []
for ip in range(partcount):
    parts.append(dict)
    parts[ip] = {'mass': masses[ip], 'x': starting_positions[ip][0], 'y': starting_positions[ip][1], 'u': starting_velocities[ip][0], 'v': starting_velocities[ip][1]}

    
done = False    
while done == False:

    screen.fill(0)
    
    screen.blit(big_partpic, (int(round(parts[0]['x']))  - width, int(round(parts[0]['y']))  - height))
    
    for ip in range(1, partcount):
        screen.blit(partpic, (int(round(parts[ip]['x'])) - width/2, int(round(parts[ip]['y'])) - height/2))
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