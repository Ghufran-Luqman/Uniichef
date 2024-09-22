import sqlite3

conn = sqlite3.connect("recipes.db")
c = conn.cursor()

'''
c.execute("""CREATE TABLE tableofrecipes (
          id text,
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
          )""")
'''
#c.execute("SELECT * FROM tableofrecipes")
#i = c.fetchall()
#print(i)


#c.execute("SELECT * FROM tableofrecipes WHERE recipe_name='Caramel Apples'")
#duplicates = c.fetchall()
#print(f"These are duplicates: {duplicates}")

#tableofrecipes has a bunch of duplicates in so im making a second table that removes all the duplicates

'''
c.execute("""CREATE TABLE tableofrecipes2 (
          id text,
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
          )""")

conn.commit()
'''
'''
c.execute("""INSERT INTO tableofrecipes2
            SELECT DISTINCT * FROM tableofrecipes
            """)

conn.commit()
'''
'''
c.execute("SELECT recipe_name FROM tableofrecipes2")
test = c.fetchall()
print(test)
'''
'''
c.execute("DELETE FROM tableofrecipes2 WHERE prep_time IS NULL")
c.execute("DELETE FROM tableofrecipes2 WHERE cook_time IS NULL")
c.execute("DELETE FROM tableofrecipes2 WHERE total_time IS NULL")
conn.commit()
'''
'''
name = "Ma'amoul (Lebanese Date Cookies)"
string = "2 cups semolina flour, 1 cup all-purpose flour, ½ teaspoon ground mahlab, ½ teaspoon salt, 1 cup clarified butter at room temperature, 5 tablespoons milk, 2 tablespoons white sugar, 1 teaspoon active dry yeast, 4 tablespoons orange blossom water or more as needed, 10 tablespoons date paste (such as Ziyad®), cut into small pieces, 2 tablespoons powdered sugar or to taste"
c.execute("""UPDATE tableofrecipes2
            SET
            ingredients = REPLACE(?, ?, "2 cups semolina flour, 1 cup all-purpose flour, ½ teaspoon ground mahlab, ½ teaspoon salt, 1 cup clarified butter at room temperature, 5 tablespoons milk, 2 tablespoons white sugar, 1 teaspoon active dry yeast, 4 tablespoons orange blossom water or more as needed, 10 tablespoons date paste (such as Ziyad®) cut into small pieces, 2 tablespoons powdered sugar or to taste")
            WHERE recipe_name=?""", (string, string, name,))
conn.commit()
'''
#c.execute("DELETE FROM tableofrecipes2 WHERE recipe_name='Cream Cheese Banana Bread'")
#conn.commit()

#c.execute("SELECT COUNT(*) FROM tableofrecipes2")
#t = c.fetchall()
#print(t)
#GET RID OF ROWS WITHOUT PREP TIME, COOK TIME AND TOTAL TIME.
#CHECK FOR EVERY ONE OF THEM IF THE INGREDIENTS ARE OK WITH THE WEIRD COMMAS

'''
c.execute("""CREATE TABLE listofingredients (
          user text,
          ingredient text,
          status boolean
          )""")
'''

#c.execute("DROP TABLE listofingredients")

#c.execute("SELECT * FROM listofingredients")
#print(c.fetchall())


c.execute("SELECT img_src FROM tableofrecipes2")
t = c.fetchmany(1)

r = t[0]

r[0]


conn.commit()
conn.close()