from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def loadnames():
    conn = sqlite3.connect("recipes.db")#connect to database
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM tableofrecipes2")#get all recipes from the table
    allrecipes = c.fetchall()#this is a 2D list containing tuples, e.g. [(recipe1,), (recipe2,)]
    conn.close()#close the connection to avoid errors
    #re-format the list of recipes
    formattedrecipes = []#prepare another list
    count = 0#prepare a count
    for item in allrecipes:#cycle through each tuple
        item = allrecipes[count]
        item = item[0]#get first item in list
        formattedrecipes.append(item)#put into another list
        count += 1#go to next tuple
    return formattedrecipes

@app.route('/home')
def home():
    recipenames = loadnames()
    return render_template("index.html", recipenames=recipenames)#return all the recipes (passing the list into the frontend)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get("Query", '')#get the user input for the search box
    recipenames = loadnames()#get every recipe from database
    newrecipelist = []#prepare a new list
    for item in recipenames:#cycle through every recipe
        if item:#checks if its empty
            if query.upper() in item.upper():#converts the query to uppercase and each name in the list to uppercase and checks if the name contains the query
                newrecipelist.append(item)#if it does, it adds it to the list

    if request.method == "POST":
        recipename = request.form.get('recipebutton')
        return render_template("recipe.html", recipename=recipename)

    return render_template("index.html", newrecipelist=newrecipelist)#returns list containing the query

@app.route('/<recipename>')
def item(recipename):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))
    ingredients = c.fetchall()
    for item in ingredients:
        item = item[0]
        item = [ingredient.strip() for ingredient in item.split(',')]#turns it into a list
    return render_template('recipe.html', ingredients=ingredients, recipename=recipename, item=item)


if __name__ == "__main__":
    app.run(debug=True)