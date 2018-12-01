import pyglet, random
import assets, mapDraw, enemySpawn, globalVar
from pyglet.window import key

gameWindow = pyglet.window.Window(1280,720)
main_batch = pyglet.graphics.Batch()

class Player(pyglet.sprite.Sprite):
    '''
    Player Class
    Includes movement with the WASD keys and prevents collision with obstacles
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(img=assets.playerF_img,*args,**kwargs)

        self.key_handler = key.KeyStateHandler()
        self.moveX,self.moveY = 0,0
        self.coord = [self.x,self.y]

        self.health = 10
        self.damage = 1

        self.dead = False

    def update(self):
        #Makes sure the player doesn't move after dying
        if self.dead == False:
            #WASD movement
            #Only one key is registered at a time
            if self.key_handler[key.A]:
                self.moveX = -30
                self.moveY = 0
                self.image=assets.playerL_img
                enemySpawn.moveLargeEnemies()
            elif self.key_handler[key.D]:
                self.moveX = 30
                self.moveY = 0
                self.image=assets.playerR_img
                enemySpawn.moveLargeEnemies()
            elif self.key_handler[key.S]:
                self.moveY = -30
                self.moveX = 0
                self.image=assets.playerF_img
                enemySpawn.moveLargeEnemies()
            elif self.key_handler[key.W]:
                self.moveY = 30
                self.moveX = 0
                self.image=assets.playerB_img
                enemySpawn.moveLargeEnemies()
            else:
                self.moveX = 0
                self.moveY = 0
            #Makes sure that the destination of the player is not blocked by an obstacle or an enemy
            destination = [self.x + self.moveX,self.y + self.moveY]
            if destination not in globalVar.obstacle_coord and destination not in globalVar.enemy_coord:
                self.x += self.moveX
                self.y += self.moveY
                self.moveX = 0
                self.moveY = 0
                self.coord = [self.x,self.y]

            #Initiates fight with enemy if the player tries to occupy the space of that enemy
            if destination in globalVar.enemy_coord:
                self.fight_enemy(globalVar.enemy_list[globalVar.enemy_coord.index(destination)])

    #Reduces HP from both enemy and player based on their respective damages
    #Calls deletion of enemy if their HP reaches 0
    #Calls death of player if player HP reaches 0
    def fight_enemy(self,other_object):
        enemyindex = other_object.index
        other_object.health -= self.damage
        self.health -= other_object.damage
        
        print('HP: ',self.health,'Enemy: ',other_object.health)
        
        if self.health <= 0:
            self.death()
        if other_object.health <= 0:
            del(globalVar.enemy_coord[enemyindex])
            del(globalVar.enemy_list[enemyindex])
            
            #Lowers the index of all monsters above the deleted monster by 1
            for index in range(enemyindex,len(globalVar.enemy_list)):
                globalVar.enemy_list[index].index -= 1
                
            other_object.delete()
            
    #Handles player death
    def death(self):
        self.dead = True
        print('You Died')
        gameWindow.remove_handlers(player.key_handler)

player = Player(x=120,y=150,batch=main_batch)

def main():
    global player
    background = pyglet.sprite.Sprite(img=assets.background_img,
                                      x=gameWindow.width//2,y=gameWindow.height//2)
    obstacle = mapDraw.draw_obstacles(main_batch)
    enemy = enemySpawn.Small_monster(x=120,y=240,batch=main_batch)
    enemy2 = enemySpawn.Small_monster(x=210,y=150,batch=main_batch)
    enemy3 = enemySpawn.Small_monster(x=120,y=360,batch=main_batch)
    enemy4 = enemySpawn.Medium_monster(x=300,y=120,batch=main_batch)
    enemy5 = enemySpawn.Medium_monster(x=240,y=300,batch=main_batch)
    enemy6 = enemySpawn.Large_monster(x=360,y=360,batch=main_batch)

    gameWindow.push_handlers(player.key_handler)

    def updatePlayer(dt):
        player.update()

    def updateEnemy(dt):
        for obj in globalVar.enemy_list:
            if obj.moveWithPlayer == False:
                obj.update()

    @gameWindow.event
    def on_draw():
        gameWindow.clear()
    
        background.draw()
        main_batch.draw()
    
    pyglet.clock.schedule_interval(updateEnemy,1/8.0)
    pyglet.clock.schedule_interval(updatePlayer,1/10.0)
    pyglet.app.run()
	
if __name__ == "__main__":
    main()
