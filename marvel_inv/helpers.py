import secrets
from marvel import Marvel 
from functools import wraps
from flask import request, jsonify, json
from marvel_inv.models import User
import decimal


marvel = Marvel(PUBLIC_KEY= "153e490f01bf43d03d92c5600d25053d", 
                PRIVATE_KEY= "7fe5e10498b80c1e0011ac6fa0966fd368c98cc8")

def APIMarvel(name):
    marvel = Marvel(PUBLIC_KEY = "d04361fb613e941e150ff9c6b928b1b4", PRIVATE_KEY = "42be969884a8c719cfbc8f4479895d2189a3697e" )
    characters = marvel.characters
    my_char = characters.all(name=name)["data"]["results"]
    return my_char



def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})
        
        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        
        return our_flask_function(our_user, *args, **kwargs)
    return decorated







class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
    
    
    
    
    







