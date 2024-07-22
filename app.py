import os,json

from flask import Flask,flash,render_template,flash,request, redirect, session, g,render_template_string
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func,any_,update
from flask_bcrypt import check_password_hash,bcrypt
# from flask_bcrypt import 
# from bcrypt import  check_password_hash
from forms import SignUpForm,LoginForm,EditPassword,creationForm,userEditForm
from models import db,User,Recipe,RecipeUser,connect_db,Favorite

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# pg_dump --column-inserts --data-only --table=recipes capstone1 > recipes.sql

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL'))
    # os.environ.get('DATABASE_URL', 'postgresql:///capstone1')) 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.debug = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

# toolbar = DebugToolbarExtension(app)
# bcrypt = Bcrypt(app)
connect_db(app)
app.app_context().push()
db.create_all()



@app.before_request
def add_user_to_g():
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
    






    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        

        

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!,you have successfuly logged in", "success")
        
            return redirect("/")

        flash("Invalid credentials.", 'danger')

            

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("you have successfuly log out", "success")
    return redirect('/login')




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

        )
        db.session.commit()
 
        do_login(user)

        return redirect("/")
    else:
        return render_template('signup.html', form=form)

@app.route('/')
def homepage():
  """Show homepage:

  - anon users: no messages
  - logged in: 100 most recent messages of followed_users
  """

  return render_template('home.html')





@app.route("/create/<int:user_id>", methods=["GET", "POST"])
def create_recipe(user_id):
    user = User.query.get_or_404(user_id)
    form = creationForm()
    
    if form.validate_on_submit():
        new_recipe = RecipeUser(
            name=form.name.data,
            ingredients=form.ingredients.data,

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
    
    form=userEditForm()
    return render_template ("editProfile.html",form=form)


@app.route('/users/profile', methods=["POST"])
def handleModification():
    """Handle modification of users' profiles."""
    form=userEditForm()
    user=g.user
    passwordcorrect=user.password
    Current_password=form.Current_password.data

    if check_password_hash(passwordcorrect, Current_password):
        username=form.username.data,
        email=form.email.data
       
        if form.validate_on_submit():
            user.username=username
            user.email=email
            user.password=form.password
            db.session.commit()
            flash('Your profile has been modified.', category='success')

            return render_template("/usersdetail.html",user=user)
        flash("wrong username", 'danger')
        return redirect('/users/profile')
    flash("wrong password", 'danger')
    return redirect('/')
    


@app.route("/creation/<int:user_id>")
def creation(user_id):
    user = User.query.get_or_404(user_id)
    user_recipe=[]


    
    recipe_creation=db.session.query(RecipeUser).filter(RecipeUser.user_id==user_id)
    for recipe in recipe_creation:
        user_recipe.append({
            'name': recipe.name,
            'image': recipe.image,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            "user_id":recipe.user_id
        })    


    return render_template('creation.html',user_recipe=user_recipe)



 
@app.route("/others/<int:user_id>")
def others(user_id):
    user = User.query.get_or_404(user_id)
    user_recipe=[]


    
    recipe_creation=db.session.query(RecipeUser).filter(RecipeUser.user_id != user_id)
    for recipe in recipe_creation:
        user_recipe.append({
            'name': recipe.name,
            'image': recipe.image,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            "user_id":recipe.user_id
        })    

    return render_template('creation.html',user_recipe=user_recipe)






# Create a function to retrieve and process recipes
def get_processed_recipes(recipe_type):
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any(recipe_type)).all()
    recipes = []

    for result in results:
        recipes.append({
            "id": result.id,
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients": result.ingredients
        })

    unique_recipes = {}
    for recipe in recipes:
        unique_recipes[recipe['recipe_name']] = recipe

    unique_recipe_list = list(unique_recipes.values())
    return unique_recipe_list





def update_and_get_recipes(recipe_type, recipe_id, favorite=True):
    # Update the favorite status

    db.session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.favorite_recipe: favorite})
   
    # Retrieve the recipes of the specified type
    results = db.session.query(Recipe).filter(Recipe.recipe_type.any(recipe_type)).all()
    recipes = []
    for result in results:
        recipes.append({
            "id": result.id,
            "recipe_name": result.recipe_name,
            "recipe_image": result.recipe_image,
            "recipe_description": result.recipe_description,
            "ingredients": result.ingredients
        })

    unique_recipes = {}
    for recipe in recipes:
        unique_recipes[recipe['recipe_name']] = recipe

    unique_recipe_list = list(unique_recipes.values())
    return unique_recipe_list



