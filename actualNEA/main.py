from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import ast

app = Flask(__name__)
app.secret_key = 'ilikecooking'

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

def convert2mins(addTime, minutescheck):
    #print(f"(convert2mins) passed in number: {addTime}")
    #print(f"(convert2mins) passed in number LENGTH: {len(str(addTime))}")
    if minutescheck:
        if minutescheck == True:
            #only mins
            #print(f"only mins")
            return addTime
    if len(str(addTime)) == 1:
        #this is hours only
        #print(f"This is hours only")
        addTime = addTime * 60# converted into minutes
    elif len(str(addTime)) == 2:
        #print(f"alr in mins so dont do anything")
        #already in minutes therefore we don't need to do anything
        pass
    elif len(str(addTime)) == 3:
        #print(f"first digit is hours, last 2 are mins.")
        #first digit is hours, last 2 are minutes
        temp = int(addTime[0]) * 60#hours into mins
        addTime = int(str(addTime)[1:])
        addTime = addTime + temp#gets total mins
    
    elif len(str(addTime)) == 4:
        #print(f"first 2 digits are hours, last 2 are mins")
        temp = int(addTime[0]) + int(addTime[1])
        temp = temp * 60
        addTime = int(str(addTime[2:]))
        addTime = addTime + temp
    else:
        #print(f"addTime: {addTime}")
        #print(f"length: {len(str(addTime))}")
        raise ValueError#shouldnt happen but if it does then programmer/user will be alerted
    return addTime

def get_additional_time(time4recipe):
    totaltime = time4recipe[2]
    #print(f"inital totaltime: {totaltime}")
    #print(f"lenght: {len(str(totaltime))}")
    #try:
        #print(f"{str(totaltime)[3]}")
    #except:
        #pass
    addTime = []
    for time in totaltime.split():
        if time.isdigit():
            addTime.append(int(time))
    total = addTime[0]
    #print(f"addtime: {addTime}")
    #print(f"total: {total}")
    try:
        #print(f"tried")
        if str(totaltime)[3] == 'i':
            #print(f"its in mins3")
            minutescheck = True
            totaltime = convert2mins(total, minutescheck)
            pass
        elif str(totaltime)[4] == 'i':
            #print(f"its in mins4")
            minutescheck = True
            totaltime = convert2mins(total, minutescheck)
            pass
        else:
            #print(f"did else")
            minutescheck = False
            totaltime = convert2mins(total, minutescheck)
    
    except:
        #print(f"excepted")
        minutescheck = False
        totaltime = convert2mins(total, minutescheck)
    #print(f"length of add time: {len(addTime)}")
    if len(addTime) > 1:
        #print(f"bigger than 1")
        totaltime = int(totaltime) + int(addTime[1])

    #print(f"TOTALTIME IN MINUTES FULL: {totaltime}")
    #now we've converted total time to minutes
    #repeat for preptime
    preptime = time4recipe[0]
    #print(f"inital preptime: {preptime}")
    #print(f"lenght: {len(str(preptime))}")
    #try:
        #print(f"{str(preptime)[3]}")
    #except:
        #pass
    addTime = []
    for time in preptime.split():
        if time.isdigit():
            addTime.append(int(time))
    temppreptime = addTime[0]
    try:
        #print(f"tried")
        if str(preptime)[3] == 'i':
            #print(f"its in mins3")
            minutescheck = True
            preptime = convert2mins(temppreptime, minutescheck)
            pass
        elif str(preptime)[4] == 'i':
            #print(f"its in mins4")
            minutescheck = True
            preptime = convert2mins(temppreptime, minutescheck)
            pass
        else:
            #print(f"did else")
            minutescheck = False
            preptime = convert2mins(temppreptime, minutescheck)
    
    except:
        #print(f"excepted")
        minutescheck = False
        preptime = convert2mins(temppreptime, minutescheck)
    if len(addTime) > 1:
        preptime = int(preptime) + int(addTime[1])
    #print(f"preptime after conversion: {preptime}")

    #repeat for cook time
    cooktime = time4recipe[1]
    #print(f"inital cooktime: {cooktime}")
    #print(f"lenght: {len(str(cooktime))}")
    #try:
        #print(f"{str(cooktime)[3]}")
    #except:
        #pass
    addTime = []
    for time in cooktime.split():
        if time.isdigit():
            addTime.append(int(time))
    tempcooktime = addTime[0]
    try:
        #print(f"tried")
        if str(cooktime)[3] == 'i':
            #print(f"its in mins3")
            minutescheck = True
            cooktime = convert2mins(tempcooktime, minutescheck)
            pass
        elif str(cooktime)[4] == 'i':
            #print(f"its in mins4")
            minutescheck = True
            cooktime = convert2mins(tempcooktime, minutescheck)
            pass
        else:
            #print(f"did else")
            minutescheck = False
            cooktime = convert2mins(tempcooktime, minutescheck)
    
    except:
        #print(f"excepted")
        minutescheck = False
        cooktime = convert2mins(tempcooktime, minutescheck)
    if len(addTime) > 1:
        cooktime = int(cooktime) + int(addTime[1])
    #print(f"cooktime after conversion: {cooktime}")

    cookAndPrep = int(cooktime) + int(preptime)
    #print(f"cook and prep time added: {cookAndPrep}")
    #print(f"total time: {totaltime}")
    addTime = totaltime - cookAndPrep
    #print(f"calculated addTIme from minusing them: {addTime}")

    #convert addTime to hours and minutes
    if addTime/60 > 1:
        hours = addTime // 60
        mins = addTime % 60
        addTime = f"{hours} hrs {mins}"
    return addTime

