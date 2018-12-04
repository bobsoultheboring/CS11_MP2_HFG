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

        self.timer = []
        self.count = 0
        self.spawnTimer = 0
        self.wait = 15

        self.batch = batch

        self.item_list = []
        self.item_coord = []

        #location of all the individual spawners
        #self.locations = [[300,510]] #for debug
        self.locations = [[810,120],[390,270],[810,360],[600,300]]
        self.spawnerList = []

        for i in self.locations:
            self.item_list.append([])
            self.timer.append(0)
        
        for spawner in self.locations:
            self.spawnerList.append(pyglet.sprite.Sprite(img=assets.spawner_img,x=spawner[0],y=spawner[1],batch=batch))

    #Update function to spawn items
    #Spawns a monster once every eight 'turns'
    def update(self):
        for spawnInd in range(len(self.item_list)):
            if self.item_list[spawnInd] == []:
                self.timer[spawnInd] += 1
                if self.timer[spawnInd] == self.wait:
                    print('spawn at: ', spawnInd)
                    self.spawnItem(spawnInd)
                    self.timer[spawnInd] = 0
        # if self.spawnTimer < 1:
        #     self.spawnTimer += 1
        # elif self.spawnTimer == 1:
        #     print('Time to spawn!')
        #     print(self.timer,self.count,self.timer[self.count])
        #     if self.timer[self.count] > self.wait:
        #         print('spawn at: ', self.count)
        #         self.spawnItem(self.count)
        #         self.timer[self.count] = 0
        #         self.count += 1
        #     self.spawnTimer = 0

	#Decides which monster to spawn, spawns them in one of the spawner objects
    def spawnItem(self,itemInd):
        print('Spawning!')
        pickSpawn = ''
        if len(interface.Craving.prioIngreds) > 0:
            pickSpawn = random.choice(interface.Craving.prioIngreds)
            print(interface.Craving.prioIngreds)
            del interface.Craving.prioIngreds[interface.Craving.prioIngreds.index(pickSpawn)]
        else:
            pickSpawn = random.choice(CookBook.Ingredients)
        interface.Craving.item_names.append(pickSpawn)
        self.item_list[itemInd] = ItemEntity(img=assets.items_img[assets.items_img.index(pyglet.resource.image('{}.png'.format(pickSpawn)))] , 
            x=self.locations[itemInd][0], y=self.locations[itemInd][1], name = pickSpawn, spawnerID = itemSpawner_first,batch = self.batch)
        print('item_list: ',self.item_list)
        
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

        self.difficulty = 'normal'
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
        self.locations = [[600,510],[840,150],[240,240]]
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
            if possible[i] in self.obstacles.obstacle_coord or possible[i] in [[450,360],[480,420]]:
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
            if possible2[i] in self.obstacles.obstacle_coord or possible2[i] in [[450,360],[480,420]]:
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

        self.monsterType = 'small'

        self.spawner.monsterCount_small += 1
        
        self.health = 1
        self.damage = 5

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

        self.monsterType = 'medium'

        self.spawner.monsterCount_medium += 1
        
        self.health = 2
        self.damage = 10

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

        self.monsterType = 'large'

        self.spawner.monsterCount_large += 1
        
        self.health = 3
        self.damage = 10

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
    def __init__(self,obstacleID,spawnerID,itemID,*args,**kwargs):
        super().__init__(img=assets.playerF_img,*args,**kwargs)

        self.obstacles = obstacleID
        self.spawner = spawnerID
        self.iSpawner = itemID

        self.key_handler = key.KeyStateHandler()
        self.moveX,self.moveY = 0,0
        self.coord = [self.x,self.y]

        self.satiety = 100.0
        self.health = 10.0
        self.damage = 1

        self.dead = False
        self.retry = False

        self.nearItems = []
        self.onCooker = False

        self.nearbyTiles = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]

        self.highScore = '0'
        self.newHighScore = False

    def nearItemFinder(self):
        self.nearItems = []
        for n in itemSpawner_first.item_list:
            if n != []:
                if self.iSpawner.item_coord[self.iSpawner.item_list.index(n)] in self.nearbyTiles:
                    self.nearItems.append(n)

    def update(self):
        #Check if there are gettable items nearby
        self.nearbyTiles = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]
        itemNearby = False
        #Checks if player is standing on the cooking spot
        if [self.x,self.y] == [330,510]:
            self.onCooker = True
        else:
            self.onCooker = False
        if len(itemSpawner_first.item_coord) > 0:
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
            #Handles item consumption/use
            elif self.key_handler[key._1]:
                if self.onCooker == True and interface.inventory[0] != 'null':
                    CookBook.itemCook(interface.inventory[0])
                elif interface.inventory[0] != 'null':
                    CookBook.itemEat(interface.inventory[0])
                interface.inventory_update_subtract(interface.inventory[0])
            elif self.key_handler[key._2]:
                if self.onCooker == True and interface.inventory[1] != 'null':
                    CookBook.itemCook(interface.inventory[1])
                elif interface.inventory[1] != 'null':
                    CookBook.itemEat(interface.inventory[1])
                interface.inventory_update_subtract(interface.inventory[1])
            elif self.key_handler[key._3]:
                if self.onCooker == True and interface.inventory[2] != 'null':
                    CookBook.itemCook(interface.inventory[2])
                elif interface.inventory[2] != 'null':
                    CookBook.itemEat(interface.inventory[2])
                interface.inventory_update_subtract(interface.inventory[2])
            #Handles item pickup
            elif self.key_handler[key.SPACE]:
                    if itemNearby:
                        interface.item_get(self.nearItems[0])
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

            #Removes 1 satiety point every update if player isn't starving
            if self.satiety > 0:
                self.satiety -= 0.1

            #Logic for handling starvation
            if self.satiety <= 0:
                self.health -= 0.1

            #Triggers game over if health goes to 0
            if self.health <= 0:
                self.death()

            #Changes difficulty based on satiety
            if self.satiety >= 80: 
                self.spawner.difficulty = 'normal'
            elif 80 > self.satiety >= 65:
                self.spawner.difficulty = 'medium'
            elif 65 > self.satiety >= 45:
                self.spawner.difficulty = 'hard'

    #Reduces HP from both enemy and player based on their respective damages
    #Calls deletion of enemy if their HP reaches 0
    #Calls death of player if player HP reaches 0
    def fight_enemy(self,other_object):
        if self.dead == False:
            enemyindex = other_object.index
            other_object.health -= self.damage
            if self.satiety > 0:
                self.satiety -= other_object.damage
                if self.satiety < 0:
                    self.satiety = 0

            print('SP: ',self.satiety,'Enemy: ',other_object.health)
            
            if self.health <= 0:
                self.death()
            if other_object.health <= 0:
                if other_object.monsterType == 'small':
                    #Scoring:
                    player_score.addScore(10)

                    self.spawner.monsterCount_small -= 1
                elif other_object.monsterType == 'medium':
                    #Scoring:
                    player_score.addScore(30)

                    self.spawner.monsterCount_medium -= 1
                elif other_object.monsterType == 'large':
                    #Scoring:
                    player_score.addScore(50)

                    self.spawner.monsterCount_large -= 1

                del(self.spawner.enemy_coord[enemyindex])
                del(self.spawner.enemy_list[enemyindex])
                
                #Lowers the index of all monsters above the deleted monster by 1
                for index in range(enemyindex,len(self.spawner.enemy_list)):
                    self.spawner.enemy_list[index].index -= 1
                    
                other_object.delete()
            
    #Handles player death
    def death(self):
        self.dead = True
        interface.actionText.text = "You passed out."
        self.read_Score()
        self.highscorelabel = pyglet.text.Label(text = 'High Score',font_name='Arial Black',font_size=15, x=1055, y=350, 
            color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
        if int(player_score.Score_Label.text) > int(self.highScore):
            self.High_Score = pyglet.text.Label(text = player_score.Score_Label.text,font_name='Arial Black',font_size=40, x=1055, y=400, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
            self.NEWlabel = pyglet.text.Label(text = 'NEW',font_name='Arial Black',font_size=30, x=1055, y=450, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
            self.newHighScore = True
        elif int(player_score.Score_Label.text) <= int(self.highScore):
            self.High_Score = pyglet.text.Label(text = self.highScore,font_name='Arial Black',font_size=40, x=1055, y=400, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
        rToRespawn = pyglet.text.Label('Hold R to save score and exit',
                               font_name='Times New Roman',
                               font_size=14,
                               x=1055, y=175, color = (0,0,0,255),
                               anchor_x='center', anchor_y='center', batch=entity_batch)
        print('You Died')

    def read_Score(self):
        scoreFile = open('high_score.txt','r')
        self.highScore = scoreFile.readline().rsplit()[0]
        scoreFile.close()

    def timeup(self):
        interface.actionText.text = "You ran out of time."
        self.highscorelabel = pyglet.text.Label(text = 'High Score',font_name='Arial Black',font_size=15, x=1055, y=350, 
            color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
        if int(player_score.Score_Label.text) > int(self.highScore):
            self.High_Score = pyglet.text.Label(text = player_score.Score_Label.text,font_name='Arial Black',font_size=40, x=1055, y=400, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
            self.NEWlabel = pyglet.text.Label(text = 'NEW',font_name='Arial Black',font_size=30, x=1055, y=450, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
            self.newHighScore = True
        elif int(player_score.Score_Label.text) <= int(self.highScore):
            self.High_Score = pyglet.text.Label(text = self.highScore,font_name='Arial Black',font_size=40, x=1055, y=400, 
                color = (100,0,0,255), anchor_x = 'center', anchor_y = 'center', batch=entity_batch)
        rToRespawn = pyglet.text.Label('Hold R to save score & exit',
                               font_name='Times New Roman',
                               font_size=14,
                               x=1055, y=175, color = (0,0,0,255),
                               anchor_x='center', anchor_y='center', batch=entity_batch)


class Key_Command():
    def __init__(self,*args,**kwargs):

        self.key_handler = key.KeyStateHandler()
        self.retry = False

    def update(self):
        if self.key_handler[key.R]:
            self.retry = True


class SP_Bar(pyglet.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.satiety_img,*args, **kwargs)
        
        self.continueUpdate = True

    def update(self):
            self.scale_x = player.satiety/100 
        

class HP_Bar(pyglet.sprite.Sprite):
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.health_img,*args, **kwargs)

        self.continueUpdate = True

    def update(self):
        if self.scale > 0:
            self.continueUpdate = True
            self.scale = player.health/10
        else:
            self.continueUpdate = False

class Scoring:
    def __init__(self):
        self.Score_Label = pyglet.text.Label(text = '000000',font_name='Arial Black',font_size=20, x = (1280 - 100) , y = (720 - 150) , 
            color = (100,0,0,255), anchor_x = 'right', anchor_y = 'center', batch=entity_batch)
        self.Score = 0

    def addScore(self,points):
        self.Score += points
        self.Score_Label.text = '0'*(6-len(str(self.Score)))+'{}'.format(self.Score)

satiety = SP_Bar(x=125,y=205,batch=entity_batch)
satietyBar = pyglet.sprite.Sprite(img=assets.satietyBar_img,x=123,y=203,batch=entity_batch)
health = HP_Bar(x=125,y=75,batch=entity_batch)

player_score = Scoring()

obstacles_first = ObstacleGroup(obstacleFile='obstacles_first.txt',batch=entity_batch)
spawner_first = EnemySpawners(obstacleID=obstacles_first,batch=entity_batch)   
itemSpawner_first = ItemSpawning(batch = entity_batch)
keyCommand = Key_Command(batch = entity_batch) 
#player pos: x=480,y=150
player = Player(obstacleID=obstacles_first,spawnerID=spawner_first,itemID=itemSpawner_first,x=480,y=150,batch=entity_batch)
