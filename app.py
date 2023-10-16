import os,json,requests

from flask import Flask,render_template,flash,request, redirect, session, g,render_template_string
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func,any_,update
from flask_bcrypt import check_password_hash,bcrypt
# from flask_bcrypt import 
# from bcrypt import  check_password_hash
from forms import SignUpForm,LoginForm,EditPassword,creationForm,userEditForm
from models import db,User,Recipe,RecipeUser,connect_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)



# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone1'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

toolbar = DebugToolbarExtension(app)
# bcrypt = Bcrypt(app)
connect_db(app)
app.app_context().push()
db.create_all()



@app.before_request
def add_user_to_g():
        

        # METHOD = "recipes.search.v3"
        # format_type = "json"
        # # recipe_types= "Appetizer"
        # access_token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ4NDUzNUJFOUI2REY5QzM3M0VDNUNBRTRGMEJFNUE2QTk3REQ3QkMiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJTRVUxdnB0dC1jTno3Rnl1VHd2bHBxbDkxN3cifQ.eyJuYmYiOjE2OTczMjU5NjUsImV4cCI6MTY5NzQxMjM2NSwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.ZYTJf0IQ7daBmvkMuk574v7sfM53Ye_SuQlDCQBbXdauWr8ANbJFsitbYsuHza3KJe4nFyLVWcLwb1cPwqb_PZzmk9-7KuNxnHLoUk_1_YhipEL-X-EjDmtH0DD4cj7yMx6iKe8CNXV0H8yPCfxqPkFmGXNvlxPMMZ4Mk8yNyWSr8oyydfAtjzI_fudmAtiAzrk_aL3wn8okA0A0GS2ocjCCKZFdiWE_VJz0zQ5czmMZJkBb_dFqShHrlFsocUAGK3P-OM7pHdAQHLq2eFaVprOBCOnguytawZCZBeuGsq5_VRQyj3gn9nTUZpnUdwA0PhGM7BoPr3pJgecPY2L-sQ"
        # response = requests.get(
        # "https://platform.fatsecret.com/rest/server.api",
        # params={
        #     "method": METHOD,
        #     "format": format_type,
        #     "max_results":"50",
        #     "must_have_images":True
        #     # "recipe_types":recipe_types

        #     # "region":region
        # },
        # headers={"Authorization": f'Bearer {access_token}'}
        # )

        # # Create a cursor
        # # cursor = db.cursor()
        
        # # Make an API call to get the list of recipes
        # if response.status_code == 200:

        #     if format_type == "json":
        #          recipe_data = json.loads(response.content.decode('utf-8'))
        #          for recipe in recipe_data['recipes']['recipe']:
        #                 new_recipe = Recipe(recipe_name=recipe['recipe_name'],
        #                                     recipe_description=recipe["recipe_description"],
        #                                     recipe_image=recipe["recipe_image"],
        #                                     recipe_type=recipe["recipe_types"]["recipe_type"],
        #                                     ingredients=recipe['recipe_ingredients']['ingredient']
        #                 )
        #                 db.session.add(new_recipe)
        #                 db.session.commit()


            
            
                        
                        

                      


                # db.session.add(new_recipe)
                # db.session.commit()
        

                                
        if CURR_USER_KEY in session:
          g.user = User.query.get(session[CURR_USER_KEY])
        else:
           g.user = None

    


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]




@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    user=g.user


    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
        
            return redirect("/")

        flash("Invalid credentials.", 'danger')

            

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("you have successfuly log out", 'success')
    return redirect('/login')
    # flash("Invalid credentials.", 'danger')


    flash("You have successfully logged out.", 'success')
    return redirect("/login")



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = SignUpForm()
    if form.validate_on_submit():
        # try:
        user = User.signup(
        username=form.username.data,
        password=form.password.data,
        email=form.email.data,
                # country=form.country.data
        )
        db.session.commit()
            # import pdb
            # pdb.set_trace()
        # except IntegrityError:
        #     import pdb
        #     pdb.set_trace()
        #     flash("Username already taken", 'danger')
        #     return render_template("signup.html", form=form)
        
        do_login(user)

        return redirect("/")
    else:
        return render_template('signup.html', form=form)



            
   

