
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,ARRAY,String,Boolean,Integer

bcrypt = Bcrypt()
db = SQLAlchemy()




class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'


    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username=db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password=db.Column(
        db.Text,
        nullable=False
    )


    @classmethod
    def signup(cls, username, email,password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False
    
# models.py
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(255), nullable=False)
    recipe_image=db.Column(db.Text,nullable=True)
    recipe_type=db.Column(ARRAY(String))
    recipe_description=db.Column(db.String(255), nullable=False)
    ingredients =db.Column(ARRAY(String))
    # store recipe that have been selected as favorite
    favorite_recipe=db.Column(Boolean, default=False)
    # favorite_recipe=db.Column(db.String(255), nullable=False)
    # user_favorites = db.Column(ARRAY(Integer), default=[])
    


    # def is_favorite(self):
    #     return self.favorite_recipe
 
    # def set_as_favorite(self):
    #     self.favorite_recipe = True
    # instructions =db.Column(db.Text, nullable=False)

    # favorite = db.Column(db.Boolean, nullable=True, default=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class RecipeUser(db.Model):
    __tablename__ = 'user_recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image=db.Column(db.Text,nullable=True)
    description=db.Column(db.String(255), nullable=False)
    ingredients =db.Column(db.String(255), nullable=False)
    # instructions =db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))


    # if user favorites a recipe do this:
    #
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)






