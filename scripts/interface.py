import pyglet, random
import assets, CookBook, entities

inventory = ['null','null','null']
display_batch = pyglet.graphics.Batch()

class Countdown(object):
    def __init__(self, time):
        self.lazy_timecheck = 840 #14 minutes = 840
        self.time = time
        self.timeScore = 30
        self.time_display = pyglet.text.Label(('8:00'),
            font_name = 'Arial Black',
            font_size = 50,
            x = (1280 - 100) , y = (720 - 100),
            color = (0,0,0,255),
            anchor_x = 'right', anchor_y = 'center',
            batch = display_batch)
        #AM/PM label
        self.timePartition = pyglet.text.Label('PM',
            font_name = 'Arial Black',
            font_size = 20,
            x = (1280 - 100) , y = (720 - 60),
            color = (0,0,0,255),
            anchor_x = 'right', anchor_y = 'center',
            batch = display_batch)
 
    def update(self):
        #For scoring:
        self.timeScore -= 1

        self.time += 1
        self.lazy_timecheck -= 1
        self.mins = self.time//60
        self.secs = self.time%60
        if self.mins >= 12:
            self.timePartition.text = 'AM'
        if self.mins > 12:
            self.mins -= 12 
        if self.secs >= 10:
            self.time_display.text = '{}:{}'.format(self.mins, self.secs)
        else:
            self.time_display.text = '{}:0{}'.format(self.mins, self.secs)
 
        return self.lazy_timecheck

class FoodCrave():
    def __init__(self):
        #This is a sample counter, probably to be declared and modified somewhere else (e.g. entities). 
        #If implemented, it should increment after the player manages to complete a food.
        self.Priority = 0

        #Randomly picked food (if priority%3 != 0), or drink (if priority%3 == 0)
        self.To_Prepare = self.Get_FoodDrink(self.Priority)

        #LIST of Ingredients for craving
        #Ingredients that have been added to the respective "machine" can be removed from this list
        self.Ingredients = CookBook.Recipe.get(self.To_Prepare)[1]

        print(self.To_Prepare, self.Ingredients)
        self.item_names = []
        #Edit this to preserve Cookbook's dictionary
        self.ingreds = []
        self.prioIngreds = []
        for ing in self.Ingredients:
            self.ingreds.append(ing)
            self.prioIngreds.append(ing)

    def Get_FoodDrink(self,Priority):
        #This is a counter, probably to be declared and modified somewhere else (e.g. entities). 
        #It increments after the player manages to complete a food.

        if Priority%3 != 0: 
            return random.choice(CookBook.Food)
        else: 
            #return random.choice(CookBook.Drinks)
            return random.choice(CookBook.Food)

    def crave(self):
        self.Priority += 1
        self.To_Prepare = self.Get_FoodDrink(self.Priority)
        self.Ingredients = CookBook.Recipe.get(self.To_Prepare)[1]
        self.ingreds = []
        self.prioIngreds = []
        for ing in self.Ingredients:
            self.ingreds.append(ing)
            self.prioIngreds.append(ing)
        for ing in range(len(self.prioIngreds)-1,-1,-1):
            if self.prioIngreds[ing] in self.item_names:
                del self.prioIngreds[ing]
        print('prioIngreds: ',self.prioIngreds)
        print(self.To_Prepare, self.Ingredients)
        CurrentCraving.Draw_Craving()
        CurrentCraving.Draw_Items_in_Slots(self.Ingredients)

