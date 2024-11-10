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
    flashmessage = 'False'
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    confirmpassword = request.form.get('confirmpassword')
    if password:
        if len(password) > 6:
            username4len = str(username)
            password4len = str(password)
            if username and password and password == confirmpassword:
                password = generate_password_hash(password)
                try:
                    c.execute("""INSERT INTO users (username, password)
                    VALUES (?, ?)""", (username, password))
                    c.execute("SELECT * FROM users")
                    print(f"All values in database: {c.fetchall()}.")
                    conn.commit()
                    c.close()
                    conn.close()
                    return redirect(url_for('login'))
                except:
                    flashmessage = 'sameusername'
            elif password != confirmpassword:
                flashmessage = "passwords do not match"
            elif len(username4len) < 1 and len(password4len) >= 1 or len(password4len) < 1 and len(username4len) >= 1:
                flashmessage = 'notfilledout'
        else:
            flashmessage = "password too short"
    return render_template("signup.html", flashmessage=flashmessage)

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
    if 'username' not in session:#if they're username isnt actually saved
        return redirect(url_for('login'))#redirects them back to the login page.
    
    row = ""
    newlist = ""
    newrecipelist = []
    displayonwebsite = []
    query = request.args.get("Query", '')#the '' is a default value.
    query2 = request.args.get("querying")

    if query:
        session['query'] = query
    if query2:
        session['query2'] = query2

    print(f"query: {query}")
    print(f"query2: {query2}")
    print(f"session['query']: {session['query']}")
    print(f"session['query2']: {session['query2']}")


    username = session['username']
    #print(username)
    t=0
    #t=4
    if 'ingrsearch_history' not in session or request.args.get('reset') == "reset" or t==4:
            session['ingrsearch_history'] = []
            session['alert'] = ""
            session['query'] = ""
            session['query2'] = ""
            print(f"resettting")

    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()

    session['alert'] = ""

    c.execute("SELECT recipe_name FROM tableofrecipes2")
    row = c.fetchall()
    try:
        row = list(row)
    except:
        pass
    count = 0
    newlist = []
    for item in row:
        item = row[count]
        item = item[0]
        newlist.append(item)
        count += 1
    #print(f"finished list: {newlist}")#i have removed the tuples


    
    recipenames = loadnames()
    newrecipelist = []
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
                newrecipelist.append(item)#if it does, it adds it to the list
    if len(newrecipelist) == 0:
        session['alert'] = 'norecipessearch'
        session['query'] = ""



    ingredientlist = loadingr()
    anotherlist = []
    anotherrlist = []
    forwebsite = []
    count = 0
    if session['query2']:
        session['ingrsearch_history'].append(session['query2'])
        session.modified = True

        print(f"session['ingrsearch_history]: {session['ingrsearch_history']}")

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
        print(f"anothertemplist: {anothertemplist}")
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
                            print(f"breaking")
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

            if newrecipelist:
                if newrecipelist == forwebsite:
                    displayonwebsite = newrecipelist
                else:
                    for recipe in newrecipelist:
                        for anotherrecipe in forwebsite:
                            if recipe == anotherrecipe:
                                alrthere = False
                                for item in displayonwebsite:
                                    if item == recipe:
                                        alrthere = True
                                if alrthere == False:
                                    displayonwebsite.append(recipe)
                                
                #print(f"newrecipelist: {newrecipelist}")
                #print(f"forwebsite: {forwebsite}")
                #print(f"displayonwebsite: {displayonwebsite}")
            if len(displayonwebsite) == 0:
                session['alert'] = 'nocriteria'
                session['query'] = ""
                session['query2'] = ""
                return render_template("home.html", row=row, newlist=newlist, newrecipelist=displayonwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'])
            else:
                print(f"top")
                return render_template("home.html", row=row, newlist=newlist, newrecipelist=forwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'])
        except:
            pass


    if len(forwebsite) > 0:
        session['alert'] = ""
    elif len(forwebsite) < 1 and request.args.get('reset') != "reset" and request.args.get('querying') != None:#if they havent clicked the reset button and they havent just loaded the page
        print("no recipes")
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
        if newrecipelist == forwebsite:
            displayonwebsite = newrecipelist
        else:
            for recipe in newrecipelist:
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
        #print(f"newrecipelist: {newrecipelist}")
        #print(f"forwebsite: {forwebsite}")
        print(f"displayonwebsite: {displayonwebsite}")
        print(f"bottom")
        return render_template("home.html", row=row, newlist=newlist, newrecipelist=displayonwebsite, querying=session['ingrsearch_history'], username=username, alert=session['alert'], search_history=session['search_history'])

    c.close()
    conn.close()
    print(f"vbottom")
    return render_template("home.html", row=row, newlist=newlist, newrecipelist=newrecipelist, username=username, alert=session['alert'])

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
        print("clicked on button")
        try:
            username = session['username']
        except:
            alert = "nousername"
            break
        print(f"username: {username}")
            
        c.execute("SELECT recipe_name FROM userspecrecipes WHERE userid=?", (username,))
        name = c.fetchall()
        print(f"name: {name}")
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