def grab_time(altlistofrecipes):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    times = []
    for recipe in altlistofrecipes:
        c.execute("SELECT prep_time, cook_time, total_time FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        time4recipe = c.fetchall()#2D array, structured like: [(preptime, cooktime, totaltime)]
        time4recipe = time4recipe[0]# (preptime, cooktime, totaltime)
        # Calculate additional time
        #print(f"\n\nrecipename: {recipe}\n\n")
        #print(f"time4recipe: {time4recipe}")
        addTime = get_additional_time(time4recipe)
        #print(f"final additional time: {addTime}")
        time4recipe = list(time4recipe)
        time4recipe.insert(2, addTime)# at index 2, insert additional time, so its like (preptime, cooktime, addtime, totaltime)
        times.append(time4recipe)
    return times

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

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    flashmessage = 'False'#avoids error for later
    conn = sqlite3.connect("recipes.db")#connects to the database
    c = conn.cursor()#makes it quicker to access database
    username = request.form.get('username')#pull username inputted from user
    password = request.form.get('password')#pull password inputted from user
    confirmpassword = request.form.get('confirmpassword')#pull confirmation password from user
    if password:#if they have inputted a password - helps check they have inputted everything
        if len(password) > 6:#checks that password is at least 7 characters
            username4len = str(username)
            password4len = str(password)#putting both in the right form for comparison
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
                    flashmessage = 'sameusername'#if an error occurs it will be from inserting the data into the database. since the database is set up to have each username as unique, if the username is not unique, then it will return an error, leading here, where a variable is set to a specific string that will trigger a message to popup in the front end telling the user that their username is not unique.
            elif password != confirmpassword:#if the password and confirmation password do not match. If confirmation password is empty then it will not match password.
                flashmessage = "passwords do not match"#then this will lead to an error message being returned to the user
            elif len(username4len) < 1 and len(password4len) >= 1 or len(password4len) < 1 and len(username4len) >= 1:#if the user has filled out only password or only username then return error (if they have not filled out any, it is assumed that they are just loading the page, and so nothing will be done).
                flashmessage = 'notfilledout'#leads to an error message telling the user to fill out all fields
        else:#their password is shorter than 7 characters
            flashmessage = "password too short"#therefore return to the user an error telling them to make their password longer.
    return render_template("signup.html", flashmessage=flashmessage)#returns the signup page

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['alert'] = ""
    login = False
    flashmessage = False
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    username4len = str(username)
    password4len = str(password)
    if username and password:
        c.execute("SELECT username, password FROM users")
        listofusernames = c.fetchall()
        for item in listofusernames:
            if item[0].lower() == username.lower():#if usernames match
                if check_password_hash(item[1], password):#if passwords of that username match
                    login = True
                    break
                elif item[1] != password:
                    flashmessage = 'incorrect'
                else:
                    print("unknown error")
                    flashmessage = 'unknownerror'
        if login == True:
            username = username.title()
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flashmessage = 'incorrect'
    elif len(username4len) < 1 and len(password4len) >= 1 or len(password4len) < 1 and len(username4len) >= 1:
        flashmessage = 'notfilledout'
    return render_template("login.html", flashmessage=flashmessage)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:#if they're not logged in (if they're not assigned a username) - username stored globally
        return redirect(url_for('login'))#redirects them back to the login page.
    
    recipesFilteredByName = []#prepare temporary lists
    altlistofrecipes = []
    recipesearch = request.args.get("recipesearch", '')#Query that user has entered for the 'filter by names'
    ingredientsearch = request.args.get("ingredientsearch")#Query that user has entered for the 'filter by ingredients'

    images = []
    
    if recipesearch:#if they have not submitted anything then this value will be empty
        session['recipesearch'] = recipesearch#store variable globally
    if ingredientsearch:
        session['ingredientsearch'] = ingredientsearch


    username = session['username']#pull username

    if 'ingrsearch_history' not in session or request.args.get('reset') == "reset":#if they click the reset button
            session['ingrsearch_history'] = []
            session['alert'] = ""
            session['recipesearch'] = ""
            session['ingredientsearch'] = ""
            #resets all filters

    conn = sqlite3.connect("recipes.db")#connect to database
    c = conn.cursor()

    session['alert'] = ""#default value, avoids errors
    
    allrecipenames = loadnames()#get all recipe names
    splitwords = session['recipesearch'].upper().split()#format query
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
        session['recipesearch'] = ""#reset global variable

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
        elif noOfPrevIngredients == 1:#if there's only one recipesearch item
            for recipe in recipesWMatchingIngs:
                recipesFilteredByIngredient.append(recipe)#add it to list
        try:
            x = recipesFilteredByIngredient[0]#temporary variable tests if an error will be returned
            if len(recipesFilteredByIngredient) > 0:#if there is more than one recipe filtered by ingredients
                session['alert'] == ""#reset

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
                    session['recipesearch'] = ""#reset
                    session['ingredientsearch'] = ""
                    return render_template("home.html", recipesFilteredByName=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'])
                else:
                    images = grab_image(altlistofrecipes)
                    times = grab_time(altlistofrecipes)
                    servings = grab_servings(altlistofrecipes)
                    rating = grab_rating(altlistofrecipes)
                    cuisine_path = grab_cuisine_path(altlistofrecipes)
                    nutrition = grab_nutrition(altlistofrecipes)
                    url = grab_url(altlistofrecipes)#grab all the information to be displayed on the website
                    return render_template("home.html", recipesFilteredByName=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)
            else:
                images = grab_image(recipesFilteredByIngredient)
                times = grab_time(recipesFilteredByIngredient)
                servings = grab_servings(recipesFilteredByIngredient)
                rating = grab_rating(recipesFilteredByIngredient)
                cuisine_path = grab_cuisine_path(recipesFilteredByIngredient)
                nutrition = grab_nutrition(recipesFilteredByIngredient)
                url = grab_url(recipesFilteredByIngredient)
                return render_template("home.html", recipesFilteredByName=recipesFilteredByIngredient, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)
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
        print(f"ALLPREPTIME: {allpreptime}")

    session['search_history'] = session['recipesearch']

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
                session['recipesearch'] = ""
                session['ingredientsearch'] = ""
        images = grab_image(altlistofrecipes)
        times = grab_time(altlistofrecipes)
        servings = grab_servings(altlistofrecipes)
        rating = grab_rating(altlistofrecipes)
        cuisine_path = grab_cuisine_path(altlistofrecipes)
        nutrition = grab_nutrition(altlistofrecipes)
        url = grab_url(altlistofrecipes)
        return render_template("home.html", recipesFilteredByName=altlistofrecipes, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)

    
    images = grab_image(recipesFilteredByName)
    times = grab_time(recipesFilteredByName)
    servings = grab_servings(recipesFilteredByName)
    rating = grab_rating(recipesFilteredByName)
    cuisine_path = grab_cuisine_path(recipesFilteredByName)
    nutrition = grab_nutrition(recipesFilteredByName)
    url = grab_url(recipesFilteredByName)
    c.close()
    conn.close()#close database connection to avoid errors from SQLite
    return render_template("home.html", recipesFilteredByName=recipesFilteredByName, username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url)

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('ingrsearch_history')
    session.pop('alert')
    return redirect(url_for('login'))

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
        #print("clicked on button")
        try:
            username = session['username']
        except:
            alert = "nousername"
            break
        #print(f"username: {username}")
            
        c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))
        name = c.fetchall()
        #print(f"name: {name}")
        duplicates = False
        '''
        length = len(name)
        count = 0
        duplicates = False
        while count < length:
            try:
                first = name[count][0]
                print(f"first: {first}")
                second = name[count+1][0]
                print(f"second: {second}")
            except:
                print("no duplicates")
                duplicates = False
                break
            if first == second:
                print("there are duplicates")
                duplicates = True
                break
            count += 1
        '''
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
            '''
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
            '''
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
    username = session['username']
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))
    recipes = c.fetchall()
    recipelist = []
    alert = ""
    try:
        testvar = recipes[0][0]
        for recipe in recipes:
            print(recipe[0])
            recipelist.append(recipe[0])
        print(f"recipelist: {recipelist}")
        '''for recipe in recipelist:
            ingredientlist = []
            c.execute("SELECT id FROM userspecrecipes WHERE recipe_name=?", (recipe,))
            id = c.fetchall()[0][0]
            print(f"id: {id}")
            c.execute("SELECT ingredient_name, state FROM ingredients WHERE recipeid=?", (id,))
            ingredients = c.fetchall()
            print(f"ingredients: {ingredients}")'''
    except:
        print("no recipes")
        alert = "norecipes"

    c.close()
    conn.close()
    return render_template("lists.html", username=username, recipelist=recipelist, alert=alert)

