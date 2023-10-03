import os,json,requests

from flask import Flask,render_template,flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
# from flask_bcrypt import 
# from bcrypt import  check_password_hash
from forms import SignUpForm,LoginForm,EditPassword
from models import db,User,Recipe,connect_db

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
    """If we're logged in, add curr user to Flask global."""

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

@app.route('/logout')
def logout():
    """Handle logout of user."""

    user = User.query.get_or_404(user.id)
    if user:
        do_logout(user)
        flash("you have successfuly log out", 'success')
        return redirect('/login')
    flash("Invalid credentials.", 'danger')



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
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                country=form.country.data
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        

        if user:
            do_login(user)
            flash(f"Hello {user.username}! welcome back ", "success")
        
            return redirect("/")

        flash("Invalid credentials.", 'danger')

            

    return render_template('login.html', form=form)

# app.py
@app.route('/')
def homepage():
  """Show homepage:

  - anon users: no messages
  - logged in: 100 most recent messages of followed_users
  """
  form=SignUpForm()

  if g.user:
    METHOD = "recipe.search.v3"
    format_type = "json"
    access_token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjVGQUQ4RTE5MjMwOURFRUJCNzBCMzU5M0E2MDU3OUFEMUM5NjgzNDkiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJYNjJPR1NNSjN1dTNDeldUcGdWNXJSeVdnMGsifQ.eyJuYmYiOjE2OTYyODYyODcsImV4cCI6MTY5NjM3MjY4NywiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.ExWEPgtTJwHQyqgeaBwX0k4cXbrtjirfo1eP2OmhZ8uxgTBdVKttUj9oxYEBD6Vl16NMQq8p39iQ_WIeH1Myqh8zTJc8LCUrCxec2Dc4pcaeCrdyLQ0bqqkKadPsd78UnuhQajtC0OK6_cuYHlXLN5YtUTWBU9iINWkyaXoIUlBi8Fy6Et8JaRAN3R6OpNmQZ5-QWok8OsLDA0g9km4zoW1UmglupaUqVvGk8Ah2stOHU9sCLpb6-AS5fi7FFqdSXk3GSKJMUp52QYYc7cRiMbpcEUhH4IpD5G9FnQXNyeTJ8Tn2L_HzeVo10myBUlortSLgGA3DdYqZn11FOEI3OA"

    # Assign the response variable outside of the if statement
    response = requests.get(
    "https://platform.fatsecret.com/rest/server.api",
    params={
      "method": METHOD,
      # "search_expression": search_expression,
      # "page_number": page_number,
      # "max_results": max_results,
      "format": format_type,
      # "region":region
    },
    headers={"Authorization": f'Bearer {access_token}'}
     
  )

  if response.status_code == 200:
    if format_type == "json":
      # Parse the JSON response
      json_data = response.json()
      # data=jsonify(json_data)
      # food_list = data["foods"]["food"]
      json_data = json.loads(response.content)
      recipe_types = json_data["recipe_types"]["recipe_type"]
    return render_template('home.html',recipe_types=recipe_types)
  else:
    return render_template('base.html',form=form)

@app.route('/{{recipe}}')
def getRecipeDescription(recipe):
    METHOD = "recipes.search.v3"
    format_type = "json"
    recipe_types = recipe

    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVGQUQ4RTE5MjMwOURFRUJCNzBCMzU5M0E2MDU3OUFEMUM5NjgzNDkiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJYNjJPR1NNSjN1dTNDeldUcGdWNXJSeVdnMGsifQ.eyJuYmYiOjE2OTYyODYyODcsImV4cCI6MTY5NjM3MjY4NywiaXNzIjoiaHR0cHM6Ly9vYXV0aC5mYXRzZWNyZXQuY29tIiwiYXVkIjoiYmFzaWMiLCJjbGllbnRfaWQiOiI3M2Q1YTlkYWI3NmQ0MjZkOGNlMTlhYzE1OTljMDg4NiIsInNjb3BlIjpbImJhc2ljIl19.ExWEPgtTJwHQyqgeaBwX0k4cXbrtjirfo1eP2OmhZ8uxgTBdVKttUj9oxYEBD6Vl16NMQq8p39iQ_WIeH1Myqh8zTJc8LCUrCxec2Dc4pcaeCrdyLQ0bqqkKadPsd78UnuhQajtC0OK6_cuYHlXLN5YtUTWBU9iINWkyaXoIUlBi8Fy6Et8JaRAN3R6OpNmQZ5-QWok8OsLDA0g9km4zoW1UmglupaUqVvGk8Ah2stOHU9sCLpb6-AS5fi7FFqdSXk3GSKJMUp52QYYc7cRiMbpcEUhH4IpD5G9FnQXNyeTJ8Tn2L_HzeVo10myBUlortSLgGA3DdYqZn11FOEI3OA"

    response1 = requests.get(
    "https://platform.fatsecret.com/rest/server.api",
    params={
        "method": METHOD,
        "format": format_type,
        "recipe_types": recipe_types,
    },
    headers={"Authorization": f'Bearer {access_token}'},
    )

    if response1.status_code == 200:
        if format_type == "json":
            API_datas = json.loads(response1.content)
            recipe_descriptions = []
            for data in API_datas["recipes"]["recipe"]:
                recipe_descriptions.append(data["recipe_description"])
            return render_template("description.html", recipe_descriptions)
        else:
            return f"Request failed with status code: {response1.status_code}"
    else:
        return f"Request failed with stats code: {response1.status_code}"



