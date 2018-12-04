import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

firstFloor_img = pyglet.resource.image('first_floor.png')
playerF_img = pyglet.resource.image('player_Front.png')
playerB_img = pyglet.resource.image('player_Back.png')
playerL_img = pyglet.resource.image('player_Left.png')
playerR_img = pyglet.resource.image('player_Right.png')
obstacle_img = pyglet.resource.image('obstacle.png')
monsterSmall_img = pyglet.resource.image('monster_small.png')
monsterMedium_img = pyglet.resource.image('monster_medium.png')
monsterLarge_img = pyglet.resource.image('monster_large.png')
spawner_img = pyglet.resource.image('enemy_spawner.png')
itemcontainer_img = pyglet.resource.image('itemcontainer.png')
craving_bg = pyglet.resource.image('temporaryCravingBG.png')
#item images
items_img = [pyglet.resource.image("null.png"), pyglet.resource.image("ing1.png"), pyglet.resource.image("ing2.png"), pyglet.resource.image("ing3.png")]
food_img = [pyglet.resource.image("test food.png")]
###Additions:
#Ingredients for CravingHeader_img
CravingIngredients_img = [pyglet.resource.image("ing1.png"), pyglet.resource.image("ing2.png"), pyglet.resource.image("ing3.png")]
#Cravings Bar
CravingHeader_img = pyglet.resource.image('cravebar.png')
CravingHeader_img.anchor_x = CravingHeader_img.width//2
CravingHeader_img.anchor_y = CravingHeader_img.height

IngredientSlot_img = pyglet.resource.image('ingredslot.png')

#Additional assets for the craving bar
CravingPlate_img = pyglet.resource.image('foodplate.png')
CravingArrow_img = pyglet.resource.image('foodarrow.png')


health_img = pyglet.resource.image('red.png')
satiety_img = pyglet.resource.image('blue.png')

satietyBar_img = pyglet.resource.image('satietybar.png')
cookSpot_img = pyglet.resource.image('cookSpot.png')

def center_image(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

center_image(firstFloor_img)
center_image(playerF_img)
center_image(playerB_img)
center_image(playerL_img)
center_image(playerR_img)
center_image(obstacle_img)
center_image(monsterSmall_img)
center_image(monsterMedium_img)
center_image(monsterLarge_img)
center_image(spawner_img)
center_image(craving_bg)
center_image(IngredientSlot_img)
center_image(health_img)
satiety_img.anchor_y = satiety_img.width//2
satietyBar_img.anchor_y = satiety_img.width//2
center_image(CravingPlate_img)
center_image(CravingArrow_img)
center_image(cookSpot_img)

for i in items_img:
    center_image(i)
for i in food_img:
    center_image(i)

