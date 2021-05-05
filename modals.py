from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(arr):
    db.app = arr
    db.init_app(arr)

class User(db.Model):
    """User Model Table"""

    __tablename__ = "users"

    username = db.Column(db.String(20),primary_key=True)

    password = db.Column(db.Text,nullable=False)

    email = db.Column(db.String(50),unique=True)

    first_name = db.Column(db.String(30),nullable=False)

    last_name = db.Column(db.String(30),nullable=False)

    tweets = db.relationship("Feedbacks",cascade="all,delete",backref="user")

    def __repr__(self):
        return f"username of {self.username}"

    @classmethod
    def register(cls,username,password,email,first,last):
        hash_psw = bcrypt.generate_password_hash(password)
        string_hash_psw = hash_psw.decode("utf8")
        return cls(
            username=username,
            password=string_hash_psw,
            email=email,
            first_name=first,
            last_name=last)

    @classmethod
    def authenticate(cls,username,password):
        auth_user = User.query.filter_by(username=username).first()
        if auth_user and bcrypt.check_password_hash(auth_user.password,password):
            return auth_user
        else:
            return False

class Feedbacks(db.Model):
    """Feedback Model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.String(200),nullable=False)

    content = db.Column(db.Text,nullable=False)

    username = db.Column(db.Text,db.ForeignKey("users.username"))

    def __repr__(self):
        return f"feedback title {self.title}"

    # user = db.relationship("User",backref="feedbacks")