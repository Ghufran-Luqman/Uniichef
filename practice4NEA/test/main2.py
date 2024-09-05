import sqlite3
'''
        recipe_name text,
        prep_time text,
        cook_time text,
        total_time text,
        servings integer,
        yield text,
        ingredients text,
        directions text,
        rating real,
        url text,
        cuisine_path text,
        nutrition text,
        timing text,
        img_src text
'''
conn = sqlite3.connect("recipes.db")
c = conn.cursor()


#-----------------ingredients-----------------#

c.execute("SELECT ingredients FROM tableofrecipes")
row = c.fetchall()
#for item in row:
    #item = item[0]#this is for fetchall
    #item = [ingredient.strip() for ingredient in item.split(',')]#turns it into a list
    #print(item)
print(row)
#---------------------------------------------#
#------------------directions-----------------#
#note: these two methods work for all of them except ingredients
'''
c.execute("SELECT directions FROM tableofrecipes")
row = c.fetchone()
row = row[0]
print(row)
'''

'''
c.execute("SELECT directions FROM tableofrecipes")
row = c.fetchmany(3)
for item in row:
    item = list(item)
    item2 = item[0]
    item.pop(0)
    print(item2)
'''
#---------------------------------------------#

conn.close()
