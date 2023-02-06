from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime 


#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import secrets to generate user token 
import secrets

#flask login to check for an authentication user
from flask_login import UserMixin, LoginManager

#import for flask marshmallow
from flask_marshmallow import Marshmallow

#create instance of SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)
    
    def __init__(self, email, password, first_name = '', last_name = '', id = '',  token = ''):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name 
        self.email = email
        self.token = self.set_token(24)
        
        
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database!"
    
class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(500), nullable = True)
    comics = db.Column(db.Numeric(precision=12, scale=2))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    img_head = db.Column(db.String())
    
    def __init__ (self, name, description, comics, img_head, user_token, id="" ):
        self.id = self.set_id()
        self.name = name
        self.description = description 
        self.comics = comics
        self.user_token = user_token 
        self.img_head = img_head
        
    def set_id(self):
        return secrets.token_urlsafe()
    
    def __repr__(self):
        return f"The following Hero has been added: {self.name}"
    
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comics', 'img_head']
        
            
hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)   