@app.route('/<username>/<recipename>')
def newrecipe(username, recipename):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    ingredientlist = []
    c.execute("SELECT id FROM userspecrecipes WHERE recipe_name=? AND userid=?", (recipename, username))
    id = c.fetchall()[0][0]
    c.execute("SELECT ingredient_name, state FROM ingredients WHERE recipeid=?", (id,))
    ingredients = c.fetchall()
    for item in ingredients:
        ingredientlist.append(item)

    c.execute("SELECT directions FROM tableofrecipes2 WHERE recipe_name = ?", (recipename,))
    instructions = c.fetchall()
    if instructions:
        instructions = instructions[0][0]
        splitup = instructions.split('\n')
        instructionlist = []
        for string in splitup:
            if string.strip():
                instructionlist.append(string)
        instructionlist[-1] = f"By: {instructionlist[-1]}"
    
    c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))
    image = c.fetchall()
    if image:
        image = image[0]
        image = image[0]
    '''
    newingredientlist = []
    for item in ingredientlist:
        newinglist2 = []
        if item[1] == 0:
            newinglist2.append(item[0])
            newinglist2.append(False)
            newingredientlist.append(newinglist2)
        elif item[1] == 1:
            newinglist2.append(item[0])
            newinglist2.append(True)
            newingredientlist.append(newinglist2)
        else:
            raise KeyError
    print(f"newingredientlist {newingredientlist}")
    '''

    newingredientlist = []
    for item in ingredientlist:
        newinglist2 = []
        if item[1] == 0:
            newinglist2.append(item[0])
            newinglist2.append(False)
            newingredientlist.append(newinglist2)
        elif item[1] == 1:
            newinglist2.append(item[0])
            newinglist2.append(True)
            newingredientlist.append(newinglist2)
        else:
            raise KeyError

    print(f"newinglist: {newingredientlist}")

    ingredientpressed = request.args.get('pressed')
    if ingredientpressed:
        ingredientpressed = ast.literal_eval(ingredientpressed)
        print(f"ingredientpressed: {ingredientpressed}")
        for item in newingredientlist:
            if item[0] == ingredientpressed[0] and ingredientpressed[1] == False:
                c.execute("SELECT ingredient_name FROM ingredients WHERE ingredient_name=?", (ingredientpressed[0],))
                temp = c.fetchall()[0][0]
                print(f"SUIIIIIIIIIIIIIIIIIIIIII: {temp}\n")
                c.execute("""UPDATE ingredients 
                            set state = ?
                            WHERE ingredient_name = ? AND recipeid=?
                            """, (True, temp, id))
                c.execute("SELECT * FROM ingredients WHERE recipeid=?", (id,))
                t = c.fetchall()
                conn.commit()
                print(f"\nALL: {t}\n")
                ingredientpressed.pop(1)
                ingredientpressed.append(True)
                print(f"newingpressed {ingredientpressed}")
                pos = newingredientlist.index(item)
                newingredientlist[pos] = ingredientpressed
                print(f"newinglistmodified: {newingredientlist}")
            elif item[0] == ingredientpressed[0] and ingredientpressed[1] == True:
                c.execute("SELECT ingredient_name FROM ingredients WHERE ingredient_name=?", (ingredientpressed[0],))
                temp = c.fetchall()[0][0]
                print(f"SUIIIIIIIIIIIIIIIIIIIIII: {temp}\n")
                c.execute("""UPDATE ingredients 
                            set state = ?
                            WHERE ingredient_name = ? AND recipeid=?
                            """, (False, temp, id))
                c.execute("SELECT * FROM ingredients WHERE recipeid=?", (id,))
                t = c.fetchall()
                conn.commit()
                print(f"\nALL: {t}\n")
                ingredientpressed.pop(1)
                ingredientpressed.append(False)
                print(f"newingpressed {ingredientpressed}")
                pos = newingredientlist.index(item)
                newingredientlist[pos] = ingredientpressed
                print(f"newinglistmodified: {newingredientlist}")

            

    c.close()
    conn.close()
    return render_template('userrecipe.html', recipename=recipename, username=username, item=newingredientlist, image=image, instructions=instructionlist)


if __name__ == "__main__":
    app.run(debug=True)
