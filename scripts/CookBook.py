import pyglet
import interface, entities

#Ingredients = ['ham', 'cheese', 'mayonnaise', 'bread', 'chicken', 'fish', 
#    'soy sauce', 'garlic', 'salt & pepper', 'butter', 'leek', 'meat', 'parsley', 
#    'potatoes', 'onion', 'eggs', 'flour', 'sugar', 'milk', 'chocolate chips', 'pasta', 
#    'oranges', 'raspberries', 'strawberries', 'banana', 'lime', 'vanilla', 'mangoes']
Ingredients = ['ing1', 'ing2', 'ing3'] #removed 'null' for now
#########################################################################################
Drinks = ['orange juice', 'mango shake', 'four-fruit shake', 'strawberry cheesecake shake', 
    'home-made cola']
Food = ['test food']
#Food = ['ham sandwich', 'chicken sandwich', 'baked fish', 'salt crust', 'skillet steak', 
#    'pork chop', 'basic cupcakes', 'basic cookies', 'stir fry', 'mac and cheese']
#########################################################################################

Recipe = {
    #Format:
    #    <FOOD> : (COOKING PLACE , INGREDIENTS as tuple)

    #Salad
    'test food' : ('pot',
                  ['ing1', 'ing2', 'ing3']),
    #Sandwich
    'ham sandwich' : ('microwave',
                        ['bread', 'ham', 'cheese', 'mayonnaise']), 
    'chicken sandwich' : ('microwave',
                        ['bread', 'chicken', 'mayonnaise']), 

    #Fish
    'baked fish' : ('oven',
                        ['fish', 'soy sauce', 'garlic', 'salt & pepper']), 
    'salt crust' : ('oven',
                        ['fish', 'salt & pepper', 'salt & pepper', 'butter', 'garlic', 'leek']), 

    #Meat
    'skillet steak' : ('stove',
                        ['meat', 'garlic', 'salt & pepper', 'butter', ' parsley', 'potatoes']),
    'pork chop' : ('stove',
                        ['meat', 'garlic', 'salt & pepper', 'onion']), 

    #Pastries
    'basic cupcakes' : ('oven',
                        ['eggs', 'flour', 'sugar', 'butter', 'milk']), 
    'basic cookies' : ('oven',
                        ['eggs', 'flour', 'sugar', 'butter', 'chocolate chips']), 

    #Pasta
    'stir fry' : ('stove',
                        ['pasta', 'chicken', 'soy sauce', 'garlic', 'parsley']), 
    'mac and cheese' : ('stove',
                        ['pasta', 'milk', 'cheese']), 

    #Drinks
    'orange juice' : ('blender',
                        ['sugar', 'oranges']),
    'mango juice' : ('blender',
                        ['sugar', 'milk', 'mangoes']),
    'strawberry cheesecake shake' : ('blender',
                        ['sugar', 'cheese', 'strawberries', 'vanilla']),
    'four-fruit shake' : ('blender',
                        ['oranges', 'raspberries', 'strawberries', 'banana', 'sugar']),
    'home-made cola' : ('blender',
                        ['sugar', 'sugar', 'lime', 'lime', 'vanilla', 'oranges'])
}

def itemEat(item):
    if(item in interface.Craving.ingreds):
        #Makes sure satiety doesn't go above 100
        if entities.player.satiety + 5 >= 100:
            entities.player.satiety = 100
        else:
            entities.player.satiety += 5
        interface.actionText.text = "Needs lamb sauce. And other ingredients."

        #Score:
        entities.player_score.addScore((interface.Timer.timeScore//6)*2) #"Perfect" score is 10
        interface.Timer.timeScore = 30
    else:
        interface.actionText.text = "You ate it. Nothing happened."

def itemCook(item):
    if(item in interface.Craving.ingreds):
        interface.actionText.text = "You added the {} into the cooking device."
        #Deletes the sprite of the ingredient
        print('delete',interface.Craving.Ingredients.index(item))
        interface.CurrentCraving.Slots[interface.Craving.ingreds.index(item)].delete()
        interface.Craving.ingreds[interface.Craving.ingreds.index(item)] = 'None'

        #If all the ingredients become 'None', restart craving, increases satiety, and adds score
        noneNum = 0
        for i in interface.Craving.ingreds:
            if i == 'None':
                noneNum += 1
            if noneNum == len(interface.Craving.ingreds):
                interface.actionText.text = "Finally. Some good fucking food."
                if entities.player.satiety + 40 >= 100:
                    entities.player.satiety = 100
                else:
                    entities.player.satiety += 40
                #Score:
                entities.player_score.addScore(20 * (interface.Timer.timeScore//6)) #Perfect score is 100
                interface.Timer.timeScore = 30

                interface.CurrentCraving.Slots = [] #Deletes the NoneType sprites in Slots
                interface.Craving.crave()
    else:
        interface.actionText.text = "The {} burned out of existence."