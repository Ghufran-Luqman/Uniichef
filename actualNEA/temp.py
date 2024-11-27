from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import ast
def loadIngr():
    ...
def getrecipename(x):
    ...
def filter_by_ingredient(ingredientsearch):
    conn = sqlite3.connect("recipe.db")
    c = conn.cursor()
    ingredientlist = loadIngr()#loads the ingredients
    temporarylist = []#prepare temporary lists
    temporaryingredientlist = []
    recipesFilteredByIngredient = []
    if session['ingredientsearch']:#if they have searched for recipes by ingredients
        session['ingrsearch_history'].append(session['ingredientsearch'])#add their query to a list of previously searched ingredients
        session.modified = True

        for item in ingredientlist:
            item = list(item)
            item = item[0]
            temporarylist = [ingredient.strip() for ingredient in item.split(',')]
            temporaryingredientlist.append(temporarylist)#formats ingredients
        noOfPrevIngredients = len(session['ingrsearch_history'])#takes the number of previously searched for ingredients
        recipesWMatchingIngs = []#prepare more temporary lists
        ingredientListWCommas = []
        if noOfPrevIngredients <= 1:#if they have 1 previously searched for ingredient
            for previousIngredientFilter in session['ingrsearch_history']:#OR list, cycles through queries
                for item in temporaryingredientlist:#cycles through ingredients
                        for ingredient in item:
                            if previousIngredientFilter.upper() in ingredient.upper():#if ingredient contains query
                                recipename = getrecipename(item)#pulls recipe name
                                if recipename == None:#no recipe name
                                    pass#move onto next ingredient
                                else:
                                    recipesWMatchingIngs.append(recipename)#if there is a recipe name, add it to a list to be displayed onto website
                                break#break from loop
        elif noOfPrevIngredients > 1:#if they have more than one previously searched for ingredient
            firstrecipesearch = session['ingrsearch_history'][0]#take the first ingredient they searched for
            for item in temporaryingredientlist:#cycles through ingredients
                for ingredient in item:
                    if firstrecipesearch.upper() in ingredient.upper():#if the ingredient is in the first query
                        recipename = getrecipename(item)#get the recipe name
                        if recipename == None:#if no recipe name
                            pass#move onto next ingredient
                        else:
                            recipesWMatchingIngs.append(recipename)#if there is a recipe name then add it to a list to be displayed onto the website
                            break#break from the loop
        if noOfPrevIngredients > 1:#continue on
            for item in recipesWMatchingIngs:#for every recipe in this list of recipes
                tobreak = False
                c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (item,))#gets recipes original ingredients
                recipesings = c.fetchall()[0]
                recipesings = list(recipesings)
                recipesings = recipesings[0]#format
                ingredientListWCommas = [ingredient.strip() for ingredient in recipesings.split(',')]#puts original ings into list separated by the comma
                #ingredientListWCommas is the ingredient list (all cleaned up) for this specific recipe
                lengthOfIngList = len(ingredientListWCommas)#length of list of ingredients
                count = 0#prepare counter
                while count != lengthOfIngList and tobreak == False:#while all queries have not been matched and there isn't a reason to break
                    count2 = 0#prepare a second count
                    queryCount = 0#and a count for queries
                    while count2 != noOfPrevIngredients and tobreak == False:#noOfPrevIngredients is how many queries there are
                        if session['ingrsearch_history'][count2].upper() in ingredientListWCommas[count].upper():#if queried ingredient is in an ingredient of the recipe
                            count2 += 1#increment count
                            for ingredientrecipesearch in session['ingrsearch_history']:#cycles through all the queries
                                for aningredient in ingredientListWCommas:
                                    if ingredientrecipesearch.upper() in aningredient.upper():#if queried ingredient is in the recipe ingredient list
                                        queryCount += 1#increments query count
                                        break

                            if queryCount == len(session['ingrsearch_history']):#if all queries are in the recipe ingredients
                                recipesFilteredByIngredient.append(item)#adds them to be displayed on the website
                                tobreak = True#no need to cycle anymore therefore break from loop
                                break
                                    
                        else:#if the first queried item is not in the recipe list then break
                            break
                    count += 1#cycle to the next ingredient in the recipe ingredient list
        elif noOfPrevIngredients == 1:#if there's only one query item
            for recipe in recipesWMatchingIngs:
                recipesFilteredByIngredient.append(recipe)#add it to list


ingredientsearch = request.args.get("ingredientsearch")#Query that user has entered for the 'filter by ingredients'
if ingredientsearch:
    session['ingredientsearch'] = ingredientsearch
filter_by_ingredient(session['ingredientsearch'])