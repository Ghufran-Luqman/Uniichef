import sqlite3

conn = sqlite3.connect("recipes.db")
c = conn.cursor()

#c.execute("DELETE FROM tableofrecipes WHERE prep_time IS NULL OR prep_time = ''")
#c.execute("DELETE FROM tableofrecipes WHERE prep_time = '(None,)'")
#c.execute("DELETE FROM tableofrecipes WHERE cook_time IS NULL OR cook_time = ''")
#c.execute("DELETE FROM tableofrecipes WHERE total_time IS NULL OR cook_time = ''")
#c.execute("DELETE FROM tableofrecipes WHERE yield IS NULL OR cook_time = ''")
#conn.commit()
#c.execute("SELECT COUNT(prep_time) FROM tableofrecipes")
#c.execute("SELECT COUNT(cook_time) FROM tableofrecipes")
#c.execute("SELECT COUNT(total_time) FROM tableofrecipes")
#c.execute("SELECT COUNT(yield) FROM tableofrecipes")
count = c.fetchall()
print(count)
#c.execute("SELECT cook_time FROM tableofrecipes")
#rows = c.fetchall()
#print(rows)
#while True:
    #rows = c.fetchmany(100)
    #if not rows:
        #break
    #for row in rows:
        #print(row)

conn.close()