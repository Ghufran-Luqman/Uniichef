from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'ilikecooking'

def loadnames():
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    c.execute("SELECT recipe_name FROM tableofrecipes2")
    list = c.fetchall()
    c.close()
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
    username = request.args.get('username')
    password = request.args.get('password')
    username4len = str(username)
    password4len = str(password)
    if username and password:
        #do conn.close() as soon as possible
        try:
            c.execute("""INSERT INTO users (username, password)
            VALUES (?, ?)""", (username, password))
            c.execute("SELECT * FROM users")
            print(f"All values in database: {c.fetchall()}.")
            conn.commit()
            c.close()
            conn.close()
        except:
            flashmessage = 'sameusername'
    elif len(username4len) < 1 and len(password4len) >= 1 or len(password4len) < 1 and len(username4len) >= 1:
        flashmessage = 'notfilledout'
    return render_template("signup.html", flashmessage=flashmessage)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login = False
    flashmessage = False
    conn = sqlite3.connect("recipes.db")
    c = conn.cursor()
    username = request.args.get('username')
    password = request.args.get('password')
    username4len = str(username)
    password4len = str(password)
    if username and password:
        c.execute("SELECT username, password FROM users")
        listofusernames = c.fetchall()
        for item in listofusernames:
            if item[0].lower() == username.lower():#if usernames match
                if item[1] == password:#if passwords of that username match
                    login = True
                    break
                elif item[1] != password:
                    flashmessage = 'incorrect'
                else:
                    print("unknown error")
                    flashmessage = 'unknownerror'
        if login == True:
            return redirect(url_for('home', username=username))
        else:
            flashmessage = 'incorrect'
    elif len(username4len) < 1 and len(password4len) >= 1 or len(password4len) < 1 and len(username4len) >= 1:
        flashmessage = 'notfilledout'
    return render_template("login.html", flashmessage=flashmessage)

@app.route('/home', methods=['GET', 'POST'])
def home():
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

    query2 = request.args.get("querying")
        
    if 'search_history' not in session or request.args.get('reset') == "reset":
        session['search_history'] = []
    

    ingredientlist = loadingr()
    anotherlist = []
    anotherrlist = []
    forwebsite = []
    count = 0
    if query2:
        session['search_history'].append(query2)
        session.modified = True

        #for querying in session['search_history']:
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
        tempcount = len(session['search_history'])
        #print(f"tempcount: {tempcount}")
        anothertemplist = []
        tempvar = []
        if tempcount <= 1:
            #for abc in session['search_history']:
                #print(f"abc: {abc}")
            for abc in session['search_history']:#OR list
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
            firstquery = session['search_history'][0]
            for item in anotherrlist:
                for ingredient in item:
                    if firstquery.upper() in ingredient.upper():
                        recipename = getrecipename(item)
                        if recipename == None:
                            pass
                        else:
                            anothertemplist.append(recipename)
                            break
        if tempcount > 1:#if there's more than one query item
            #print(f"anothertemplist: {anothertemplist}")
            for item in anothertemplist:#for every recipe in this list of recipes
                #print(f"session['search_history']: {session['search_history']}")
                #print(f"anothertemplist: {anothertemplist}")
                #print("a")
                c.execute("SELECT ingredients FROM tableofrecipes2 WHERE recipe_name=?", (item,))#gets recipes original ings
                recipesings = c.fetchall()[0]
                recipesings = list(recipesings)
                recipesings = recipesings[0]
                tempvar = [ingredient.strip() for ingredient in recipesings.split(',')]#puts original ings into list separated by the comma
                a = len(tempvar)#length of list of ingredients
                temporarycount = 0
                while temporarycount != a:
                    #print("b")
                    tempcount2 = 0
                    getout = 0
                    temp = 0
                    while tempcount2 != tempcount:
                        #print("c")
                        #print(f"recipename: {item}")
                        #print(f"session['search_history'][tempcount2].upper(): {session['search_history'][tempcount2].upper()}")
                        #print(f"temporarycount: {temporarycount}")
                        #print(f"tempvar: {tempvar}")
                        #print(f"tempvar[temporarycount].upper(): {tempvar[temporarycount].upper()}")
                        if session['search_history'][tempcount2].upper() in tempvar[temporarycount].upper():#if queried ingredient is in an ingredient of the recipe
                            #print(f"yes")
                            tempcount2 += 1
                            for ingredientquery in session['search_history']:#cycles through all the queries
                                #print(f"session['search_history']:{session['search_history']}")
                                #print(f"ingredientquery: {ingredientquery}")
                                for aningredient in tempvar:
                                    #print(f"tempvar: {tempvar}")
                                    #print(f"aningredient: {aningredient}")
                                    if ingredientquery.upper() in aningredient.upper():#if queried ingredient is in the recipe ingredient list
                                        #print(f"adding, ingredientquery: {ingredientquery.upper()}, aningredient: {aningredient.upper()}")
                                        temp += 1
                                        #print(f"temp (which has increased by 1): {temp}")
                                        break

                            if temp == len(session['search_history']):#if all queries are in the recipe ingredients
                                #print(f"adding {item} to forwebsite...")
                                forwebsite.append(item)#adds them to be displayed on the website
                                break
                                        
                            '''
                            for aningredient in tempvar:
                                print(f"tempcount2: {tempcount2}")
                                if session['search_history'][tempcount2].upper() in aningredient.upper():
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
        #print(f"sessicon search history: {session['search_history']}")


        try:
            x = forwebsite[0]
            return render_template("home.html", row=row, newlist=newlist, newrecipelist=forwebsite, querying=session['search_history'])
        except:
            pass

    c.close()
    conn.close()
    return render_template("home.html", row=row, newlist=newlist, newrecipelist=newrecipelist)


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
    
    c.close()
    conn.close()
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
    c.close()
    conn.close()
    return render_template('test.html', list=list2)


if __name__ == "__main__":
    app.run(debug=True)
