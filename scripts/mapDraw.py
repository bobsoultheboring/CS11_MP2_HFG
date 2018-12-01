import pyglet
import globalVar

#Reads from the "obstacles.txt" file and places the coordinates inside obstacle_coord
def read_obstacles():
	global obstacle_coord
	obs = open('obstacles.txt','r')
	readObstacles = True
	while readObstacles:
		line = obs.readline().rstrip().split()
		if line == [] or line[0] == 'Layer':
			pass
		elif line[0] == 'XXXXXX':
			readObstacles = False
			break
		else:
			obsX = 60+int(line[0])*30
			obsY = 90+int(line[1])*30
			obstacle_coord.append([obsX,obsY])
	obs.close()

#Turns the obstacle coordinates into sprites
def draw_obstacles(batch = None):
    obstacles = []
    for coordinate in globalVar.obstacle_coord:
        obstacles.append(pyglet.sprite.Sprite(img=obstacle_img,x=coordinate[0],
                                              y=coordinate[1],batch=batch))
    return obstacles
