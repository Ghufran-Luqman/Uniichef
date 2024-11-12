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
'''
c.execute("SELECT ingredients FROM tableofrecipes2")
te = c.fetchall()
a = te
count2 = 0
for item in a:#item is the ingredient string
    item = item[0]
    t = item.strip()
    #t = tuple(t.split("''"))#t is the tuple ready to be put back in
    tee = te[count2][0]#tee is the original currently in db
    count2 += 1
    print(tee)
    c.execute("""UPDATE tableofrecipes2
            SET
            ingredients = REPLACE(?, ?, ?)
            WHERE ingredients=?""", (tee, tee, t, tee))
    conn.commit()
'''    

#if t == te[2]:
          #print("yes")
#else:
          #print("no")

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
'''
e = 'Fig and Honey Jam with Walnuts'
c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (e, ))
a = "4 cups Mission figs - stemmed, 2 cups honey, 1 cup water, ¼ cup butter, 3 tablespoons lemon juice, 2 teaspoons ground cinnamon, 1 ½ teaspoons vanilla extract, 1 teaspoon ground cloves, 1 teaspoon salt, ½ teaspoon grated fresh ginger , 1 cup chopped walnuts"
t = c.fetchall()[0][0]
print(t)
#t = t.strip()
if a == t:
          print(t.strip())
          print("yes")
else:
          print("no")
'''
#t = "Grilled Brie and Pear Sandwich"
#c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (t,))
#print(c.fetchall())
#c.execute("DELETE FROM tableofrecipes2 WHERE recipe_name=?", (t,))

'''
t = "Apple Crisp"
c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (t,))
y = c.fetchall()[0]
y = list(y)
y = y[0]
a = [ingredient.strip() for ingredient in y.split(',')]
print(a)
'''
'''
t = "Ma'amoul (Lebanese Date Cookies)"
c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (t,))
print(c.fetchall())
'''
'''
c.execute("""CREATE TABLE users (
          id integer PRIMARY KEY AUTOINCREMENT,
          username text UNIQUE NOT NULL,
          password text NOT NULL
          )""")
'''
'''
c.execute("""CREATE TABLE userspecrecipes (
          id integer PRIMARY KEY AUTOINCREMENT,
          userid text NOT NULL,
          recipe_name text NOT NULL
          )""")
'''
'''
c.execute("""CREATE TABLE ingredients (
          id integer PRIMARY KEY AUTOINCREMENT,
          recipeid integer NOT NULL,
          ingredient_name text NOT NULL,
          state boolean NOT NULL DEFAULT FALSE,
          FOREIGN KEY (recipeid) REFERENCES userspecrecipes (id)
          )""")
'''
#c.execute("""INSERT INTO users (username, password)
          #VALUES (?, ?)""", ("test", "test"))
'''
c.execute("DROP TABLE userspecrecipes")
conn.commit()
c.execute("DROP TABLE ingredients")
conn.commit()
'''
'''
t = '8 small Granny Smith apples or as needed'
c.execute("""UPDATE ingredients 
            set state = ?
            WHERE ingredient_name = ?
            """, (False, t))

c.execute("SELECT * FROM users")
print(c.fetchall())
c.execute("SELECT * FROM userspecrecipes")
print(c.fetchall())
c.execute("SELECT * FROM ingredients")
print(c.fetchall())
'''

c.execute("SELECT servings, yield FROM tableofrecipes2")
t = c.fetchall()
print(t)

conn.commit()
conn.close()
