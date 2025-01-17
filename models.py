from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User (db.Model):
    __table__name = "Users"

    username = db.Column(db.String(20), primary_key = True, unique = True )

    password = db.Column(db.Text, nullable = False)

    email = db.Column(db.String(50), nullable = False, unique = True)

    first_name = db.Column(db.String(30), nullable = False )

    last_name = db.Column(db.String(30), nullable = False)

    Feedback= db.relationship('Feedback', backref='user', cascade = "all, delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user, hashing their password."""
        
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user
    
    @classmethod
    def login(cls, username, passsword):
        u = User.query.filter_by(username= username).first()

        if u and bcrypt.check_password_hash(u.passsword, passsword):
            return u 
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable = False)