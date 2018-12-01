import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

background_img = pyglet.resource.image('background.png')
playerF_img = pyglet.resource.image('player_Front.png')
playerB_img = pyglet.resource.image('player_Back.png')
playerL_img = pyglet.resource.image('player_Left.png')
playerR_img = pyglet.resource.image('player_Right.png')
obstacle_img = pyglet.resource.image('obstacle.png')
monsterSmall_img = pyglet.resource.image('monster_small.png')
monsterMedium_img = pyglet.resource.image('monster_medium.png')
monsterLarge_img = pyglet.resource.image('monster_large.png')

def center_image(image):
    image.anchor_x = image.width//2
    image.anchor_y = image.height//2

center_image(background_img)
center_image(playerF_img)
center_image(playerB_img)
center_image(playerL_img)
center_image(playerR_img)
center_image(obstacle_img)
center_image(monsterSmall_img)
center_image(monsterMedium_img)
center_image(monsterLarge_img)