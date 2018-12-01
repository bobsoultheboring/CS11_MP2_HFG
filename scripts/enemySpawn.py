import pyglet, random
import assets, mapDraw, globalVar
from main import player

class Enemy(pyglet.sprite.Sprite):
    '''
    Base class for all enemy types
    Includes HP and damage
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Places the monster's 'callsign' inside globalVar.enemy_list
        self.index = len(globalVar.enemy_list)
        globalVar.enemy_list.append(self)
        globalVar.enemy_coord.append([self.x,self.y])

        self.move = 0
        self.moveX,self.moveY = 0,0
        self.direction = 0
        self.destination = []
        self.possibleDestinations = []

        self.playerFound = False
        self.moveWithPlayer = False

    def update(self):
        #Initiates a fight with the player if the monster attempts to occupy the player's spot
        if self.destination == player.coord:
            player.fight_enemy(globalVar.enemy_list[self.index])
            
        #Moves the monster and prevents them from colliding with other monsters
        #Also prevents them from occupying the same space as the player
        if self.destination not in globalVar.enemy_coord and self.destination != player.coord:
            self.x += self.moveX
            self.y += self.moveY
            
            #Updates the current coordinate of the monster to the globalVar.enemy_coord list
            globalVar.enemy_coord[self.index] = [self.x,self.y]
            
            self.moveX = 0
            self.moveY = 0

    #Removes all coordinates of obstacles from the possible destinations of the monster
    def randomPossibleDestinations(self):
        possible = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]
        for i in range(len(possible)-1,-1,-1):
            if possible[i] in globalVar.obstacle_coord:
                del(possible[i])
        self.possibleDestinations = possible

    #Sets destination to a random element in possibleDestinations
    def randomDestination(self):
        direct = random.randint(0,len(self.possibleDestinations)-1)
        self.destination = self.possibleDestinations[direct]
        self.moveX = self.destination[0] - self.x
        self.moveY = self.destination[1] - self.y

    #Returns invalid destinations as None type to preserve the index of the list
    def directPossibleDestinations(self):
        possible2 = [[self.x-30,self.y],[self.x+30,self.y],[self.x,self.y-30],[self.x,self.y+30]]
        for i in range(len(possible2)-1,-1,-1):
            if possible2[i] in globalVar.obstacle_coord:
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

        self.health = 1
        self.damage = 1       
        
    def update(self):
        #This enemy type only moves once every two 'turns'
        super(Small_monster,self).randomPossibleDestinations()
        super(Small_monster,self).randomDestination()
        if self.move < 4:
            self.move += 1
        elif self.move == 4:
            super(Small_monster,self).update()
            self.move = 0

class Medium_monster(Enemy):
    '''
    Subclass of enemy for medium monsters
    Includes logic for determining enemy movement
    This monster chases the player if they are within range
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.monsterMedium_img,*args,**kwargs)

        self.health = 2
        self.damage = 2       
        
    def update(self):
        #This enemy type only moves once every turns
        if self.move < 2:
            self.move += 1
        elif self.move == 2:
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
            self.move = 0        
        
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

        self.health = 3
        self.damage = 2       

        self.moveWithPlayer = True
        
    def update(self):
        #This enemy type only moves once every two 'turns'
        #Small monsters move randomly
        super(Large_monster,self).randomPossibleDestinations()
        super(Large_monster,self).randomDestination()
        if self.move < 1:
            self.globalFindPlayer()
            self.move += 1
        elif self.move == 1:
            super(Large_monster,self).directPossibleDestinations()
            super(Large_monster,self).directDestination()
            super(Large_monster,self).update()
            self.move = 0

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
    for obj in globalVar.enemy_list:
        if obj.moveWithPlayer == True:
            obj.update()
            