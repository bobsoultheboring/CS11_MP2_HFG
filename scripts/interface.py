import pyglet, random
import assets, CookBook

inventory = ['null','null','null']
display_batch = pyglet.graphics.Batch()

class FoodCrave():
    def __init__(self):
        #This is a sample counter, probably to be declared and modified somewhere else (e.g. entities). 
        #If implemented, it should increment after the player manages to complete a food.
        self.Priority = 1

        #Randomly picked food (if priority%3 != 0), or drink (if priority%3 == 0)
        self.To_Prepare = self.Get_FoodDrink(self.Priority)

        #LIST of Ingredients for craving
        #Ingredients that have been added to the respective "machine" can be removed from this list
        self.Ingredients = CookBook.Recipe.get(self.To_Prepare)[1]
        print(self.To_Prepare, self.Ingredients)

    def Get_FoodDrink(self,Priority):
        #This is a counter, probably to be declared and modified somewhere else (e.g. entities). 
        #It increments after the player manages to complete a food.

        if Priority%3 != 0: 
            return random.choice(CookBook.Food)
        else: 
            return random.choice(CookBook.Drinks)

Craving = FoodCrave()

class CravingBar(object):
    def __init__(self):
        self.CravingBar = [] #Should contain the Bar and the Slots
        self.Slots = [] #Should contain the item sprites in the slots
        self.Draw_CravingBar()
        self.Draw_Items_in_Slots()

    def Draw_CravingBar(self):
        #Header
        self.CravingBar.append(pyglet.sprite.Sprite(assets.CravingHeader_img, x = 1280/2, y = (720), batch = display_batch))

        #Slots
        self.temp_y = (720-assets.CravingHeader_img.height)+(assets.CravingHeader_img.height/2) #Position: CenterY of Bar
        
        self.temp_x = 1280//2
        self.temp_x -= ((14*2) + (assets.IngredientSlot_img.width*3))-7

        for i in range(6):
            self.temp_x += 7
            self.temp_x += assets.IngredientSlot_img.width//2
            self.CravingBar.append(pyglet.sprite.Sprite(img=assets.IngredientSlot_img,x=self.temp_x, y=self.temp_y, batch = display_batch))
            self.temp_x += assets.IngredientSlot_img.width//2
            self.temp_x += 7
            
    def Draw_Items_in_Slots(self):
        self.temp_x = 1280//2
        self.temp_x -= ((14*2) + (assets.IngredientSlot_img.width*3))-7

        for i in range(len(Craving.Ingredients)):
            _1 = random.choice(assets.CravingIngredients_img) #Randomized for now.
            _1.anchor_x = _1.width//2
            _1.anchor_y = _1.height//2

            self.temp_x += 7
            self.temp_x += assets.IngredientSlot_img.width//2
            self.Slots.append(pyglet.sprite.Sprite(img=_1, x=self.temp_x, y=self.temp_y, batch = display_batch))
            self.temp_x += assets.IngredientSlot_img.width//2
            self.temp_x += 7

CurrentCraving = CravingBar()

class Inventory_Slot():
    '''Controls the CONTENTS of the inventory slots. 
       The actual slots are drawn using draw_containers()''' 
    def __init__(self, x, anchorIndex,batch = None):
        self.x = x
        self.anchorindex = anchorIndex
        self.current_item_anchor = "null"
        self.current_item = assets.items_img[assets.items_img.index(pyglet.resource.image("null.png"))]
        self.item_display = pyglet.sprite.Sprite(img=self.current_item,x=self.x, y=90)
        self.item_description = pyglet.text.Label('',
                                font_name='Times New Roman',
                                font_size=10,
                                x=self.x, y=160, color = (0,0,0,255),
                                anchor_x='center', anchor_y='center', batch=display_batch)
    def update(self):
        self.current_item_anchor = inventory[self.anchorindex]
        self.current_item = assets.items_img[assets.items_img.index(pyglet.resource.image("{}.png".format(self.current_item_anchor)))]
        assets.center_image(self.current_item)
        self.item_display = pyglet.sprite.Sprite(img=self.current_item,x=self.x, y=75, batch=display_batch)
        if self.current_item_anchor == "null":
            self.item_description.text = "no item held"
        self.item_description.text = self.current_item_anchor
		

def draw_containers(batch = None):
    containers = []
    containerImage = assets.itemcontainer_img
    for coordinate in [905, 1055, 1205]:
        assets.center_image(assets.itemcontainer_img)
        containers.append(pyglet.sprite.Sprite(img=containerImage,x=coordinate, y=75, batch=batch))
    return containers
	
def inventory_update_add(item):
    if inventory[0] == "null":
        inventory[0] = item
    elif inventory[1] == "null":
        inventory [1] = item
    else:
        inventory[2] = item

def inventory_update_subtract(item):
    replacement_index = inventory.index(item)
    inventory[replacement_index] = 'null'

def item_get(itemEntity):
    if ("null" in inventory):
        inventory_update_add(itemEntity.itemName)
        print(inventory) ####### FOR DEBUG
        actionText.text = 'You picked up the {}'.format(itemEntity.itemName)
    else:
        actionText.text = 'Your inventory is full.'

slot_1 = Inventory_Slot(x = 905, anchorIndex = 0,batch=display_batch)
slot_2 = Inventory_Slot(x = 1055, anchorIndex = 1,batch=display_batch)
slot_3 = Inventory_Slot(x = 1205, anchorIndex = 2,batch=display_batch)
actionText = pyglet.text.Label('',
                               font_name='Times New Roman',
                               font_size=14,
                               x=1040, y=180, color = (0,0,0,255),
                               anchor_x='center', anchor_y='center', batch=display_batch)
inventory_slots = draw_containers(batch=display_batch)