# app.py
@app.route('/')
def homepage():
  """Show homepage:

  - anon users: no messages
  - logged in: 100 most recent messages of followed_users
  """
  user=g.user
  if user:
      return render_template('home.html',user=user)
  else:
      return render_template('base.html')

#   form=SignUpForm()
#   METHOD = "recipe_types.get.v2"
#   format_type = "json"
#   access_token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ4NDUzNUJFOUI2REY5QzM3M0VDNUNBRTRGMEJFNUE2QTk3REQ3QkMiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJTRVUxdnB0dC1jTno3Rnl1VHd2bHBxbDkxN3cifQ.eyJuYmYiOjE2OTY2MDYzODMsImV4cCI6MTY5NjY5Mjc4MywiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.vaF86UfvXV7ckBWZPU0j-THxmoT6q6zEtqov4BQ2bvDkWaGTLeKzu0gBLqvBJ6mdmOmcmjrkwZFRiX6cX-bRlQVexTZw8hR6W4aEumzj9FdZ9SeYHX8zLAM04mXLZmiH8NJmgCop5cYUxJ_idS11xPif7Yj6hAJ-d9_qLnf2lnXgH7dxB4xINZVDPK4sr558EeV8KyMW2ZGaQivMAiQOCBJ5cpn8OoeitWnQwgx0G8NmULNAvbxfxNnLzFzZnBDF1JHXB5vftEHpc9YW2h8Un8v5W27GNsVq2nfL2irIWqimD6GFwt2sfsfNgbYz8Z_wHTif63bf-jsdHGv5e6_mQQ"
#   response = requests.get(
#     "https://platform.fatsecret.com/rest/server.api",
#     params={
#       "method": METHOD,
#       # "search_expression": search_expression,
#       # "page_number": page_number,
#       # "max_results": max_results,
#       "format": format_type,
#       # "region":region
#     },
#     headers={"Authorization": f'Bearer {access_token}'}
     
#   )

#   if g.user:
#     if response.status_code == 200:

#     # METHOD = "recipe.search.v3"
#     # format_type = "json"
#     # access_token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjVGQUQ4RTE5MjMwOURFRUJCNzBCMzU5M0E2MDU3OUFEMUM5NjgzNDkiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJYNjJPR1NNSjN1dTNDeldUcGdWNXJSeVdnMGsifQ.eyJuYmYiOjE2OTYyODYyODcsImV4cCI6MTY5NjM3MjY4NywiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.ExWEPgtTJwHQyqgeaBwX0k4cXbrtjirfo1eP2OmhZ8uxgTBdVKttUj9oxYEBD6Vl16NMQq8p39iQ_WIeH1Myqh8zTJc8LCUrCxec2Dc4pcaeCrdyLQ0bqqkKadPsd78UnuhQajtC0OK6_cuYHlXLN5YtUTWBU9iINWkyaXoIUlBi8Fy6Et8JaRAN3R6OpNmQZ5-QWok8OsLDA0g9km4zoW1UmglupaUqVvGk8Ah2stOHU9sCLpb6-AS5fi7FFqdSXk3GSKJMUp52QYYc7cRiMbpcEUhH4IpD5G9FnQXNyeTJ8Tn2L_HzeVo10myBUlortSLgGA3DdYqZn11FOEI3OA"
#      # if format_type == "json":
#     # Parse the JSON response
#     # json_data = response.json()
#       # data=jsonify(json_data)
#       # food_list = data["foods"]["food"]
#         json_data = json.loads(response.content)
#         # import pdb
#         # pdb.set_trace()
#         recipe_tyypes = json_data["recipe_types"]["recipe_type"]
#   return render_template('home.html',user=user) 
#     else:
#         return f"Request failed with status code: {response.status_code}"
  
