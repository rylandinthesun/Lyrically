from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect db to Flask app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    bio = db.Column(db.Text)
    likes = db.relationship("Lyric", secondary="likes")
    saves = db.relationship("Lyric", secondary="saves")

    @classmethod
    def signup(cls, email, password, username):
        """Sign up user by Hashing password and adding user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            password=hashed_pwd,
            username=username,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Lyric(db.Model):
    """An individual set of Lyrics and it's info."""

    __tablename__ = "lyrics"

    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.Text, nullable=False)
    track_name = db.Column(db.Text, nullable=False)
    artist_name = db.Column(db.Text, nullable=False)
    album_name = db.Column(db.Text, nullable=False)
    album_image = db.Column(db.Text, nullable=False)
    

class Like(db.Model):
    """Table to connect user to each lyrics they like."""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    lyric_id = db.Column(db.Integer, db.ForeignKey('lyrics.id', ondelete='cascade'), unique=True)

class Save(db.Model):
    """Table to connect user to lyrics they want to save."""

    __tablename__ = "saves"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    lyric_id = db.Column(db.Integer, db.ForeignKey('lyrics.id', ondelete='cascade'), unique=True)