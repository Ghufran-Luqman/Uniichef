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
name = "Cherry Chicken"
string = "3 tablespoons vegetable oil, 1 (4 pound) whole chicken, cut into 8 pieces, salt and pepper to taste, ½ cup all-purpose flour for dusting, 1 (15 ounce) can pitted dark cherries packed in water, ½ cup white sugar, 1 tablespoon cornstarch, 1 orange - with peel, quartered and thinly sliced, ½ cup slivered almonds, toasted"
c.execute("""UPDATE tableofrecipes2
            SET
            ingredients = REPLACE(?, ?, "3 tablespoons vegetable oil, 1 (4 pound) whole chicken cut into 8 pieces, salt and pepper to taste, ½ cup all-purpose flour for dusting, 1 (15 ounce) can pitted dark cherries packed in water, ½ cup white sugar, 1 tablespoon cornstarch, 1 orange - with peel - quartered and thinly sliced, ½ cup slivered almonds - toasted")
            WHERE recipe_name=?""", (string, string, name,))
conn.commit()


#c.execute("SELECT COUNT(*) FROM tableofrecipes2")
#t = c.fetchall()
#print(t)
#GET RID OF ROWS WITHOUT PREP TIME, COOK TIME AND TOTAL TIME.
#CHECK FOR EVERY ONE OF THEM IF THE INGREDIENTS ARE OK WITH THE WEIRD COMMAS

conn.commit()
conn.close()