#   flash("Invalid credentials.", 'danger')
#   return render_template('base.html')




# @app.route('/{{recipe}}')
# def getRecipeDescription(recipe):
#     METHOD = "recipes.search.v3"
#     format_type = "json"
#     recipe_types = recipe
#     # import pdb
#     # pdb.set_trace()

#     access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ4NDUzNUJFOUI2REY5QzM3M0VDNUNBRTRGMEJFNUE2QTk3REQ3QkMiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJTRVUxdnB0dC1jTno3Rnl1VHd2bHBxbDkxN3cifQ.eyJuYmYiOjE2OTY0NjIzNzQsImV4cCI6MTY5NjU0ODc3NCwiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.RILQiKnc_4HmE1SDwXztuF9S_solHWgKqMJg8HPswwBQs5-T9nz6idE2rS-_lJDUCYEiY-7XuwnsB4DkQq3nE7lv6rAzwjQSR7lcWmtBZ7q8jIvyU7DMyCHyWsEz-v3TngvdyYzTEkKTa-Q5MDUyUuKZs1SePzrU_etLykRpyBULfeq6xffgOE_mUIN6I5zKqwsgb7MsXLD7p5v8FbsifWlGGrVUE18jB6Lm-5ySj8Igz7OZ6DbwC_N2Zo3XimhpjkOERItOBUdkNIZrFK_ahH29Q1u0wIg65iYCCfEA380Cd8hmVUObiKmhtXEfR9xpi8MndJfUsIIeCLSIqwQ3Gg"

#     response1 = requests.get(
#     "https://platform.fatsecret.com/rest/server.api",
#     params={
#         "method": METHOD,
#         "format": format_type,
#         "recipe_types": recipe_types,
#     },
#     headers={"Authorization": f'Bearer {access_token}'},
#     )

#     if response1.status_code == 200:
#         # import pdb 
#         # pdb.set_trace()
#         if format_type == "json":
#             API_datas = json.loads(response1.content)
#             recipe_descriptions = []
#             recipe_names=[]
            
#             for data in API_datas["recipes"]["recipe"]:
#                 recipe_descriptions.append(data["recipe_description"])
#                 recipe_names.append(data["recipe_name"])
                
#                 # import pdb 
#                 # pdb.set_trace()
#             return render_template("description.html", recipe_descriptions=recipe_descriptions,recipe_names=recipe_names)
#         else:
#             return f"Request failed with status code: {response1.status_code}"
#     else:
#         return f"Request failed with status code: {response1.status_code}"

@app.route("/create/<int:user_id>", methods=["GET", "POST"])
def create_recipe(user_id):
    user = User.query.get_or_404(user_id)
    form = creationForm()
    
    if form.validate_on_submit():
        new_recipe = RecipeUser(
            name=form.name.data,
            ingredients=form.ingredients.data,
            # instructions=form.instructions.data,
            image=form.image.data,
            description=form.description.data,
            user_id=int(user_id)
        )
        
        db.session.add(new_recipe)
        db.session.commit()
        flash("New recipe added")
        return redirect("/")
    else:
        return render_template("Addrecipe.html", form=form,user=user)

    

