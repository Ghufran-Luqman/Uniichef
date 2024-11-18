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

def loadingr():
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

def grab_image(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofimages = []
    for recipe in displayonwebsite:
        c.execute("SELECT img_src FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        imagefromdb = c.fetchall()
        for image in imagefromdb:
            listofimages.append(image[0])
    return listofimages

def grab_servings(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofservings = []
    for recipe in displayonwebsite:
        c.execute("SELECT servings FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        servingfromdb = c.fetchall()
        for serving in servingfromdb:
            listofservings.append(serving[0])
    return listofservings

def grab_rating(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofratings = []
    for recipe in displayonwebsite:
        c.execute("SELECT rating FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        ratingfromdb = c.fetchall()
        for arating in ratingfromdb:
            listofratings.append(arating[0])
    return listofratings

def grab_cuisine_path(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofcuisinepaths = []
    for recipe in displayonwebsite:
        c.execute("SELECT cuisine_path FROM tableofrecipes2 WHERE recipe_name=?", (recipe,))
        cuisinepathfromdb = c.fetchall()
        for acuisinepath in cuisinepathfromdb:
            acuisinepath = acuisinepath[0]
            newcuisinepath = acuisinepath.split('/')
            acuisinepath = newcuisinepath[1]
            listofcuisinepaths.append(acuisinepath)
    return listofcuisinepaths

def grab_nutrition(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    listofnutritions = []
    for recipe in displayonwebsite:
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

def grab_time(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    times = []
    for recipe in displayonwebsite:
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

def grab_url(displayonwebsite):
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    
    listofurls = []
    for recipe in displayonwebsite:
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
    
    listofrecipes = []
    displayonwebsite = []
    query = request.args.get("Query", '')#the '' is a default value.
    query2 = request.args.get("querying")

    images = []
    
    if query:
        session['query'] = query
    if query2:
        session['query2'] = query2

    alert2 = ""
    
    #print(f"query: {query}")
    #print(f"query2: {query2}")
    #print(f"session['query']: {session['query']}")
    #print(f"session['query2']: {session['query2']}")


    username = session['username']
    #print(username)
    t=0
    #t=4
    if 'ingrsearch_history' not in session or request.args.get('reset') == "reset" or t==4:
            session['ingrsearch_history'] = []
            session['alert'] = ""
            session['query'] = ""
            session['query2'] = ""
            #print(f"resettting")

    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    session['alert'] = ""
    
    recipenames = loadnames()
    splitwords = session['query'].upper().split()
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
                listofrecipes.append(item)#if it does, it adds it to the list
    if len(listofrecipes) == 0:
        session['alert'] = 'norecipessearch'
        session['query'] = ""

    addlist = request.args.get('saveonhomepage')
    recipename = addlist
    #print(f"recipename: {recipename}")
    #print(f"addlist: {addlist}")
    if addlist:
        c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (recipename,))
        ingredientlist = c.fetchall()
        if ingredientlist:
            ingredientlist = ingredientlist[0]
        #print(f"ingredientlist: {ingredientlist}")
        #print(f"recipename: {recipename}")
        while addlist:#if user clicks on this button
            username = session['username']
            c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))
            name = c.fetchall()
            duplicates = False
            #cycle through previously saved recipes
            for previousrecipe in name:
                if previousrecipe[0] == recipename:
                    duplicates = True
            if duplicates == False:#if they haven't added this recipe before
                c.execute("""INSERT INTO userspecrecipes (userid, recipe_name)
                            VALUES (?, ?)""", (username, recipename))
                conn.commit()
                c.execute("SELECT id FROM userspecrecipes WHERE recipe_name = ? AND userid = ?", (recipename, username))
                e = c.fetchall()
                id = e[0][0]
                for i in ingredientlist:
                    c.execute("""INSERT INTO ingredients (recipeid, ingredient_name)
                            VALUES (?, ?)""", (id, i))
                    conn.commit()
                alert2 = "success"
            elif duplicates == True:
                alert2 = "duplicates"
            addlist = ""
            
    ingredientlist = loadingr()
    anotherlist = []
    anotherrlist = []
    forwebsite = []
    count = 0
    if session['query2']:
        session['ingrsearch_history'].append(session['query2'])
        session.modified = True

        #print(f"session['ingrsearch_history]: {session['ingrsearch_history']}")

        #for querying in session['ingrsearch_history']:
        for item in ingredientlist:
            item = list(item)
            item = item[0]
            anotherlist = [ingredient.strip() for ingredient in item.split(',')]
            anotherrlist.append(anotherlist)
        '''
            for item in anotherrlist:
                for ingredient in item:
                    if querying.upper() in ingredient.upper():#if user input is in an ingredient
                        recipename = getrecipename(item)#get recipe name
                        if recipename == None:
                            pass
                        else:
                            forwebsite.append(recipename)
                        break
        '''
        tempcount = len(session['ingrsearch_history'])
        #print(f"tempcount: {tempcount}")
        anothertemplist = []
        tempvar = []
        if tempcount <= 1:
            #for abc in session['ingrsearch_history']:
                #print(f"abc: {abc}")
            for abc in session['ingrsearch_history']:#OR list
                for item in anotherrlist:
                        for ingredient in item:
                            if abc.upper() in ingredient.upper():
                                recipename = getrecipename(item)
                                if recipename == None:
                                    pass
                                else:
                                    anothertemplist.append(recipename)
                                break
        elif tempcount > 1:
            firstquery = session['ingrsearch_history'][0]
            for item in anotherrlist:
                for ingredient in item:
                    if firstquery.upper() in ingredient.upper():
                        recipename = getrecipename(item)
                        if recipename == None:
                            pass
                        else:
                            anothertemplist.append(recipename)
                            break
        #print(f"anothertemplist: {anothertemplist}")
        if tempcount > 1:#if there's more than one query item
            #print(f"anothertemplist: {anothertemplist}")
            for item in anothertemplist:#for every recipe in this list of recipes
                tobreak = False
                #print(f"session['ingrsearch_history']: {session['ingrsearch_history']}")
                #print(f"anothertemplist: {anothertemplist}")
                #print("a")
                c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (item,))#gets recipes original ings
                recipesings = c.fetchall()[0]
                recipesings = list(recipesings)
                recipesings = recipesings[0]
                tempvar = [ingredient.strip() for ingredient in recipesings.split(',')]#puts original ings into list separated by the comma
                #tempvar is the ingredient list (all cleaned up) for this specific recipe
                a = len(tempvar)#length of list of ingredients
                temporarycount = 0
                while temporarycount != a and tobreak == False:
                    #print("b")
                    tempcount2 = 0
                    temp = 0
                    while tempcount2 != tempcount and tobreak == False:#tempcount is how many queries there are
                        #print("c")
                        #print(f"recipename: {item}")
                        #print(f"session['ingrsearch_history'][tempcount2].upper(): {session['ingrsearch_history'][tempcount2].upper()}")
                        #print(f"temporarycount: {temporarycount}")
                        #print(f"tempvar: {tempvar}")
                        #print(f"tempvar[temporarycount].upper(): {tempvar[temporarycount].upper()}")
                        if session['ingrsearch_history'][tempcount2].upper() in tempvar[temporarycount].upper():#if queried ingredient is in an ingredient of the recipe
                            #print(f"yes")
                            tempcount2 += 1
                            for ingredientquery in session['ingrsearch_history']:#cycles through all the queries
                                #print(f"session['ingrsearch_history']:{session['ingrsearch_history']}")
                                #print(f"ingredientquery: {ingredientquery}")
                                for aningredient in tempvar:
                                    #print(f"tempvar: {tempvar}")
                                    #print(f"aningredient: {aningredient}")
                                    if ingredientquery.upper() in aningredient.upper():#if queried ingredient is in the recipe ingredient list
                                        #print(f"adding, ingredientquery: {ingredientquery.upper()}, aningredient: {aningredient.upper()}")
                                        temp += 1
                                        #print(f"temp (which has increased by 1): {temp}")
                                        break

                            if temp == len(session['ingrsearch_history']):#if all queries are in the recipe ingredients
                                #print(f"adding {item} to forwebsite...")
                                forwebsite.append(item)#adds them to be displayed on the website
                                tobreak = True
                                break
                                        
                            '''
                            for aningredient in tempvar:
                                print(f"tempcount2: {tempcount2}")
                                if session['ingrsearch_history'][tempcount2].upper() in aningredient.upper():
                                    print("SUCCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                                    forwebsite.append(item)#add them to be displayed on the website
                            '''
                                    
                        else:#if the first queried item is not in the recipe list then break
                            #print(f"no")
                            #print(f"breaking")
                            break
                        #print(f"herenow")


                    #if tempcount2 == tempcount:
                        #print("SUCCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                        #forwebsite.append(item)#add them to be displayed on the website
                    temporarycount += 1#cycle to the next ingredient in the recipe ingredient list
                    #print(f"temporarycount: {temporarycount}")
        elif tempcount == 1:#if there's only one query item
            for recipe in anothertemplist:
                forwebsite.append(recipe)

                    

        #print(f"forwebsite: {forwebsite}")
        #print(f"sessicon search history: {session['ingrsearch_history']}")


        try:
            x = forwebsite[0]
            if len(forwebsite) > 0:
                session['alert'] == ""

            if listofrecipes:
                if listofrecipes == forwebsite:
                    displayonwebsite = listofrecipes
                else:
                    for recipe in listofrecipes:
                        for anotherrecipe in forwebsite:
                            if recipe == anotherrecipe:
                                alrthere = False
                                for item in displayonwebsite:
                                    if item == recipe:
                                        alrthere = True
                                if alrthere == False:
                                    displayonwebsite.append(recipe)
                            
                    #print(f"listofrecipes: {listofrecipes}")
                    #print(f"forwebsite: {forwebsite}")
                    #print(f"displayonwebsite: {displayonwebsite}")
                if len(displayonwebsite) == 0:
                    session['alert'] = 'nocriteria'
                    session['query'] = ""
                    session['query2'] = ""
                    return render_template("home.html", listofrecipes=displayonwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], alert2=alert2)
                else:
                    #print(f"top")
                    images = grab_image(displayonwebsite)
                    times = grab_time(displayonwebsite)
                    servings = grab_servings(displayonwebsite)
                    rating = grab_rating(displayonwebsite)
                    cuisine_path = grab_cuisine_path(displayonwebsite)
                    nutrition = grab_nutrition(displayonwebsite)
                    url = grab_url(displayonwebsite)
                    return render_template("home.html", listofrecipes=displayonwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url, alert2=alert2)
            else:
                images = grab_image(forwebsite)
                times = grab_time(forwebsite)
                servings = grab_servings(forwebsite)
                rating = grab_rating(forwebsite)
                cuisine_path = grab_cuisine_path(forwebsite)
                nutrition = grab_nutrition(forwebsite)
                url = grab_url(forwebsite)
                return render_template("home.html", listofrecipes=forwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url, alert2=alert2)
        except:
            pass

    if len(forwebsite) > 0:
        session['alert'] = ""
    elif len(forwebsite) < 1 and request.args.get('reset') != "reset" and request.args.get('querying') != None:#if they havent clicked the reset button and they havent just loaded the page
        #print("no recipes")
        session['alert'] = "norecipes"
        session['ingrsearch_history'] = []
    
    preptime = request.args.get('preptime')
    cooktime = request.args.get('cooktime')
    totaltime = request.args.get('totaltime')

    if preptime:
        c.execute("SELECT prep_time FROM tableofrecipes2")
        allpreptime = c.fetchall()
        print(f"ALLPREPTIME: {allpreptime}")

    session['search_history'] = session['query']

    if forwebsite:
        if listofrecipes == forwebsite:
            displayonwebsite = listofrecipes
        else:
            for recipe in listofrecipes:
                for anotherrecipe in forwebsite:
                    if recipe == anotherrecipe:
                        alrthere = False
                        for item in displayonwebsite:
                            if item == recipe:
                                alrthere = True
                        if alrthere == False:
                            displayonwebsite.append(recipe)
        if len(displayonwebsite) == 0:
                session['alert'] = 'nocriteria'
                session['query'] = ""
                session['query2'] = ""
        #print(f"listofrecipes: {listofrecipes}")
        #print(f"forwebsite: {forwebsite}")
        #print(f"displayonwebsite: {displayonwebsite}")
        #print(f"bottom")
        images = grab_image(displayonwebsite)
        times = grab_time(displayonwebsite)
        servings = grab_servings(displayonwebsite)
        rating = grab_rating(displayonwebsite)
        cuisine_path = grab_cuisine_path(displayonwebsite)
        nutrition = grab_nutrition(displayonwebsite)
        url = grab_url(displayonwebsite)
        return render_template("home.html", listofrecipes=displayonwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url, alert2=alert2)

    
    #print(f"vbottom")
    images = grab_image(listofrecipes)
    times = grab_time(listofrecipes)
    servings = grab_servings(listofrecipes)
    rating = grab_rating(listofrecipes)
    cuisine_path = grab_cuisine_path(listofrecipes)
    nutrition = grab_nutrition(listofrecipes)
    url = grab_url(listofrecipes)
    c.close()
    conn.close()
    return render_template("home.html", listofrecipes=listofrecipes, username=username, alert=session['alert'], search_history=session['search_history'], images=images, times=times, servings=servings, rating=rating, cuisine_path=cuisine_path, nutrition=nutrition, url=url, alert2=alert2)

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
        

    addlist = request.args.get("saverecipe")
    while addlist == 'button':#if user clicks on this button
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
            e = c.fetchall()
            id = e[0][0]
            for i in ingredientlist:
                c.execute("""INSERT INTO ingredients (recipeid, ingredient_name)
                        VALUES (?, ?)""", (id, i))
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
        addlist = ""
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
