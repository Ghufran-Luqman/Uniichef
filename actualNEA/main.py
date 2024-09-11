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



@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    c.execute("SELECT recipe_name FROM tableofrecipes2")
    row = c.fetchall()
    conn.close()
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
    for item in recipenames:
        if item:#checks if its empty
            if query.upper() in item.upper():#converts the query to uppercase and each name in the list to uppercase and sees if the name contains the query
                newrecipelist.append(item)#if it does, it adds it to the list

    if request.method == "POST":
        recipename = request.form.get('recipebutton')
        return render_template("recipe.html", recipename=recipename)
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
    return render_template('recipe.html', ingredients=ingredients, recipename=recipename, item=ingredientlist)

@app.route('/test', methods=['GET', 'POST'])
def test():
    ingredient = request.form.get('ingredient')
    return render_template('test.html', ingredient=ingredient)

if __name__ == "__main__":
    app.run(debug=True)