@app.route('/users/profile', methods=["GET"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    
    form=userEditForm()
    return render_template ("editProfile.html",form=form)


@app.route('/users/profile', methods=["POST"])
def handleModification():
    """Handle modification of users' profiles."""
    form=userEditForm()
    user=g.user
    passwordcorrect=user.password
    Current_password=form.Current_password.data
    # import pdb
    # pdb.set_trace()
    if check_password_hash(passwordcorrect, Current_password):
        username=form.username.data,
        email=form.email.data
       
        if form.validate_on_submit():
            user.username=username
            user.email=email
            user.password=password
            db.session.commit()
            flash('Your profile has been modified.', category='success')
            # im                                                                                                                 port pdb
            # pdb.set_trace()
            # user= User(email=user.email,username=user.username,image_url=user.image_url,location=user.location,bio=user.bio,header_image_url=user.header_image_url)
            # # db.session.add(user)
            return render_template("/usersdetail.html",user=user)
        flash("wrong username", 'danger')
        return redirect('/users/profile')
    flash("wrong password", 'danger')
    return redirect('/')
    

@app.route("/Appetizer")
def Appetizer():
    # import pdb
    # pdb.set_trace()
    
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Appetizer")).all()
    for result in results:
            appetizer_recipes = []

    # Extract the required fields from the results
    for result in results:
        appetizer_recipes.append({
            "id":result.id,
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })

    unique_recipes = {}
    for recipe in appetizer_recipes :
        unique_recipes[recipe['recipe_name']] = recipe

# Convert the dictionary values back to a list to get unique recipes
        unique_recipe_list = list(unique_recipes.values())

    # Render the results using a template (assuming you have a template)
    return render_template('appetizers.html', unique_recipe_list = unique_recipe_list )

@app.route("/Breakfast")
def Breakfast():
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Breakfast")).all()
    for result in results:
            breakfast_recipes = []

    # Extract the required fields from the results
    for result in results:
        breakfast_recipes.append({
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })

    # Render the results using a template (assuming you have a template)
    return render_template('breakfast.html', breakfast_recipes=breakfast_recipes)

@app.route("/Dessert")
def Dessert():
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Dessert")).all()
    # iterate over the results array and only take unique value 
    
    for result in results:
            Dessert_recipes = []

    # Extract the required fields from the results
    for result in results:
        Dessert_recipes.append({
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })
        # import pdb
        # pdb.set_trace()

    unique_recipes = {}
    for recipe in Dessert_recipes:
        unique_recipes[recipe['recipe_name']] = recipe

# Convert the dictionary values back to a list to get unique recipes
        unique_recipe_list = list(unique_recipes.values())

# Now, unique_recipe_list contains unique recipes
    # for recipe in unique_recipe_list:
    #      print(recipe)


    # Render the results using a template (assuming you have a template)
    return render_template('dessert.html', unique_recipe_list=unique_recipe_list)


@app.route("/Main-dish")
def Main():
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Dessert")).all()
    for result in results:
            Main_recipes = []

    # Extract the required fields from the results
    for result in results:
        Main_recipes.append({
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients

        })

    # Render the results using a template (assuming you have a template)
    return render_template('Main.html', Main_recipes=Main_recipes)


@app.route("/Baked")
def baked():
    # import pdb
    # pdb.set_trace()
    
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Baked")).all()
    for result in results:
           baked_recipes = []

    # Extract the required fields from the results
    for result in results:
       baked_recipes.append({
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })

    unique_recipes = {}
    for recipe in baked_recipes :
        unique_recipes[recipe['recipe_name']] = recipe

# Convert the dictionary values back to a list to get unique recipes
        unique_recipe_list = list(unique_recipes.values())

    # Render the results using a template (assuming you have a template)
    return render_template('baked.html', unique_recipe_list = unique_recipe_list )




@app.route("/creation/<int:user_id>")
def creation(user_id):
    user = User.query.get_or_404(user_id)
    user_recipe=[]
    # name=RecipeUser.name,
    # image=RecipeUser.image,
    # description=RecipeUser.description,
    # ingredients=RecipeUser.ingredients

    
    recipe_creation=db.session.query(RecipeUser).filter(RecipeUser.user_id==user_id)
    for recipe in recipe_creation:
        user_recipe.append({
            'name': recipe.name,
            'image': recipe.image,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            "user_id":recipe.user_id
        })    
    # import pdb
    # pdb.set_trace()

    return render_template('creation.html',user_recipe=user_recipe)



 
@app.route("/others/<int:user_id>")
def others(user_id):
    user = User.query.get_or_404(user_id)
    user_recipe=[]
    # name=RecipeUser.name,
    # image=RecipeUser.image,
    # description=RecipeUser.description,
    # ingredients=RecipeUser.ingredients

    
    recipe_creation=db.session.query(RecipeUser).filter(RecipeUser.user_id != user_id)
    for recipe in recipe_creation:
        user_recipe.append({
            'name': recipe.name,
            'image': recipe.image,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            "user_id":recipe.user_id
        })    
    # import pdb
    # pdb.set_trace()

    return render_template('creation.html',user_recipe=user_recipe)


@app.route("/<int:recipe_id>")
def show_recipe(recipe_id):
    """Show a single recipe."""
    # import pdb
    # pdb.set_trace()
    
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Appetizer")).all()
    for result in results:
            appetizer_recipes = []

    # Extract the required fields from the results
    for result in results:
        appetizer_recipes.append({
            "id":result.id,
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })

    unique_recipes = {}
    for recipe in appetizer_recipes :
        unique_recipes[recipe['recipe_name']] = recipe

# Convert the dictionary values back to a list to get unique recipes
        unique_recipe_list = list(unique_recipes.values())

    # session = db.session
    # update(Recipe).where(Recipe.id == recipe_id ).values(favorite_recipe=True).execute(session)
    # db.session.commit()
    db.session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.favorite_recipe: True})
    db.session.commit()


