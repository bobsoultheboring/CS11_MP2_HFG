import pyglet, random
import assets, entities, interface
from pyglet.window import key

gameWindow = pyglet.window.Window(1280,720)

def updateItemsUI(dt):
    entities.itemSpawner_first.update()
    interface.slot_1.update()
    interface.slot_2.update()
    interface.slot_3.update()

changeScore = False

def firstFloor():
    firstFloorBackground = pyglet.sprite.Sprite(img=assets.firstFloor_img,
                                      x=gameWindow.width//2,y=gameWindow.height//2)

    playerStats = [entities.satiety,entities.health]
    
    gameWindow.push_handlers(entities.player.key_handler)

    def updatePlayerFirst(dt):
        global changeScore
        entities.player.update()
        entities.keyCommand.update()
        if entities.player.dead == True:
            pyglet.clock.unschedule(Game_Timer)
            gameWindow.remove_handlers(entities.player.key_handler)
            gameWindow.push_handlers(entities.keyCommand.key_handler)
        for obj in playerStats:
            if obj.continueUpdate == True:
                obj.update()
        #Restarts game if the player chooses to
        if entities.keyCommand.retry == True:
            pyglet.app.exit()
        #Activates changing of high score
        if entities.player.newHighScore == True:
            changeScore = True

    def updateEnemyFirst(dt):
        entities.spawner_first.update()
        for obj in entities.spawner_first.enemy_list:
            if obj.moveWithPlayer == False:
                obj.update()    

    def Game_Timer(dt):
        time_check = interface.Timer.update()
        if time_check == 0:
            entities.player.timeup()
            interface.Timer.time_display.text = 'Time\'s Up!'
            interface.Timer.time_display.font_size = 20

            entities.player.dead = True
            pyglet.clock.unschedule(updateEnemyFirst)
            pyglet.clock.unschedule(updateItemsUI)
                

    @gameWindow.event
    def on_draw():
        gameWindow.clear()
    
        firstFloorBackground.draw()
        entities.entity_batch.draw()
        interface.display_batch.draw()
    
    pyglet.clock.schedule_interval(Game_Timer, 1)
    pyglet.clock.schedule_interval(updateEnemyFirst,1/4.0)
    pyglet.clock.schedule_interval(updatePlayerFirst,1/10.0)
    pyglet.clock.schedule_interval(updateItemsUI, 1/10.0)
    pyglet.app.run()
	
if __name__ == "__main__":
    firstFloor()

if changeScore == True:
    scoreFile = open('high_score.txt','w')
    scoreFile.write(entities.player_score.Score_Label.text)
    scoreFile.close()