def checking(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    existing_favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if not existing_favorite:
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()
        flash("Favorited recipe")
    else:
        flash("Recipe is already a favorite")


@app.route("/Lunch")
def Lunch():
    unique_recipe_list = get_processed_recipes("Lunch")
    return render_template('recipe/lunch.html', unique_recipe_list=unique_recipe_list)

@app.route("/Lunchup/<int:recipe_id>/<int:user_id>")
def Lunchup_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Lunch", recipe_id, favorite=True)
    return render_template('recipe/lunch.html', unique_recipe_list=unique_recipe_list)

@app.route("/Lunchdown/<int:recipe_id>/<int:user_id>")
def down_recipeLunch(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    unique_recipe_list = update_and_get_recipes("Lunch", recipe_id, favorite=False)
    return render_template('recipe/lunch.html', unique_recipe_list=unique_recipe_list)

@app.route("/Baked")
def Baked():
    unique_recipe_list = get_processed_recipes("Baked")
    return render_template('recipe/Baked.html', unique_recipe_list=unique_recipe_list)

@app.route("/Bakedup/<int:recipe_id>/<int:user_id>")
def Baked_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Baked", recipe_id, favorite=True)
    return render_template('recipe/Baked.html', unique_recipe_list=unique_recipe_list)

@app.route("/Bakeddown/<int:recipe_id>/<int:user_id>")
def Baked_recipeLunch(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    unique_recipe_list = update_and_get_recipes("Baked", recipe_id, favorite=False)
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    return render_template('recipe/Baked.html', unique_recipe_list=unique_recipe_list)

@app.route("/Side Dish")
def SideDish():
    unique_recipe_list = get_processed_recipes("Side Dish")
    return render_template('recipe/SideDish.html', unique_recipe_list=unique_recipe_list)

@app.route("/SideDishup/<int:recipe_id>/<int:user_id>")
def SideDish_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Side Dish", recipe_id, favorite=True)
    return render_template('recipe/SideDish.html', unique_recipe_list=unique_recipe_list)

@app.route("/SideDishdown/<int:recipe_id>/<int:user_id>")
def down_recipeSideDish(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    unique_recipe_list = update_and_get_recipes("Side Dish", recipe_id, favorite=False)
    return render_template('recipe/SideDish.html', unique_recipe_list=unique_recipe_list)


@app.route("/Sauce and Condiment")
def SauceCondiment():
    unique_recipe_list = get_processed_recipes("Sauce and Condiment")
    return render_template('recipe/SauceCondiment.html', unique_recipe_list=unique_recipe_list)

@app.route("/SauceCondimentup/<int:recipe_id>/<int:user_id>")
def SauceCondiment_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Sauce and Condiment", recipe_id, favorite=True)
    return render_template('recipe/SauceCondiment.html', unique_recipe_list=unique_recipe_list)

@app.route("/SauceCondimentdown/<int:recipe_id>/<int:user_id>")
def down_SauceCondiment(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Sauce and Condiment", recipe_id, favorite=False)
    return render_template('recipe/SauceCondiment.html', unique_recipe_list=unique_recipe_list)


@app.route("/Appetizer")
def Appetizer():
    unique_recipe_list = get_processed_recipes("Appetizer")
    return render_template('recipe/appetizer.html', unique_recipe_list=unique_recipe_list)

@app.route("/Appetizerup/<int:recipe_id>/<int:user_id>")
def SAppetizer(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Appetizer", recipe_id, favorite=True)
    return render_template('recipe/appetizer.html', unique_recipe_list=unique_recipe_list)

@app.route("/Appetizerdown/<int:recipe_id>/<int:user_id>")
def downAppetizer(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Appetizer", recipe_id, favorite=False)
    return render_template('recipe/appetizer.html', unique_recipe_list=unique_recipe_list)


@app.route("/Breakfast")
def Breakfast():
    unique_recipe_list = get_processed_recipes("Breakfast")
    return render_template('recipe/breakfast.html', unique_recipe_list=unique_recipe_list)

@app.route("/Breakfastup/<int:recipe_id>/<int:user_id>")
def SABreakfast(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Breakfast", recipe_id, favorite=True)
    return render_template('recipe/breakfast.html', unique_recipe_list=unique_recipe_list)

@app.route("/Breakfastdown/<int:recipe_id>/<int:user_id>")
def downBreakfast(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Breakfast", recipe_id, favorite=False)
    flash("unfavorited")
    return render_template('recipe/breakfast.html', unique_recipe_list=unique_recipe_list)

@app.route("/Salad and Salad Dressing")
def SaladDressing():
    unique_recipe_list = get_processed_recipes("Salad and Salad Dressing")
    return render_template('recipe/SaladDressing.html', unique_recipe_list=unique_recipe_list)

@app.route("/SaladDressingup/<int:recipe_id>/<int:user_id>")
def SaladDressing_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Salad and Salad Dressing", recipe_id, favorite=True)
    return render_template('recipe/SaladDressing.html', unique_recipe_list=unique_recipe_list)


@app.route("/SaladDressingdown/<int:recipe_id>/<int:user_id>")
def down_SaladDressing(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Salad and Salad Dressing", recipe_id, favorite=False)
    
    return render_template('recipe/SaladDressing.html', unique_recipe_list=unique_recipe_list)

@app.route("/Dessert")
def SaladDressingo():
    unique_recipe_list = get_processed_recipes("Dessert")
    return render_template('recipe/Dessert.html', unique_recipe_list=unique_recipe_list)

@app.route("/Dessertup/<int:recipe_id>/<int:user_id>")
def dessert_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Dessert", recipe_id, favorite=True)
    # flash("favorited recipe")
    return render_template('recipe/Dessert.html', unique_recipe_list=unique_recipe_list)

@app.route("/Dessertdown/<int:recipe_id>/<int:user_id>")
def dessert(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
        # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Dessert", recipe_id, favorite=False)
    return render_template('recipe/Dessert.html', unique_recipe_list=unique_recipe_list)

@app.route("/Snack")
def Snacko():
    unique_recipe_list = get_processed_recipes("Snack")
    return render_template('recipe/Snack.html', unique_recipe_list=unique_recipe_list)

@app.route("/Snackup/<int:recipe_id>/<int:user_id>")
def snack_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Snack", recipe_id, favorite=True)
    # flash("favorited recipe")
    return render_template('recipe/Snack.html', unique_recipe_list=unique_recipe_list)

@app.route("/Snackdown/<int:recipe_id>/<int:user_id>")
def snacks(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
    # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Snack", recipe_id, favorite=False)
    return render_template('recipe/Snack.html', unique_recipe_list=unique_recipe_list)

@app.route("/Main Dish")
def Maindish():
    unique_recipe_list = get_processed_recipes("Main Dish")
    return render_template('recipe/MainDish.html', unique_recipe_list=unique_recipe_list)

@app.route("/MainDishup/<int:recipe_id>/<int:user_id>")
def main_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Main Dish", recipe_id, favorite=True)
    # flash("favorited recipe")
    return render_template('recipe/MainDish.html', unique_recipe_list=unique_recipe_list)

@app.route("/MainDishdown/<int:recipe_id>/<int:user_id>")
def mains(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
    # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    
    unique_recipe_list = update_and_get_recipes("Snack", recipe_id, favorite=False)
    return render_template('recipe/MainDish.html', unique_recipe_list=unique_recipe_list)


@app.route("/Beverage")
def Beverage():
    unique_recipe_list = get_processed_recipes("Beverage")
    return render_template('recipe/beverage.html', unique_recipe_list=unique_recipe_list)

@app.route("/Beverageup/<int:recipe_id>/<int:user_id>")
def beverages_recipe(recipe_id,user_id):
    usero = User.query.get_or_404(user_id)
    checking(recipe_id,user_id)
    unique_recipe_list = update_and_get_recipes("Beverage", recipe_id, favorite=True)
    # flash("favorited recipe")
    return render_template('recipe/beverage.html', unique_recipe_list=unique_recipe_list)


@app.route("/Beveragedown/<int:recipe_id>/<int:user_id>")
def beverage(recipe_id,user_id):
    user = User.query.get_or_404(user_id)
    # Check if the specified recipe is a favorite for the user
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    
    if favorite:
        # Recipe is a favorite, remove the favorite record
        db.session.delete(favorite)
        db.session.commit()
        flash("Unfavorited recipe")
    unique_recipe_list = update_and_get_recipes("Beverage", recipe_id, favorite=False)
    return render_template('recipe/beverage.html', unique_recipe_list=unique_recipe_list)

    
@app.route("/favorite/<int:user_id>")
def favorite(user_id):
    """List all favorite recipes."""
    recipe_favorites=[]
    user = User.query.get_or_404(user_id)
    favorite_records = Favorite.query.filter_by(user_id=user_id).all()

    # Extract the recipe_ids from the favorite records 
    recipe_ids = [record.recipe_id for record in favorite_records]
    # making sure there won't be any duplicates record of id
    recipe_dids = list(set(recipe_ids))

    # Query the Recipe table to get the details of the favorite recipes
    favorites = Recipe.query.filter(Recipe.id.in_(recipe_dids)).all()

    for fav in favorites:
            recipe_favorites.append({
            'id': fav.id,
            'recipe_name': fav.recipe_name,
            'recipe_image': fav.recipe_image,
            'recipe_description': fav.recipe_description,
            'ingredients': fav.ingredients
            # 'user_id': user.id
        })
  
    return render_template("favorite.html",recipe_favorites=recipe_favorites,favorites=favorites)
      
    