# Commit the changes



    # Render the results using a template (assuming you have a template)
    return render_template('appetizers.html', unique_recipe_list = unique_recipe_list )

@app.route("/Appetizer/<int:recipe_id>")
def down_recipe(recipe_id):
    """Downvote a recipe."""
    flash('Your profile has been modified.', category='success')

    results = db.session.query(Recipe).filter(Recipe.recipe_type.any("Appetizer")).all()
    for result in results:
            appetizer_recipes = []

    # Extract the required fields from the results
    for result in results:
        appetizer_recipes.append({
            "id":result.id,
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients":result.ingredients
        })

    unique_recipes = {}
    for recipe in appetizer_recipes :
        unique_recipes[recipe['recipe_name']] = recipe

# Convert the dictionary values back to a list to get unique recipes
        unique_recipe_list = list(unique_recipes.values())

    # session = db.session
    # update(Recipe).where(Recipe.id == recipe_id ).values(favorite_recipe=True).execute(session)
    # db.session.commit()
    db.session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.favorite_recipe: False})
    db.session.commit()

    return render_template('appetizers.html', unique_recipe_list = unique_recipe_list )



@app.route("/favorite")
def favorite():
    """List all favorite recipes."""
    recipe_favorites=[]
    favorites= db.session.query(Recipe).filter(Recipe.favorite_recipe == True)
    for fav in favorites:
        recipe_favorites.append({
            'id': fav.id,
            'recipe_name': fav.recipe_name,
            'recipe_image': fav.recipe_image,
            'recipe_description': fav.recipe_description,
            'ingredients': fav.ingredients
        })
    return render_template("favorite.html",recipe_favorites=recipe_favorites)



    

      
    # for favorite in favorites:
    #     fav=favorite["recipe_name"]
    import pdb
    pdb.set_trace()
    return render_template("appetizers.html")

    






    
    






#     search_term = request.args.get('term', 'Appetizer')  # Default to 'Appetizer' if 'term' not provided

#     # Modify the query to use LIKE and ANY together
#     results = Recipe.query.filter(func.any(Recipe.recipe_type.ilike('%' + search_term + '%'))).all()

#    Search for rows where 'Breakfast' is in the 'recipe_type' array
#     search_term = 'Appetizer'
    # results = db.session.query(Recipe.recipe_name, Recipe.recipe_image).filter(any_(Recipe.recipe_type).contains(search_term)).all()
    # import pdb
    # pdb.set_trace()

    # Get the results
    # results = db.query.all()
    # for result in results:
    #     recipe_name, recipe_image = result
    # print(f"Recipe Name: {recipe_name}, Recipe Image: {recipe_image}")


    
