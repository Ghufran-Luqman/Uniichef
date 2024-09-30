from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def loadnames():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM tableofrecipes2")
    list = c.fetchall()
    conn.close()
    recipenames = []
    count = 0
    for item in list:
        item = list[count]
        item = item[0]
        recipenames.append(item)
        count += 1
    return recipenames

def loadingr():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2")
    t = c.fetchall()

    ingredientlist = []
    for item in t:
        ingredientlist.append(item)
    return ingredientlist

def getrecipename(ingredientlist):
    ingredientlist = ", ".join(ingredientlist)

    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    print(ingredientlist)
    c.execute("SELECT recipe_name FROM tableofrecipes2 WHERE ingredients=?", (ingredientlist,))
    try:
        return c.fetchall()[0][0]
    except:
        pass

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    c.execute("SELECT recipe_name FROM tableofrecipes2")
    row = c.fetchall()
    row = list(row)
    count = 0
    newlist = []
    for item in row:
        item = row[count]
        item = item[0]
        newlist.append(item)
        count += 1
    #print(f"finished list: {newlist}")#i have removed the tuples

    query = request.args.get("Query", '')#the '' is a default value.
    recipenames = loadnames()
    newrecipelist = []
    splitwords = query.upper().split()
    for item in recipenames:
        if item:#checks if its empty
            wordsfound = True
            #if all(word in item.upper() for word in splitwords):
            for word in splitwords:
                if word not in item.upper():
                    wordsfound = False
                    break
            if wordsfound:
            #if query.upper() in item.upper():#converts the query to uppercase and each name in the list to uppercase and sees if the name contains the query
                newrecipelist.append(item)#if it does, it adds it to the list

    querying = request.args.get("querying")
    ingredientlist = loadingr()
    anotherlist = []
    anotherrlist = []
    forwebsite = []
    count = 0
    if querying:
        for item in ingredientlist:#('hgffgffgh, jhjygjgyjg',)
            item = list(item)
            item = item[0]
            anotherlist = [ingredient.strip() for ingredient in item.split(',')]
            anotherrlist.append(anotherlist)
        for item in anotherrlist:
            for ingredient in item:
                if querying.upper() in ingredient.upper():#if user input is in an ingredient
                    recipename = getrecipename(item)#get recipe name
                    if recipename == None:
                        pass
                    else:
                        print(recipename)
                        forwebsite.append(recipename)
                    break
    try:
        x = forwebsite[0]
        return render_template("index.html", row=row, newlist=newlist, newrecipelist=forwebsite, querying=querying)
    except:
        pass
            
    conn.close()
    return render_template("index.html", row=row, newlist=newlist, newrecipelist=newrecipelist)


@app.route('/<recipename>', methods=['GET', 'POST'])
def item(recipename):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))
    ingredients = c.fetchall()
    ingredientlist = []
    for item in ingredients:
        item = item[0]
        ingredientlist = [ingredient.strip() for ingredient in item.split(',')]#turns it into a list
    if request.method == "POST":
        haveingredient = request.form.get('checkmark')
        print(f"haveingredient:{haveingredient}")
        if haveingredient:
            print(f"inserting haveingredient")
            c.execute("""INSERT INTO listofingredients (user, ingredient, status)
                VALUES (?, ?, ?)""", ("default", haveingredient, "True",))
            conn.commit()
        c.execute("SELECT * FROM listofingredients")
        listt = c.fetchall()
        print(f"initial list:{listt}")
        list2 = []
        for item in listt:
            item1 = f"{item[0]}, {item[1]}, {item[2]}"
            list2.append(item1)
        print(f"list2: {list2}")
    addlist = request.args.get("roundbutton")
    if addlist == 'button':
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        c.execute("SELECT * FROM listofingredients")
        listt = c.fetchall()
        list2 = []
        for item in listt:
            item1 = f"{item[0]}, {item[1]}, {item[2]}"
            list2.append(item1)
        #print(f"list2: {list2}")


        for item in ingredientlist:
            c.execute("INSERT INTO listofingredients (user, ingredient, status) VALUES (?, ?, ?)", ('default', item, 'False'))
        conn.commit()
        c.execute("SELECT * FROM listofingredients")
        print(f"SUIIIIIIIIIIIIIIII:{c.fetchall()}")
        return redirect(url_for('item', recipename=recipename))
    c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))
    image = c.fetchall()
    if image:
        image = image[0]
        image = image[0]

    return render_template('recipe.html', ingredients=ingredients, recipename=recipename, item=ingredientlist, image=image)

@app.route('/test', methods=['GET', 'POST'])
def test():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()

    if request.method == "POST":
        print(f"deleting...")
        t = "default"
        c.execute("DELETE FROM listofingredients WHERE user=?", (t,))
        conn.commit()
    c.execute("SELECT ingredient FROM listofingredients")
    listt = c.fetchall()
    #print(f"initial list:{listt}")
    list2 = []
    for item in listt:
        item1 = f"{item[0]}"
        list2.append(item1)
    #print(f"list2: {list2}")
    conn.close()
    return render_template('test.html', list=list2)

if __name__ == "__main__":
    app.run(debug=True)