class CravingBar(object):
    def __init__(self):

        self.CravingBar = [] #Should contain the Bar and the Slots
        self.Slots = [] #Should contain the item sprites in the slots
        self.Draw_CravingBar()

        #Draws craving plate and arrow beside the ingredients
        self.cravePlate = pyglet.sprite.Sprite(assets.CravingPlate_img,x = 1280//2-350,y=640,batch=display_batch)
        self.craveArrow = pyglet.sprite.Sprite(assets.CravingArrow_img,x = 1280//2-270,y=650,batch=display_batch)
        self.cookSpot = pyglet.sprite.Sprite(assets.cookSpot_img,x = 1280//2-240,y=650,batch=display_batch)
        self.craving = pyglet.sprite.Sprite(assets.items_img[0],x = 1280//2-350,y=660,batch=display_batch)

    def Draw_Craving(self):
        self.craving.image = assets.food_img[CookBook.Food.index(Craving.To_Prepare)]
	
    def Draw_CravingBar(self):
        #Header
        self.CravingBar.append(pyglet.sprite.Sprite(assets.CravingHeader_img, x = 1280/2, y = (720), batch = display_batch))

        #Slots
        self.temp_y = (720-assets.CravingHeader_img.height)+(assets.CravingHeader_img.height/2) #Position: CenterY of Bar
        
        self.temp_x = 1280//2-50
        self.temp_x -= ((14*2) + (assets.IngredientSlot_img.width*3))-7

        for i in range(6):
            self.temp_x += 7
            self.temp_x += assets.IngredientSlot_img.width//2
            self.CravingBar.append(pyglet.sprite.Sprite(img=assets.IngredientSlot_img,x=self.temp_x, y=self.temp_y, batch = display_batch))
            self.temp_x += assets.IngredientSlot_img.width//2
            self.temp_x += 7
            
    def Draw_Items_in_Slots(self, ingredients):
        self.temp_x = 1280//2-50
        self.temp_x -= ((14*2) + (assets.IngredientSlot_img.width*3))-7
        for i in (ingredients):
            _1 = assets.items_img[CookBook.Ingredients.index(i) + 1] 
            _1.anchor_x = _1.width//2
            _1.anchor_y = _1.height//2

            self.temp_x += 7
            self.temp_x += assets.IngredientSlot_img.width//2
            self.Slots.append(pyglet.sprite.Sprite(img=_1, x=self.temp_x, y=self.temp_y, batch = display_batch))
            self.temp_x += assets.IngredientSlot_img.width//2
            self.temp_x += 7
        
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
                                x=self.x, y=150, color = (0,0,0,255),
                                anchor_x='center', anchor_y='center', batch=display_batch)
    def update(self):
        self.current_item_anchor = inventory[self.anchorindex]
        self.current_item = assets.items_img[assets.items_img.index(pyglet.resource.image("{}.png".format(self.current_item_anchor)))]
        assets.center_image(self.current_item)
        self.item_display = pyglet.sprite.Sprite(img=self.current_item,x=self.x, y=75, batch=display_batch)
        if self.current_item_anchor == "null":
            self.item_description.text = ''
        else:
            self.item_description.text = self.current_item_anchor
		

def draw_containers(batch = None):
    containers = []
    containerImage = assets.itemcontainer_img
    for coordinate in [955, 1055, 1155]:
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
        del Craving.item_names[Craving.item_names.index(itemEntity.itemName)]
        entities.itemSpawner_first.item_list[entities.itemSpawner_first.item_list.index(entities.player.nearItems[0])].delete()
        entities.itemSpawner_first.item_list[entities.itemSpawner_first.item_list.index(entities.player.nearItems[0])] = []
        print(inventory) ####### FOR DEBUG
        actionText.text = 'You picked up the {}'.format(itemEntity.itemName)
    else:
        actionText.text = 'Your inventory is full.'

slot_1 = Inventory_Slot(x = 955, anchorIndex = 0,batch=display_batch)
slot_2 = Inventory_Slot(x = 1055, anchorIndex = 1,batch=display_batch)
slot_3 = Inventory_Slot(x = 1155, anchorIndex = 2,batch=display_batch)
actionText = pyglet.text.Label('',
                               font_name='Times New Roman',
                               font_size=14,
                               x=1055, y=200, color = (0,0,0,255),
                               anchor_x='center', anchor_y='center', batch=display_batch)
inventory_slots = draw_containers(batch=display_batch)
Timer = Countdown(time = 480)
Craving = FoodCrave()
CurrentCraving = CravingBar()
Craving.crave()