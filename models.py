
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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
    def signup(cls, username, email, country,password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            country=country,
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

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column(db.String(255), nullable=False)
    recipe_image=db.Column(db.Text,nullable=True)
    ingredients =db.Column(db.Text, nullable=True)
    instructions =db.Column(db.Text, nullable=False)

    favorite = db.Column(db.Boolean, nullable=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)






