from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import ast
import sqlite3
conn = sqlite3.connect('recipes.db')
c = conn.cursor()
recipename=""
ingredientlist=""
username=""



savebutton = request.args.get("saverecipe")
while savebutton == 'button':#if user clicks on this button, since the value of the button is 'button'
    #if the user is simply loading the page then 'savebutton' will not have any value, whereas if the
    #user clicks on the button then 'savebutton' will have the value of 'button'.

    #check if the user has previously saved this recipe
    c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))#get all recipes this
    #user has saved before
    name = c.fetchall()
    duplicates = False#assume they have not saved this recipe before
    for previousrecipe in name:#cycle through previously saved recipes (this is a 2D array)
        if previousrecipe[0] == recipename:#if a previously saved recipe is the same as the recipe they are
            #trying to save then
            duplicates = True#they have saved this recipe before
    if duplicates == False:#if they haven't added this recipe before
        c.execute("""INSERT INTO userspecrecipes (userid, recipe_name)
                    VALUES (?, ?)""", (username, recipename))#save the recipe as they haven't added this recipe before
        conn.commit()#save changes
        c.execute("SELECT id FROM userspecrecipes WHERE recipe_name = ? AND userid = ?", (recipename, username))#gets ID
        #of the recipe user just saved to put into the ingredients
        temporaryvariable = c.fetchall()
        id = temporaryvariable[0][0]#as it is a 2D array (due to SQLite's formatting)
        for ingredient in ingredientlist:#cycles through the ingredients in the recipe
            c.execute("""INSERT INTO ingredients (recipeid, ingredient_name)
                    VALUES (?, ?)""", (id, ingredient))#putting in the recipeid and ingredient name (the state is defaulted to false)
            conn.commit()#save changes
        alert = "success"#sets variable that will return message to user that the recipe has successfully been added
    elif duplicates == True:#they have already saved this recipe before
        alert = "duplicates"#sets variable that will return message to user that they have saved this recipe before
    savebutton = ""#resets the value of the button (so that they do not try to add it again accidentally by reloading the page)

