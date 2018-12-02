import pyglet, random
import assets, interface, CookBook
from pyglet.window import key

entity_batch = pyglet.graphics.Batch()

class ItemSpawning():
    '''
    Handles Itemspawns. Set at certain locations only.
    Based off of the EnemySpawners class.
    '''
    def __init__(self,batch,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.spawn = False

        self.timer = 0
        self.wait = 15

        self.batch = batch

        self.item_list = []
        self.item_coord = []

        #location of all the individual spawners
        #self.locations = [[500,510]] #original
        self.locations = [[290,510]] #for debug - location:blender in kitchen
        self.spawnerList = []
        
        for spawner in self.locations:
            self.spawnerList.append(pyglet.sprite.Sprite(img=assets.spawner_img,x=spawner[0],y=spawner[1],batch=batch))

    #Update function to spawn items
    #Spawns a monster once every eight 'turns'
    def update(self):
        if len(self.locations) > 0:
            self.checkCapacity()
            if self.spawn == True:
                if self.timer < self.wait:
                    self.timer += 1
                elif self.timer == self.wait:
                    self.spawnItem()
                    self.timer = 0
                
    #Checks if any items need to be spawned
    def checkCapacity(self):
        if len(self.item_list) < 1:
            self.spawn = True
        else:
            self.spawn = False

	#Decides which monster to spawn, spawns them in one of the spawner objects
    def spawnItem(self):
        pickSpawn = random.choice(CookBook.Ingredients)
        pick = [0,0,0,0,0,1,1,1,1,2]
        self.item_list.append(ItemEntity(img=assets.items_img[assets.items_img.index(pyglet.resource.image('{}.png'.format(pickSpawn)))] , 
            x=self.locations[0][0], y=self.locations[0][1], name = pickSpawn, spawnerID = itemSpawner_first))

class ItemEntity(pyglet.sprite.Sprite):
    def __init__(self,name,spawnerID,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Places the monster's 'callsign' inside enemy_list
        self.spawner = spawnerID
        self.index = len(self.spawner.item_list)
        self.spawner.item_coord.append([self.x,self.y])
        self.itemName = name

class ObstacleGroup():
    '''
    Collective class for all obstacles
    Blocks player and enemy movement
    '''
    def __init__(self,obstacleFile,batch,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.obstacle_coord = []
        self.obstacle_list = []
        self.obstacle_file = obstacleFile
        
        self.batch = batch

        self.readObstacles()
        self.drawObstacles()
    
    def readObstacles(self):
        obs = open(self.obstacle_file,'r')
        readObstacles = True
        while readObstacles:
            line = obs.readline().rstrip().split()
            if line == [] or line[0] == 'Layer':
                pass
            elif line[0] == 'XXXXXX':
                readObstacles = False
                break
            else:
                obsX = 180+int(line[0])*30
                obsY = 90+int(line[1])*30
                self.obstacle_coord.append([obsX,obsY])
        obs.close()

    def drawObstacles(self):
        for coordinate in self.obstacle_coord:
            self.obstacle_list.append(pyglet.sprite.Sprite(img=assets.obstacle_img,x=coordinate[0],
                                                            y=coordinate[1],batch=self.batch))

class EnemySpawners():
    '''
    Collective class for all objects that spawns enemies based on certain conditions
    Always maintains the same number of monsters based on difficulty
    Only spawns one monster at a time (Even with multiple spawners)
    '''
    def __init__(self,obstacleID,batch,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Normal difficulty - 4 monsters in total, should have at least 1 slime and 1 slug
        #                  - 80% chance to spawn slimes, 20% chance to spawn slugs
        #Medium difficulty - 6 monsters in total, should have at least 1 slimes and 2 slugs
        #                  - 60% change to spawn slimes, 30% change to spawn slugs, 10% change to spawn tallmen
        #Hard difficulty   - 7 monsers in total, should have at least 2 slugs and 1 tallmen
        #                  - 50% chance to spawn slimes, 40% chance to spawn slugs, 10% change to spawn tallmen

        self.difficulty = 'hard'
        self.spawn = False

        self.timer = 0
        self.wait = 15

        self.obstacles = obstacleID
        self.batch = batch

        self.monsterCount_small = 0
        self.monsterCount_medium = 0
        self.monsterCount_large = 0

        self.enemy_list = []
        self.enemy_coord = []

        #location of all the individual spawners
        self.locations = [[600,510]]
        self.spawnerList = []
        
        for spawner in self.locations:
            self.spawnerList.append(pyglet.sprite.Sprite(img=assets.spawner_img,x=spawner[0],y=spawner[1],batch=batch))

    #Update function to spawn monsters
    #Spawns a monster once every eight 'turns'
    def update(self):
        if len(self.locations) > 0:
            self.checkMonsters()
            if self.spawn == True:
                if self.timer < self.wait:
                    self.timer += 1
                elif self.timer == self.wait:
                    if self.difficulty == 'normal':
                        self.spawnMonster(1,1)
                    elif self.difficulty == 'medium':
                        self.spawnMonster(1,2)
                    elif self.difficulty == 'hard':
                        self.spawnMonster(0,2,1)
                    self.timer = 0
                
    #Checks if any monsters need to be spawned
    def checkMonsters(self):
        if self.difficulty == 'normal':
            if len(self.enemy_list) < 4:
                self.spawn = True
            else:
                self.spawn = False
        elif self.difficulty == 'medium':
            if len(self.enemy_list) < 6:
                self.spawn = True
            else:
                self.spawn = False
        elif self.difficulty == 'hard':
            if len(self.enemy_list) < 7:
                self.spawn = True
            else:
                self.spawn = False

    #Decides which monster to spawn, spawns them in one of the spawner objects
    def spawnMonster(self,slimeCount=0,slugCount=0,tallCount=0):
        pickSpawn = random.randint(0,len(self.spawnerList)-1)
        pick = []
        if self.difficulty == 'normal':
            pick = [0,0,0,0,0,0,0,0,1,1]
        elif self.difficulty == 'medium':
            pick = [0,0,0,0,0,0,1,1,1,2]
        elif self.difficulty == 'hard':
            pick = [0,0,0,0,0,1,1,1,1,2]
            
        if self.monsterCount_small < slimeCount:
            self.enemy_list.append(Small_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
        elif self.monsterCount_medium < slugCount:
            self.enemy_list.append(Medium_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
        elif self.monsterCount_large < tallCount:
            self.enemy_list.append(Large_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
        else:
            if self.difficulty == 'normal' or self.difficulty == 'medium':
                spin = random.randint(0,9)
                if pick[spin] == 0:
                    self.enemy_list.append(Small_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
                elif pick[spin] == 1:
                    self.enemy_list.append(Medium_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
            elif self.difficulty == 'hard':
                spin = random.randint(0,9)
                if pick[spin] == 0:
                    self.enemy_list.append(Small_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
                elif pick[spin] == 1:
                    self.enemy_list.append(Medium_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
                elif pick[spin] == 2:
                    self.enemy_list.append(Large_monster(spawnerID=spawner_first,obstacleID=self.obstacles,
                                                    x=self.locations[pickSpawn][0],y=self.locations[pickSpawn][1],batch=self.batch))
    
class Enemy(pyglet.sprite.Sprite):
    '''
    Base class for all enemy types
    Includes HP and damage
    '''
    def __init__(self,obstacleID,spawnerID,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Places the monster's 'callsign' inside enemy_list
        self.spawner = spawnerID
        self.index = len(self.spawner.enemy_list)
        self.spawner.enemy_coord.append([self.x,self.y])

        self.obstacles = obstacleID
        
        self.moveX,self.moveY = 0,0
        self.direction = 0
        self.destination = []
        self.possibleDestinations = []

        self.playerFound = False
        self.moveWithPlayer = False

    def update(self):
        #Initiates a fight with the player if the monster attempts to occupy the player's spot
        if self.destination == player.coord:
            player.fight_enemy(self.spawner.enemy_list[self.index])
            
        #Moves the monster and prevents them from colliding with other monsters
        #Also prevents them from occupying the same space as the player
        if self.destination not in self.spawner.enemy_coord and self.destination != player.coord:
            self.x += self.moveX
            self.y += self.moveY
            
            #Updates the current coordinate of the monster to the enemy_coord list
            self.spawner.enemy_coord[self.index] = [self.x,self.y]
            
            self.moveX = 0
            self.moveY = 0

    #Removes all coordinates of obstacles from the possible destinations of the monster
    def randomPossibleDestinations(self):
        possible = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]
        for i in range(len(possible)-1,-1,-1):
            if possible[i] in self.obstacles.obstacle_coord:
                del(possible[i])
            elif possible[i] in self.spawner.enemy_coord:
                del(possible[i])
        self.possibleDestinations = possible

    #Sets destination to a random element in possibleDestinations
    def randomDestination(self):
        if len(self.possibleDestinations) > 0:
            direct = random.randint(0,len(self.possibleDestinations)-1)
            self.destination = self.possibleDestinations[direct]
        else:
            self.destination = [self.x,self.y]
        self.moveX = self.destination[0] - self.x
        self.moveY = self.destination[1] - self.y

    #Returns invalid destinations as None type to preserve the index of the list
    def directPossibleDestinations(self):
        possible2 = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]
        for i in range(len(possible2)-1,-1,-1):
            if possible2[i] in self.obstacles.obstacle_coord:
                possible2[i] = None
            if possible2[i] in self.spawner.enemy_coord:
                possible2[i] = None
        self.possibleDestinations = possible2
        
    #Determines the direction of a monster that found the player and checks for walls
    def directDestination(self):
        order = []
        posDes = self.possibleDestinations
        if self.direction == 0:
            order = [posDes[0],posDes[2],posDes[3],posDes[1]]
        elif self.direction == 1:
            order = [posDes[1],posDes[2],posDes[3],posDes[0]]
        elif self.direction == 2:
            order = [posDes[2],posDes[0],posDes[1],posDes[3]]
        elif self.direction == 3:
            order = [posDes[3],posDes[0],posDes[1],posDes[2]]
        ordNum = 0
        while ordNum < 4:
            if order[ordNum] == None:
                ordNum += 1
            else:
                if ordNum == 1 and order[2] != None:
                    spin = random.randint(1,2)
                    self.destination = order[spin]
                    break
                else:
                    self.destination = order[ordNum]
                    break
        self.moveX = self.destination[0] - self.x
        self.moveY = self.destination[1] - self.y  
        
class Small_monster(Enemy):
    '''
    Subclass of enemy for small monsters
    Includes logic for determining enemy movement
    This monster moves randomly
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.monsterSmall_img,*args,**kwargs)

        self.spawner.monsterCount_small += 1
        
        self.health = 1
        self.damage = 1

        self.timer = 0
        self.wait = 3

    def update(self):
        #This enemy type only moves once every two 'turns'
        super(Small_monster,self).randomPossibleDestinations()
        super(Small_monster,self).randomDestination()
        if self.timer < self.wait:
            self.timer += 1
        elif self.timer == self.wait:
            super(Small_monster,self).update()
            self.timer = 0

class Medium_monster(Enemy):
    '''
    Subclass of enemy for medium monsters
    Includes logic for determining enemy movement
    This monster chases the player if they are within range
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.monsterMedium_img,*args,**kwargs)

        self.spawner.monsterCount_medium += 1
        
        self.health = 2
        self.damage = 2

        self.timer = 0
        self.wait = 1

    def update(self):
        #This enemy type only moves once every turn
        if self.timer < self.wait:
            self.timer += 1
        elif self.timer == self.wait:
            self.playerFound = True
            self.findPlayer()
            if self.playerFound == False:
                #If the player isn't found, the medium monster goes to a random direction
                self.randomPossibleDestinations()
                self.randomDestination()
            elif self.playerFound == True:
                super(Medium_monster,self).directPossibleDestinations()
                super(Medium_monster,self).directDestination()
            super(Medium_monster,self).update()
            self.timer = 0        
        
    def findPlayer(self):
        #Sets the enemy's line of sight. For Medium monsters that have an LoS of 4 tiles
        leftSide,rightSide,downSide,upSide = [],[],[],[]
        lowerLeft,lowerRight,upperLeft,upperRight = [],[],[],[]
        for i in range(1,5):
            leftSide.append([self.x-i*30,self.y])
            rightSide.append([self.x+i*30,self.y])
            downSide.append([self.x,self.y-i*30])
            upSide.append([self.x,self.y+i*30])
        for i in range(1,4):
            lowerLeft.append([self.x-i*30,self.y-30])
            lowerRight.append([self.x+i*30,self.y-30])
            upperLeft.append([self.x-i*30,self.y+30])
            upperRight.append([self.x+i*30,self.y+30])
            if i < 3:
                lowerLeft.append([self.x-i*30,self.y-60])
                lowerRight.append([self.x+i*30,self.y-60])
                upperLeft.append([self.x-i*30,self.y+60])
                upperRight.append([self.x+i*30,self.y+60])
            if i < 2:
                lowerLeft.append([self.x-i,self.y-90])
                lowerRight.append([self.x+i*30,self.y-90])
                upperLeft.append([self.x-i*30,self.y+90])
                upperRight.append([self.x+i*30,self.y+90])
            
        #Detects if the player is nearby and sets the direction towards them
        self.playerFound = True
        if player.coord in leftSide:
            self.direction = 0
        elif player.coord in rightSide:
            self.direction = 1
        elif player.coord in downSide:
            self.direction = 2
        elif player.coord in upSide:
            self.direction = 3
        elif player.coord in lowerLeft:
            spin = random.randint(0,1)
            if spin == 0:
                self.direction = 0
            elif spin == 1:
                self.direction = 2
        elif player.coord in lowerRight:
            spin = random.randint(0,1)
            if spin == 0:
                self.direction = 1
            elif spin == 1:
                self.direction = 2
        elif player.coord in upperLeft:
            spin = random.randint(0,1)
            if spin == 0:
                self.direction = 0
            elif spin == 1:
                self.direction = 3
        elif player.coord in upperRight:
            spin = random.randint(0,1)
            if spin == 0:
                self.direction = 1
            elif spin == 1:
                self.direction = 3
        else:
            self.playerFound = False

class Large_monster(Enemy):
    '''
    Subclass of enemy for large monsters
    Includes logic for determining enemy movement
    This monster knows where the player is
    Moves along with the player's actions
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.monsterLarge_img,*args,**kwargs)

        self.spawner.monsterCount_large += 1
        
        self.health = 3
        self.damage = 2

        self.timer = 0
        self.wait = 1

        self.moveWithPlayer = True
        
    def update(self):
        #This enemy type only moves once every two 'turns'
        #Small monsters move randomly
        super(Large_monster,self).randomPossibleDestinations()
        super(Large_monster,self).randomDestination()
        if self.timer < self.wait:
            self.globalFindPlayer()
            self.timer += 1
        elif self.timer == self.wait:
            super(Large_monster,self).directPossibleDestinations()
            super(Large_monster,self).directDestination()
            super(Large_monster,self).update()
            self.timer = 0

    #Determines direction nearest to the player
    def globalFindPlayer(self):
        distance = []
        for i in range(2):
            distance.append(player.coord[i] - [self.x,self.y][i])
        difference = abs(distance[0]) - abs(distance[1])
        if difference > 0:
            if distance[0] < 0:
                self.direction = 0
            elif distance[0] > 0:
                self.direction = 1
        elif difference < 0:
            if distance[1] < 0:
                self.direction = 2
            elif distance[1] > 0:
                self.direction = 3

def moveLargeEnemies():
    #Moves enemies that move along with player
    for obj in spawner_first.enemy_list:
        if obj.moveWithPlayer == True:
            obj.update()

class Player(pyglet.sprite.Sprite):
    '''
    Player Class
    Includes movement with the WASD keys and prevents collision with obstacles
    '''
    def __init__(self,obstacleID,spawnerID,*args,**kwargs):
        super().__init__(img=assets.playerF_img,*args,**kwargs)

        self.obstacles = obstacleID
        self.spawner = spawnerID

        self.key_handler = key.KeyStateHandler()
        self.moveX,self.moveY = 0,0
        self.coord = [self.x,self.y]

        self.health = 10
        self.damage = 1
        self.dead = False
        self.nearItems = []
    def nearItemFinder(self):
        self.nearItems = []
        for n in itemSpawner_first.item_list:
            if((abs(self.x - itemSpawner_first.item_coord[itemSpawner_first.item_list.index(n)][0]) < 90) and 
                (abs(self.y - itemSpawner_first.item_coord[itemSpawner_first.item_list.index(n)][1]) < 90)):
                self.nearItems.append(n)
    def update(self):
        #Check if there are gettable items nearby
        itemNearby = False
        if len(itemSpawner_first.item_list) > 0:
            self.nearItemFinder()
            if len(self.nearItems) > 0:
                itemNearby = True
        #Makes sure the player doesn't move after dying
        if self.dead == False:
            #WASD movement
            #Only one key is registered at a time
            if self.key_handler[key.A]:
                self.moveX = -30
                self.moveY = 0
                self.image=assets.playerL_img
                moveLargeEnemies()
            elif self.key_handler[key.D]:
                self.moveX = 30
                self.moveY = 0
                self.image=assets.playerR_img
                moveLargeEnemies()
            elif self.key_handler[key.S]:
                self.moveY = -30
                self.moveX = 0
                self.image=assets.playerF_img
                moveLargeEnemies()
            elif self.key_handler[key.W]:
                self.moveY = 30
                self.moveX = 0
                self.image=assets.playerB_img
                moveLargeEnemies()
            elif self.key_handler[key.SPACE]:
                    if itemNearby:
                        interface.item_get(self.nearItems[0])
                        print(itemSpawner_first.item_list[itemSpawner_first.item_list.index(self.nearItems[0])])
                        del itemSpawner_first.item_list[itemSpawner_first.item_list.index(self.nearItems[0])]
                    else:
	                    interface.actionText.text = "There's nothing here."
            else:
                self.moveX = 0
                self.moveY = 0
            #Makes sure that the destination of the player is not blocked by an obstacle or an enemy
            destination = [self.x + self.moveX,self.y + self.moveY]
            if destination not in self.obstacles.obstacle_coord and destination not in self.spawner.enemy_coord:
                self.x += self.moveX
                self.y += self.moveY
                self.moveX = 0
                self.moveY = 0
                self.coord = [self.x,self.y]

            #Initiates fight with enemy if the player tries to occupy the space of that enemy
            if destination in self.spawner.enemy_coord:
                self.fight_enemy(self.spawner.enemy_list[self.spawner.enemy_coord.index(destination)])

    #Reduces HP from both enemy and player based on their respective damages
    #Calls deletion of enemy if their HP reaches 0
    #Calls death of player if player HP reaches 0
    def fight_enemy(self,other_object):
        if self.dead == False:
            enemyindex = other_object.index
            other_object.health -= self.damage
            self.health -= other_object.damage

            print('HP: ',self.health,'Enemy: ',other_object.health)
            
            if self.health <= 0:
                self.death()
            if other_object.health <= 0:
                del(self.spawner.enemy_coord[enemyindex])
                del(self.spawner.enemy_list[enemyindex])
                
                #Lowers the index of all monsters above the deleted monster by 1
                for index in range(enemyindex,len(self.spawner.enemy_list)):
                    self.spawner.enemy_list[index].index -= 1
                    
                other_object.delete()
            
    #Handles player death
    def death(self):
        self.dead = True
        print('You Died')
         
obstacles_first = ObstacleGroup(obstacleFile='obstacles_first.txt',batch=entity_batch)
spawner_first = EnemySpawners(obstacleID=obstacles_first,batch=entity_batch)   
itemSpawner_first = ItemSpawning(batch = entity_batch) 
player = Player(obstacleID=obstacles_first,spawnerID=spawner_first,x=480,y=150,batch=entity_batch)
