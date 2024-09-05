import sqlite3

conn = sqlite3.connect("recipes.db")
c = conn.cursor()

#c.execute("""CREATE TABLE tableofrecipes (
          #id integer,
          #recipe_name text,
          #prep_time text,
          #cook_time text,
          #total_time text,
          #servings integer,
          #yield text,
          #ingredients text,
          #directions text,
          #rating real,
          #url text,
          #cuisine_path text,
          #nutrition text,
          #timing text,
          #img_src text
          #)""")
#c.execute("ALTER TABLE tableofrecipes DROP COLUMN id")
conn.commit()
conn.close()