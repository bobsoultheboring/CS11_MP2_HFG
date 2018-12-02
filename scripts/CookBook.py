#Ingredients = ['ham', 'cheese', 'mayonnaise', 'bread', 'chicken', 'fish', 
#    'soy sauce', 'garlic', 'salt & pepper', 'butter', 'leek', 'meat', 'parsley', 
#    'potatoes', 'onion', 'eggs', 'flour', 'sugar', 'milk', 'chocolate chips', 'pasta', 
#    'oranges', 'raspberries', 'strawberries', 'banana', 'lime', 'vanilla', 'mangoes']
Ingredients = ['ing1', 'ing2', 'ing3'] #removed 'null' for now
#########################################################################################
Drinks = ['orange juice', 'mango shake', 'four-fruit shake', 'strawberry cheesecake shake', 
    'home-made cola']
Food = ['ham sandwich', 'chicken sandwich', 'baked fish', 'salt crust', 'skillet steak', 
    'pork chop', 'basic cupcakes', 'basic cookies', 'stir fry', 'mac and cheese']
#########################################################################################

Recipe = {
    #Format:
    #    <FOOD> : (COOKING PLACE , INGREDIENTS as tuple)

    #Sandwich
    'ham sandwich' : ('microwave',
                        ('bread', 'ham', 'cheese', 'mayonnaise')), 
    'chicken sandwich' : ('microwave',
                        ('bread', 'chicken', 'mayonnaise')), 

    #Fish
    'baked fish' : ('oven',
                        ('fish', 'soy sauce', 'garlic', 'salt & pepper')), 
    'salt crust' : ('oven',
                        ('fish', 'salt & pepper', 'salt & pepper', 'butter', 'garlic', 'leek')), 

    #Meat
    'skillet steak' : ('stove',
                        ('meat', 'garlic', 'salt & pepper', 'butter', ' parsley', 'potatoes')),
    'pork chop' : ('stove',
                        ('meat', 'garlic', 'salt & pepper', 'onion')), 

    #Pastries
    'basic cupcakes' : ('oven',
                        ('eggs', 'flour', 'sugar', 'butter', 'milk')), 
    'basic cookies' : ('oven',
                        ('eggs', 'flour', 'sugar', 'butter', 'chocolate chips')), 

    #Pasta
    'stir fry' : ('stove',
                        ('pasta', 'chicken', 'soy sauce', 'garlic', 'parsley')), 
    'mac and cheese' : ('stove',
                        ('pasta', 'milk', 'cheese')), 

    #Drinks
    'orange juice' : ('blender',
                        ('sugar', 'oranges')),
    'mango juice' : ('blender',
                        ('sugar', 'milk', 'mangoes')),
    'strawberry cheesecake shake' : ('blender',
                        ('sugar', 'cheese', 'strawberries', 'vanilla')),
    'four-fruit shake' : ('blender',
                        ('oranges', 'raspberries', 'strawberries', 'banana', 'sugar')),
    'home-made cola' : ('blender',
                        ('sugar', 'sugar', 'lime', 'lime', 'vanilla', 'oranges'))
}