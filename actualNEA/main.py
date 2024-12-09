from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import ast

app = Flask(__name__)
app.secret_key = 'ilikecooking'

alert=''

def loadnames():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM tableofrecipes2")
    list2 = c.fetchall()
    c.close()
    conn.close()
    recipenames = []
    count = 0
    for item in list2:
        item = list2[count]
        item = item[0]
        recipenames.append(item)
        count += 1
    return recipenames

def loadIngr():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2")
    t = c.fetchall()
    c.close()
    conn.close()

    ingredientlist = []
    for item in t:
        ingredientlist.append(item)
    return ingredientlist

def grab_image(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofimages = []
    for recipe in altlistofrecipes:
        c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        imagefromdb = c.fetchall()
        for image in imagefromdb:
            listofimages.append(image[0])
    return listofimages

def grab_servings(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofservings = []
    for recipe in altlistofrecipes:
        c.execute("SELECT servings FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        servingfromdb = c.fetchall()
        for serving in servingfromdb:
            listofservings.append(serving[0])
    return listofservings

def grab_rating(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofratings = []
    for recipe in altlistofrecipes:
        c.execute("SELECT rating FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        ratingfromdb = c.fetchall()
        for arating in ratingfromdb:
            listofratings.append(arating[0])
    return listofratings

def grab_cuisine_path(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofcuisinepaths = []
    for recipe in altlistofrecipes:
        c.execute("SELECT cuisine_path FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        cuisinepathfromdb = c.fetchall()
        for acuisinepath in cuisinepathfromdb:
            acuisinepath = acuisinepath[0]
            newcuisinepath = acuisinepath.split('/')
            acuisinepath = newcuisinepath[1]
            listofcuisinepaths.append(acuisinepath)
    return listofcuisinepaths

def grab_nutrition(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofnutritions = []
    for recipe in altlistofrecipes:
        c.execute("SELECT nutrition FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        nutritionfromdb = c.fetchall()
        for nutrition in nutritionfromdb:
            listofnutritions.append(nutrition[0])
    return listofnutritions

def convert2mins(addTime):
    addTime = addTime * 60# converted into minutes
    return addTime

def get_additional_time(time4recipe):
    #print(f"\n\n\nall: {time4recipe}")
    totaltime = time4recipe[2]#as it's structured like (preptime, cooktime, totaltime)
    addTime = []#prepare list for additional time
    for time in totaltime.split():#since totaltime is a string, this function splits the string into a list
        if time.isdigit():#since each time has numbers and letters, e.g. '5 mins', we need only the numbers
            addTime.append(int(time))#since its a number convert to integer, and add it to a list.
    #addTime contains all the digits. If there are two numbers then it's in hours and minutes, if there is one then
    #it may only be in hours, or may only be in minutes
    total = addTime[0]#grabs the hours (if any)
    #print(f"totaltime: {totaltime}")
    #print(f"totaltime.split(): {totaltime.split()}")
    #print(f"addtime: {addTime}")
    #print(f"total: {total}")
    if str(totaltime)[3] == 'i' or str(totaltime)[4] == 'i':#checks if 'total' is in mins
        #print("in minutes")
        #as its in minutes total time is equal to this amount of mins
        totaltime = addTime[0]
    else:
        #print("in hours")
        totaltime = convert2mins(total)#it's in hours therefore convert to minutes
    
    if len(addTime) > 1:#if there are any minutes. if the length is 1 then it's in either minutes or hours only
        #otherwise, it is in hours and minutes.
        totaltime = int(totaltime) + int(addTime[1])#adds the hours and minutes to determine total time in minutes.
    #print(f"totaltime: {totaltime}\n")

    #now we've converted total time to minutes
    #repeat for preptime
    preptime = time4recipe[0]

    addTime = []
    for time in preptime.split():
        if time.isdigit():
            addTime.append(int(time))
    temppreptime = addTime[0]
    if str(preptime)[3] == 'i' or str(preptime)[4] == 'i':
        #in mins
        preptime = addTime[0]
    else:
        #in hours
        preptime = convert2mins(temppreptime)
    
    if len(addTime) > 1:
        preptime = int(preptime) + int(addTime[1])
    #print(f"final preptime in minutes: {preptime}")

    #repeat for cook time
    cooktime = time4recipe[1]
    addTime = []
    for time in cooktime.split():
        if time.isdigit():
            addTime.append(int(time))
    tempcooktime = addTime[0]
    if str(cooktime)[3] == 'i' or str(cooktime)[4] == 'i':
        #in mins
        cooktime = addTime[0]
    else:
        #in hours
        cooktime = convert2mins(tempcooktime)
    
    if len(addTime) > 1:
        cooktime = int(cooktime) + int(addTime[1])
    #print(f"final cooktime in mins: {cooktime}")

    cookAndPrep = int(cooktime) + int(preptime)
    #print(f"cooktime and preptime added together: {cookAndPrep}")
    #print(f"totaltime: {totaltime}")
    addTime = totaltime - cookAndPrep
    #print(f"therefore additional time = totaltime - (cooktime + preptime) = {addTime}")

    #convert addTime to hours and minutes
    if addTime/60 >= 1:#if additional time is more than an hour
        hours = addTime // 60
        mins = addTime % 60
        addTime = f"{hours} hrs {mins}"
    #print(f"addTime in hours and mins: {addTime}")
    return addTime

def grab_time(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    times = []#prepares list of times to be displayed on website
    for recipe in altlistofrecipes:#cycles through list of recipes
        c.execute("SELECT prep_time, cook_time, total_time FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))#get prep, cook and total time for the recipe
        time4recipe = c.fetchall()#2D array, structured like: [(preptime, cooktime, totaltime)]
        time4recipe = time4recipe[0]# (preptime, cooktime, totaltime)
        addTime = get_additional_time(time4recipe)#calculates additional time by passing in prep, cook and total time
        time4recipe = list(time4recipe)#converts tuple to list
        time4recipe.insert(2, addTime)#at index 2, insert additional time, so its like (preptime, cooktime, addtime, totaltime)
        times.append(time4recipe)#add it to times to be displayed on website
    return times#return list of times

def grab_url(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    
    listofurls = []
    for recipe in altlistofrecipes:
        c.execute("SELECT url FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        urlfromdb = c.fetchall()
        for url in urlfromdb:
            listofurls.append(url[0])
    return listofurls

def getrecipename(ingredientlist):
    ingredientlist = ", ".join(ingredientlist)

    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    c.execute("SELECT recipe_name FROM tableofrecipes2 WHERE ingredients=?", (ingredientlist,))
    try:
        tempreturn = c.fetchall()[0][0]
        c.close()
        conn.close()
        return tempreturn
    except:
        pass

def checklength(username, password, confirmpassword):
    count = 0
    if len(username) == 0:
        count +=1
    if len(password) == 0:
        count += 1
    if len(confirmpassword) == 0:
        count += 1
    if count == 3 or count == 2 or count == 1:#they havent filled out all fields
        return True
    else:#they have filled out all fields
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":#if the user is submitting any data
        flashmessage = 'False'#avoids error for later
        conn = sqlite3.connect("recipes.db")#connects to the database
        c = conn.cursor()#makes it quicker to access database
        username = request.form.get('username')#pull username inputted from user
        password = request.form.get('password')#pull password inputted from user
        confirmpassword = request.form.get('confirmpassword')#pull confirmation password from user
        username4len = str(username)
        password4len = str(password)#putting both in the right form for comparison
        confirmpassword4len = str(confirmpassword)
        result = checklength(username4len, password4len, confirmpassword4len)
        if result == True:#if they have filled out at least 1 field but not filled out the rest
            flashmessage = 'notfilledout'#leads to an error message telling the user to fill out all fields
        if password and username and confirmpassword:#if they have inputted all fields
            if len(password) > 6:#checks that password is at least 7 characters
                if username and password and password == confirmpassword:#check all exist and check that confirmation password matches password
                    password = generate_password_hash(password)#securely hash password to avoid hacking
                    try:
                        c.execute("""INSERT INTO users (username, password)
                        VALUES (?, ?)""", (username, password))#at this point all checks have been passed, so 
                        conn.commit()#save
                        c.close()
                        conn.close()#close connection (avoids errors)
                        return redirect(url_for('login'))#redirect to login page as they are successful
                    except:#if an error occurs then it will move here
                        flashmessage = 'sameusername'#if an error occurs it will be from inserting the data into the database. since the database is set up to have each username as unique,
                        #if the username is not unique, then it will return an error, leading here, where a variable is set to a specific string that will trigger a message to popup in the
                        #front end telling the user that their username is not unique.
                elif password != confirmpassword:#if the password and confirmation password do not match. If confirmation password is empty then it will not match password.
                    flashmessage = "passwords do not match"#then this will lead to an error message being returned to the user
            else:#their password is shorter than 7 characters
                flashmessage = "password too short"#therefore return to the user an error telling them to make their password longer.
        return render_template("signup.html", flashmessage=flashmessage)#returns the signup page
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":#if the user is submitting data
        session['alert'] = ""#avoids an error by resetting the global alert variable
        login = False#avoids errors
        flashmessage = False
        conn = sqlite3.connect("recipes.db")#connects to database
        c = conn.cursor()
        username = request.form.get('username')#get username
        password = request.form.get('password')#get password
        if username and password:#if they are both not empty
            c.execute("SELECT username, password FROM users")#get all usernames and passwords from the database
            listofaccounts = c.fetchall()#this is a 2D array stuctured like: [(username1, password1), (username2, password2)]
            for item in listofaccounts:#cycles through all accounts
                if item[0].lower() == username.lower():#if usernames match
                    if check_password_hash(item[1], password):#if the password of that username matches. Checked through hashing the submitted password
                        #the same way as the password in the database
                        login = True#they have successfully logged in
                        break
                    elif item[1] != password:#if the password does not match
                        flashmessage = 'incorrect'#return message to user that they are incorrect
                    else:
                        print("unknown error")
                        flashmessage = 'unknownerror'
            if login == True:#if they are successful
                username = username.title()#capitalize username
                session['username'] = username#assign username to a global variable
                return redirect(url_for('home'))#redirect to home
            else:#if they are not successful
                flashmessage = 'incorrect'#return message to user that they are incorrect
        else:
            flashmessage = 'notfilledout'#return message to user that they must fill out all fields
        return render_template("login.html", flashmessage=flashmessage)
    return render_template("login.html")#therefore only return the page

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:#if they're not logged in (if they're not assigned a username) - username stored globally
        return redirect(url_for('login'))#redirects them back to the login page.
    
    recipesFilteredByName = []#prepare temporary lists
    altlistofrecipes = []
    recipesearchname = request.args.get("recipesearchname")#Query that user has entered for the 'filter by names'
    ingredientsearch = request.args.get("ingredientsearch")#Query that user has entered for the 'filter by ingredients'


    images = []
    
    if recipesearchname:#if they have not submitted anything then this value will be empty
        session['recipesearchname'] = recipesearchname#store variable globally
    if ingredientsearch:
        session['ingredientsearch'] = ingredientsearch


    username = session['username']#pull username

    if 'ingrsearch_history' not in session or request.args.get('reset') == "reset":#if they click the reset button
            session['ingrsearch_history'] = []#reset the ingredient search history
            session['alert'] = ""#reset the alert
            session['recipesearchname'] = ""#reset the filter by name
            session['ingredientsearch'] = ""#reset the current ingredient search
            #resets all filters

    conn = sqlite3.connect("recipes.db")#connect to database
    c = conn.cursor()

    session['alert'] = ""#default value, avoids errors
    
    allrecipenames = loadnames()#get all recipe names
    splitwords = session['recipesearchname'].upper().split()#format query
    for item in allrecipenames:#cycles through all recipe names
        if item:#checks if its empty
            wordsfound = True#assume query is in the recipe name
            for word in splitwords:#cycles through queries
                if word not in item.upper():
                    wordsfound = False#query is not in the recipe name
                    break
            if wordsfound:
                recipesFilteredByName.append(item)#if query is in a recipe name then add it to a list
    if len(recipesFilteredByName) == 0:#if there are no recipes which contain the query
        session['alert'] = 'norecipessearch'#sets a variable which will be used to return an error
        session['recipesearchname'] = ""#reset global variable

    savebutton = request.args.get('saveonhomepage')#pull whether or not they have clicked the 'save recipe' button
    recipename = savebutton
    if savebutton:#if user clicks on this button
        c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))#gets ingredients of that recipe
        ingredientlist = c.fetchall()
        if ingredientlist:#if there are any ingredients of that recipe
            ingredientlist = ingredientlist[0]#formats ingredient list
        while savebutton:#loops through until break
            username = session['username']#pulls username
            c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))#pulls saved recipes from this user
            name = c.fetchall()
            duplicates = False#assume they have not saved this recipe before
            #cycle through previously saved recipes
            for previousrecipe in name:
                if previousrecipe[0] == recipename:
                    duplicates = True#they have previously saved this recipe
            if duplicates == False:#if they haven't added this recipe before
                c.execute("""INSERT INTO userspecrecipes (userid, recipe_name)
                            VALUES (?, ?)""", (username, recipename))#saves recipe under their name into database
                conn.commit()
                c.execute("SELECT id FROM userspecrecipes WHERE recipe_name = ? AND userid = ?", (recipename, username))#pulls ID for ingredient list
                temporaryvariable = c.fetchall()
                id = temporaryvariable[0][0]
                ingredientlist = ingredientlist[0]
                ingredientlist = ingredientlist.split(",")
                for ingredient in ingredientlist:
                    c.execute("""INSERT INTO ingredients (recipeid, ingredient_name)
                            VALUES (?, ?)""", (id, ingredient))#saves ingredient list
                    conn.commit()
                session['alert'] = "success"#return to user that it has been successful
            elif duplicates == True:#checks if they have added this recipe before
                session['alert'] = "duplicates"#return to user that they have already added this recipe
            savebutton = ""#break from loop
            
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
        try:
            x = recipesFilteredByIngredient[0]#temporary variable tests if an error will be returned
            if len(recipesFilteredByIngredient) > 0:#if there is more than one recipe filtered by ingredients
                session['alert'] == ""#reset error message

            if recipesFilteredByName:#if there are any recipes filtered by name
                if recipesFilteredByName == recipesFilteredByIngredient:#if this list is the same as the list of recipes filtered by ingredient
                    altlistofrecipes = recipesFilteredByName#put it into list to be displayed onto website
                else:#this list is not the same as the list of recipes filtered by ingredient, therefore we need to sort through them
                    for recipe in recipesFilteredByName:#cycles through recipes that are filtered by name
                        for anotherrecipe in recipesFilteredByIngredient:#cycles through recipes that are filtered by ingredient
                            if recipe == anotherrecipe:#if they are equal
                                alrthere = False#assume that this recipe is not already there in the list that is to be displayed on the website
                                for item in altlistofrecipes:#cycles through list to be displayed onto website
                                    if item == recipe:
                                        alrthere = True#this recipe is already there in the list so we don't have to add it (we don't want duplicates)
                                if alrthere == False:
                                    altlistofrecipes.append(recipe)#this recipe is not already there so therefore add it
                if len(altlistofrecipes) == 0:#if there are no recipes which match both
                    session['alert'] = 'nocriteria'#return to user that their criteria doesn't match any recipes
                    session['recipesearchname'] = ""#reset
                    session['ingredientsearch'] = ""
                    return render_template("home.html", recipesToBeDisplayed=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'])
                else:
                    images = grab_image(altlistofrecipes)
                    times = grab_time(altlistofrecipes)
                    servings = grab_servings(altlistofrecipes)
                    rating = grab_rating(altlistofrecipes)
                    cuisine_path = grab_cuisine_path(altlistofrecipes)
                    nutrition = grab_nutrition(altlistofrecipes)
                    url = grab_url(altlistofrecipes)#grab all the information to be displayed on the website
                    return render_template("home.html", recipesToBeDisplayed=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)
            else:
                images = grab_image(recipesFilteredByIngredient)
                times = grab_time(recipesFilteredByIngredient)
                servings = grab_servings(recipesFilteredByIngredient)
                rating = grab_rating(recipesFilteredByIngredient)
                cuisine_path = grab_cuisine_path(recipesFilteredByIngredient)
                nutrition = grab_nutrition(recipesFilteredByIngredient)
                url = grab_url(recipesFilteredByIngredient)
                return render_template("home.html", recipesToBeDisplayed=recipesFilteredByIngredient, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)
        except:
            pass#if an error is returned then it will pass

    if len(recipesFilteredByIngredient) > 0:
        session['alert'] = ""#reset
    elif len(recipesFilteredByIngredient) < 1 and request.args.get('reset') != "reset" and request.args.get('querying') != None:#if they havent clicked the reset button and they havent just loaded the page
        session['alert'] = "norecipes"#alert to the user there are no recipes which match their criteria
        session['ingrsearch_history'] = []#reset the ingredient search history
    
    preptime = request.args.get('preptime')
    cooktime = request.args.get('cooktime')
    totaltime = request.args.get('totaltime')

    if preptime:
        c.execute("SELECT prep_time FROM tableofrecipes2")
        allpreptime = c.fetchall()
        #print(f"ALLPREPTIME: {allpreptime}")

    session['search_history'] = session['recipesearchname']

    #same code as before, used again to check if there are any matching recipes between the filters in case an error was returned before.
    if recipesFilteredByIngredient:
        if recipesFilteredByName == recipesFilteredByIngredient:
            altlistofrecipes = recipesFilteredByName
        else:
            for recipe in recipesFilteredByName:
                for anotherrecipe in recipesFilteredByIngredient:
                    if recipe == anotherrecipe:
                        alrthere = False
                        for item in altlistofrecipes:
                            if item == recipe:
                                alrthere = True
                        if alrthere == False:
                            altlistofrecipes.append(recipe)
        if len(altlistofrecipes) == 0:
                session['alert'] = 'nocriteria'
                session['recipesearchname'] = ""
                session['ingredientsearch'] = ""
        images = grab_image(altlistofrecipes)
        times = grab_time(altlistofrecipes)
        servings = grab_servings(altlistofrecipes)
        rating = grab_rating(altlistofrecipes)
        cuisine_path = grab_cuisine_path(altlistofrecipes)
        nutrition = grab_nutrition(altlistofrecipes)
        url = grab_url(altlistofrecipes)
        return render_template("home.html", recipesToBeDisplayed=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)


    
    images = grab_image(recipesFilteredByName)
    times = grab_time(recipesFilteredByName)
    servings = grab_servings(recipesFilteredByName)
    rating = grab_rating(recipesFilteredByName)
    cuisine_path = grab_cuisine_path(recipesFilteredByName)
    nutrition = grab_nutrition(recipesFilteredByName)
    url = grab_url(recipesFilteredByName)
    c.close()
    conn.close()#close database connection to avoid errors from SQLite
    return render_template("home.html", recipesToBeDisplayed=recipesFilteredByName, username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)

@app.route('/logout')#creates url of /logout
def logout():
    session.pop('username')#removes username variable from session
    session.pop('ingrsearch_history')#same but with ingredient filter history
    session.pop('alert')#same but with alert
    return redirect(url_for('login'))#redirects to /login (login page)

@app.route('/<recipename>', methods=['GET', 'POST'])
def item(recipename):
    instructionlist = []
    alert = ""
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))
    ingredients = c.fetchall()
    ingredientlist = []
    for item in ingredients:
        item = item[0]
        ingredientlist = [ingredient.strip() for ingredient in item.split(',')]#turns it into a list
    
    c.execute("SELECT directions FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))
    instructions = c.fetchall()
    if instructions:
        instructions = instructions[0][0]
        splitup = instructions.split('\n')
        instructionlist = []
        for string in splitup:
            if string.strip():
                instructionlist.append(string)
        

    savebutton = request.args.get("saverecipe")
    while savebutton == 'button':#if user clicks on this button
        try:
            username = session['username']
        except:
            alert = "nousername"
            break
        
        #check if this recipe exists
        c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))
        recipeCheck = c.fetchall()
        if len(recipeCheck) < 1:
            #recipe does not exist
            #therefore return an error message telling the user that the recipe does not exist, and redirect them to the home page
            alert = "non-existent recipe"
            return render_template("recipe.html", alert=alert)

        c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))
        name = c.fetchall()
        duplicates = False
        #Cycle through previously saved recipes
        for previousrecipe in name:
            if previousrecipe[0] == recipename:
                duplicates = True
        if duplicates == False:# If they haven't added this recipe before
            c.execute("""INSERT INTO userspecrecipes (userid, recipe_name)
                        VALUES (?, ?)""", (username, recipename))#Insert into database
            conn.commit()
            c.execute("SELECT id FROM userspecrecipes WHERE recipe_name = ? AND userid = ?", (recipename, username))
            temporaryvariable = c.fetchall()
            id = temporaryvariable[0][0]
            for ingredient in ingredientlist:
                c.execute("""INSERT INTO ingredients (recipeid, ingredient_name)
                        VALUES (?, ?)""", (id, ingredient))
                conn.commit()
            alert = "success"
        elif duplicates == True:
            alert = "duplicates"
        savebutton = ""
        
    c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))
    image = c.fetchall()
    if image:
        image = image[0]
        image = image[0]
    c.close()
    conn.close()
    return render_template('recipe.html', ingredients=ingredients, recipename=recipename, item=ingredientlist, image=image, alert=alert, instructions=instructionlist)

@app.route('/lists')
def lists():
    username = session['username']#get username from global variable
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))#get all recipes which
    #the user has saved
    recipes = c.fetchall()#2D array like: [(recipe1,), (recipe2,)]
    recipelist = []#prepare a list for the website
    alert = ""#avoids errors
    try:
        testvar = recipes[0][0]#if there is an error it means the user has not saved any recipes
        for recipe in recipes:#cycles through the recipes
            recipelist.append(recipe[0])#add it to the list
    except:#if there was an error produced
        alert = "norecipes"#sets a variable that will later return an error to the user telling them
        #that they have not saved any recipes
    c.close()
    conn.close()
    return render_template("lists.html", username=username, recipelist=recipelist, alert=alert)


@app.route('/<username>/<recipename>')
def newrecipe(username, recipename):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    alert = ''#prevents error
    c.execute("SELECT id FROM userspecrecipes WHERE recipe_name=? AND userid=?", (recipename, username))#grab the ID of the saved recipe
    id = c.fetchall()[0][0]#format as it is a 2D array
    c.execute("SELECT ingredient_name, state FROM ingredients WHERE recipeid=?", (id,))#from the ID get the ingredients as well as the state
    ingredients = c.fetchall()

    c.execute("SELECT directions FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))#get instructions of recipe (from main database)
    instructions = c.fetchall()
    instructions = instructions[0][0]#formats instructions as it is a 2D array
    splitup = instructions.split('\n')#they are separated by new lines in the database
    instructionlist = []#prepare an instruction list
    for string in splitup:
        if string.strip():
            instructionlist.append(string)#adds the newly formatted instructions to another list to be displayed on the website
    
    c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))#gets the image
    image = c.fetchall()
    image = image[0]
    image = image[0]#formats the image as its a 2D array

    newingredientlist = []#prepare another ingredient list. this will be a 2D array
    for item in ingredients:#cycle through the ingredients in the original ingredient list
        newinglist2 = []#prepare yet another list, this will be placed inside the 'newingredientlist' multiple times
        if item[1] == 0:#if the ingredient's state is unticked
            newinglist2.append(item[0])#add it to the list
            newinglist2.append(False)#as well as its state in boolean
            newingredientlist.append(newinglist2)#add the ingredient's information into another list, as a 2D array
        elif item[1] == 1:#if the ingredient's state is ticked
            newinglist2.append(item[0])
            newinglist2.append(True)
            newingredientlist.append(newinglist2)#same as before
        else:
            raise ValueError#program should not each here, it is to grab my attention as a developer in case the data was incorrectly formatted


    ingredientpressed = request.args.get('pressed')
    if ingredientpressed:#if the user has clicked the button
        ingredientpressed = ast.literal_eval(ingredientpressed)#the value of the button is the ingredient and its state structured like: [ingredient, state]
        #the value is stored as a string therefore this function is used to convert it to a list securely
        for item in newingredientlist:#cycles through the saved ingredients
            if item[0] == ingredientpressed[0] and ingredientpressed[1] == False:#if the ingredient matches the one in the ingredients list and it is unticked
                #then we must tick it as the user clicked the button whilst it was unticked
                #ingredientpressed[0] is the ingredient name
                #ingredientpressed[1] is the state
                c.execute("""UPDATE ingredients 
                            set state = ?
                            WHERE ingredient_name = ? AND recipeid=?
                            """, (True, ingredientpressed[0], id))#update the state of the ingredient to be true.
                conn.commit()#save changes
                ingredientpressed.pop(1)
                ingredientpressed.append(True)#replace the list from the front-end from false to true
                pos = newingredientlist.index(item)
                newingredientlist[pos] = ingredientpressed#update the 2D array that is to be displayed on the website
            elif item[0] == ingredientpressed[0] and ingredientpressed[1] == True:#if the ingredient matches the one in the ingredients list and it is ticked
                #then untick the ingredient
                c.execute("""UPDATE ingredients 
                            set state = ?
                            WHERE ingredient_name = ? AND recipeid=?
                            """, (False, ingredientpressed[0], id))#change the state from true to false in the database
                conn.commit()#save changes
                ingredientpressed.pop(1)
                ingredientpressed.append(False)#update list
                pos = newingredientlist.index(item)
                newingredientlist[pos] = ingredientpressed#update 2D array
    c.close()
    conn.close()
    return render_template('userrecipe.html', recipename=recipename, username=username, item=newingredientlist, image=image, instructions=instructionlist, alert=alert)


if __name__ == "__main__":
    app.run(debug=True)
