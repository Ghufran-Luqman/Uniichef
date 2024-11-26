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

def filter_by_name(recipenames, query):
    newrecipelist = []#prepare a new list
    splitwords = query.upper().split()#format query by splitting with whitespace
    for recipe in recipenames:#cycles through all recipe names
        if recipe:#if the recipe is not empty
            wordsfound = True#asume query is in the recipe name already
            for word in splitwords:#cycles through queries
                if word not in recipe.upper():#if the query is not in the recipe name
                    wordsfound = False#query is not in the recipe name
                    break#so no need to check if the query is in the recipe name
            if wordsfound:#if it reaches this point then the recipe name contains both queries
                newrecipelist.append(recipe)#therefore add them to the list
    if len(newrecipelist) > 0:#checks if there are any recipes which contain the queries
        return newrecipelist
    else:
        alert = "no recipes"#if there are not, it assigns a variable which will lead to a message alerting the user that no recipes match their query being returned
        return alert

@app.route('/home')
def home():
    alert = ""
    recipenames = loadnames()#get all recipe names
    query = request.args.get("Query")#gets user input
    if query:#if they have inputted anything
        result = filter_by_name(recipenames, query)
        if result == "no recipes":#checks if there is an error message
            alert = result
        else:
            return render_template("home.html", recipenames=result)#if there isn't then there must be a list of recipes, therefore return them
    return render_template("home.html", recipenames=recipenames, alert=alert)#return all the recipes if no query or if there are no recipes in the newrecipelist

@app.route('/<recipename>')
def recipe(recipename):#gets recipe name
    item=""#avoids an error
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))#gets ingredients
    ingredients = c.fetchall()
    ingredientlist = []
    for item in ingredients:
        item = item[0]
        ingredientlist = [ingredient.strip() for ingredient in item.split(',')]#turns it into a list for formatting
    return render_template('recipe.html', recipename=recipename, ingredientlist=ingredientlist)


if __name__ == "__main__":
    app.run(debug=True)